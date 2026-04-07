# Release Process for luker-otclient

This project uses GitHub Actions to automatically create releases and build client archives. Follow these steps to properly create a new release.

## Prerequisites

- All changes committed and pushed to `main` branch
- Git is installed and configured

## Release Steps

### 1. Update Version Number

First, update the version in `updater/version.txt`:

```bash
# Edit updater/version.txt
# Change the version to your new version (e.g., 1.0.5)
# The file should contain ONLY the version number with no quotes or extra text
```

**Important:** The version in `version.txt` MUST match the git tag you create in step 3.

### 2. Commit Version Update

```bash
git add updater/version.txt
git commit -m "Release version X.Y.Z"
git push origin main
```

### 3. Create and Push Git Tag

Create a git tag with the format `vX.Y.Z` (e.g., `v1.0.5`):

```bash
git tag v1.0.5
git push origin v1.0.5
```

## What Happens Next

The GitHub Actions workflow (`release.yml`) will automatically:

1. **Verify the version** - Checks that `updater/version.txt` matches the tag version
2. **Create a client zip** - Archives the entire client, excluding unnecessary files:
   - `.git/`, `.github/`, `.gitignore`, `.vscode/`, `.idea/`
   - Temporary files, logs, caches, screenshots, minimap data
   - Personal configs: `.claude/`, `proxy.js`, `characterdata/`
3. **Create GitHub Release** - Automatically creates a release on GitHub with:
   - Tag: `v1.0.5`
   - Name: `Release v1.0.5`
   - Attached zip file: `luker-otclient-1.0.5.zip`
   - Release notes with installation instructions

## Example: Creating v1.0.5

```bash
# 1. Update version
echo "1.0.5" > updater/version.txt

# 2. Commit and push
git add updater/version.txt
git commit -m "Release version 1.0.5"
git push origin main

# 3. Create and push tag
git tag v1.0.5
git push origin v1.0.5

# Done! The workflow will handle the rest
```

## Troubleshooting

**Error: version.txt does not match tag**
- Make sure `updater/version.txt` contains exactly `X.Y.Z` (without the `v` prefix)
- Make sure the version in the file matches your tag (e.g., tag `v1.0.5` needs `1.0.5` in the file)

**Release not creating?**
- Check GitHub Actions in the repository for workflow run status
- Verify the tag was pushed with `git push origin v1.0.5`
- Ensure the tag format matches `vX.Y.Z`

## Notes

- The workflow is triggered by pushing tags that match the pattern `v*`
- The zip file excludes all personal configs, caches, and development files
- Release notes are auto-generated with a template
- The `GITHUB_TOKEN` is automatically provided by GitHub Actions
