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
import os
from struct import unpack

CPU_TYPE_POWERPC = 0x12
CPU_TYPE_POWERPC64 = 0x1000012
CPU_TYPE_I386 = 0x7
CPU_TYPE_X86_64 = 0x1000007
CPU_TYPE_MC680x0 = 0x6
CPU_TYPE_HPPA = 0xb
CPU_TYPE_I860 = 0xf
CPU_TYPE_MC88000 = 0xd
CPU_TYPE_SPARC = 0xe


def display_cputype(cputype):

    if cputype == CPU_TYPE_POWERPC:
        return "ppc"
    elif cputype == CPU_TYPE_POWERPC64:
        return "ppc64"
    elif cputype == CPU_TYPE_I386:
        return "i386"
    elif cputype == CPU_TYPE_X86_64:
        return "x86_64"
    elif cputype == CPU_TYPE_MC680x0:
        return "m68k"
    elif cputype == CPU_TYPE_HPPA:
        return "hppa"
    elif cputype == CPU_TYPE_I860:
        return "i860"
    elif cputype == CPU_TYPE_MC88000:
        return "m88k"
    elif cputype == CPU_TYPE_SPARC:
        return "sparc"
    else:
        return "unknow arch"


def main(argv):
    with open(argv.filename, 'rb') as fat_file:
        magic = unpack('>I', fat_file.read(4))[0]
        assert magic == 0xcafebabe
        nfat_arch = unpack('>I', fat_file.read(4))[0]
        print "[+] FAT file with %d arch%s" % (nfat_arch, "s" if nfat_arch > 1 else "")

        binarys = []
        for i in range(nfat_arch):
            cputype, cpusubtype = unpack('>II', fat_file.read(8))
            offset, size, align = unpack('>III', fat_file.read(12))
            binarys.append((cputype, cpusubtype, offset, size, align))

        try:
            os.makedirs(argv.output_dir)
        except:
            pass

        for binary in binarys:
            cputype, cpusubtype, offset, size, align = binary
            fat_file.seek(offset)
            data = fat_file.read(size)
            filename = argv.output_dir + '/fatcut' + argv.filename.replace('/', '-') + '-' + display_cputype(cputype)
            print "\t[+] write 0x%x bytes from offset 0x%x into %s" % (size, offset, filename)
            with open(filename, 'wb') as sortie:
                sortie.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract binary from FAT file')
    parser.add_argument('filename', help='Fat file')
    parser.add_argument('--output-dir', '-o', help='select outpur directory (default = .)', default='.')
    argv = parser.parse_args()
    main(argv)
