# AppBridge Release & Update System

AppBridge uses GitHub Releases for its update and installation system.

## Versioning Rules

We follow a specific versioning pattern: `VX.Y.Z` (e.g., `V1.0.0`)

1. **Major Version (`X`)**: Stable release version (e.g., `1`).
2. **Minor Version (`Y`)**: Incremented when the patch version reaches 10.
3. **Patch Version (`Z`)**: Incremented for small updates/patches.

**Example Sequence**:
- `V1.0.8`
- `V1.0.9`
- `V1.1.0` (Patch reached 10, so increment middle number and reset patch)
- `V1.1.9`
- `V1.2.0`

## Tagging Convention

- Tags should be prefixed with an uppercase `V`.
- Example: `V1.0.0`

## Creating a Release

1. **Update `VERSION`**:
   In `src/core/updater.py`, set `VERSION = "1.0.0"` (without the 'V').
2. **GitHub Release**:
   - Create a tag `V1.0.0`.
   - The `install.sh` script will automatically pull the source code from this tag.
   - Users can update by running `appbridge update`.

## Repository URL
The official repository is: `https://github.com/ZimnyySTD/AppBridge/`
