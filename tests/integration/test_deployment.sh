#!/bin/bash

# Note: We use -eu but NOT -o pipefail in tests to allow test failures to be caught
set -eu
IFS=$'\n\t'

###############################################################################
# AI Workflow Deployment Integration Test
#
# Tests the complete installation and uninstallation cycle
# Ensures all files are properly deployed and cleaned up
#
# Usage: ./test_deployment.sh
###############################################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test workspace
TEST_DIR="/tmp/ai_workflow_test_$$"
COMMANDS_DIR="$TEST_DIR/.claude/commands"

# Project root (relative to this script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

###############################################################################
# Helper Functions
###############################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

test_start() {
    TESTS_RUN=$((TESTS_RUN + 1))
    log_info "Test $TESTS_RUN: $1"
}

test_pass() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    log_success "$1"
}

test_fail() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    log_error "$1"
}

cleanup() {
    log_info "Cleaning up test environment..."
    rm -rf "$TEST_DIR"
}

###############################################################################
# Test Setup
###############################################################################

setup_test_environment() {
    log_info "Setting up test environment at $TEST_DIR"

    # Create test directories
    mkdir -p "$COMMANDS_DIR"

    # Set HOME to test directory for installation
    export HOME="$TEST_DIR"

    log_success "Test environment created"
}

###############################################################################
# Test Cases
###############################################################################

test_installation_dry_run() {
    test_start "Installation dry-run simulation"

    cd "$PROJECT_ROOT"

    if ./install.sh --dry-run --verbose > /tmp/install_dryrun.log 2>&1; then
        test_pass "Dry-run completed successfully"
        return 0
    else
        test_fail "Dry-run failed"
        cat /tmp/install_dryrun.log
        return 1
    fi
}

test_manifest_completeness() {
    test_start "Manifest file completeness"

    cd "$PROJECT_ROOT"

    # Source the manifest
    # shellcheck source=scripts/install.manifest
    source scripts/install.manifest

    local missing_count=0
    local total_count=0

    # Check command files (handle wildcards)
    for pattern in "${COMMAND_FILES[@]}"; do
        if [[ "$pattern" == *"*"* ]]; then
            # Expand wildcard
            local files_found=0
            for file in $pattern; do
                if [[ -f "$file" ]]; then
                    files_found=$((files_found + 1))
                    total_count=$((total_count + 1))
                fi
            done
            if [[ $files_found -eq 0 ]]; then
                log_error "No files matching pattern: $pattern"
                missing_count=$((missing_count + 1))
            fi
        else
            # Direct file check
            total_count=$((total_count + 1))
            if [[ ! -f "$PROJECT_ROOT/$pattern" ]]; then
                log_error "Missing command file: $pattern"
                missing_count=$((missing_count + 1))
            fi
        fi
    done

    # Check lib files
    for lib in "${COMMANDS_LIB_FILES[@]}"; do
        total_count=$((total_count + 1))
        if [[ ! -f "$PROJECT_ROOT/$lib" ]]; then
            log_error "Missing lib file: $lib"
            missing_count=$((missing_count + 1))
        fi
    done

    # Check agents files
    for agent in "${COMMANDS_AGENTS_FILES[@]}"; do
        total_count=$((total_count + 1))
        if [[ ! -f "$PROJECT_ROOT/$agent" ]]; then
            log_error "Missing agent file: $agent"
            missing_count=$((missing_count + 1))
        fi
    done

    # Check MCP files
    for mcp in "${SRC_MCP_FILES[@]}"; do
        total_count=$((total_count + 1))
        if [[ ! -f "$PROJECT_ROOT/$mcp" ]]; then
            log_error "Missing MCP file: $mcp"
            missing_count=$((missing_count + 1))
        fi
    done

    if [[ $missing_count -eq 0 ]]; then
        test_pass "All $total_count manifest files exist"
        return 0
    else
        test_fail "$missing_count file(s) missing from manifest (checked $total_count files)"
        return 1
    fi
}

test_full_installation() {
    test_start "Full installation with copy method"

    cd "$PROJECT_ROOT"

    # Run installation
    if ./install.sh --copy --no-backup --verbose > /tmp/install_full.log 2>&1; then
        test_pass "Installation completed"
    else
        test_fail "Installation failed"
        cat /tmp/install_full.log
        return 1
    fi

    # Verify installation
    local errors=0

    # Check command files installed
    if [[ ! -f "$COMMANDS_DIR/wf_03_prime.md" ]]; then
        log_error "wf_03_prime.md not installed"
        ((errors++))
    fi

    # Check lib directory
    if [[ ! -d "$COMMANDS_DIR/commands/lib" ]]; then
        log_error "commands/lib/ directory not created"
        ((errors++))
    fi

    # Check agents directory
    if [[ ! -d "$COMMANDS_DIR/commands/agents" ]]; then
        log_error "commands/agents/ directory not created"
        ((errors++))
    fi

    # Check MCP directory
    if [[ ! -d "$COMMANDS_DIR/src/mcp" ]]; then
        log_error "src/mcp/ directory not created"
        ((errors++))
    fi

    # Check doc_guard.py
    if [[ ! -f "$COMMANDS_DIR/scripts/doc_guard.py" ]]; then
        log_error "scripts/doc_guard.py not installed"
        ((errors++))
    fi

    # Check MCP Gateway
    if [[ ! -f "$COMMANDS_DIR/src/mcp/gateway.py" ]]; then
        log_error "src/mcp/gateway.py not installed"
        ((errors++))
    fi

    if [[ $errors -eq 0 ]]; then
        test_pass "All files verified after installation"
        return 0
    else
        test_fail "$errors verification error(s) found"
        return 1
    fi
}

test_file_permissions() {
    test_start "File permissions verification"

    local errors=0

    # Check script executability
    if [[ ! -x "$PROJECT_ROOT/install.sh" ]]; then
        log_error "install.sh not executable"
        ((errors++))
    fi

    if [[ ! -x "$PROJECT_ROOT/uninstall.sh" ]]; then
        log_error "uninstall.sh not executable"
        ((errors++))
    fi

    if [[ $errors -eq 0 ]]; then
        test_pass "File permissions are correct"
        return 0
    else
        test_fail "$errors permission error(s) found"
        return 1
    fi
}

test_uninstallation() {
    test_start "Complete uninstallation"

    cd "$PROJECT_ROOT"

    # Run uninstallation
    if ./uninstall.sh --force --verbose > /tmp/uninstall.log 2>&1; then
        test_pass "Uninstallation completed"
    else
        test_fail "Uninstallation failed"
        cat /tmp/uninstall.log
        return 1
    fi

    # Verify cleanup
    local remaining=0

    # Check if command files removed
    if [[ -f "$COMMANDS_DIR/wf_03_prime.md" ]]; then
        log_error "wf_03_prime.md still exists after uninstall"
        remaining=$((remaining + 1))
    fi

    # Check if lib directory removed
    if [[ -d "$COMMANDS_DIR/commands/lib" ]]; then
        log_error "commands/lib/ directory still exists"
        remaining=$((remaining + 1))
    fi

    # Check if agents directory removed
    if [[ -d "$COMMANDS_DIR/commands/agents" ]]; then
        log_error "commands/agents/ directory still exists"
        remaining=$((remaining + 1))
    fi

    # Check if MCP directory removed
    if [[ -d "$COMMANDS_DIR/src/mcp" ]]; then
        log_error "src/mcp/ directory still exists"
        remaining=$((remaining + 1))
    fi

    # Check for any remaining files (excluding manifest which may be intentional)
    if [[ -d "$COMMANDS_DIR" ]]; then
        local files_remaining
        files_remaining=$(find "$COMMANDS_DIR" -type f ! -name '.ai_workflow_manifest' | wc -l)
        if [[ $files_remaining -gt 0 ]]; then
            log_warning "$files_remaining file(s) still remain:"
            find "$COMMANDS_DIR" -type f ! -name '.ai_workflow_manifest' | head -5 | sed 's/^/    /'
            remaining=$((remaining + files_remaining))
        fi
    fi

    if [[ $remaining -eq 0 ]]; then
        test_pass "All files removed successfully"
        return 0
    else
        test_fail "$remaining file(s)/director(y|ies) remain after uninstall"
        return 1
    fi
}

test_strict_mode_enabled() {
    test_start "Shell strict mode verification"

    local errors=0

    # Check install.sh has strict mode
    if grep -q "set -euo pipefail" "$PROJECT_ROOT/install.sh"; then
        : # Found, do nothing
    else
        log_error "install.sh missing 'set -euo pipefail'"
        ((errors++))
    fi

    # Check uninstall.sh has strict mode
    if grep -q "set -euo pipefail" "$PROJECT_ROOT/uninstall.sh"; then
        : # Found, do nothing
    else
        log_error "uninstall.sh missing 'set -euo pipefail'"
        ((errors++))
    fi

    if [[ $errors -eq 0 ]]; then
        test_pass "Strict mode enabled in all scripts"
        return 0
    else
        test_fail "$errors script(s) missing strict mode"
        return 1
    fi
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo "======================================================================"
    echo "AI Workflow Deployment Integration Tests"
    echo "======================================================================"
    echo ""

    # Setup
    setup_test_environment
    trap cleanup EXIT

    # Run tests
    echo ""
    echo "Running Tests..."
    echo "----------------------------------------------------------------------"

    test_strict_mode_enabled
    test_manifest_completeness
    test_file_permissions
    test_installation_dry_run
    test_full_installation
    test_uninstallation

    # Summary
    echo ""
    echo "======================================================================"
    echo "Test Summary"
    echo "======================================================================"
    echo "Total Tests:  $TESTS_RUN"
    echo -e "${GREEN}Passed:       $TESTS_PASSED${NC}"
    echo -e "${RED}Failed:       $TESTS_FAILED${NC}"
    echo "======================================================================"

    if [[ $TESTS_FAILED -eq 0 ]]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some tests failed${NC}"
        exit 1
    fi
}

# Run main function
main "$@"
