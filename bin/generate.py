#!/usr/bin/env python3
from argparse import ArgumentParser;
import os.path;
import fontforge;

# תיב־ףלארבע
# ./generate.py -u 1514 -u 1497 -u 1489 -u 1470 -u 1507 -u 1500 -u 1488 -u 1512 -u 1489 -u 1506

parser = ArgumentParser(description = 'FontForge: from SVG fonts generator');
parser.add_argument(
    '-u',
    '--utf',
    type = int,
    action = 'append',
    help = 'UTF code point as integer value',
    metavar = 'codepoint',
    default = []
);
parser.add_argument(
    '-o',
    '--output-filename',
    required = True,
    type = str,
    help = 'TTF output file name without extension',
    metavar = 'file name'
);

args = parser.parse_args();
print(args);
font = fontforge.open('blank.sfd');

for c in args.utf:
    charCode = '%0.4X' % c;
    fileName = '3/u{}-{}.svg'.format(charCode, charCode);
    if os.path.isfile(fileName):
        font.createChar(c).importOutlines(fileName);

font.generate('{}.ttf'.format(args.output_filename));
