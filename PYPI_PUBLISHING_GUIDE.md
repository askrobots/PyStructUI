# Publishing PyStructUI to PyPI

## Requirements for PyPI

### 1. PyPI Account
- Create account at https://pypi.org/account/register/
- Verify email address
- (Optional) Set up 2FA for security

### 2. Build Tools
```bash
pip install --upgrade pip setuptools wheel twine
```

### 3. Package Structure ✅ (Already Complete!)
- [x] `setup.py` with all metadata
- [x] `README.md` for long description
- [x] `__init__.py` with version
- [x] Proper package structure
- [x] License (MIT implied in setup.py)

### 4. Additional Files Needed

#### Create LICENSE file
```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 PyStructUI Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

#### Create MANIFEST.in
```bash
cat > MANIFEST.in << 'EOF'
include README.md
include LICENSE
recursive-include pystructui *.py
recursive-include examples *.py
EOF
```

#### Create .gitignore
```bash
cat > .gitignore << 'EOF'
*.pyc
__pycache__/
build/
dist/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
.tox/
.env
venv/
EOF
```

## Publishing Steps

### 1. Test Package Locally
```bash
# In pystructui directory
pip install -e .

# Test it works
python -c "from pystructui import render; print(render({'type': 'button', 'text': 'Test'}))"
```

### 2. Build Distribution
```bash
# Clean any previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python setup.py sdist bdist_wheel

# Check the distribution
ls dist/
# Should see:
# pystructui-0.1.0-py3-none-any.whl
# pystructui-0.1.0.tar.gz
```

### 3. Test with TestPyPI (Optional but Recommended)
```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ pystructui
```

### 4. Upload to PyPI
```bash
# Upload to real PyPI
twine upload dist/*

# You'll be prompted for:
# Username: __token__
# Password: <your-api-token>
```

### 5. Create API Token (Recommended)
1. Login to https://pypi.org
2. Go to Account Settings → API tokens
3. Create new API token
4. Save it securely
5. Use as password with username `__token__`

### 6. Verify Installation
```bash
# Install from PyPI
pip install pystructui

# Test it
python -c "from pystructui import render; print('Success!')"
```

## Automation with GitHub Actions

Create `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install --upgrade pip setuptools wheel twine
    - name: Build package
      run: python setup.py sdist bdist_wheel
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Version Management

Update version in:
1. `pystructui/__init__.py`
2. `setup.py`

Follow semantic versioning:
- MAJOR.MINOR.PATCH (e.g., 1.0.0)
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

## Quick Commands to Publish

```bash
# Full publishing process
cd /Users/danq/websheet/dbbasic/pystructui

# 1. Add missing files
echo "MIT License..." > LICENSE
echo "include README.md..." > MANIFEST.in

# 2. Build
python setup.py sdist bdist_wheel

# 3. Check package
twine check dist/*

# 4. Upload to PyPI
twine upload dist/*

# 5. Done! Now anyone can:
pip install pystructui
```

## Package Name Availability

✅ **Good news!** "pystructui" appears to be available on PyPI!

Once published, users worldwide can:
```bash
pip install pystructui
```

And immediately start building web apps without HTML templates!