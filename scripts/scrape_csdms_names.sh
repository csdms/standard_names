#! /bin/bash

URLS="http://csdms.colorado.edu/wiki/CSN_Quantity_Templates \
  http://csdms.colorado.edu/wiki/CSN_Object_Templates \
  http://csdms.colorado.edu/wiki/CSN_Operation_Templates \
  http://csdms.colorado.edu/wiki/CSN_Examples"
snscrape $URLS
