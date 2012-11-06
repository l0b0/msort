#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#
# NAME
#        msort.py - Sort multi-line blocks of text
#
# SYNOPSIS
#        ./msort.py -b 'pattern' -s 'pattern' < input_file > result_file
#
# DESCRIPTION
#        Sort any multi-line block text.
#
# BUGS
#        https://github.com/l0b0/msort/issues
#
# COPYRIGHT
#        Copyright © 2012 Victor Engmark. License GPLv3+: GNU GPL
#        version 3 or later <http://gnu.org/licenses/gpl.html>.
#        This is free software: you are free to change and redistribute it.
#        There is NO WARRANTY, to the extent permitted by law.
#
################################################################################

"""msort.py - Multiline sort of standard input

Default syntax:

./msort.py -b 'pattern' -s 'pattern' < input_file > result_file

Options:
-v,--verbose    Verbose mode
-h,--help       Print this message
-b,--bp         Block pattern (dotall multiline); used to extract blocks
-s,--sp         Sort pattern (dotall multiline); extracted to sort blocks

Example:

for vcard in *.vcf
do
    ./msort.py -b 'BEGIN:VCARD.*?END:VCARD\\r\\n\\r\\n' -s '^N:(.*)$' \\
        < "$vcard" > "$vcard"2
    mv "$vcard"2 "$vcard"
done

Orders vCards in all vcf files by last name."""

import getopt
import re
import sys

class Usage(Exception):
    """Raise in case of invalid parameters"""
    def __init__(self, msg):
        self.msg = msg

def _compare_pattern(sort_pattern, text1, text2):
    """Function to sort by regex"""
    matches = [
        re.search(sort_pattern, text, re.DOTALL | re.MULTILINE)
        for text in [text1, text2]]
    text_matches = []
    for match in matches:
        if match is None:
            text_matches.append('')
        else:
            text_matches.append(match.group(1))

    return cmp(text_matches[0], text_matches[1])

def split_and_sort(text, block_pattern, sort_pattern):
    """Split into blocks, sort them, and join them up again
    @param text: String of blocks to sort
    @param block_pattern: Regular expression corresponding to the border between
    the blocks
    @param sort_pattern: Gets a subset of each block to sort by"""

    text_blocks = re.findall(block_pattern, text, re.DOTALL | re.MULTILINE)
    #print text_blocks

    text_blocks.sort(lambda x, y: _compare_pattern(sort_pattern, x, y))

    return ''.join(text_blocks)

def main(argv = None):
    """Argument handling"""

    if argv is None:
        argv = sys.argv

    # Defaults
    block_pattern = ''
    sort_pattern = ''

    try:
        try:
            opts, args = getopt.getopt(
                argv[1:],
                'hb:s:',
                ['help', 'bp=', 'sp='])
        except getopt.GetoptError, err:
            raise Usage(err.msg)

        for option, value in opts:
            if option in ('-h', '--help'):
                print(__doc__)
                return 0
            elif option in ('-b', '--bp'):
                block_pattern = value
            elif option in ('-s', '--sp'):
                sort_pattern = value
            else:
                raise Usage('Unhandled option %s' % option)

        if block_pattern == '' or sort_pattern == '' or args:
            raise Usage(__doc__)

        text = sys.stdin.read()

        print split_and_sort(text, block_pattern, sort_pattern)

    except Usage, err:
        sys.stderr.write(err.msg + '\n')
        return 2

if __name__ == '__main__':
    sys.exit(main())
