# Copyright 2010-2012 RethinkDB, all rights reserved.
#!/usr/bin/env python
import sys

"""This script is used to generate the RDB_MAKE_SEMILATTICE_JOINABLE_*() macro
definitions.

This script is meant to be run as follows (assuming you are in the
"rethinkdb/src" directory):

$ ../scripts/generate_join_macros.py > rpc/semilattice/joins/macros.hpp

"""

def generate_make_semilattice_joinable_macro(nfields):
    print "#define RDB_MAKE_SEMILATTICE_JOINABLE_%d(type_t%s) \\" % \
        (nfields, "".join(", field%d" % (i+1) for i in xrange(nfields)))
    unused = "UNUSED " if nfields == 0 else ""
    print "    inline void semilattice_join(%stype_t *_a_, %sconst type_t &_b_) { \\" % (unused, unused)
    for i in xrange(nfields):
        print "        semilattice_join(&_a_->field%d, _b_.field%d); \\" % (i + 1, i + 1)
    print "    } \\"
    # Putting this here makes us require a semicolon after macro invocation.
    print "    extern int semilattice_joinable_force_semicolon_declaration"

def generate_make_equality_comparable_macro(nfields):
    print "#define RDB_MAKE_EQUALITY_COMPARABLE_%d(type_t%s) \\" % \
        (nfields, "".join(", field%d" % (i+1) for i in xrange(nfields)))
    unused = "UNUSED " if nfields == 0 else ""
    print "    inline bool operator==(%sconst type_t &_a_, %sconst type_t &_b_) { \\" % (unused, unused)
    if nfields == 0:
        print "        return true; \\"
    else:
        print "        return " + " && ".join("_a_.field%d == _b_.field%d" % (i + 1, i + 1) for i in xrange(nfields)) + "; \\"
    print "    } \\"
    # Putting this here makes us require a semicolon after macro invocation.
    print "    extern int semilattice_joinable_force_semicolon_declaration"

if __name__ == "__main__":

    print "#ifndef RPC_SEMILATTICE_JOINS_MACROS_HPP_"
    print "#define RPC_SEMILATTICE_JOINS_MACROS_HPP_"
    print

    print "/* This file is automatically generated by '%s'." % " ".join(sys.argv)
    print "Please modify '%s' instead of modifying this file.*/" % sys.argv[0]
    print

    print """
/* The purpose of these macros is to make it easier to define semilattice joins
for types that consist of a fixed set of fields which it is a simple product of.
In the same namespace as the type, call `RDB_MAKE_SEMILATTICE_JOINABLE_[n]()`,
where `[n]` is the number of fields in the type. The first parameter is the name
of the type; the remaining parameters are the fields. You will also need an
`==` operator; for this you can use `RDB_MAKE_EQUALITY_COMPARABLE_[n]()`.

Example:
    struct point_t {
        vclock_t<int> x, y;
    };
    RDB_MAKE_SEMILATTICE_JOINABLE_2(point_t, x, y)

You can also use this with templated types, but it's pretty hacky:
    template<class T>
    struct pair_t {
        T a, b;
    };
    template<class T>
    RDB_MAKE_SEMILATTICE_JOINABLE_2(pair_t<T>, a, b)
*/
    """.strip()
    print

    for nfields in xrange(0, 20):
        generate_make_semilattice_joinable_macro(nfields)
        generate_make_equality_comparable_macro(nfields)
        print

    print "#endif  // RPC_SEMILATTICE_JOINS_MACROS_HPP_"
