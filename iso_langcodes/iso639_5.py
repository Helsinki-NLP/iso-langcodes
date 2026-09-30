"""
ISO 639-5 - Language groups.

This module provides the definitions of language groups according to ISO 639-5.
It allows to retrieve the languages inside of a group and the parent in the
language tree for any given language supported by the standard.
"""

from .data.iso639_5_data import get_data

_data = get_data()

LanguageGroup = _data["LanguageGroup"]
LanguageParent = _data["LanguageParent"]
ISO2Glottolog = _data["ISO2Glottolog"]
Glottolog2ISO = _data["Glottolog2ISO"]

VERBOSE = 0


def language_group(groupcode):
    """
    Returns a list of language codes within the given language group.
    """
    children = set()
    if groupcode in LanguageGroup:
        for lang in LanguageGroup[groupcode]:
            if lang in LanguageGroup:
                for child in language_group(lang):
                    children.add(child)
            else:
                children.add(lang)
    else:
        return [groupcode]
    return sorted(children)


def language_group_children(groupcode):
    """
    Returns a list of language codes that are immediate children of the given language group.
    """
    if groupcode in LanguageGroup:
        return LanguageGroup[groupcode]
    if VERBOSE:
        print(f"unknown language group {groupcode}", file=__import__('sys').stderr)
    return []


def language_parent(langcode):
    """
    Returns the parent language code for the given language.
    """
    if langcode in LanguageParent:
        return LanguageParent[langcode]
    if VERBOSE:
        print(f"no parent found for '{langcode}'", file=__import__('sys').stderr)
    return None


def iso2glottolog(iso_code):
    """
    Convert ISO 639-5 code to Glottolog ID.
    """
    if iso_code in ISO2Glottolog:
        return ISO2Glottolog[iso_code]
    if VERBOSE:
        print(f"no glottolog ID found for '{iso_code}'", file=__import__('sys').stderr)
    return None


def glottolog2iso(glottolog_id):
    """
    Convert Glottolog ID to ISO 639-5 code.
    """
    if glottolog_id in Glottolog2ISO:
        return Glottolog2ISO[glottolog_id]
    if VERBOSE:
        print(f"no ISO639-5 code found for '{glottolog_id}'", file=__import__('sys').stderr)
    return None
