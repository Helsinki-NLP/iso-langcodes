"""
langcodes - Python modules for working with language codes, language groups and language scripts.

This package provides:
- ISO 639-3: conversion between ISO language codes
- ISO 639-5: language groups and families according to ISO 639-5
- ISO 15924: language scripts and their connection to languages
"""

from . import iso639_3
from . import iso639_5
from . import iso15924

__version__ = "1.0.0"
__author__ = "Joerg Tiedemann"
__all__ = ["iso639_3", "iso639_5", "iso15924"]
