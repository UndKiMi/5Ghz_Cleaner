# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.6.x   | :white_check_mark: |
| < 1.6   | :x:                |

## Security Features

### Built-in Security
- ✅ **No Telemetry**: No data collection or external connections
- ✅ **Local Processing**: All operations are performed locally
- ✅ **Administrator Privileges**: Required only for system-level operations
- ✅ **Restore Points**: Automatic system restore point creation
- ✅ **Dry-Run Mode**: Preview changes before applying them
- ✅ **Protected Files**: Critical system files are protected from deletion

### Security Audits
This project uses automated security audits:
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner
- **CodeQL**: GitHub's semantic code analysis
- **Pylint**: Code quality and security checks

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. **DO NOT** open a public issue
2. Email the maintainer directly (see GitHub profile)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Time
- Initial response: Within 48 hours
- Fix timeline: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next release cycle

## Security Best Practices

### For Users
1. **Always run as Administrator** for full functionality
2. **Create restore points** before major operations
3. **Use Dry-Run mode** to preview changes
4. **Keep the application updated** to the latest version
5. **Download only from official sources**

### For Developers
1. **Never commit secrets** or API keys
2. **Validate all user inputs**
3. **Use parameterized queries** for database operations
4. **Follow principle of least privilege**
5. **Keep dependencies updated**

## Known Security Considerations

### Administrator Privileges
This application requires administrator privileges for:
- System file operations
- Registry modifications
- Service management
- Restore point creation

**Why it's safe:**
- All operations are transparent and logged
- Dry-run mode allows preview
- No external connections
- Open-source code for audit

### File Deletion
The application can delete files. Safety measures:
- Protected file list prevents critical system file deletion
- Confirmation dialogs for destructive operations
- Restore points created before major changes
- Recycle bin used when possible

## License Compliance

This project is licensed under **CC BY-NC-SA 4.0**:
- ✅ Free for personal use
- ✅ Free for educational use
- ❌ Commercial use prohibited
- ✅ Modifications allowed (must share alike)
- ✅ Attribution required

## Contact

For security concerns: See GitHub profile for contact information

---

**Last Updated**: 2025-01-14
**Version**: 1.6.0
