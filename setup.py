"""
Setup script for 5GHz Cleaner
"""
from setuptools import setup, find_packages
import os

# Read README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="5ghz-cleaner",
    version="1.6.0",
    author="UndKiMi",
    author_email="contact@example.com",
    description="Windows Cleaning and Optimization Tool with Maximum Security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UndKiMi/5Ghz_Cleaner",
    project_urls={
        "Bug Tracker": "https://github.com/UndKiMi/5Ghz_Cleaner/issues",
        "Documentation": "https://github.com/UndKiMi/5Ghz_Cleaner/tree/main/docs",
        "Source Code": "https://github.com/UndKiMi/5Ghz_Cleaner",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "scripts"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: French",
        "Natural Language :: English",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "bandit>=1.7.5",
            "safety>=2.3.5",
            "pip-audit>=2.6.1",
        ],
        "build": [
            "pyinstaller>=5.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "5ghz-cleaner=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "assets/icons/*.ico",
            "assets/icons/*.svg",
            "config/*.json",
            "SIGNATURE.json",
            "CHECKSUMS.txt",
        ],
    },
    keywords=[
        "windows",
        "cleaner",
        "optimization",
        "system-tools",
        "disk-cleanup",
        "temp-files",
        "privacy",
        "security",
    ],
    platforms=["Windows"],
    license="CC BY-NC-SA 4.0",
    zip_safe=False,
)
