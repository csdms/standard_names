#! /usr/bin/env python

import os
import yaml

def _load_names ():
    names_file = os.path.join (os.path.dirname (__file__),
                               'data', 'standard_names.yaml')
    with open (names_file, 'r') as f:
        names = yaml.load_all (f)

        d = {}
        for name in names:
            for (k, v) in name.items ():
                assert (k in ['names', 'objects', 'quantities',
                              'operators'])
                try:
                    d[k] |= set (v)
                except KeyError:
                    d[k] = set (v)

    globals ()['NAMES'] = d.pop ('names', set ())
    globals ()['OBJECTS'] = d.pop ('objects', set ())
    globals ()['QUANTITIES'] = d.pop ('quantities', set ())
    globals ()['OPERATORS'] = d.pop ('operators', set ())

_load_names ()

if __name__ == '__main__':
    for name in NAMES:
        print name

