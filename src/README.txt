====
CSDMS Standard Names
====

package name: CmtStandardNames
version: 0.1
release data: 2013-03-15

Python utilities for working with CSDMS standard names.

Install
=======

    easy_install CmtStandardNames


Examples
========

snscrape
--------

    snscrape http://csdms.colorado.edu/wiki/CSN_Quantity_Templates \
             http://csdms.colorado.edu/wiki/CSN_Object_Templates \
             http://csdms.colorado.edu/wiki/CSN_Operation_Templates \
            > data/scraped.yaml

snbuild
-------

    snbuild data/models.yaml data/scraped.yaml > standard_names/data/standard_names.yaml

snbuild
-------

    sndump -n -o -q -op --format=wiki > standard_names.wiki

Author
======

author: Eric Hutton
email: eric.hutton@colorado.edu
