from pathlib import Path
from setuptools import find_packages, setup

BASE_DIR = Path(__file__).resolve().parent
LONG_DESCRIPTION = (BASE_DIR / "README.rst").read_text(encoding="utf-8")

setup(
    name="buienradar",
    version="1.0.10",
    description="Library and CLI tools for interacting with buienradar.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    url="https://github.com/mjj4791/python-buienradar",
    author="mjj4791",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords="buienradar weather",
    packages=find_packages(exclude=("contrib", "docs", "tests")),
    python_requires=">=3.9",
    install_requires=[
        "tzdata; platform_system=='Windows'",
        "docopt",
        "requests",
        "xmltodict",
        "vincenty",
    ],
    entry_points={
        "console_scripts": [
            "buienradar=buienradar.__main__:main",
        ],
    },
)
