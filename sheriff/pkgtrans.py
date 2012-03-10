# Package name and version translation
#
# Copyright (c) 2008 Paulo Matias
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import re

class Translator:
    pkgsrc_pkgs = {}
    pkgsrc_list = []
    def __init__(self, filename='pkg-trans-table'):
        """ Inits the translation database. """
        f = open(filename)
        for line in f:
            line = re.split('\s+', line.strip())
            self.pkgsrc_pkgs[line[0]] = line[1:]
            self.pkgsrc_list.append(line[0])
        f.close()
    def translate_name(self, pkgname):
        """ Translates pkgname from pkgsrc to archlinux. """
        return self.pkgsrc_pkgs[pkgname][0]
    def translate_version(self, pkgname, arch_pkgver):
        """ Translates pkgver from archlinux to pkgsrc. """
        entry = self.pkgsrc_pkgs[pkgname]
        if len(entry) == 1:
            return arch_pkgver
        if entry[1] == 'i':
            return None
        m = re.search(entry[1], arch_pkgver)
        return entry[2] % m.groups()
    