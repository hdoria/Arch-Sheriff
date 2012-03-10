# NetBSD pkg-vulnerabilities parsing
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

import re, fnmatch

def vuln_iterator(filename):
    """ Iterates through entries in the pkg-vulnerabilities file.
        Yields (pkgdesc, vulntype, vulnurl) tuples. """
    f = open(filename)
    for line in f:
        assert(isinstance(line, str))
        line = line.strip()
        # Ignore signature, hash and comment lines.
        if line == '' or line.startswith('#') or line.startswith('-----') or \
           line.startswith('Hash: '):
            continue
        # Forced EOF.
        if line.startswith('Version: '):
            break
        # Yield a tuple for the entry.
        yield tuple(re.split(r'\s+', line, 2))
    f.close()
    
def parse_alternates(pkgdesc):
    """ Parses alternates, like 'a{b,c}d{e,f}' in a pkgdesc str.
        Returns ['a', ('b','c'), 'd', ('e','f')] for the given example. """
    assert(isinstance(pkgdesc, str))
    parsed_pkgdesc = []
    while len(pkgdesc) > 0:
        i = pkgdesc.find('{')
        if i == -1:
            parsed_pkgdesc.append(pkgdesc)
            break
        parsed_pkgdesc.append(pkgdesc[:i])
        pkgdesc = pkgdesc[i+1:]
        i = pkgdesc.find('}')
        parsed_pkgdesc.append(tuple(pkgdesc[:i].split(',')))
        pkgdesc = pkgdesc[i+1:]
    return parsed_pkgdesc

def gen_alternates_recurse(pkgdesc):
    """ Recurse through the already-parsed pkgdesc dict, generating alternates. """
    assert(isinstance(pkgdesc, list))
    if len(pkgdesc) <= 1:
        yield ''.join(pkgdesc)
    else:
        prefix = pkgdesc[0]
        alternates = pkgdesc[1]
        pkgdesc = pkgdesc[2:]
        for alt in alternates:
            for x in gen_alternates_recurse(pkgdesc):
                yield prefix + alt + x
    
def gen_alternates(pkgdesc):
    """ Yields all possible alternates from the pkgdesc str. """
    pkgdesc = parse_alternates(pkgdesc)
    for x in gen_alternates_recurse(pkgdesc):
        yield x
    
def vuln_alternate_iterator(filename):
    """ Same as vuln_iterator, but takes alternates into account.
        Yields (pkgdesc, original_pkgdesc, vulntype, vulnurl). """
    for (pkgdesc, vulntype, vulnurl) in vuln_iterator(filename):
        for x in gen_alternates(pkgdesc):
            yield (x, pkgdesc, vulntype, vulnurl)

def parse_pkgdesc(pkgdesc):
    """ Parse pkgdesc, spliting package name pattern and version constraints.
        Returns ('pkgname', '>ver1', '<ver2') for Dewey-style comparision.
        Returns ('pkgname', 'ver') for glob version matching. """
    assert(isinstance(pkgdesc, str))
    # Find version comparisions.
    split_points = [pkgdesc.find(c) for c in '<>']
    split_points = [i for i in split_points if i != -1]
    split_points.sort()
    # Split the str.
    parsed_pkgdesc = []
    j = 0
    for i in split_points:
        parsed_pkgdesc.append(pkgdesc[j:i])
        j = i
    parsed_pkgdesc.append(pkgdesc[j:])
    
    if len(parsed_pkgdesc) == 1:
        # Do not use Dewey-style version comparision. Use glob matching.
        m = re.match('^([A-Za-z0-9_-]+)-([][!a-z0-9*?.-]+?)$', pkgdesc)
        if m:
            return m.groups()
        # Version pattern not found. Match any version.
        return (pkgdesc, '*')
    
    return tuple(parsed_pkgdesc)
    
def pkgname_filter(pkgname):
    """ Filters pkgname before matching. """
    if re.search('^py\d{2}-', pkgname):
        # Strip Python version from pkgname, as it's present in the binary package name,
        # but is not present in the pkgsrc package name.
        return 'py-' + pkgname[5:]
    return pkgname

def vuln_pkg_matcher_iterator(filename, pkg_list, unmatched_callback=None):
    """ Same as vuln_alternate_iterator, but matchs pkgnames against a package list,
        and splits up the version patterns.
        Yields (pkgname, (version_pattern,), original_pkgdesc, vulntype, vulnurl). """
    assert(isinstance(pkg_list, list))
    for (pkgdesc, orig_pkgdesc, vulntype, vulnurl) in vuln_alternate_iterator(filename):
        pkgdesc = parse_pkgdesc(pkgdesc)
        pkgnames = fnmatch.filter(pkg_list, pkgname_filter(pkgdesc[0]))
        for pkgname in pkgnames:
            yield (pkgname, pkgdesc[1:], orig_pkgdesc, vulntype, vulnurl)
        if len(pkgnames) == 0 and unmatched_callback != None:
            unmatched_callback((pkgdesc, orig_pkgdesc, vulntype, vulnurl))
