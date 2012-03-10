# Package version matching
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

import re, fnmatch, dewey

def match(version_patterns, version):
    """ Returns True if version matchs to the version_patterns tuple. """
    if version == None:
        return True
    for pattern in version_patterns:
        assert(isinstance(pattern, str))
        m = re.match(r'^([<>]=?)(.+)$', pattern)
        if m:
            # Dewey-style comparision
            pat_op, pat_ver = m.groups()
            result = dewey.compare_versions(version, pat_ver)
            for op_res, op_sign in {-1:'<', 0:'=', +1:'>'}.iteritems():
                if (result == op_res) and (not op_sign in pat_op):
                    return False
        else:
            # Glob version matching
            if not fnmatch.fnmatch(version, pattern):
                return False
    return True
