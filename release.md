# AppBridge Release & Update System

AppBridge uses GitHub Releases for its update and installation system. This document explains how to set up releases so the application can correctly identify and apply updates.

## Tagging Convention

AppBridge expects tags to follow Semantic Versioning (e.g., `v1.2.3`).
- The 'v' prefix is optional but recommended.
- The version in the code (`src/core/updater.py`) must match the tag for the app to consider itself up-to-date.

## Creating a Release

When you are ready to release a new version:

1. **Update the Version in Code**:
   Modify `VERSION = "X.Y.Z"` in `src/core/updater.py` to match your new version.
2. **Commit and Push**:
   Push your changes to the main branch.
3. **Draft a New Release**:
   - Go to the "Releases" section of your GitHub repository.
   - Click "Draft a new release".
   - Create a new tag (e.g., `v0.1.1`).
   - Set the Release Title (e.g., `AppBridge v0.1.1`).
   - GitHub will automatically create a source code tarball (`.tar.gz`), which is what the `install.sh` script downloads.
4. **Publish Release**.

## How the Update Works

1. `appbridge update` calls `src/core/updater.py`.
2. The script queries the GitHub API: `https://api.github.com/repos/yourusername/AppBridge/releases/latest`.
3. It compares the `tag_name` from GitHub with the local `VERSION`.
4. If they differ, it offers to download the latest `install.sh` from the repository and run it.
5. The `install.sh` script downloads the source for that specific tag, extracts it, and overwrites the files in `/opt/appbridge`.

## Important Note

Ensure the `REPO` variable in `src/core/updater.py` and `install.sh` is updated to point to your actual GitHub repository (e.g., `yourusername/AppBridge`) before your first release.
