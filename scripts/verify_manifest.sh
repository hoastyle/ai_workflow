#!/bin/bash

###############################################################################
# Manifest Consistency Verification Script
#
# Verifies that install.sh and uninstall.sh use the same file manifests
# from install.manifest
#
# Usage: ./scripts/verify_manifest.sh
###############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Function: Print colored messages
print_status() {
    local status=$1
    local message=$2
    case $status in
        ok)     echo -e "${GREEN}✅${NC} $message" ;;
        error)  echo -e "${RED}❌${NC} $message" ;;
        warn)   echo -e "${YELLOW}⚠️ ${NC} $message" ;;
        info)   echo -e "${BLUE}ℹ️ ${NC} $message" ;;
    esac
}

# Function: Extract array definition from file
extract_array() {
    local file=$1
    local array_name=$2
    grep -A 100 "declare.*${array_name}=" "$file" | head -20
}

# Function: Check if source statements exist
check_source_statements() {
    echo "📋 Checking source statements..."
    echo ""

    local errors=0

    # Check install.sh
    if grep -q "source.*install.manifest" "$PROJECT_ROOT/install.sh"; then
        print_status ok "install.sh sources install.manifest"
    else
        print_status error "install.sh does NOT source install.manifest"
        ((errors++))
    fi

    # Check uninstall.sh
    if grep -q "source.*install.manifest" "$PROJECT_ROOT/uninstall.sh"; then
        print_status ok "uninstall.sh sources install.manifest"
    else
        print_status error "uninstall.sh does NOT source install.manifest"
        ((errors++))
    fi

    return $errors
}

# Function: Verify manifest file exists and is valid
check_manifest_file() {
    echo ""
    echo "📄 Checking manifest file..."
    echo ""

    if [[ ! -f "$SCRIPT_DIR/install.manifest" ]]; then
        print_status error "install.manifest not found at $SCRIPT_DIR/install.manifest"
        return 1
    fi

    print_status ok "install.manifest exists"

    # Source and validate
    if source "$SCRIPT_DIR/install.manifest" 2>/dev/null; then
        print_status ok "install.manifest can be sourced successfully"
        return 0
    else
        print_status error "install.manifest failed to source"
        return 1
    fi
}

# Function: Verify arrays are exported
check_array_exports() {
    echo ""
    echo "🔍 Checking array exports in install.manifest..."
    echo ""

    local errors=0

    # Source the manifest
    source "$SCRIPT_DIR/install.manifest" || return 1

    # Check each array
    if [[ -n "${COMMAND_FILES[@]}" ]]; then
        print_status ok "COMMAND_FILES: ${#COMMAND_FILES[@]} items"
    else
        print_status error "COMMAND_FILES is empty or not exported"
        ((errors++))
    fi

    if [[ -n "${CONFIG_FILES[@]}" ]]; then
        print_status ok "CONFIG_FILES: ${#CONFIG_FILES[@]} items"
    else
        print_status error "CONFIG_FILES is empty or not exported"
        ((errors++))
    fi

    if [[ -n "${SCRIPT_FILES[@]}" ]]; then
        print_status ok "SCRIPT_FILES: ${#SCRIPT_FILES[@]} items - ${SCRIPT_FILES[*]}"
    else
        print_status error "SCRIPT_FILES is empty or not exported"
        ((errors++))
    fi

    if [[ -n "${DOC_FILES[@]}" ]]; then
        print_status ok "DOC_FILES: ${#DOC_FILES[@]} items"
    else
        print_status warn "DOC_FILES is empty (optional)"
    fi

    return $errors
}

# Function: Check syntax of install.sh and uninstall.sh
check_script_syntax() {
    echo ""
    echo "🔧 Checking script syntax..."
    echo ""

    local errors=0

    if bash -n "$PROJECT_ROOT/install.sh" 2>/dev/null; then
        print_status ok "install.sh syntax is valid"
    else
        print_status error "install.sh has syntax errors"
        ((errors++))
    fi

    if bash -n "$PROJECT_ROOT/uninstall.sh" 2>/dev/null; then
        print_status ok "uninstall.sh syntax is valid"
    else
        print_status error "uninstall.sh has syntax errors"
        ((errors++))
    fi

    if bash -n "$SCRIPT_DIR/install.manifest" 2>/dev/null; then
        print_status ok "install.manifest syntax is valid"
    else
        print_status error "install.manifest has syntax errors"
        ((errors++))
    fi

    return $errors
}

# Function: Test that scripts can source manifest
test_source() {
    echo ""
    echo "⚙️ Testing script sourcing..."
    echo ""

    local errors=0

    # Test by sourcing in current context
    (
        cd "$SCRIPT_DIR"

        # Source the manifest in the scripts directory context
        source "./install_utils.sh" || exit 1
        source "./install.manifest" || exit 1

        # Verify arrays are available
        [[ -n "${SCRIPT_FILES[@]}" ]] || exit 1
        exit 0
    ) 2>/dev/null

    if [[ $? -eq 0 ]]; then
        print_status ok "Manifest files can be sourced successfully"
    else
        print_status error "Failed to source manifest files"
        ((errors++))
    fi

    return $errors
}

# Main function
main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║       Installation Manifest Consistency Verification          ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""

    local total_errors=0

    # Run all checks
    check_source_statements || ((total_errors+=$?))
    check_manifest_file || ((total_errors+=$?))
    check_array_exports || ((total_errors+=$?))
    check_script_syntax || ((total_errors+=$?))
    test_source || ((total_errors+=$?))

    # Summary
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [[ $total_errors -eq 0 ]]; then
        echo -e "${GREEN}✅ All manifest consistency checks passed!${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "💡 Consistency Notes:"
        echo "   • Both install.sh and uninstall.sh source install.manifest"
        echo "   • File manifests are defined in a single location"
        echo "   • Adding new files only requires updating install.manifest"
        echo ""
        return 0
    else
        echo -e "${RED}❌ $total_errors manifest consistency check(s) failed!${NC}"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        return 1
    fi
}

# Run main function
main
exit $?
