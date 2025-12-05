#!/bin/bash

###############################################################################
# Installation Utilities Library for ai_workflow
#
# Provides common functions for install.sh and uninstall.sh
# Handles file operations, backups, verification, and user feedback
###############################################################################

set -o pipefail

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation directories
INSTALL_DIR="${HOME}/.claude"
COMMANDS_DIR="${INSTALL_DIR}/commands"
BACKUP_DIR="${INSTALL_DIR}/backup"

###############################################################################
# Output Functions
###############################################################################

# Print colored message
print_message() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

# Print info message (blue)
info() {
    print_message "$BLUE" "ℹ️  $1"
}

# Print success message (green)
success() {
    print_message "$GREEN" "✅ $1"
}

# Print warning message (yellow)
warning() {
    print_message "$YELLOW" "⚠️  $1"
}

# Print error message (red)
error() {
    print_message "$RED" "❌ $1"
}

# Print verbose message (only if VERBOSE=1)
verbose() {
    if [[ "${VERBOSE:-0}" == "1" ]]; then
        info "$1"
    fi
}

###############################################################################
# Validation Functions
###############################################################################

# Check if running in the correct directory (ai_workflow root)
check_working_directory() {
    # Check for CLAUDE.md in current directory
    if [[ ! -f "CLAUDE.md" ]]; then
        error "Must run from ai_workflow project root directory"
        error "Current directory: $(pwd)"
        return 1
    fi
    # Also check for at least one wf_*.md command file
    if ! compgen -G "wf_*.md" > /dev/null 2>&1; then
        error "No command files (wf_*.md) found in project directory"
        error "Current directory: $(pwd)"
        return 1
    fi
    verbose "Working directory verified: $(pwd)"
    return 0
}

# Check if target file/directory already exists
check_file_exists() {
    local file="$1"
    if [[ -e "$file" ]]; then
        return 0  # File exists
    else
        return 1  # File doesn't exist
    fi
}

# Check write permissions for directory
check_write_permission() {
    local dir="$1"

    # If directory doesn't exist, check parent
    if [[ ! -d "$dir" ]]; then
        dir=$(dirname "$dir")
    fi

    if [[ ! -w "$dir" ]]; then
        error "No write permission for: $dir"
        return 1
    fi
    return 0
}

# Verify installed file
verify_installed_file() {
    local source="$1"
    local target="$2"

    if [[ ! -e "$target" ]]; then
        error "Installation failed for $target"
        return 1
    fi

    # For symbolic links, verify the link target
    if [[ -L "$target" ]]; then
        local link_target=$(readlink "$target")
        verbose "Verified symlink: $target -> $link_target"
    fi

    verbose "Verified installed file: $target"
    return 0
}

###############################################################################
# Directory Management Functions
###############################################################################

# Create installation directories
create_install_directories() {
    verbose "Creating installation directories..."

    if ! mkdir -p "$COMMANDS_DIR" 2>/dev/null; then
        error "Failed to create $COMMANDS_DIR"
        return 1
    fi
    verbose "Created: $COMMANDS_DIR"

    return 0
}

# Create backup directory with timestamp
create_backup_directory() {
    local backup_timestamp=$(date +%Y-%m-%d_%H-%M-%S)
    local timestamped_backup="${BACKUP_DIR}/${backup_timestamp}"

    if ! mkdir -p "$timestamped_backup" 2>/dev/null; then
        error "Failed to create backup directory: $timestamped_backup"
        return 1
    fi

    echo "$timestamped_backup"
    return 0
}

###############################################################################
# Backup Functions
###############################################################################

# Backup existing file before installation
backup_file() {
    local source_file="$1"
    local backup_dir="$2"
    local filename=$(basename "$source_file")

    if [[ ! -e "$source_file" ]]; then
        verbose "No existing file to backup: $source_file"
        return 0
    fi

    if ! cp "$source_file" "${backup_dir}/${filename}" 2>/dev/null; then
        error "Failed to backup: $source_file"
        return 1
    fi

    success "Backed up: $source_file -> ${backup_dir}/${filename}"
    return 0
}

# Restore file from backup
restore_file() {
    local backup_file="$1"
    local target_file="$2"

    if [[ ! -e "$backup_file" ]]; then
        error "Backup file not found: $backup_file"
        return 1
    fi

    if ! cp "$backup_file" "$target_file" 2>/dev/null; then
        error "Failed to restore: $target_file from $backup_file"
        return 1
    fi

    success "Restored: $target_file from $backup_file"
    return 0
}

###############################################################################
# Installation Functions
###############################################################################

# Install file by copying
install_file_copy() {
    local source="$1"
    local target="$2"

    verbose "Copying: $source -> $target"

    if ! cp "$source" "$target" 2>/dev/null; then
        error "Failed to copy: $source to $target"
        return 1
    fi

    if ! verify_installed_file "$source" "$target"; then
        return 1
    fi

    return 0
}

# Install file by symbolic link
install_file_link() {
    local source="$1"
    local target="$2"
    local abs_source=$(cd "$(dirname "$source")" && pwd)/$(basename "$source")

    verbose "Creating symlink: $target -> $abs_source"

    # Remove existing target if it exists (already backed up)
    if [[ -e "$target" ]] || [[ -L "$target" ]]; then
        rm -f "$target"
    fi

    if ! ln -s "$abs_source" "$target" 2>/dev/null; then
        error "Failed to create symlink: $target -> $abs_source"
        return 1
    fi

    if ! verify_installed_file "$source" "$target"; then
        return 1
    fi

    return 0
}

###############################################################################
# Cleanup Functions
###############################################################################

# Remove installed files
remove_installed_files() {
    local files_to_remove=("$@")

    for file in "${files_to_remove[@]}"; do
        if [[ -e "$file" ]] || [[ -L "$file" ]]; then
            verbose "Removing: $file"
            if ! rm -f "$file" 2>/dev/null; then
                error "Failed to remove: $file"
                return 1
            fi
        fi
    done

    return 0
}

# Clean up empty directories
cleanup_empty_directories() {
    local dirs=("$@")

    for dir in "${dirs[@]}"; do
        # Only remove if directory is empty
        if [[ -d "$dir" ]] && [[ -z "$(ls -A "$dir" 2>/dev/null)" ]]; then
            verbose "Removing empty directory: $dir"
            rmdir "$dir" 2>/dev/null
        fi
    done

    return 0
}

###############################################################################
# Utility Functions
###############################################################################

# List installed files
list_installed_files() {
    if [[ ! -d "$COMMANDS_DIR" ]]; then
        info "No installed commands found"
        return 0
    fi

    echo ""
    info "Installed commands in $COMMANDS_DIR:"
    ls -1 "$COMMANDS_DIR" | sed 's/^/  /'
    echo ""

    if [[ -f "$INSTALL_DIR/CLAUDE.md" ]]; then
        info "Configuration: $INSTALL_DIR/CLAUDE.md"
    fi
}

# Count installed files
count_installed_files() {
    if [[ ! -d "$COMMANDS_DIR" ]]; then
        echo 0
        return 0
    fi

    ls -1 "$COMMANDS_DIR" 2>/dev/null | wc -l
}

# List available backup snapshots
list_backup_snapshots() {
    if [[ ! -d "$BACKUP_DIR" ]]; then
        info "No backups found"
        return 0
    fi

    echo ""
    info "Available backup snapshots:"
    ls -1d "${BACKUP_DIR}"/*/ 2>/dev/null | xargs -I {} basename {} | sed 's/^/  /'
    echo ""
}

# Parse yes/no response from user
prompt_yes_no() {
    local prompt="$1"
    local response

    while true; do
        read -p "${prompt} (y/n): " -r response
        case "$response" in
            [yY][eE][sS]|[yY])
                return 0
                ;;
            [nN][oO]|[nN])
                return 1
                ;;
            *)
                echo "Please answer y or n"
                ;;
        esac
    done
}

###############################################################################
# Status Report Functions
###############################################################################

# Print installation summary
print_install_summary() {
    local method="$1"
    local file_count="$2"

    echo ""
    success "Installation completed successfully!"
    echo ""
    info "Summary:"
    echo "  - Installation method: $method"
    echo "  - Files installed: $file_count"
    echo "  - Commands directory: $COMMANDS_DIR"
    echo "  - Configuration: $INSTALL_DIR/CLAUDE.md"
    echo ""
}

# Print uninstall summary
print_uninstall_summary() {
    echo ""
    success "Uninstallation completed successfully!"
    echo ""
}

# Print backup information
print_backup_info() {
    local backup_dir="$1"

    echo ""
    info "Backup created: $backup_dir"
    echo "  Use this directory to recover previous configuration if needed"
    echo ""
}

###############################################################################
# Error Handling
###############################################################################

# Clean up on error (rollback)
cleanup_on_error() {
    error "Installation failed, attempting rollback..."
    # This should be called with specific cleanup logic from install.sh
}

# Exit with error message
exit_with_error() {
    local message="$1"
    error "$message"
    exit 1
}

###############################################################################
# Installation Manifest Functions (NEW - Track installed files)
###############################################################################

# Manifest file location
MANIFEST_FILE="${COMMANDS_DIR}/.ai_workflow_manifest"

# Create or reset installation manifest
create_installation_manifest() {
    verbose "Creating installation manifest: $MANIFEST_FILE"

    # Create manifest with header
    cat > "$MANIFEST_FILE" << 'EOF'
# AI Workflow Installation Manifest
# This file tracks files installed by ai_workflow
# DO NOT EDIT MANUALLY - Managed by install.sh/uninstall.sh
#
# Format: One file path per line (relative to ~/.claude/)
# Lines starting with # are comments
EOF

    if [[ ! -f "$MANIFEST_FILE" ]]; then
        error "Failed to create manifest file: $MANIFEST_FILE"
        return 1
    fi

    verbose "Manifest created successfully"
    return 0
}

# Add file to installation manifest
add_to_manifest() {
    local installed_file="$1"

    # Convert to relative path from INSTALL_DIR
    local rel_path="${installed_file#${INSTALL_DIR}/}"

    # Avoid duplicates
    if grep -Fxq "$rel_path" "$MANIFEST_FILE" 2>/dev/null; then
        verbose "Already in manifest: $rel_path"
        return 0
    fi

    echo "$rel_path" >> "$MANIFEST_FILE"
    verbose "Added to manifest: $rel_path"
    return 0
}

# Read manifest and return list of installed files
read_manifest() {
    if [[ ! -f "$MANIFEST_FILE" ]]; then
        warning "Manifest file not found: $MANIFEST_FILE"
        return 1
    fi

    # Read non-comment, non-empty lines
    grep -v '^#' "$MANIFEST_FILE" | grep -v '^$' || true
    return 0
}

# Check if manifest exists
manifest_exists() {
    [[ -f "$MANIFEST_FILE" ]]
}

# Remove file from manifest
remove_from_manifest() {
    local file_to_remove="$1"
    local rel_path="${file_to_remove#${INSTALL_DIR}/}"

    if [[ ! -f "$MANIFEST_FILE" ]]; then
        return 0
    fi

    # Create temporary file without the line
    grep -Fxv "$rel_path" "$MANIFEST_FILE" > "${MANIFEST_FILE}.tmp" 2>/dev/null || true
    mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"

    verbose "Removed from manifest: $rel_path"
    return 0
}

# Count files in manifest
count_manifest_files() {
    if [[ ! -f "$MANIFEST_FILE" ]]; then
        echo 0
        return 0
    fi

    read_manifest | wc -l
    return 0
}

# Verify all manifest files exist
verify_manifest_files() {
    if [[ ! -f "$MANIFEST_FILE" ]]; then
        warning "No manifest file to verify"
        return 1
    fi

    local missing_count=0
    local total_count=0

    while IFS= read -r rel_path; do
        ((total_count++))
        local full_path="${INSTALL_DIR}/${rel_path}"

        if [[ ! -e "$full_path" ]]; then
            warning "Missing file from manifest: $rel_path"
            ((missing_count++))
        fi
    done < <(read_manifest)

    if [[ $missing_count -gt 0 ]]; then
        error "Manifest verification failed: $missing_count/$total_count files missing"
        return 1
    fi

    success "Manifest verification passed: all $total_count files present"
    return 0
}

###############################################################################
# Export functions for use in scripts
###############################################################################

export -f print_message info success warning error verbose
export -f check_working_directory check_file_exists check_write_permission verify_installed_file
export -f create_install_directories create_backup_directory
export -f backup_file restore_file
export -f install_file_copy install_file_link
export -f remove_installed_files cleanup_empty_directories
export -f list_installed_files count_installed_files list_backup_snapshots prompt_yes_no
export -f print_install_summary print_uninstall_summary print_backup_info
export -f cleanup_on_error exit_with_error

# NEW: Export manifest functions
export -f create_installation_manifest add_to_manifest read_manifest manifest_exists
export -f remove_from_manifest count_manifest_files verify_manifest_files

export INSTALL_DIR COMMANDS_DIR BACKUP_DIR
export RED GREEN YELLOW BLUE NC
export MANIFEST_FILE
