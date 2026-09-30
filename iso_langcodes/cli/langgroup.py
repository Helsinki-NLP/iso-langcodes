#!/usr/bin/env python3
"""
langgroup - print language groups according to ISO639-5.

Usage: langgroup [OPTIONS] LANGCODE*

Options:
  -h: help
  -c: group children
  -g: group languages
  -G: group by grandparent
  -n: don't print final newline
  -p: print parent code of each given language code
  -P: print parents all the way up the language tree
  -v: verbose output
"""

import argparse
import sys

from .. import iso639_5


def main():
    parser = argparse.ArgumentParser(description='Print language groups according to ISO639-5')
    parser.add_argument('-c', '--children', action='store_true', help='group children')
    parser.add_argument('-g', '--group', action='store_true', help='group languages')
    parser.add_argument('-G', '--grandparent', action='store_true', help='group by grandparent')
    parser.add_argument('-n', '--no-newline', action='store_true', help="don't print final newline")
    parser.add_argument('-p', '--parent', action='store_true', help='print parent code of each given language code')
    parser.add_argument('-P', '--parents', action='store_true', help='print parents all the way up the language tree')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('langcodes', nargs='*', help='language codes')

    args = parser.parse_args()

    if args.verbose:
        iso639_5.VERBOSE = 1

    # Read from STDIN or take codes from command line args
    if args.langcodes:
        codes = args.langcodes
    else:
        codes = sys.stdin.read().split()

    if args.parent:
        converted = [iso639_5.language_parent(code) for code in codes]
        print(' '.join(str(c) for c in converted), end='')
        if not args.no_newline:
            print()
    elif args.parents:
        trees = []
        for lang in codes:
            parents = []
            while True:
                p = iso639_5.language_parent(lang)
                if not p:
                    break
                parents.append(p)
                lang = p
                if p == 'mul':
                    break
            if parents:
                trees.append(':'.join(parents))
            else:
                trees.append('none')
        print(' '.join(trees), end='')
        if not args.no_newline:
            print()
    elif args.group or args.grandparent:
        groups = {}
        for code in codes:
            parent = iso639_5.language_parent(code) or code
            if args.grandparent:
                parent = iso639_5.language_parent(parent) or parent
            if parent not in groups:
                groups[parent] = set()
            groups[parent].add(code)
        for key in sorted(groups.keys()):
            if args.no_newline:
                print('+'.join(sorted(groups[key])), end=' ')
            else:
                print(key, end='\t')
                print(' '.join(sorted(groups[key])))
    else:
        for code in codes:
            if args.children:
                print(' '.join(iso639_5.language_group_children(code)), end='')
            else:
                print(' '.join(iso639_5.language_group(code)), end='')
            if not args.no_newline:
                print()


if __name__ == '__main__':
    main()
