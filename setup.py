"""
AIS² Setup Configuration

This setup file is provided for compatibility with tools that prefer setup.py
over pyproject.toml. The canonical configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages

setup(
    name="AIS2",
    version="1.0.0",
    description="Adversarially Isolated Stateless² Rendering Architecture",
    author="Anonymous",
    author_email="research@osdi.org",
    url="https://github.com/Dedoc-9/AIS2",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "streamlit>=1.28.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
            "ruff>=0.1.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
