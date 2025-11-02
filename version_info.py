"""
Version Information for 5GH'z Cleaner
Used by PyInstaller to embed metadata in the executable
This helps reduce antivirus false positives
"""

VSVersionInfo(
    ffi=FixedFileInfo(
        # File version: 1.7.0.0
        filevers=(1, 7, 0, 0),
        # Product version: 1.7.0.0
        prodvers=(1, 7, 0, 0),
        # Contains a bitmask that specifies the valid bits in fileFlags
        mask=0x3f,
        # Contains a bitmask that specifies the Boolean attributes of the file
        flags=0x0,
        # Operating system: Windows NT
        OS=0x40004,
        # File type: Application
        fileType=0x1,
        # File subtype
        subtype=0x0,
        # Creation date
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',  # Language: US English, Character set: Unicode
                    [
                        StringStruct('CompanyName', 'UndKiMi'),
                        StringStruct('FileDescription', '5GHz Cleaner - Windows 11 Cleaning & Optimization Tool'),
                        StringStruct('FileVersion', '1.7.0.0'),
                        StringStruct('InternalName', '5Ghz_Cleaner'),
                        StringStruct('LegalCopyright', 'Copyright (c) 2025 UndKiMi - CC BY-NC-SA 4.0'),
                        StringStruct('OriginalFilename', '5Ghz_Cleaner.exe'),
                        StringStruct('ProductName', '5GHz Cleaner'),
                        StringStruct('ProductVersion', '1.7.0.0'),
                        StringStruct('Comments', 'Windows 11 system cleaning and optimization utility. Open source, no telemetry, 100% local processing.'),
                        StringStruct('LegalTrademarks', ''),
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
    ]
)
