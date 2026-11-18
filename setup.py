"""Setup configuration for unified-file-reader.

Developed and tested on Python 3.12.8 (recommended). 
Other versions within 3.9–3.12 should also work.
"""

from setuptools import setup, find_packages

setup(
    name="unified-file-reader",
    version="0.1.3",
    packages=find_packages(),
    python_requires=">=3.9",
)
