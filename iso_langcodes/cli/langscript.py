#!/usr/bin/env python3
"""
langscript - detect characters from various scripts.

Usage: langscript [OPTIONS] < input.txt > script-codes.txt

Find the script of a text and print the script codes line by line.

Options:
  -a ............ print all scripts found in each line
  -l <langid> ... language hint (start by looking at language-specific scripts first)
  -L ............ two-column input (langid <TAB> text)
  -n ............ print script names instead of script codes
  -h ............ print usage information
  -r ............ also print region/territory
  -R ............ like -r but print default region if no other region found
  -D ............ suppress default script codes
  -1 ............ also print ISO-639-1 code
  -3 ............ also print ISO-639-3 code
"""

import argparse
import sys

from .. import iso15924
from .. import iso639_3


def get_region(lang, use_default=False):
    """Get region and cache values to avoid looking them up again."""
    region = iso15924.language_territory(lang, use_default) or "XX"
    return region


def get_default_region(lang):
    """Get default region and cache values to avoid looking them up again."""
    region = iso15924.default_territory(lang) or "XX"
    return region


def get_default_script(lang):
    """Get default script and cache values to avoid looking them up again."""
    script = iso15924.default_script(lang) or ""
    return script


def main():
    parser = argparse.ArgumentParser(description='Detect characters from various scripts')
    parser.add_argument('-a', '--all', action='store_true', help='print all scripts found in each line')
    parser.add_argument('-l', '--lang', help='language hint')
    parser.add_argument('-L', '--lang-text', action='store_true', help='two-column input (langid <TAB> text)')
    parser.add_argument('-n', '--names', action='store_true', help='print script names instead of script codes')
    parser.add_argument('-r', '--region', action='store_true', help='also print region/territory')
    parser.add_argument('-R', '--region-default', action='store_true', help='like -r but print default region if no other region found')
    parser.add_argument('-D', '--suppress-default', action='store_true', help='suppress default script codes')
    parser.add_argument('-1', '--iso639-1', action='store_true', help='also print ISO-639-1 code')
    parser.add_argument('-3', '--iso639-3', action='store_true', help='also print ISO-639-3 code')

    args = parser.parse_args()

    default_script = ""
    default_region = "XX"
    region = "XX"

    if args.lang:
        default_script = get_default_script(args.lang)
        default_region = get_default_region(args.lang)
        region = get_region(args.lang, args.region_default)

    for line in sys.stdin:
        line = line.rstrip('\n')
        if args.lang_text:
            parts = line.split('\t')
            if len(parts) >= 2:
                lang = parts[0]
                text = parts[1]
            else:
                lang = args.lang
                text = line
        else:
            lang = args.lang
            text = line

        if args.lang_text:
            default_region = get_default_region(lang)
            default_script = get_default_script(lang)

        if args.all:
            scripts = iso15924.script_of_string(text, lang, allow_non_standard=True)
            if isinstance(scripts, dict):
                sorted_scripts = sorted(scripts.keys(), key=lambda s: scripts[s], reverse=True)
                for s in sorted_scripts:
                    if args.names:
                        print(f"{iso15924.script_name(s)} ({scripts[s]})", end=' ')
                    else:
                        print(f"{s} ({scripts[s]})", end=' ')
            print()
        else:
            output = []
            langcode = lang

            if lang:
                if lang == 'ku' or lang == 'kur':
                    script = iso15924.script_of_string(text, lang)
                    if script:
                        langid = f'ku_{script}'
                        default_script = get_default_script(iso639_3.get_iso639_3(langid))
                if args.iso639_1:
                    output.append(iso639_3.get_iso639_1(langcode, True))
                elif args.iso639_3:
                    output.append(iso639_3.get_iso639_3(langcode, True))

            script = iso15924.script_of_string(text, lang) or default_script
            # If the script is Han, try to detect simplified vs traditional
            if script == 'Hani':
                chinese_script = iso15924.detect_chinese_script(text)
                if chinese_script in ('Hans', 'Hant'):
                    script = chinese_script

            if not args.suppress_default or (script != default_script and script != 'Zyyy'):
                if args.names:
                    if script:
                        # Handle special Chinese script codes
                        if script in ('Hans', 'Hant'):
                            output.append(script)
                        else:
                            output.append(iso15924.script_name(script))
                else:
                    if script:
                        output.append(script)

            # Update region if we have dynamic language labels
            if lang and (args.region or args.region_default):
                if args.lang_text:
                    region = get_region(lang, args.region_default)
                if not args.suppress_default or (region != default_region and region != 'XX'):
                    if region:
                        output.append(region)

            print('_'.join(output))


if __name__ == '__main__':
    main()
