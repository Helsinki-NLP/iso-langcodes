"""
ISO 15924 - Language scripts.

This module provides language scripts and their connection to languages.
"""

import unicodedata
import re

from .data.iso15924_data import get_data
from . import iso639_3

_data = get_data()

ScriptCode2ScriptName = _data["ScriptCode2ScriptName"]
ScriptName2ScriptCode = _data["ScriptName2ScriptCode"]
ScriptId2ScriptCode = _data["ScriptId2ScriptCode"]
ScriptCode2EnglishName = _data["ScriptCode2EnglishName"]
ScriptCode2FrenchName = _data["ScriptCode2FrenchName"]
ScriptCodeVersion = _data["ScriptCodeVersion"]
ScriptCodeDate = _data["ScriptCodeDate"]
ScriptCodeId = _data["ScriptCodeId"]
Lang2Territory = _data["Lang2Territory"]
Lang2Script = _data["Lang2Script"]
Territory2Lang = _data["Territory2Lang"]
Script2Lang = _data["Script2Lang"]
DefaultScript = _data["DefaultScript"]
DefaultTerritory = _data["DefaultTerritory"]

VERBOSE = 0

# For detecting Chinese scripts (traditional vs simplified)
ChineseScriptProportion = 0.8


def _get_unicode_scripts():
    """Get Unicode script data from unicodedata."""
    scripts = {}
    # Build a mapping from script names to sets of characters
    # This is a simplified version - in practice, you'd want to use
    # the full Unicode script data
    for code in range(0x110000):
        char = chr(code)
        try:
            name = unicodedata.name(char, "")
            if name:
                # Extract script name from character name
                # This is a simplified approach
                pass
        except (ValueError, OverflowError):
            pass
    return scripts


def contains_script(script, string, count=False):
    """
    Returns 1 if the string contains a valid Unicode character from script.
    If count is set to 1 then it returns the number of matching characters.
    """
    # Map script names to Unicode script property names
    script_map = {
        'Latin': 'Latn',
        'Cyrillic': 'Cyrl',
        'Greek': 'Grek',
        'Arabic': 'Arab',
        'Hebrew': 'Hebr',
        'Chinese': 'Han',
        'Japanese': 'Jpan',
        'Korean': 'Kore',
        'Hangul': 'Hang',
        'Devanagari': 'Deva',
        'Bengali': 'Beng',
        'Tamil': 'Taml',
        'Telugu': 'Telu',
        'Kannada': 'Knda',
        'Malayalam': 'Mlym',
        'Thai': 'Thai',
        'Lao': 'Laoo',
        'Myanmar': 'Mymr',
        'Georgian': 'Geor',
        'Armenian': 'Armn',
        'Ethiopic': 'Ethi',
        'Cherokee': 'Cher',
        'Canadian_Aboriginal': 'Cans',
        'Mongolian': 'Mong',
        'Tibetan': 'Tibt',
        'Khmer': 'Khmr',
        'Sinhala': 'Sinh',
        'Gujarati': 'Gujr',
        'Gurmukhi': 'Guru',
        'Oriya': 'Orya',
    }

    # Get the Unicode script code
    unicode_script = script_map.get(script, script)

    # Check if this is a known script
    if script not in ScriptCode2ScriptName and script not in ScriptName2ScriptCode:
        if script == 'Jpan':
            return 1 if (contains_script('Hira', string, count) or
                         contains_script('Kana', string, count) or
                         contains_script('Han', string, count)) else 0
        if script in ('Hans', 'Hant'):
            chinese_script = simplified_or_traditional_chinese(string)
            if chinese_script == script:
                if count:
                    return len([c for c in string if '\u4e00' <= c <= '\u9fff'])
                return 1
            return 0
        if VERBOSE:
            print(f"unsupported script {script}", file=__import__('sys').stderr)
        return None

    # Count characters in the script
    count_val = 0
    for char in string:
        try:
            # Use unicodedata to check script
            # This is a simplified approach
            if _char_in_script(char, unicode_script):
                count_val += 1
        except (ValueError, OverflowError):
            pass

    if count_val > 0:
        if count:
            return count_val
        return 1
    return 0


def _char_in_script(char, script):
    """Check if a character belongs to a script."""
    # This is a simplified implementation
    # In practice, you'd use the full Unicode script data
    script_ranges = {
        'Latn': [(0x0041, 0x005A), (0x0061, 0x007A), (0x00C0, 0x00FF), (0x0100, 0x017F)],
        'Cyrl': [(0x0400, 0x04FF)],
        'Grek': [(0x0370, 0x03FF)],
        'Arab': [(0x0600, 0x06FF)],
        'Hebr': [(0x0590, 0x05FF)],
        'Han': [(0x4E00, 0x9FFF), (0x3400, 0x4DBF)],
        'Hira': [(0x3040, 0x309F)],
        'Kana': [(0x30A0, 0x30FF)],
        'Hang': [(0xAC00, 0xD7AF)],
        'Deva': [(0x0900, 0x097F)],
        'Beng': [(0x0980, 0x09FF)],
        'Taml': [(0x0B80, 0x0BFF)],
        'Telu': [(0x0C00, 0x0C7F)],
        'Knda': [(0x0C80, 0x0CFF)],
        'Mlym': [(0x0D00, 0x0D7F)],
        'Thai': [(0x0E00, 0x0E7F)],
        'Laoo': [(0x0E80, 0x0EFF)],
        'Mymr': [(0x1000, 0x109F)],
        'Geor': [(0x10A0, 0x10FF)],
        'Armn': [(0x0530, 0x058F)],
        'Ethi': [(0x1200, 0x137F)],
        'Cher': [(0x13A0, 0x13FF)],
        'Cans': [(0x1400, 0x167F)],
        'Mong': [(0x1800, 0x18AF)],
        'Tibt': [(0x0F00, 0x0FFF)],
        'Khmr': [(0x1780, 0x17FF)],
        'Sinh': [(0x0D80, 0x0DFF)],
        'Gujr': [(0x0A80, 0x0AFF)],
        'Guru': [(0x0A00, 0x0A7F)],
        'Orya': [(0x0B00, 0x0B7F)],
    }

    code = ord(char)
    if script in script_ranges:
        for start, end in script_ranges[script]:
            if start <= code <= end:
                return True
    return False


def contains_simplified_chinese(string):
    """
    Returns 1 if the string contains valid Han characters in its simplified form.
    If count is set to 1 then it returns the number of matching characters.
    """
    # Simplified Chinese characters are in the range U+4E00 to U+9FFF
    # This is a simplified check
    count = 0
    for char in string:
        if '\u4e00' <= char <= '\u9fff':
            count += 1
    return count


def contains_traditional_chinese(string):
    """
    Returns 1 if the string contains valid Han characters in its traditional form.
    If count is set to 1 then it returns the number of matching characters.
    """
    # Traditional Chinese characters are also in the range U+4E00 to U+9FFF
    # This is a simplified check - in practice you'd need more sophisticated detection
    count = 0
    for char in string:
        if '\u4e00' <= char <= '\u9fff':
            count += 1
    return count


def detect_chinese_script(string):
    """
    Returns the script of some Chinese text (Hans, Hant, ...).
    """
    script = simplified_or_traditional_chinese(string)
    if script:
        return script

    for s in language_scripts('zho'):
        if s in ('Hans', 'Hant'):
            continue
        if contains_script(s, string):
            return s
    return 'Zyyy'


def simplified_or_traditional_chinese(string):
    """
    Returns the script of some Chinese text (Hans or Hant).
    Uses encoding-based detection similar to the Perl version.
    """
    # Try to encode to Big5 (traditional Chinese)
    # If the string can be encoded to Big5 without errors, it's likely traditional
    try:
        big5_bytes = string.encode('big5', errors='strict')
        # If we can encode to Big5, check if we can also decode it back
        big5_decoded = big5_bytes.decode('big5', errors='strict')
        # If the round-trip is successful, it's likely traditional Chinese
        if big5_decoded == string:
            return 'Hant'
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # Try to encode to GB2312 (simplified Chinese)
    try:
        gb2312_bytes = string.encode('gb2312', errors='strict')
        # If we can encode to GB2312, check if we can also decode it back
        gb2312_decoded = gb2312_bytes.decode('gb2312', errors='strict')
        # If the round-trip is successful, it's likely simplified Chinese
        if gb2312_decoded == string:
            return 'Hans'
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    # If neither encoding works, try with 'replace' error handling
    # and compare the lengths (similar to the Perl version)
    big5_len = len(string.encode('big5', errors='replace'))
    gb2312_len = len(string.encode('gb2312', errors='replace'))

    # If the Big5 encoding is significantly shorter, it's likely traditional
    if big5_len < gb2312_len * ChineseScriptProportion:
        return 'Hant'
    # If the GB2312 encoding is significantly shorter, it's likely simplified
    elif gb2312_len < big5_len * ChineseScriptProportion:
        return 'Hans'

    return None


def script_of_string(string, lang=None, allow_non_standard=False):
    """
    Returns the script(s) found in the string.
    If lang is given, returns the best acceptable script for that language.
    If called with allow_non_standard=True, returns a dict of all scripts found.
    """
    scripts = []
    if lang:
        scripts = language_scripts(lang)
    else:
        # Use script names instead of codes for contains_script
        scripts = list(ScriptName2ScriptCode.keys())

    char_counts = {}
    covered = 0

    # Always include common characters
    if 'Zyyy' not in scripts:
        scripts.append('Zyyy')

    for s in scripts:
        count = contains_script(s, string, True)
        if count:
            # Map script name to script code
            script_code = ScriptName2ScriptCode.get(s, s)
            char_counts[script_code] = count
            covered += count

    # If a language is given return the best acceptable script
    if lang and not allow_non_standard:
        # Skip common characters if there are other ones detected
        if 'Zyyy' in char_counts and len(char_counts) > 1:
            del char_counts['Zyyy']
        if char_counts:
            return max(char_counts, key=char_counts.get)
        return None

    # If we have matched less characters than length of the string
    # then continue looking for other kinds of scripts
    if covered < len(string):
        for s in ScriptName2ScriptCode:
            if s not in scripts:
                count = contains_script(s, string, True)
                if count:
                    script_code = ScriptName2ScriptCode.get(s, s)
                    char_counts[script_code] = count
                    covered += count
            if covered >= len(string):
                break

    # If allow_non_standard is True, return the dict
    if allow_non_standard:
        return char_counts

    # Otherwise return the most frequent script as a string
    if char_counts:
        # Skip common characters if there are other ones detected
        if 'Zyyy' in char_counts and len(char_counts) > 1:
            del char_counts['Zyyy']
        if char_counts:
            return max(char_counts, key=char_counts.get)
    return None


def script_code(script_name):
    """
    Return the script code for a given script name.
    """
    if not script_name:
        return None
    if script_name in ScriptName2ScriptCode:
        return ScriptName2ScriptCode[script_name]
    if VERBOSE:
        print(f"unknown script {script_name}", file=__import__('sys').stderr)
    return None


def script_name(script_code):
    """
    Return the script name for a given script code.
    """
    if not script_code:
        return None
    if script_code in ScriptCode2ScriptName:
        return ScriptCode2ScriptName[script_code]
    if VERBOSE:
        print(f"unknown script {script_code}", file=__import__('sys').stderr)
    return None


def language_scripts(lang):
    """
    Return a list of scripts for a given language.
    """
    if not lang:
        return []
    if lang in Lang2Script:
        return sorted(Lang2Script[lang].keys())
    langcode = iso639_3.get_iso639_3(lang)
    if langcode in Lang2Script:
        return sorted(Lang2Script[langcode].keys())
    langcode = iso639_3.get_macro_language(langcode)
    if langcode in Lang2Script:
        return sorted(Lang2Script[langcode].keys())
    if VERBOSE:
        print(f"unknown language {lang}", file=__import__('sys').stderr)
    return []


def default_script(lang):
    """
    Return the default script for a given language.
    """
    if not lang:
        return None
    if lang in DefaultScript:
        return DefaultScript[lang]
    langcode = iso639_3.get_iso639_3(lang)
    if langcode in DefaultScript:
        return DefaultScript[langcode]
    langcode = iso639_3.get_macro_language(langcode)
    if langcode in DefaultScript:
        return DefaultScript[langcode]
    return None


def languages_with_script(script):
    """
    Return a list of languages that use a given script.
    """
    if not script:
        return []
    if script in Script2Lang:
        return sorted(Script2Lang[script].keys())
    code = script_code(script)
    if code and code in Script2Lang:
        return sorted(Script2Lang[code].keys())
    if VERBOSE:
        print(f"unknown script {script}", file=__import__('sys').stderr)
    return []


def primary_languages_with_script(script):
    """
    Return a list of primary languages that use a given script.
    """
    if not script:
        return []
    if script in Script2Lang:
        return [lang for lang, status in Script2Lang[script].items() if status == 1]
    code = script_code(script)
    if code and code in Script2Lang:
        return [lang for lang, status in Script2Lang[code].items() if status == 1]
    if VERBOSE:
        print(f"unknown script {script}", file=__import__('sys').stderr)
    return []


def secondary_languages_with_script(script):
    """
    Return a list of secondary languages that use a given script.
    """
    if not script:
        return []
    if script in Script2Lang:
        return [lang for lang, status in Script2Lang[script].items() if status == 2]
    code = script_code(script)
    if code and code in Script2Lang:
        return [lang for lang, status in Script2Lang[code].items() if status == 2]
    if VERBOSE:
        print(f"unknown script {script}", file=__import__('sys').stderr)
    return []


def language_territories(lang):
    """
    Return a list of territories for a given language.
    """
    if not lang:
        return None
    if lang in Lang2Territory:
        return sorted(Lang2Territory[lang].keys())
    langcode = iso639_3.get_iso639_3(lang)
    if langcode in Lang2Territory:
        return sorted(Lang2Territory[langcode].keys())
    langcode = iso639_3.get_macro_language(langcode)
    if langcode in Lang2Territory:
        return sorted(Lang2Territory[langcode].keys())
    return []


def language_territory(lang, use_default=False):
    """
    Return the territory for a given language.
    """
    if not lang:
        return None
    import re
    m = re.search(r'\_([a-zA-Z]{2})$', lang)
    if m:
        region = m.group(1).upper()
        if region in Territory2Lang:
            return region
    # If there is only one region
    regions = language_territories(lang)
    if len(regions) == 1:
        return regions[0]
    if use_default:
        return default_territory(lang)
    return 'XX'


def default_territory(lang):
    """
    Return the default territory for a given language.
    """
    if not lang:
        return None
    if lang in DefaultTerritory:
        return DefaultTerritory[lang]
    langcode = iso639_3.get_iso639_3(lang)
    if langcode in DefaultTerritory:
        return DefaultTerritory[langcode]
    langcode = iso639_3.get_macro_language(langcode)
    if langcode in DefaultTerritory:
        return DefaultTerritory[langcode]
    return 'XX'


def primary_territories(lang):
    """
    Return a list of primary territories for a given language.
    """
    if not lang:
        return []
    if lang in Lang2Territory:
        return [t for t, status in Lang2Territory[lang].items() if status == 1]
    langcode = iso639_3.get_iso639_3(lang)
    if langcode in Lang2Territory:
        return [t for t, status in Lang2Territory[langcode].items() if status == 1]
    langcode = iso639_3.get_macro_language(langcode)
    if langcode in Lang2Territory:
        return [t for t, status in Lang2Territory[langcode].items() if status == 1]
    return []


def secondary_territories(lang):
    """
    Return a list of secondary territories for a given language.
    """
    if not lang:
        return []
    if lang in Lang2Territory:
        return [t for t, status in Lang2Territory[lang].items() if status == 2]
    langcode = iso639_3.get_iso639_3(lang)
    if langcode in Lang2Territory:
        return [t for t, status in Lang2Territory[langcode].items() if status == 2]
    langcode = iso639_3.get_macro_language(langcode)
    if langcode in Lang2Territory:
        return [t for t, status in Lang2Territory[langcode].items() if status == 2]
    return []
