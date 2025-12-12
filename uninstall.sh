#!/bin/bash

# Strict mode for better error handling
set -euo pipefail
IFS=$'\n\t'

###############################################################################
# AI Workflow Uninstallation Script
#
# Removes ai_workflow commands from ~/.claude/commands/
# and optionally CLAUDE.md from ~/.claude/
#
# Usage: ./uninstall.sh [OPTIONS]
# Options:
#   --force         Skip confirmation prompt
#   --keep-config   Keep CLAUDE.md file (don't remove)
#   --clean-backup  Also delete backup directory
#   --dry-run       Simulate uninstallation without making changes
#   --verbose       Show detailed output
#   --help          Display this help message
#
# Examples:
#   ./uninstall.sh              # Interactive uninstall
#   ./uninstall.sh --force      # Uninstall without confirmation
#   ./uninstall.sh --keep-config # Keep CLAUDE.md
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
FORCE_UNINSTALL=0
KEEP_CONFIG=0
CLEAN_BACKUP=0
DRY_RUN=0
VERBOSE=0

# Project structure
PROJECT_ROOT="${SCRIPT_DIR}"

###############################################################################
# Help and Usage
###############################################################################

show_help() {
    cat << EOF
AI Workflow Uninstallation Script

USAGE:
    ./uninstall.sh [OPTIONS]

OPTIONS:
    --force         Skip confirmation prompt and proceed with uninstallation

    --keep-config   Keep CLAUDE.md in ~/.claude/ (don't remove it)

    --clean-backup  Also delete backup directory (~/.claude/backup/)
                    Use with caution - this removes recovery points

    --dry-run       Simulate uninstallation without making changes
                    Shows what would be removed

    --verbose       Show detailed output including all file operations

    --help          Display this help message

EXAMPLES:
    # Interactive uninstall (with confirmation)
    ./uninstall.sh

    # Uninstall without confirmation
    ./uninstall.sh --force

    # Uninstall but keep CLAUDE.md configuration
    ./uninstall.sh --keep-config

    # Test what would be removed
    ./uninstall.sh --dry-run

    # Complete cleanup including backups
    ./uninstall.sh --force --clean-backup

NOTES:
    - By default, this script will ask for confirmation before removing files
    - Use --force to skip confirmation (useful in scripts)
    - Use --keep-config to preserve CLAUDE.md in case you customized it
    - Backups are kept by default for recovery purposes
    - Use --clean-backup to also remove backup directory

RECOVERY:
    If you need to recover removed files:
    1. Check ~/.claude/backup/ for available backups
    2. Run: cp ~/.claude/backup/YYYY-MM-DD_HH-MM-SS/* ~/.claude/commands/

EOF
}

###############################################################################
# Argument Parsing
###############################################################################

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --force)
                FORCE_UNINSTALL=1
                shift
                ;;
            --keep-config)
                KEEP_CONFIG=1
                shift
                ;;
            --clean-backup)
                CLEAN_BACKUP=1
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

validate_uninstallation_environment() {
    echo ""
    info "Validating uninstallation environment..."

    # Check working directory
    if ! check_working_directory; then
        error "Not in ai_workflow project directory"
        echo ""
        echo "Note: To uninstall, you must be in the ai_workflow project directory"
        echo "This prevents accidental uninstallation when project is deleted/moved"
        exit 1
    fi

    # Check if manifest exists
    if manifest_exists; then
        local file_count=$(count_manifest_files)
        info "Found installation manifest with $file_count tracked file(s)"
        verbose "Manifest file: $MANIFEST_FILE"
    else
        warning "No installation manifest found - will use fallback detection"
        warning "This may not preserve non-repo files in commands directory"
    fi

    # Check if anything is actually installed
    if [[ ! -d "$COMMANDS_DIR" ]] || [[ -z "$(ls -A "$COMMANDS_DIR" 2>/dev/null)" ]]; then
        warning "No installed commands found in $COMMANDS_DIR"
    fi

    if [[ ! -f "$INSTALL_DIR/CLAUDE.md" ]]; then
        warning "CLAUDE.md not found in $INSTALL_DIR"
    fi

    # Check write permission
    if ! check_write_permission "$INSTALL_DIR"; then
        exit_with_error "No write permission for $INSTALL_DIR"
    fi

    success "Environment validation passed"
}

###############################################################################
# Confirmation Phase
###############################################################################

confirm_uninstallation() {
    if [[ $FORCE_UNINSTALL -eq 1 ]]; then
        verbose "Force mode enabled, skipping confirmation"
        return 0
    fi

    echo ""
    list_installed_files

    echo ""
    echo "⚠️  WARNING: This will remove all installed ai_workflow commands"
    echo ""
    if [[ $KEEP_CONFIG -ne 1 ]]; then
        echo "Files to be removed:"
        echo "  - $COMMANDS_DIR/ (all command files)"
        echo "  - $INSTALL_DIR/CLAUDE.md"
        echo ""
    else
        echo "Files to be removed:"
        echo "  - $COMMANDS_DIR/ (all command files)"
        echo ""
        echo "Files to be kept:"
        echo "  - $INSTALL_DIR/CLAUDE.md (--keep-config)"
        echo ""
    fi

    if ! prompt_yes_no "Proceed with uninstallation?"; then
        info "Uninstallation cancelled"
        exit 0
    fi
}

###############################################################################
# Uninstallation Phase
###############################################################################

uninstall_commands() {
    echo ""
    info "Removing command files..."

    local removed_count=0
    local fail_count=0

    if [[ ! -d "$COMMANDS_DIR" ]]; then
        verbose "Commands directory does not exist"
        return 0
    fi

    # Get list of command files from manifest (safe approach)
    local cmd_files=()
    if manifest_exists; then
        # Read from manifest - only delete tracked files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process command files (wf_*.md) from manifest
            if [[ "$(basename "$full_path")" == wf_*.md ]]; then
                if [[ -e "$full_path" ]]; then
                    cmd_files+=("$full_path")
                fi
            fi
        done < <(read_manifest)
        verbose "Found ${#cmd_files[@]} command file(s) in manifest"
    else
        # Fallback: use find pattern (legacy installations without manifest)
        warning "No manifest found - using fallback file detection"
        warning "This may affect non-repo files in commands directory"
        while IFS= read -r -d '' file; do
            cmd_files+=("$file")
        done < <(find "$COMMANDS_DIR" -maxdepth 1 -name "wf_*.md" -print0 2>/dev/null)
    fi

    if [[ ${#cmd_files[@]} -eq 0 ]]; then
        verbose "No command files to remove"
        return 0
    fi

    for cmd_file in "${cmd_files[@]}"; do
        local basename=$(basename "$cmd_file")

        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would remove: $cmd_file"
            ((removed_count++))
        else
            if rm -f "$cmd_file"; then
                ((removed_count++))
                verbose "Removed: $cmd_file"
            else
                error "Failed to remove: $cmd_file"
                ((fail_count++))
            fi
        fi
    done

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to remove $fail_count command file(s)"
        return 1
    fi

    success "Removed $removed_count command file(s)"
    return 0
}

uninstall_claude_md() {
    if [[ $KEEP_CONFIG -eq 1 ]]; then
        verbose "Keeping CLAUDE.md (--keep-config)"
        return 0
    fi

    echo ""
    info "Removing CLAUDE.md..."

    if [[ ! -e "$INSTALL_DIR/CLAUDE.md" ]]; then
        verbose "CLAUDE.md not found, skipping"
        return 0
    fi

    if [[ $DRY_RUN -eq 1 ]]; then
        info "[DRY RUN] Would remove: $INSTALL_DIR/CLAUDE.md"
        return 0
    fi

    if rm -f "$INSTALL_DIR/CLAUDE.md"; then
        success "Removed CLAUDE.md"
        return 0
    else
        error "Failed to remove CLAUDE.md"
        return 1
    fi
}

uninstall_scripts() {
    echo ""
    info "Removing utility scripts..."

    local scripts_dir="$COMMANDS_DIR/scripts"
    local removed_count=0

    if [[ ! -d "$scripts_dir" ]]; then
        verbose "Scripts directory does not exist"
        return 0
    fi

    # Use manifest-based deletion if available
    if manifest_exists; then
        # Read from manifest - only delete tracked script files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process files in scripts directory
            if [[ "$full_path" == "$scripts_dir"/* ]]; then
                if [[ ! -e "$full_path" ]]; then
                    continue
                fi

                if [[ $DRY_RUN -eq 1 ]]; then
                    info "[DRY RUN] Would remove: $(basename $full_path)"
                    ((removed_count++))
                else
                    if rm -f "$full_path"; then
                        ((removed_count++))
                        verbose "Removed: $full_path"
                    fi
                fi
            fi
        done < <(read_manifest)
    else
        # Fallback: use SCRIPT_FILES array (legacy)
        warning "No manifest found - using fallback script detection"
        for script_file in "${SCRIPT_FILES[@]}"; do
            local target="$scripts_dir/$script_file"

            if [[ ! -e "$target" ]]; then
                continue
            fi

            if [[ $DRY_RUN -eq 1 ]]; then
                info "[DRY RUN] Would remove: $(basename $target)"
                ((removed_count++))
            else
                if rm -f "$target"; then
                    ((removed_count++))
                    verbose "Removed: $target"
                fi
            fi
        done
    fi

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$scripts_dir" 2>/dev/null
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count utility script(s)"
    fi

    return 0
}

uninstall_guides() {
    echo ""
    info "Removing guide documents..."

    local guides_dir="$COMMANDS_DIR/docs/guides"
    local removed_count=0
    local fail_count=0

    if [[ ! -d "$guides_dir" ]]; then
        verbose "Guides directory does not exist"
        return 0
    fi

    # Use manifest-based deletion if available
    if manifest_exists; then
        # Read from manifest - only delete tracked guide files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process files in guides directory
            if [[ "$full_path" == "$guides_dir"/* ]]; then
                if [[ ! -e "$full_path" ]]; then
                    continue
                fi

                if [[ $DRY_RUN -eq 1 ]]; then
                    info "[DRY RUN] Would remove: ${rel_path#commands/}"
                    ((removed_count++))
                else
                    if rm -f "$full_path"; then
                        ((removed_count++))
                        verbose "Removed: $full_path"
                    else
                        error "Failed to remove: $full_path"
                        ((fail_count++))
                    fi
                fi
            fi
        done < <(read_manifest)
    else
        # Fallback: use GUIDE_FILES array (legacy)
        warning "No manifest found - using fallback guide detection"
        for guide_file in "${GUIDE_FILES[@]}"; do
            local target="$COMMANDS_DIR/$guide_file"

            if [[ ! -e "$target" ]]; then
                continue
            fi

            if [[ $DRY_RUN -eq 1 ]]; then
                info "[DRY RUN] Would remove: $guide_file"
                ((removed_count++))
            else
                if rm -f "$target"; then
                    ((removed_count++))
                    verbose "Removed: $target"
                else
                    error "Failed to remove: $target"
                    ((fail_count++))
                fi
            fi
        done
    fi

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$guides_dir" "$COMMANDS_DIR/docs" "$COMMANDS_DIR" 2>/dev/null
    fi

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to remove $fail_count guide(s)"
        return 1
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count guide document(s)"
    fi

    return 0
}

uninstall_examples() {
    echo ""
    info "Removing example documents..."

    local examples_dir="$COMMANDS_DIR/docs/examples"
    local removed_count=0
    local fail_count=0

    if [[ ! -d "$examples_dir" ]]; then
        verbose "Examples directory does not exist"
        return 0
    fi

    # Use manifest-based deletion if available
    if manifest_exists; then
        # Read from manifest - only delete tracked example files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process files in examples directory
            if [[ "$full_path" == "$examples_dir"/* ]]; then
                if [[ ! -e "$full_path" ]]; then
                    continue
                fi

                if [[ $DRY_RUN -eq 1 ]]; then
                    info "[DRY RUN] Would remove: ${rel_path#commands/}"
                    ((removed_count++))
                else
                    if rm -f "$full_path"; then
                        ((removed_count++))
                        verbose "Removed: $full_path"
                    else
                        error "Failed to remove: $full_path"
                        ((fail_count++))
                    fi
                fi
            fi
        done < <(read_manifest)
    else
        # Fallback: use EXAMPLE_FILES array (legacy)
        warning "No manifest found - using fallback example detection"
        for example_file in "${EXAMPLE_FILES[@]}"; do
            local target="$COMMANDS_DIR/$example_file"

            if [[ ! -e "$target" ]]; then
                continue
            fi

            if [[ $DRY_RUN -eq 1 ]]; then
                info "[DRY RUN] Would remove: $example_file"
                ((removed_count++))
            else
                if rm -f "$target"; then
                    ((removed_count++))
                    verbose "Removed: $target"
                else
                    error "Failed to remove: $target"
                    ((fail_count++))
                fi
            fi
        done
    fi

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$examples_dir" "$COMMANDS_DIR/docs" "$COMMANDS_DIR" 2>/dev/null
    fi

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to remove $fail_count example(s)"
        return 1
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count example document(s)"
    fi

    return 0
}

uninstall_references() {
    echo ""
    info "Removing reference documents..."

    local references_dir="$COMMANDS_DIR/docs/reference"
    local removed_count=0
    local fail_count=0

    if [[ ! -d "$references_dir" ]]; then
        verbose "References directory does not exist"
        return 0
    fi

    # Use manifest-based deletion if available
    if manifest_exists; then
        # Read from manifest - only delete tracked reference files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process files in references directory
            if [[ "$full_path" == "$references_dir"/* ]]; then
                if [[ ! -e "$full_path" ]]; then
                    continue
                fi

                if [[ $DRY_RUN -eq 1 ]]; then
                    info "[DRY RUN] Would remove: ${rel_path#commands/}"
                    ((removed_count++))
                else
                    if rm -f "$full_path"; then
                        ((removed_count++))
                        verbose "Removed: $full_path"
                    else
                        error "Failed to remove: $full_path"
                        ((fail_count++))
                    fi
                fi
            fi
        done < <(read_manifest)
    else
        # Fallback: use REFERENCE_FILES array (legacy)
        warning "No manifest found - using fallback reference detection"
        for reference_file in "${REFERENCE_FILES[@]}"; do
            local target="$COMMANDS_DIR/$reference_file"

            if [[ ! -e "$target" ]]; then
                continue
            fi

            if [[ $DRY_RUN -eq 1 ]]; then
                info "[DRY RUN] Would remove: $reference_file"
                ((removed_count++))
            else
                if rm -f "$target"; then
                    ((removed_count++))
                    verbose "Removed: $target"
                else
                    error "Failed to remove: $target"
                    ((fail_count++))
                fi
            fi
        done
    fi

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$references_dir" "$COMMANDS_DIR/docs" "$COMMANDS_DIR" 2>/dev/null
    fi

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to remove $fail_count reference(s)"
        return 1
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count reference document(s)"
    fi

    return 0
}

uninstall_commands_lib() {
    echo ""
    info "Removing commands library files..."

    local lib_dir="$COMMANDS_DIR/commands/lib"
    local removed_count=0
    local fail_count=0

    if [[ ! -d "$lib_dir" ]]; then
        verbose "Commands library directory does not exist"
        return 0
    fi

    # Use manifest-based deletion if available
    if manifest_exists; then
        # Read from manifest - only delete tracked library files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process files in library directory
            if [[ "$full_path" == "$lib_dir"/* ]]; then
                if [[ ! -e "$full_path" ]]; then
                    continue
                fi

                if [[ $DRY_RUN -eq 1 ]]; then
                    info "[DRY RUN] Would remove: ${rel_path#commands/}"
                    ((removed_count++))
                else
                    if rm -f "$full_path"; then
                        ((removed_count++))
                        verbose "Removed: $full_path"
                    else
                        error "Failed to remove: $full_path"
                        ((fail_count++))
                    fi
                fi
            fi
        done < <(read_manifest)
    else
        # Fallback: use COMMANDS_LIB_FILES array (legacy)
        warning "No manifest found - using fallback library detection"
        for lib_file in "${COMMANDS_LIB_FILES[@]}"; do
            local target="$COMMANDS_DIR/$lib_file"

            if [[ ! -e "$target" ]]; then
                continue
            fi

            if [[ $DRY_RUN -eq 1 ]]; then
                info "[DRY RUN] Would remove: $lib_file"
                ((removed_count++))
            else
                if rm -f "$target"; then
                    ((removed_count++))
                    verbose "Removed: $target"
                else
                    error "Failed to remove: $target"
                    ((fail_count++))
                fi
            fi
        done
    fi

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$lib_dir" "$COMMANDS_DIR/commands" "$COMMANDS_DIR" 2>/dev/null
    fi

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to remove $fail_count library file(s)"
        return 1
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count library file(s)"
    fi

    return 0
}

uninstall_commands_agents() {
    echo ""
    info "Removing commands agent files..."

    local agents_dir="$COMMANDS_DIR/commands/agents"
    local removed_count=0
    local fail_count=0

    if [[ ! -d "$agents_dir" ]]; then
        verbose "Commands agents directory does not exist"
        return 0
    fi

    # Use manifest-based deletion if available
    if manifest_exists; then
        # Read from manifest - only delete tracked agent files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process files in agents directory
            if [[ "$full_path" == "$agents_dir"/* ]]; then
                if [[ ! -e "$full_path" ]]; then
                    continue
                fi

                if [[ $DRY_RUN -eq 1 ]]; then
                    info "[DRY RUN] Would remove: ${rel_path#commands/}"
                    ((removed_count++))
                else
                    if rm -f "$full_path"; then
                        ((removed_count++))
                        verbose "Removed: $full_path"
                    else
                        error "Failed to remove: $full_path"
                        ((fail_count++))
                    fi
                fi
            fi
        done < <(read_manifest)
    else
        # Fallback: use COMMANDS_AGENTS_FILES array (legacy)
        warning "No manifest found - using fallback agents detection"
        for agent_file in "${COMMANDS_AGENTS_FILES[@]}"; do
            local target="$COMMANDS_DIR/$agent_file"

            if [[ ! -e "$target" ]]; then
                continue
            fi

            if [[ $DRY_RUN -eq 1 ]]; then
                info "[DRY RUN] Would remove: $agent_file"
                ((removed_count++))
            else
                if rm -f "$target"; then
                    ((removed_count++))
                    verbose "Removed: $target"
                else
                    error "Failed to remove: $target"
                    ((fail_count++))
                fi
            fi
        done
    fi

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$agents_dir" "$COMMANDS_DIR/commands" "$COMMANDS_DIR" 2>/dev/null
    fi

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to remove $fail_count agent file(s)"
        return 1
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count agent file(s)"
    fi

    return 0
}

uninstall_src_mcp() {
    echo ""
    info "Removing MCP source files..."

    local mcp_dir="$COMMANDS_DIR/src/mcp"
    local removed_count=0
    local fail_count=0

    if [[ ! -d "$mcp_dir" ]]; then
        verbose "MCP source directory does not exist"
        return 0
    fi

    # Use manifest-based deletion if available
    if manifest_exists; then
        # Read from manifest - only delete tracked MCP files
        while IFS= read -r rel_path; do
            local full_path="${INSTALL_DIR}/${rel_path}"
            # Only process files in MCP directory
            if [[ "$full_path" == "$mcp_dir"/* || "$full_path" == "$COMMANDS_DIR/src/__init__.py" ]]; then
                if [[ ! -e "$full_path" ]]; then
                    continue
                fi

                if [[ $DRY_RUN -eq 1 ]]; then
                    info "[DRY RUN] Would remove: ${rel_path#commands/}"
                    ((removed_count++))
                else
                    if rm -f "$full_path"; then
                        ((removed_count++))
                        verbose "Removed: $full_path"
                    else
                        error "Failed to remove: $full_path"
                        ((fail_count++))
                    fi
                fi
            fi
        done < <(read_manifest)
    else
        # Fallback: use SRC_MCP_FILES array (legacy)
        warning "No manifest found - using fallback MCP detection"
        for mcp_file in "${SRC_MCP_FILES[@]}"; do
            local target="$COMMANDS_DIR/$mcp_file"

            if [[ ! -e "$target" ]]; then
                continue
            fi

            if [[ $DRY_RUN -eq 1 ]]; then
                info "[DRY RUN] Would remove: $mcp_file"
                ((removed_count++))
            else
                if rm -f "$target"; then
                    ((removed_count++))
                    verbose "Removed: $target"
                else
                    error "Failed to remove: $target"
                    ((fail_count++))
                fi
            fi
        done
    fi

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$mcp_dir" "$COMMANDS_DIR/src" "$COMMANDS_DIR" 2>/dev/null
    fi

    if [[ $fail_count -gt 0 ]]; then
        error "Failed to remove $fail_count MCP file(s)"
        return 1
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count MCP file(s)"
    fi

    return 0
}

uninstall_documentation() {
    echo ""
    info "Removing documentation files..."

    local docs_dir="$INSTALL_DIR/docs"
    local removed_count=0

    if [[ ! -d "$docs_dir" ]]; then
        verbose "Documentation directory does not exist"
        return 0
    fi

    local doc_files=()
    while IFS= read -r -d '' file; do
        doc_files+=("$file")
    done < <(find "$docs_dir" -type f -print0 2>/dev/null)

    if [[ ${#doc_files[@]} -eq 0 ]]; then
        verbose "No documentation files to remove"
        return 0
    fi

    for doc_file in "${doc_files[@]}"; do
        if [[ $DRY_RUN -eq 1 ]]; then
            info "[DRY RUN] Would remove: $doc_file"
            ((removed_count++))
        else
            if rm -f "$doc_file"; then
                ((removed_count++))
                verbose "Removed: $doc_file"
            fi
        fi
    done

    # Clean up empty directories
    if [[ $DRY_RUN -ne 1 ]]; then
        cleanup_empty_directories "$docs_dir" "$COMMANDS_DIR" 2>/dev/null
    fi

    if [[ $removed_count -gt 0 ]]; then
        success "Removed $removed_count documentation file(s)"
    fi

    return 0
}

###############################################################################
# Cleanup Phase
###############################################################################

cleanup_backups() {
    if [[ $CLEAN_BACKUP -ne 1 ]]; then
        verbose "Keeping backup directory (use --clean-backup to remove)"
        return 0
    fi

    echo ""
    echo "⚠️  WARNING: This will delete backup directory"

    if ! prompt_yes_no "Remove backup directory: $BACKUP_DIR?"; then
        info "Backup directory retained"
        return 0
    fi

    echo ""
    info "Removing backup directory..."

    if [[ ! -d "$BACKUP_DIR" ]]; then
        verbose "Backup directory does not exist"
        return 0
    fi

    if [[ $DRY_RUN -eq 1 ]]; then
        info "[DRY RUN] Would remove: $BACKUP_DIR"
        return 0
    fi

    if rm -rf "$BACKUP_DIR"; then
        success "Removed backup directory"
        return 0
    else
        error "Failed to remove backup directory"
        return 1
    fi
}

###############################################################################
# Verification Phase
###############################################################################

verify_uninstallation() {
    if [[ $DRY_RUN -eq 1 ]]; then
        return 0
    fi

    echo ""
    info "Verifying uninstallation..."

    local remaining_count=0

    # Check commands directory
    if [[ -d "$COMMANDS_DIR" ]]; then
        remaining_count=$(ls -1 "$COMMANDS_DIR" 2>/dev/null | wc -l)
    fi

    # Check CLAUDE.md
    if [[ ! $KEEP_CONFIG -eq 1 ]] && [[ -e "$INSTALL_DIR/CLAUDE.md" ]]; then
        error "CLAUDE.md still exists after uninstallation"
        return 1
    fi

    if [[ $remaining_count -gt 0 ]]; then
        error "Found $remaining_count file(s) still in $COMMANDS_DIR"
        return 1
    fi

    success "Verification passed: all files removed"
    return 0
}

###############################################################################
# Report and Summary
###############################################################################

print_uninstallation_report() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ $DRY_RUN -eq 1 ]]; then
        print_message "$BLUE" "📋 DRY RUN SUMMARY"
    else
        print_message "$GREEN" "✨ UNINSTALLATION SUMMARY"
    fi

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  Commands Removed:     $COMMANDS_DIR"
    echo "  Configuration:        $([[ $KEEP_CONFIG -eq 1 ]] && echo "KEPT" || echo "REMOVED")"
    echo "  Backup Directory:     $([[ $CLEAN_BACKUP -eq 1 ]] && echo "REMOVED" || echo "KEPT")"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

print_recovery_info() {
    echo ""
    echo "Recovery Information:"
    echo ""

    if [[ -d "$BACKUP_DIR" ]] && [[ -n "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]]; then
        echo "Backups are available in: $BACKUP_DIR"
        echo ""
        echo "To recover files from a backup:"
        echo "  1. List available backups:"
        echo "     ls -la $BACKUP_DIR"
        echo ""
        echo "  2. Restore from backup:"
        echo "     cp -r $BACKUP_DIR/YYYY-MM-DD_HH-MM-SS/* $INSTALL_DIR/"
        echo ""
    else
        echo "No backups found. To reinstall, run:"
        echo "  ./install.sh"
        echo ""
    fi
}

###############################################################################
# Main Execution
###############################################################################

main() {
    echo ""
    print_message "$BLUE" "╔════════════════════════════════════════════════════╗"
    print_message "$BLUE" "║       AI Workflow Uninstallation Script             ║"
    print_message "$BLUE" "╚════════════════════════════════════════════════════╝"
    echo ""

    # Parse arguments
    parse_arguments "$@"

    # Show configuration
    verbose "Configuration:"
    verbose "  FORCE_UNINSTALL=$FORCE_UNINSTALL"
    verbose "  KEEP_CONFIG=$KEEP_CONFIG"
    verbose "  CLEAN_BACKUP=$CLEAN_BACKUP"
    verbose "  DRY_RUN=$DRY_RUN"

    # Validation
    validate_uninstallation_environment || exit 1

    # Confirmation (unless --force)
    confirm_uninstallation || exit 0

    # Uninstallation
    uninstall_commands || exit 1
    uninstall_claude_md || exit 1
    uninstall_scripts || exit 1
    uninstall_guides || exit 1  # Critical - guides are referenced by commands
    uninstall_examples || exit 1  # Critical - examples are referenced by wf_14_doc command
    uninstall_references || exit 1  # Critical - references are referenced by commands
    uninstall_commands_lib || exit 1  # Critical - libraries used by coordination engine
    uninstall_commands_agents || exit 1  # Critical - agent definitions for multi-agent workflows
    uninstall_src_mcp || exit 1  # Critical - MCP Gateway required by all commands
    uninstall_documentation || exit 0  # Non-critical

    # Cleanup backups (if --clean-backup)
    cleanup_backups || exit 1

    # Verification
    verify_uninstallation || exit 1

    # Clean up manifest file (last step)
    if [[ $DRY_RUN -eq 0 ]] && manifest_exists; then
        verbose "Removing installation manifest: $MANIFEST_FILE"
        if rm -f "$MANIFEST_FILE"; then
            verbose "Manifest file removed"
        else
            warning "Failed to remove manifest file: $MANIFEST_FILE"
        fi
    fi

    # Report
    print_uninstallation_report
    print_recovery_info

    if [[ $DRY_RUN -eq 1 ]]; then
        info "This was a dry run. No changes were made."
        info "Run './uninstall.sh' (without --dry-run) to perform actual uninstallation."
    else
        success "Uninstallation completed successfully!"
    fi

    exit 0
}

# Run main function with all arguments
main "$@"
