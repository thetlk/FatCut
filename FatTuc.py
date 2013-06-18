#!/usr/bin/env python
# encoding: utf-8

"""
Copyright 2013 Jérémie BOUTOILLE

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
from struct import pack, unpack


def main(argv):
    with open(argv.output, 'wb') as fat_file:
        print "[+] write fat magic"
        fat_file.write(pack('>I', 0xcafebabe))
        print "[+] write narchs : %d" % len(argv.input_files)
        fat_file.write(pack('>I', len(argv.input_files)))

        offset = 0x1000
        to_write = []
        for input_file in argv.input_files:
            with open(input_file, 'rb') as macho_file:
                data = macho_file.read()
                size = len(data)
                macho_file.seek(0)
                magic, cputype, cpusubtype = unpack("<III", macho_file.read(4*3))
                print "[+] add file '%s' (cputype=0x%x, cpusubtype=0x%x, size=0x%x) at offset 0x%x" % (input_file, cputype, cpusubtype, size, offset)
                to_write.append((offset, data))
                fat_file.write(pack('>IIIII', cputype, cpusubtype, offset, size, 0xc))
                offset += size
                offset = offset + (0x1000 - offset % 0x1000)

        for offset, data in to_write:
            fat_file.seek(offset)
            fat_file.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create FAT file from binarys')
    parser.add_argument('output', help='FAT file to write')
    parser.add_argument('input_files', help='files to put into FAT file', nargs='+')
    argv = parser.parse_args()
    main(argv)
