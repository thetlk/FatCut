#!/usr/bin/env python
# encoding: utf-8

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
