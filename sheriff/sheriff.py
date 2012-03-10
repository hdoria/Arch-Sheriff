#!/usr/bin/env python
#
# Package vulnerability automatic sheriff
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

import sys, getopt
import archpkg, pkgtrans, pkgversion, pkgvulns, generatehtml

def usage():
    print """
Package vulnerability automatic sheriff

Usage: sheriff [-v pkg-vulnerabilities] [-t pkg-trans-table]
               [-w warn-file] [-i ignored-urls]
"""
    sys.exit(1)
    
def log(warn_file, msg):
    """ Log a msg to the warn_file. """
    f = open(warn_file, 'a')
    f.write(msg)
    f.close()

def warn_unmatched(warn_file):
    """ Returns a callback to log unmatched packages to warn_file. """
    def callback(tup):
        log(warn_file, 'No match for package in translation table:\n%s\n\n' % repr(tup))
    return callback
    
def load_list(filename):
    """ Loads a list of one string per line from filename. """
    f = open(filename)
    content = [x.strip() for x in f.readlines()]
    f.close()
    return content

def main(vuln_file, trans_file, warn_file, ignore_file):
    """ Sheriff """
    # Load the ignore list
    ignore_list = load_list(ignore_file)

    # Load the translation database
    trans = pkgtrans.Translator(trans_file)
    pkg_list = trans.pkgsrc_list
    
    # Creates all lists
    listeol = []; listwarn = []; listvuln =[]
    
    # Loops through the vulnerabilities list
    for (pkgname, version_patterns, original_pkgdesc, vulntype, vulnurl) in \
        pkgvulns.vuln_pkg_matcher_iterator(vuln_file, pkg_list, warn_unmatched(warn_file)):

        # Skip vulnerabilities included in the ignore list
        if vulnurl in ignore_list:
            sys.stderr.write('IGNORING %s\n' % repr((original_pkgdesc, vulntype, vulnurl)))
            continue
        
        # Translate pkgsrc name to ArchLinux package name
        arch_pkgname = trans.translate_name(pkgname)

        # Retrieve ArchLinux package version
        try:
            arch_pkgver = archpkg.get_version(arch_pkgname)
        except:
            log(warn_file, 'Arch package not available anymore: %s.\n\n' % repr(arch_pkgname))
            continue

        # Translate the version to pkgsrc format using the database
        try:
            pkgver = trans.translate_version(pkgname, arch_pkgver)
        except:
            log(warn_file, 'Could not translate version to pkgsrc: %s %s\n\n' % (pkgname, arch_pkgver))
            continue

        sys.stderr.write('CHECKING %s\n' % repr((original_pkgdesc, arch_pkgname, arch_pkgver)))
        
        
        listtemp  = [arch_pkgname, arch_pkgver, original_pkgdesc, vulntype, vulnurl]
        # Check if the version is potentially vulnerable
        if pkgversion.match(version_patterns, pkgver):
            # Choose a mark
            # By default, the entry is a vulnerability.
            t = 'VULN'
            if pkgver == None:
                # We mark the entry as warning if we can't compare package versions.
                # i.e. strategy='i' (ignore version) in the pkg-trans-table file.
                t = 'WARN'
            if vulntype == 'eol':
                # We mark the entry as package end-of-life if this is an EOL entry.
                t = 'EOL'
                
            # Add the entry to the lists, for HTML generation.
            if t == 'VULN':
                listvuln.append(listtemp)
            elif t == 'WARN':
                listwarn.append(listtemp)
            elif t == 'EOL':
                listeol.append(listtemp)
            
            # Write information to stdout
            sys.stdout.write('%s %s\n' % (t, repr((arch_pkgname, arch_pkgver, original_pkgdesc, vulntype, vulnurl))))
            sys.stdout.flush()
            
    
    # Create the base html file
    generatehtml.gen_header()    
    
    # Create tables    
    generatehtml.gen_table('VULNERABILITIES', 'begin', len(listvuln))
    for vuln in listvuln:
        generatehtml.gen_tableline(vuln)
    generatehtml.gen_table('VULNERABILITIES', 'end', len(listvuln))
        
    generatehtml.gen_table('WARNINGS', 'begin', len(listwarn))
    for vuln in listwarn:
        generatehtml.gen_tableline(vuln)
    generatehtml.gen_table('WARNINGS', 'end', len(listwarn))
    
    generatehtml.gen_table('End Of Life', 'begin', len(listeol))
    for vuln in listeol:
        generatehtml.gen_tableline(vuln)
    generatehtml.gen_table('End Of Life', 'end', len(listeol))
    
    # Create html footer
    generatehtml.gen_footer()
    
if __name__ == '__main__':
    # Try psyco JIT compiler if available.
    try:
        import psyco
        psyco.full()
    except:
        pass
    
    # Default options
    vuln_file = 'pkg-vulnerabilities'
    trans_file = 'pkg-trans-table'
    warn_file = 'warn-file'
    ignore_file = 'ignored-urls'
    
    # Process command line options.
    try: opts, args = getopt.getopt(sys.argv[1:], 'hv:t:w:i:')
    except: usage()
    for o, a in opts:
        if o == '-h':
            usage()
        elif o == '-v':
            vuln_file = a
        elif o == '-t':
            trans_file = a
        elif o == '-w':
            warn_file = a
        elif o == '-i':
            ignore_file = a
    
    main(vuln_file, trans_file, warn_file, ignore_file)