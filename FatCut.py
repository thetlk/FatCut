#!/usr/bin/env python
# encoding: utf-8

import argparse
import os
from struct import unpack

CPU_TYPE_I386 = 0x7
CPU_TYPE_MC680x0 = 0x6
CPU_TYPE_HPPA = 0xb
CPU_TYPE_ARM = 0xc
CPU_TYPE_MC88000 = 0xd
CPU_TYPE_SPARC = 0xe
CPU_TYPE_I860 = 0xf
CPU_TYPE_POWERPC = 0x12
CPU_TYPE_POWERPC64 = 0x1000012
CPU_TYPE_X86_64 = 0x1000007


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
    elif cputype == CPU_TYPE_ARM:
        return "arm"
    else:
        return "unknow arch - %x" % cputype


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

        count = 0
        for binary in binarys:
            cputype, cpusubtype, offset, size, align = binary
            fat_file.seek(offset)
            data = fat_file.read(size)
            filename = argv.output_dir + '/fatcut' + argv.filename.replace('/', '-') + '-' + display_cputype(cputype) + '-' + str(count)
            print "\t[+] write 0x%x bytes from offset 0x%x into %s" % (size, offset, filename)
            with open(filename, 'wb') as sortie:
                sortie.write(data)
            count += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract binary from FAT file')
    parser.add_argument('filename', help='Fat file')
    parser.add_argument('--output-dir', '-o', help='select output directory (default = .)', default='.')
    argv = parser.parse_args()
    main(argv)
