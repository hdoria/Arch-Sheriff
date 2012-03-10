# Dewey-style version comparision
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

modifiers = (
    (+3, r'[._-]'),
    (+2, r'pl|p|r'),
    (+1, r'nb'),
    (-1, r'pre|rc'),
    (-2, r'beta|b'),
    (-3, r'alpha|a'),
    (-4, r'cvs|svn|git|hg|darcs'),
    (-5, r'[^0-9]+'),
)

modifiers_greatest = max([x[0] for x in modifiers])

def parse_version(version):
    """ Parses the version string and returns a list of tuples
        [(modifier, num)]. """
    global modifiers, modifiers_greatest
    assert(isinstance(version, str))
    parsed_ver = []
    
    # Strip trailing garbage (i.e. 'v' in 'v3' and 'R' in 'R5').
    version = re.sub('^[^0-9]', '', version)
    
    while len(version) > 0:
        if len(parsed_ver) == 0:
            # First version item. Use greatest modifier.
            modifier = modifiers_greatest
        else:
            # Get a modifier
            for (modifier, pattern) in modifiers:
                m = re.search(r'^([._-]?' + pattern + ')([0-9]|$)', version)
                if m:
                    # Found a valid modifier
                    version = version[len(m.group(1)):] 
                    break
        
        # Get a number
        m = re.search(r'^[0-9]+', version)
        if m:
            s = m.group(0)
            num = int(s)
            version = version[len(s):]  # remove from the string
        else:
            num = 0
        parsed_ver.append((modifier, num))
        
    return parsed_ver

def compare_versions(ver1, ver2):
    """ Compare versions and return 0 if ver1==ver2, -1 if ver1<ver2
        or +1 if ver1>ver2. """
    ver1 = parse_version(ver1)
    ver2 = parse_version(ver2)
    
    if ver1 == ver2:
        return 0
    
    common_len = min(len(ver1), len(ver2))
    common_ver1 = ver1[:common_len]
    common_ver2 = ver2[:common_len]
    
    if common_ver1 < common_ver2:
        return -1
    if common_ver1 > common_ver2:
        return +1
    
    ver1 = ver1[common_len:]
    ver2 = ver2[common_len:]
    
    if len(ver1) > 0:
        if ver1[0][0] < 0:
            return -1
        return +1
    if len(ver2) > 0:
        if ver2[0][0] >= 0:
            return -1
        return +1
    