# iso-langcodes

Python modules for working with language codes, language groups and language scripts.

Currently, there are 3 modules in this package:

- `iso_langcodes.iso639_3` - conversion between ISO language codes
- `iso_langcodes.iso639_5` - language groups and families according to ISO 639-5
- `iso_langcodes.iso15924` - language scripts and their connection to languages

## Installation

```bash
pip install iso-langcodes
```

Or install from source:

```bash
pip install .
```

## Usage

### ISO 639-3

```python
from iso_langcodes import iso639_3

print(iso639_3.convert_iso639('iso639-1', 'fra'))
print(iso639_3.convert_iso639('iso639-3', 'de'))
print(iso639_3.convert_iso639('name', 'fa'))

print(iso639_3.get_iso639_1('deu'))
print(iso639_3.get_iso639_3('de'))
print(iso639_3.get_language_name('de'))
print(iso639_3.get_language_name('eng'))
print(iso639_3.get_macro_language('yue'))
```

### ISO 639-5

```python
from iso_langcodes import iso639_5

print(' '.join(iso639_5.language_group('gmw')))
print(' '.join(iso639_5.language_group('gem')))
print(' '.join(iso639_5.language_group_children('gem')))
print(iso639_5.language_parent('afr'))
print(iso639_5.language_parent('gmw'))
```

### ISO 15924

```python
from iso_langcodes import iso15924

script = iso15924.script_of_string('То је моја мачка.', 'srp')
script = iso15924.script_of_string('你是我妈妈。')
scripts = iso15924.script_of_string('То је моја мачка. Ti si moja majka.', allow_non_standard=True)

region = iso15924.default_territory('por')
script = iso15924.default_script('tur')
```

## Command Line Tools

The package provides three command-line tools:

### iso639

Convert between language codes:

```bash
iso639 fra de eng
iso639 -2 fra deu
iso639 -3 de
iso639 -m yue
```

### langgroup

Print language groups according to ISO 639-5:

```bash
langgroup gem
langgroup -c gem
langgroup -p afr gmw
```

### langscript

Detect characters from various scripts:

```bash
echo "То је моја мачка." | langscript -l srp
echo "你是我妈妈。" | langscript
```

### langglottolog

Convert between ISO 639-5 codes and Glottolog codes:

```bash
langglottolog aav afa alg
langglottolog -g aust1305 afro1255
```

## License

This software is Copyright (c) 2020 by Joerg Tiedemann.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgements

The language codes are taken from SIL International <https://iso639-3.sil.org>.
Please, check the terms of use listed at <https://iso639-3.sil.org/code_tables/download_tables>.
The current version uses the UTF-8 tables distributed in "iso-639-3_Code_Tables_20200130.zip"
from that website. This module adds some non-standard codes that are not specified
in the original tables to be compatible with some ad-hoc solutions in some resources
and tools.

The official ISO 15924 code list is taken from Unicode <https://www.unicode.org/iso15924/iso15924.txt.zip>
and the additional information about connections between languages, scripts and territories
is extracted from the Unicode CLDR project at <http://cldr.unicode.org>.
