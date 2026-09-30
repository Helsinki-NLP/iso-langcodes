"""
ISO 639-3 - Language codes and names from ISO 639.

This module provides simple functions for retrieving language names and codes
from the ISO-639 standards. The main purpose is to convert between different
variants of codes and to get the English names of languages from codes.
"""

from .data.iso639_3_data import get_data

_data = get_data()

TwoToThree = _data["TwoToThree"]
ThreeToTwo = _data["ThreeToTwo"]
TwoToTwo = _data.get("TwoToTwo", {})
ThreeToThree = _data["ThreeToThree"]
ThreeToMacro = _data["ThreeToMacro"]
NameToTwo = _data["NameToTwo"]
NameToThree = _data["NameToThree"]
TwoToName = _data["TwoToName"]
ThreeToName = _data["ThreeToName"]


def convert_iso639(type_, id_, keep=False):
    """
    Convert the language code or language name given in id_.

    The type_ specifies the output type that is generated.
    Possible types are "iso639-1" (two-letter code), "iso639-3" (three-letter-code),
    "macro" (three-letter code of the corresponding macro language) or "name" (language name).
    Default is to return the language name.

    Regional codes are stripped from the input language ID.
    """
    if type_ == "iso639-1":
        return get_iso639_1(id_, keep)
    elif type_ == "iso639-3":
        return get_iso639_3(id_, keep)
    elif type_ == "macro":
        return get_macro_language(id_, keep)
    else:
        return get_language_name(id_)


def get_iso639_1(id_, keep=False):
    """
    Return the ISO 639-1 code for a given language or three-letter code.
    Returns the same code if it is a ISO 639-1 code or 'xx' if it is not recognized.
    """
    if id_ in TwoToThree:
        return ThreeToTwo[TwoToThree[id_]]
    if id_ in ThreeToTwo:
        return ThreeToTwo[id_]
    if id_ in TwoToName:
        return id_
    lc = id_.lower()
    if lc in TwoToThree:
        return ThreeToTwo[TwoToThree[lc]]
    if lc in ThreeToTwo:
        return ThreeToTwo[lc]
    if lc in NameToTwo:
        return NameToTwo[lc]
    if lc in TwoToName:
        return lc

    # TODO: is it OK to fallback to macro language in this conversion?
    if id_ in ThreeToMacro:
        macro = ThreeToMacro[id_]
        if macro in ThreeToTwo:
            return ThreeToTwo[macro]

    # try without regional/script extension
    import re
    m = re.match(r'^([^\-\_]+)([\-\_].*)$', id_)
    if m:
        if keep:
            return get_iso639_1(m.group(1)) + m.group(2)
        return get_iso639_1(m.group(1))

    if keep:
        return id_
    return "xx"


def get_iso639_3(id_, keep=False):
    """
    Return the ISO 639-3 code for a given language or any ISO 639 code.
    Returns 'xxx' if the code is not recognized.
    """
    if id_ in TwoToThree:
        return TwoToThree[id_]
    if id_ in ThreeToThree:
        return ThreeToThree[id_]
    if id_ in ThreeToName:
        return id_
    lc = id_.lower()
    if lc in TwoToThree:
        return TwoToThree[lc]
    if lc in ThreeToThree:
        return ThreeToThree[lc]
    if lc in NameToThree:
        return NameToThree[lc]
    if lc in ThreeToName:
        return lc

    import re
    m = re.match(r'^([^\-\_]+)([\-\_].*)$', id_)
    if m:
        if keep:
            return get_iso639_3(m.group(1)) + m.group(2)
        return get_iso639_3(m.group(1))

    if keep:
        return id_
    return "xxx"


def get_macro_language(id_, keep=False):
    """
    Return the ISO 639-3 code of the macro language for a given language or any ISO 639 code.
    Returns 'xxx' if the code is not recognized.
    """
    code = get_iso639_3(id_, keep)
    if code in ThreeToMacro:
        return ThreeToMacro[code]
    return code


def get_language_name(id_):
    """
    Return the name of the language that corresponds to the given language code (any ISO639 code).
    """
    if id_ in TwoToName:
        return TwoToName[id_]
    if id_ in ThreeToName:
        return ThreeToName[id_]
    if id_ in NameToThree:
        return id_

    import re
    m = re.match(r'^([^\-\_]+)([\-\_].*)$', id_)
    if m:
        return get_language_name(m.group(1))

    if id_ != id_.lower():
        return get_language_name(id_.lower())

    return "unknown"
