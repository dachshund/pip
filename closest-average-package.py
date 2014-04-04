#!/usr/bin/env python

import json
import math
import os
import sys

fname1 = '/home/trishank/Repositories/pypi-usenix/metadata.2/targets/'\
         'unclaimed/0-7.json'
fname2 = '/home/trishank/Repositories/pypi-usenix/metadata.2/targets/'\
         'unclaimed/8-f.json'
targets = {}

with open(fname1) as f1, open(fname2) as f2:
  j1 = json.load(f1)
  t1 = j1['signed']['targets']
  targets.update(t1)

  j2 = json.load(f2)
  t2 = j2['signed']['targets']
  targets.update(t2)

total_package_and_simple_length = 0
package_counter = 0

for target_name, target_metadata in targets.iteritems():
  if target_name.startswith('/packages/'):
    project_name = target_name.split('/')[4]
    package_length = target_metadata['length']
    simple_name = '/simple/{}/index.html'.format(project_name)
    simple_length = targets[simple_name]['length']
    package_and_simple_length = package_length + simple_length
    total_package_and_simple_length += package_and_simple_length
    package_counter += 1

avg_package_and_simple_length = \
  int(math.ceil(total_package_and_simple_length / package_counter))
min_project_diff = sys.maxint
min_project_name = None
min_package_name = None

for target_name, target_metadata in targets.iteritems():
  if target_name.startswith('/packages/'):
    project_name = target_name.split('/')[4]
    package_length = target_metadata['length']
    simple_name = '/simple/{}/index.html'.format(project_name)
    simple_length = targets[simple_name]['length']
    package_and_simple_length = package_length + simple_length
    project_diff = \
      abs(package_and_simple_length - avg_package_and_simple_length)

    if project_diff < min_project_diff:
      min_project_diff = project_diff
      min_project_name = project_name
      min_package_name = target_name

#print(avg_package_and_simple_length, min_project_diff, min_project_name, min_package_name)
package_filename = os.path.basename(min_package_name)
package_version = package_filename.split('-')[1]
print('{}=={}'.format(min_project_name, package_version))


