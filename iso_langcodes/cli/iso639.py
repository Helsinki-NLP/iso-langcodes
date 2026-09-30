#!/usr/bin/env python3
"""
iso639 - a simple script to convert language codes.

Usage: iso639 [-2|-3|-m|-n|-k] [langcode]*

Convert to 3-letter-code if 2-letter code is given and vice versa.
-2 ... print 2-letter code (even if the input is a 2-letter code)
-3 ... print 3-letter code (even if the input is a 3-letter code)
-m ... print macro language instead of local language variants
-n ... don't print a final new-line
-k ... keep original code if no mapping is found
-p ... convert language pairs
-P ... convert language pairs and sort alphabetically
"""

import argparse
import sys

from .. import iso639_3


def convert_pairs(type_, langs, sorted_, keep):
    """Convert language pairs instead of single language codes."""
    converted = [iso639_3.convert_iso639(type_, lang, keep) for lang in langs.split('-')]
    if sorted_:
        converted = sorted(converted)
    return '-'.join(converted)


def main():
    parser = argparse.ArgumentParser(description='Convert language codes')
    parser.add_argument('-2', '--iso639-1', action='store_true', help='convert to two-letter code (ISO 639-1)')
    parser.add_argument('-3', '--iso639-3', action='store_true', help='convert to three-letter code (ISO 639-3)')
    parser.add_argument('-m', '--macro', action='store_true', help='convert to macro language')
    parser.add_argument('-n', '--no-newline', action='store_true', help="don't print a final new line")
    parser.add_argument('-k', '--keep', action='store_true', help='keep original code if no mapping is found')
    parser.add_argument('-p', '--pairs', action='store_true', help='convert language pairs')
    parser.add_argument('-P', '--pairs-sorted', action='store_true', help='convert language pairs and sort alphabetically')
    parser.add_argument('langcodes', nargs='*', help='language codes to convert')

    args = parser.parse_args()

    if args.iso639_1:
        type_ = 'iso639-1'
    elif args.iso639_3:
        type_ = 'iso639-3'
    elif args.macro:
        type_ = 'macro'
    else:
        type_ = 'name'

    if args.pairs or args.pairs_sorted:
        converted = [convert_pairs(type_, lang, args.pairs_sorted, args.keep) for lang in args.langcodes]
    else:
        converted = [iso639_3.convert_iso639(type_, lang, args.keep) for lang in args.langcodes]

    if type_ == 'name' and converted:
        print('"' + '" "'.join(converted) + '"', end='')
    else:
        print(' '.join(converted), end='')

    if not args.no_newline:
        print()


if __name__ == '__main__':
    main()
