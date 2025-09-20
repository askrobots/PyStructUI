"""
PyStructUI - Universal Data Structure to HTML Rendering Engine
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pystructui",
    version="0.1.0",
    author="DBBasic Team",
    author_email="dev@dbbasic.io",
    description="Convert data structures to HTML for any Python web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askrobots/PyStructUI",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Framework :: Django",
        "Framework :: FastAPI",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "flask": ["flask>=2.0.0"],
        "django": ["django>=3.2.0"],
        "fastapi": ["fastapi>=0.68.0"],
        "dev": ["pytest", "black", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "pystructui=pystructui.cli:main",
        ],
    },
)