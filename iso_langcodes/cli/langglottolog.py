#!/usr/bin/env python3
"""
langglottolog - convert between ISO 639-5 codes and Glottolog codes.

Usage: langglottolog [OPTIONS] CODE*

Options:
  -h: help
  -i: convert from ISO to Glottolog (default)
  -g: convert from Glottolog to ISO
  -n: don't print final newline
  -v: verbose output
"""

import argparse
import sys

from .. import iso639_5


def main():
    parser = argparse.ArgumentParser(description='Convert between ISO 639-5 codes and Glottolog codes')
    parser.add_argument('-i', '--iso2glottolog', action='store_true', help='convert from ISO to Glottolog (default)')
    parser.add_argument('-g', '--glottolog2iso', action='store_true', help='convert from Glottolog to ISO')
    parser.add_argument('-n', '--no-newline', action='store_true', help="don't print final newline")
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('codes', nargs='*', help='codes to convert')

    args = parser.parse_args()

    if args.verbose:
        iso639_5.VERBOSE = 1

    # Read from STDIN or take codes from command line args
    if args.codes:
        codes = args.codes
    else:
        codes = sys.stdin.read().split()

    # Default to ISO to Glottolog if neither flag is set
    if not args.glottolog2iso:
        args.iso2glottolog = True

    converted = []
    for code in codes:
        if args.glottolog2iso:
            result = iso639_5.glottolog2iso(code)
        else:
            result = iso639_5.iso2glottolog(code)
        converted.append(result if result else 'unknown')

    print(' '.join(converted), end='')
    if not args.no_newline:
        print()


if __name__ == '__main__':
    main()
