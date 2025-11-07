#!/usr/bin/env python3
"""
Setup file for bun-utils package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bun-utils",
    version="0.1.0",
    author="Benjamin Silverman",
    author_email="",
    description="Shared utilities for Bun's Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BunPrinceton/bun-utils",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - pure Python!
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
        ],
    },
)
