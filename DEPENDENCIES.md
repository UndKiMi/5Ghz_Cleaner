# Dependencies Guide

## 📦 Installation

### For Users (Windows 11 only)

```bash
pip install -r requirements.txt
```

**Optional:** For log encryption support:
```bash
pip install cryptography==41.0.7
```

### For Developers

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

---

## 📋 Dependencies Breakdown

### Core Dependencies (`requirements.txt`)

| Package | Version | Purpose | Platform |
|---------|---------|---------|----------|
| flet | 0.25.2 | UI Framework | All |
| pywin32 | 306 | Windows API | Windows only |
| psutil | 5.9.8 | System utilities | All |
| pythonnet | 3.0.5 | .NET interop | Windows only |
| cryptography | 41.0.7 | Log encryption | All (optional) |

### Development Dependencies (`requirements-dev.txt`)

| Package | Version | Purpose |
|---------|---------|---------|
| bandit | 1.7.9 | Security linting |
| safety | 3.2.7 | Dependency vulnerability scanning |
| pylint | 3.2.7 | Code quality |
| black | 23.12.1 | Code formatting |
| isort | 5.13.2 | Import sorting |
| pytest | 7.4.3 | Testing framework |
| pytest-cov | 4.1.0 | Code coverage |
| pytest-mock | 3.12.0 | Mocking for tests |
| sphinx | 7.2.6 | Documentation |
| sphinx-rtd-theme | 2.0.0 | Documentation theme |

---

## ⚠️ Platform-Specific Notes

### Windows-Only Packages

The following packages are **Windows-only** and will fail on Linux/macOS:
- `pywin32` - Windows API access
- `pythonnet` - .NET interop for LibreHardwareMonitor

### GitHub Actions

The CI/CD pipeline uses a **Linux runner** and therefore:
- Skips Windows-only dependencies
- Only installs packages needed for security audits
- Uses `requirements-dev.txt` for testing tools

---

## 🔧 Troubleshooting

### "Could not find pywin32"

**On Windows:** Install Visual C++ Redistributable, then:
```bash
pip install --upgrade pywin32
```

**On Linux/macOS:** This is expected - the application is Windows 11 only.

### "cryptography module not available"

This is **normal** - encryption is optional. To enable:
```bash
pip install cryptography==41.0.7
```

### GitHub Actions failing

If you see errors about `pywin32` in GitHub Actions, this is **expected** because:
1. GitHub Actions uses Linux runners
2. The workflow is configured to skip Windows-only packages
3. Security audits don't need Windows-specific packages

---

## 📝 Notes

- **Production:** Only `requirements.txt` is needed
- **Development:** Install both `requirements.txt` and `requirements-dev.txt`
- **CI/CD:** GitHub Actions uses a custom subset of dependencies
- **Encryption:** Optional feature, install `cryptography` if needed