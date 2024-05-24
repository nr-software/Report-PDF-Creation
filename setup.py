from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="report_pdf_wrapper",
    version="0.3.0",
    author="Alex Nuccio",
    author_email="nrsoftwareservices@gmail.com",
    description="A simple pip module for creating generic PDF reports.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nr-software/Report-PDF-Creation.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
)