#!/usr/bin/env python

# Given n=(number of bins), rewrite tuf.interposition.json to point to the
# repository with hashed delegations of unclaimed targets to n bins.

import json
import sys

assert len(sys.argv) == 2
number_of_bins = int(sys.argv[1])
tuf_interposition_json_filename = \
    'lib/python2.7/site-packages/pip/tuf.interposition.json'

with open(tuf_interposition_json_filename) as tuf_interposition_json_file:
  tuf_interposition_json = json.load(tuf_interposition_json_file)

with open(tuf_interposition_json_filename, 'wb') as \
tuf_interposition_json_file:
  tuf_interposition_json['configurations']['pypi.python.org']\
                        ['repository_mirrors']['mirror1']['url_prefix'] = \
                        'http://trishank.poly.edu/{}'.format(number_of_bins)
  json.dump(tuf_interposition_json, tuf_interposition_json_file, indent=2)


