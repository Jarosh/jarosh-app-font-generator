#!/usr/bin/env python3
from argparse import ArgumentParser;
import re;
import os.path;
import fontforge;
import xml.dom.minidom;

# bin/produce.py -u 1514 -u 1497 -u 1489 -u 1470 -u 1507 -u 1500 -u 1488 -u 1512 -u 1489 -u 1506
# bin/produce.py -o tmp/d354f2e6232680aa508ee974f404c862.ttf -n UnicodeBP fonts/noto-sans-regular/u0000-0000.svg fonts/unifont-12.1.03/u0001-0001.svg 

parser = ArgumentParser(description = 'FontForge: from SVG fonts generator');
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
    '-d',
    '--dir',
    type = str,
    help = 'Directory containing SVG files to be used along with -u option',
    metavar = 'directory path'
);
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
    'svg',
    nargs = '*'
);

args = parser.parse_args();
font = fontforge.open('blank.sfd');

font.version = '1.0';
font.comment = 'Generated by Jarosh font generator';
font.copyright = 'Jarosh';
font.fontname = args.font_name;
font.fullname = args.font_name;
font.familyname = args.font_name;
font.encoding = 'UnicodeFull';
font.weight = 'Regular';

def str2int(str):
    try: 
        return int(str);
    except ValueError:
        return 0;

def addChar(font, file, code):
    if os.path.isfile(file):
        char = font.createChar(code);
        char.importOutlines(file);
        boxBounds = char.boundingBox();
        svgBounds = xml.dom.minidom.parse(s).getElementsByTagName('svg');
        svgBounds = [] if (svgBounds.length is not 1) else list(map(str2int, svgBounds[0].getAttribute('viewBox').split(' ') or []));
        char.width = max(boxBounds[2], 0 if (len(svgBounds) is not 4) else (svgBounds[2] - svgBounds[0]));
        char.autoHint();
        char.autoInstr();
        char.simplify();

if args.dir:
    for c in args.utf:
        charCode = '%0.4X' % c;
        fileName = 'fonts/{}/u{}-{}.svg'.format(args.dir, charCode, charCode);
        addChar(font, fileName, c);

for s in args.svg:
    reg = re.search('.*u([A-F0-9]{4,6})-[A-Za-z0-9]+.svg$', s);
    if reg:
        addChar(font, s, int(reg.group(1), 16));

font.generate(args.file_path);
font.close();
