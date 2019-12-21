#!/usr/bin/env python3
from argparse import ArgumentParser;
import re;
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
    '--file-path',
    required = True,
    type = str,
    help = 'TTF output file path/name',
    metavar = 'file name'
);
parser.add_argument(
    '-n',
    '--font-name',
    type = str,
    help = 'TTF font name',
    metavar = 'font name',
    default = 'JaroshUnicode'
);
parser.add_argument(
    'svg',
    nargs = '*'
);

args = parser.parse_args();
font = fontforge.open('blank.sfd');

for c in args.utf:
    charCode = '%0.4X' % c;
    fileName = 'fonts/unifont-12.1.03/u{}-{}.svg'.format(charCode, charCode);
    if os.path.isfile(fileName):
        font.createChar(c).importOutlines(fileName);

for s in args.svg:
    reg = re.search('.*([A-F0-9]{4,6}).svg$', s);
    if reg and os.path.isfile(s):
        font.createChar(int(reg.group(1), 16)).importOutlines(s);

font.generate(args.file_path);
