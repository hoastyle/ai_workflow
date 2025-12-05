#!/bin/bash

###############################################################################
# AI Workflow Installation Script
#
# Installs ai_workflow commands to ~/.claude/commands/
# and CLAUDE.md to ~/.claude/
#
# Usage: ./install.sh [OPTIONS]
# Options:
#   --link          Use symbolic links (default, recommended)
#   --copy          Copy files instead of linking
#   --backup        Create backup before installation (default)
#   --no-backup     Skip backup creation
#   --include-docs  Also install documentation files
#   --dry-run       Simulate installation without making changes
#   --verbose       Show detailed output
#   --help          Display this help message
#
# Examples:
#   ./install.sh                    # Default installation with symlinks
#   ./install.sh --copy --no-backup # Copy files without backup
#   ./install.sh --dry-run          # Test installation without changes
###############################################################################

set -o pipefail

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source utility functions and installation manifest
source "${SCRIPT_DIR}/scripts/install_utils.sh" || exit 1
source "${SCRIPT_DIR}/scripts/install.manifest" || exit 1

###############################################################################
# Configuration
###############################################################################

# Default options
INSTALL_METHOD="copy"  # copy or link (copy is default for portability)
CREATE_BACKUP=1
INCLUDE_DOCS=0
DRY_RUN=0
VERBOSE=0

# Project structure
PROJECT_ROOT="${SCRIPT_DIR}"
CLAUDE_MD_SOURCE="${PROJECT_ROOT}/CLAUDE.md"

# Declare arrays for tracking
declare -a INSTALLED_COMMANDS
declare -a FAILED_INSTALLS

###############################################################################
# Help and Usage
###############################################################################

show_help() {
    cat << EOF
AI Workflow Installation Script

USAGE:
    ./install.sh [OPTIONS]

OPTIONS:
    --link          Use symbolic links (default, recommended)
                    Files remain in project directory and update automatically

    --copy          Copy files instead of linking
                    Creates independent copies in ~/.claude/commands/

    --backup        Create backup before installation (enabled by default)
                    Saves existing files to ~/.claude/backup/YYYY-MM-DD_HH-MM-SS/

    --no-backup     Skip backup creation

    --include-docs  Also install documentation files (COMMANDS.md, WORKFLOWS.md, etc.)

    --dry-run       Simulate installation without making changes
                    Shows what would be installed

    --verbose       Show detailed output including all file operations

    --help          Display this help message

EXAMPLES:
    # Default installation with symlinks and backup
    ./install.sh

    # Copy files instead of linking
    ./install.sh --copy

    # Dry run to preview changes
    ./install.sh --dry-run

    # Installation with documentation
    ./install.sh --include-docs

    # Quick installation without backup
    ./install.sh --no-backup --verbose

DIRECTORIES:
    Commands:       ~/.claude/commands/
    Configuration:  ~/.claude/CLAUDE.md
    Backups:        ~/.claude/backup/YYYY-MM-DD_HH-MM-SS/

DOCUMENTATION:
    For more information, see INSTALL.md in the project directory.

EOF
}

###############################################################################
# Argument Parsing
###############################################################################

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --link)
                INSTALL_METHOD="link"
                shift
                ;;
            --copy)
                INSTALL_METHOD="copy"
                shift
                ;;
            --backup)
                CREATE_BACKUP=1
                shift
                ;;
            --no-backup)
                CREATE_BACKUP=0
                shift
                ;;
            --include-docs)
                INCLUDE_DOCS=1
                shift
                ;;
            --dry-run)
                DRY_RUN=1
                shift
                ;;
            --verbose)
                VERBOSE=1
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

###############################################################################
# Validation Phase
###############################################################################

validate_installation_environment() {
    echo ""
    info "Validating installation environment..."

    # Check working directory
    if ! check_working_directory; then
        exit_with_error "Not in ai_workflow project directory"
    fi

    # Check for wf_*.md command files in project root
    local cmd_count=$(ls -1 "${PROJECT_ROOT}"/wf_*.md 2>/dev/null | wc -l)
    if [[ $cmd_count -eq 0 ]]; then
        exit_with_error "No command files (wf_*.md) found in project root"
    fi
    verbose "Found $cmd_count command files in project root"

    if [[ ! -f "$CLAUDE_MD_SOURCE" ]]; then
        exit_with_error "CLAUDE.md not found: $CLAUDE_MD_SOURCE"
    fi
    verbose "Found CLAUDE.md: $CLAUDE_MD_SOURCE"

    # Check write permission
    if ! check_write_permission "$INSTALL_DIR"; then
        exit_with_error "No write permission for $INSTALL_DIR"
    fi

    success "Environment validation passed"
}

###############################################################################
# Preparation Phase
###############################################################################

prepare_installation() {
    echo ""
    info "Preparing installation..."

    # Create installation directories
    if ! create_install_directories; then
        exit_with_error "Failed to create installation directories"
    fi

    # Create installation manifest (skip in dry-run mode)
    if [[ $DRY_RUN -eq 0 ]]; then
        if ! create_installation_manifest; then
            exit_with_error "Failed to create installation manifest"
        fi
        verbose "Created installation manifest: $MANIFEST_FILE"
    fi

    # Check for conflicts
    check_installation_conflicts

    success "Installation environment ready"
}

check_installation_conflicts() {
    local conflicts=0

    verbose "Checking for file conflicts..."

    # Check CLAUDE.md
    if [[ -e "$INSTALL_DIR/CLAUDE.md" ]]; then
        warning "CLAUDE.md already exists at $INSTALL_DIR/CLAUDE.md"
        ((conflicts++))
    fi

    # Check command files
    for cmd_file in "${PROJECT_ROOT}"/wf_*.md; do
        local basename=$(basename "$cmd_file")
        if [[ -e "$COMMANDS_DIR/$basename" ]]; then
            verbose "  File already exists: $COMMANDS_DIR/$basename"
            ((conflicts++))
        fi
    done

    if [[ $conflicts -gt 0 ]]; then
        if [[ $CREATE_BACKUP -eq 1 ]]; then
            info "Found $conflicts existing files - will create backup"
        else
            warning "Found $conflicts existing files - will be overwritten"
        fi
    fi
}

###############################################################################
# Backup Phase
###############################################################################

create_backup() {
    local files_to_backup=()

    # Check what needs backing up
    if [[ -e "$INSTALL_DIR/CLAUDE.md" ]]; then
        files_to_backup+=("$INSTALL_DIR/CLAUDE.md")
    fi

    for cmd_file in "${PROJECT_ROOT}"/wf_*.md; do
        local basename=$(basename "$cmd_file")
        if [[ -e "$COMMANDS_DIR/$basename" ]]; then
            files_to_backup+=("$COMMANDS_DIR/$basename")
        fi
    done

    if [[ ${#files_to_backup[@]} -eq 0 ]]; then
        verbose "No files to backup"
        return 0
    fi

    echo ""
    info "Creating backup of existing files..."

    local backup_path
    if ! backup_path=$(create_backup_directory); then
        error "Failed to create backup directory"
        return 1
    fi

    for file in "${files_to_backup[@]}"; do
        if ! backup_file "$file" "$backup_path"; then
            warning "Failed to backup $file, continuing anyway..."
        fi
    done

    print_backup_info "$backup_path"
    return 0
}

###############################################################################
# Installation Phase
###############################################################################

install_commands() {
    echo ""
    if [[ $INSTALL_METHOD == "link" ]]; then
        info "Installing commands (using symbolic links)..."
    else
        info "Installing commands (copying files)..."
    fi

    local cmd_count=0
    local fail_count=0

    for cmd_file in "${PROJECT_ROOT}"/wf_*.md; do
        if [[ ! -f "$cmd_file" ]]; then
            continue
        fi

        local basename=$(basename "$cmd_file")
        local target="$COMMANDS_DIR/$basename"

        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would install: $basename"
            ((cmd_count++))
        else
            if [[ $INSTALL_METHOD == "link" ]]; then
                if install_file_link "$cmd_file" "$target"; then
                    ((cmd_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $basename"
                    ((fail_count++))
                fi
            else
                if install_file_copy "$cmd_file" "$target"; then
                    ((cmd_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $basename"
                    ((fail_count++))
                fi
            fi
        fi
    done

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to install $fail_count command(s)"
        return 1
    fi

    success "Installed $cmd_count commands"
    return 0
}

install_claude_md() {
    echo ""
    info "Installing CLAUDE.md..."

    if [[ $DRY_RUN -eq 1 ]]; then
        info "[DRY RUN] Would install: CLAUDE.md -> $INSTALL_DIR/CLAUDE.md"
        return 0
    fi

    if [[ $INSTALL_METHOD == "link" ]]; then
        if ! install_file_link "$CLAUDE_MD_SOURCE" "$INSTALL_DIR/CLAUDE.md"; then
            error "Failed to install CLAUDE.md"
            return 1
        fi
    else
        if ! install_file_copy "$CLAUDE_MD_SOURCE" "$INSTALL_DIR/CLAUDE.md"; then
            error "Failed to install CLAUDE.md"
            return 1
        fi
    fi

    add_to_manifest "$INSTALL_DIR/CLAUDE.md"  # Track installed file
    success "Installed CLAUDE.md"
    return 0
}

install_scripts() {
    echo ""
    info "Installing utility scripts..."

    local scripts_count=0
    local fail_count=0

    for script_file in "${SCRIPT_FILES[@]}"; do
        local source_file="$PROJECT_ROOT/scripts/$script_file"

        if [[ ! -f "$source_file" ]]; then
            verbose "Script file not found: $script_file"
            continue
        fi

        local target="$COMMANDS_DIR/scripts/$script_file"

        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would install: $script_file"
            ((scripts_count++))
        else
            mkdir -p "$COMMANDS_DIR/scripts"
            if [[ $INSTALL_METHOD == "link" ]]; then
                if install_file_link "$source_file" "$target"; then
                    ((scripts_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $script_file"
                    ((fail_count++))
                fi
            else
                if install_file_copy "$source_file" "$target"; then
                    ((scripts_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $script_file"
                    ((fail_count++))
                fi
            fi
        fi
    done

    if [[ $scripts_count -gt 0 ]]; then
        success "Installed $scripts_count utility script(s)"
    fi

    return 0
}

install_documentation() {
    if [[ $INCLUDE_DOCS -eq 0 ]]; then
        return 0
    fi

    echo ""
    info "Installing documentation files..."

    local docs_count=0

    for doc_file in "${DOC_FILES[@]}"; do
        local source_file="$PROJECT_ROOT/$doc_file"
        if [[ ! -f "$source_file" ]]; then
            verbose "Documentation file not found: $doc_file"
            continue
        fi

        local target="$INSTALL_DIR/docs/$doc_file"

        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would install: $doc_file"
            ((docs_count++))
        else
            mkdir -p "$INSTALL_DIR/docs"
            if cp "$source_file" "$target"; then
                ((docs_count++))
            else
                warning "Failed to install: $doc_file"
            fi
        fi
    done

    if [[ $docs_count -gt 0 ]]; then
        success "Installed $docs_count documentation file(s)"
    fi

    return 0
}

install_guides() {
    echo ""
    info "Installing guide documents..."

    local guides_count=0
    local fail_count=0

    for guide_file in "${GUIDE_FILES[@]}"; do
        local source_file="$PROJECT_ROOT/$guide_file"

        if [[ ! -f "$source_file" ]]; then
            verbose "Guide file not found: $guide_file"
            continue
        fi

        local target="$COMMANDS_DIR/$guide_file"
        local target_dir=$(dirname "$target")

        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would install: $guide_file"
            ((guides_count++))
        else
            mkdir -p "$target_dir"
            if [[ $INSTALL_METHOD == "link" ]]; then
                if install_file_link "$source_file" "$target"; then
                    ((guides_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $guide_file"
                    ((fail_count++))
                fi
            else
                if install_file_copy "$source_file" "$target"; then
                    ((guides_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $guide_file"
                    ((fail_count++))
                fi
            fi
        fi
    done

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to install $fail_count guide(s)"
        return 1
    fi

    success "Installed $guides_count guide document(s)"
    return 0
}

install_examples() {
    echo ""
    info "Installing example documents..."

    local examples_count=0
    local fail_count=0

    for example_file in "${EXAMPLE_FILES[@]}"; do
        local source_file="$PROJECT_ROOT/$example_file"

        if [[ ! -f "$source_file" ]]; then
            verbose "Example file not found: $example_file"
            continue
        fi

        local target="$COMMANDS_DIR/$example_file"
        local target_dir=$(dirname "$target")

        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would install: $example_file"
            ((examples_count++))
        else
            mkdir -p "$target_dir"
            if [[ $INSTALL_METHOD == "link" ]]; then
                if install_file_link "$source_file" "$target"; then
                    ((examples_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $example_file"
                    ((fail_count++))
                fi
            else
                if install_file_copy "$source_file" "$target"; then
                    ((examples_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $example_file"
                    ((fail_count++))
                fi
            fi
        fi
    done

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to install $fail_count example(s)"
        return 1
    fi

    success "Installed $examples_count example document(s)"
    return 0
}

install_references() {
    echo ""
    info "Installing reference documents..."

    local references_count=0
    local fail_count=0

    for reference_file in "${REFERENCE_FILES[@]}"; do
        local source_file="$PROJECT_ROOT/$reference_file"

        if [[ ! -f "$source_file" ]]; then
            verbose "Reference file not found: $reference_file"
            continue
        fi

        local target="$COMMANDS_DIR/$reference_file"
        local target_dir=$(dirname "$target")

        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would install: $reference_file"
            ((references_count++))
        else
            mkdir -p "$target_dir"
            if [[ $INSTALL_METHOD == "link" ]]; then
                if install_file_link "$source_file" "$target"; then
                    ((references_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $reference_file"
                    ((fail_count++))
                fi
            else
                if install_file_copy "$source_file" "$target"; then
                    ((references_count++))
                    add_to_manifest "$target"  # Track installed file
                else
                    warning "Failed to install: $reference_file"
                    ((fail_count++))
                fi
            fi
        fi
    done

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to install $fail_count reference(s)"
        return 1
    fi

    success "Installed $references_count reference document(s)"
    return 0
}

###############################################################################
# Verification Phase
###############################################################################

verify_installation() {
    if [[ $DRY_RUN -eq 1 ]]; then
        return 0
    fi

    echo ""
    info "Verifying installation..."

    local verify_count=0
    local fail_count=0

    # Verify CLAUDE.md
    if ! [[ -e "$INSTALL_DIR/CLAUDE.md" ]]; then
        error "CLAUDE.md not found after installation"
        ((fail_count++))
    else
        ((verify_count++))
    fi

    # Verify command files
    for cmd_file in "${PROJECT_ROOT}"/wf_*.md; do
        local basename=$(basename "$cmd_file")
        local target="$COMMANDS_DIR/$basename"

        if ! [[ -e "$target" ]]; then
            error "Command file not found after installation: $basename"
            ((fail_count++))
        else
            ((verify_count++))
        fi
    done

    if [[ $fail_count -gt 0 ]]; then
        error "Verification failed: $fail_count file(s) not installed correctly"
        return 1
    fi

    success "Verification passed: all files installed correctly"
    return 0
}

###############################################################################
# Report and Summary
###############################################################################

print_installation_report() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ $DRY_RUN -eq 1 ]]; then
        print_message "$BLUE" "📋 DRY RUN SUMMARY"
    else
        print_message "$GREEN" "✨ INSTALLATION SUMMARY"
    fi

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  Installation Directory:  $COMMANDS_DIR"
    echo "  Configuration File:      $INSTALL_DIR/CLAUDE.md"
    echo "  Installation Method:     $([[ $INSTALL_METHOD == "link" ]] && echo "Symbolic Links (Recommended)" || echo "File Copy")"
    echo "  Backup Created:          $([[ $CREATE_BACKUP -eq 1 ]] && echo "Yes" || echo "No")"
    echo "  Include Documentation:   $([[ $INCLUDE_DOCS -eq 1 ]] && echo "Yes" || echo "No")"
    echo ""

    if [[ -d "$COMMANDS_DIR" ]]; then
        local cmd_count=$(ls -1 "$COMMANDS_DIR" | wc -l)
        echo "  Commands Installed:      $cmd_count"
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

print_next_steps() {
    echo ""
    echo "Next Steps:"
    echo ""
    echo "1. Verify installation:"
    echo "   ls ~/.claude/commands/"
    echo ""
    echo "2. Load project context:"
    echo "   /wf_03_prime"
    echo ""
    echo "3. For detailed usage, read:"
    echo "   cat $INSTALL_DIR/COMMANDS.md"
    echo ""
    if [[ $INSTALL_METHOD == "link" ]]; then
        echo "ℹ️  Note: Commands are symlinked to the project directory."
        echo "   To uninstall, run: ./uninstall.sh from the project directory"
        echo ""
    fi
}

###############################################################################
# Main Execution
###############################################################################

main() {
    echo ""
    print_message "$BLUE" "╔════════════════════════════════════════════════════╗"
    print_message "$BLUE" "║         AI Workflow Installation Script             ║"
    print_message "$BLUE" "╚════════════════════════════════════════════════════╝"
    echo ""

    # Parse arguments
    parse_arguments "$@"

    # Show configuration
    verbose "Configuration:"
    verbose "  INSTALL_METHOD=$INSTALL_METHOD"
    verbose "  CREATE_BACKUP=$CREATE_BACKUP"
    verbose "  INCLUDE_DOCS=$INCLUDE_DOCS"
    verbose "  DRY_RUN=$DRY_RUN"

    # Validation
    validate_installation_environment || exit 1

    # Preparation
    prepare_installation || exit 1

    # Backup (if enabled)
    if [[ $CREATE_BACKUP -eq 1 ]]; then
        create_backup || exit 1
    fi

    # Installation
    install_commands || exit 1
    install_claude_md || exit 1
    install_scripts || exit 1
    install_guides || exit 1  # Critical - guides are referenced by commands
    install_examples || exit 1  # Critical - examples are referenced by wf_14_doc command
    install_references || exit 1  # Critical - references are referenced by commands
    install_documentation || exit 0  # Non-critical

    # Verification
    verify_installation || exit 1

    # Report
    print_installation_report
    print_next_steps

    if [[ $DRY_RUN -eq 1 ]]; then
        info "This was a dry run. No changes were made."
        info "Run './install.sh' (without --dry-run) to perform actual installation."
    else
        success "Installation completed successfully!"
    fi

    exit 0
}

# Run main function with all arguments
main "$@"
