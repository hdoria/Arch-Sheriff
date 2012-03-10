# Arch Linux Package Information Retrieving
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

import re, os, urllib, shlex

__cache__ = {}

def get_aur_version(package):
    """ Retrieve package version from AUR. """
    f = urllib.urlopen('http://aur.archlinux.org/packages/%s/%s/PKGBUILD' % (package, package))
    content = f.read()
    f.close()
    m = re.search('\npkgver=(.+?)\n', content)
    return ''.join(shlex.split(m.group(1)))

def get_pacman_version(package):
    """ Retrieve package version from pacman. """
    if not re.match('^[A-Za-z0-9_-]+$', package):
        raise RuntimeError, "Invalid package name '%s'. Stoping by security." % package
    f = os.popen("LC_ALL=C pacman -Si '%s' 2>/dev/null" % package)
    content = f.read()
    f.close()
    m = re.search('\nVersion\\s+:\\s+(.+?)-\\d+\n', content)
    return m.group(1)
    
def get_version(package):
    """ Retrieve package version. """
    global __cache__
    if __cache__.has_key(package):
        return __cache__[package]
    try:
        __cache__[package] = get_pacman_version(package)
    except:
        __cache__[package] = get_aur_version(package)
    return __cache__[package]
