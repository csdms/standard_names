====================
CSDMS Standard Names
====================

Python utilities for working with CSDMS standard names.

Install
=======

    easy_install CmtStandardNames


Examples
========

snscrape
--------

Scrape names for URLs that are known to contain standard names and put them
in a text file with one names per line.

    > snscrape http://csdms.colorado.edu/wiki/CSN_Quantity_Templates \
               http://csdms.colorado.edu/wiki/CSN_Object_Templates \
               http://csdms.colorado.edu/wiki/CSN_Operation_Templates \
              > scraped.txt

snbuild
-------

Build a database of standard names, object, quantities, operators from a
text file that contains a list of full names. The database is a simple
YAML file.

    > snbuild scraped.txt > names.yaml

sndump
------

Dump a standard-names database (YAML) file to a given format. The following
will dump full names (-n), operators (-o), quantities (-q), and operators
(-op). The output format will be as MediaWiki markdown (other options are
*plain*, *txt*, and *yaml*).

    > sndump -n -o -q -op --format=wiki names.yaml > names.wiki

Putting it all together
-----------------------

Since each of these commands can read from *stdin* and print to *stdout*, they
can be used in a chain like,

    > URLS="http://csdms.colorado.edu/wiki/CSN_Quantity_Templates \
            http://csdms.colorado.edu/wiki/CSN_Object_Templates \
            http://csdms.colorado.edu/wiki/CSN_Operation_Templates \
            http://csdms.colorado.edu/wiki/CSN_Examples"
    > snscrape $URLS | snbuild - | sndump - -n -o -q -op --format=wiki
