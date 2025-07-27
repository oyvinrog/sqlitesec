# PyPI Upload Guide for SqliteSec

Your `sqlitesec` package is now ready for PyPI! Here's how to upload it:

## Pre-upload Checklist

✅ Package structure created (`sqlitesec/` directory)  
✅ `pyproject.toml` configured with proper metadata  
✅ `LICENSE` file created  
✅ `README.md` updated  
✅ Package builds successfully  
✅ Local installation tested  

## Before First Upload

### 1. Update Author Information
Edit `pyproject.toml` and replace placeholder values:
```toml
authors = [
    {name = "Your Real Name", email = "your.real.email@example.com"}
]
```

### 2. Update Repository URLs
Replace the GitHub URLs with your actual repository:
```toml
[project.urls]
Homepage = "https://github.com/yourusername/sqlitesec"
Documentation = "https://github.com/yourusername/sqlitesec#readme"
Repository = "https://github.com/yourusername/sqlitesec.git"
Issues = "https://github.com/yourusername/sqlitesec/issues"
```

### 3. Create PyPI Account
- Go to https://pypi.org/account/register/
- Verify your email address
- Set up two-factor authentication (recommended)

## Upload Process

### 1. Test on TestPyPI First (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ sqlitesec
```

### 2. Upload to PyPI
```bash
# Upload to PyPI
twine upload dist/*

# You'll be prompted for username and password
# Or you can use API tokens (recommended)
```

### 3. Using API Tokens (Recommended)
1. Go to PyPI Account Settings → API tokens
2. Create a new token with scope "Entire account"
3. Use token for upload:
```bash
twine upload dist/* --username __token__ --password pypi-your-token-here
```

## After Upload

### Test Installation
```bash
# In a fresh environment
pip install sqlitesec

# Test import
python -c "from sqlitesec import SqliteSec; print('Success!')"
```

### Check Your Package
Visit: https://pypi.org/project/sqlitesec/

## Future Updates

1. Update version in `pyproject.toml`
2. Rebuild package: `python -m build`
3. Upload new version: `twine upload dist/*`

## Current Package Status

- **Version**: 1.0.0
- **Built files**: 
  - `dist/sqlitesec-1.0.0.tar.gz` (source distribution)
  - `dist/sqlitesec-1.0.0-py3-none-any.whl` (wheel)
- **Dependencies**: cryptography>=3.0.0
- **Python support**: 3.8+

## Notes

- The package name `sqlitesec` appears to be available on PyPI
- Consider adding more comprehensive documentation
- You may want to add unit tests before publishing
- Version 1.0.0 indicates a stable release - consider starting with 0.1.0 if this is experimental

Your package is ready to go! 🚀 