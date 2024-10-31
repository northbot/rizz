from setuptools import setup, find_packages

setup(
    author="(:",
    name="rizz",
    description="Extracts domains and subdomains from a HackerOne CSV file.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            'rizz = rizz.main:main'
        ]
    },
)
