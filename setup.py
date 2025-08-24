
"""
Setup script for remov    install_requires=[
        'numpy>=1.21.0,<2.0.0',
        'Pillow>=8.0.0',
        'opencv-python-headless>=4.5.0',
    ],e-bg package.
A self-contained background removal tool with vendored dependencies.
"""

from setuptools import setup, find_packages
import os


def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "A self-contained background removal tool"

setup(
    name="remove-the-bg",
    version='1.1.2',
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered background removal tool with auto-installing dependencies and vendored rembg",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/remove-the-bg",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "rem=remove_the_bg.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "remove_the_bg": ["vendor/**/*", "models/*"],
    },

    install_requires=[
        "numpy>=1.21.0,<2.0.0",
        "Pillow>=8.0.0",
        "opencv-python-headless>=4.5.0",
    ],
    extras_require={
        "full": [
            "rembg>=2.0.0",
        ]
    },
)
