#!/usr/bin/env python

from __future__ import division

import numpy as np
import matplotlib.pyplot as plt


def measure_times(minimum_bin_exponent, maximum_bin_exponent):
  """All in seconds."""

  # indexed by number of bins
  times = {}

  for i in xrange(minimum_bin_exponent, maximum_bin_exponent + 1):
    number_of_bins = 2**i
    log_filename = '{}.log'.format(number_of_bins)
    line_counter = 0

    total_metadata_processing_time = 0
    total_metadata_download_time = 0
    total_target_download_and_processing_time = 0
    total_install_time = 0

    with open(log_filename) as log_file:
      for line in log_file:
        metadata_processing_time, metadata_download_time, \
        target_download_and_processing_time, install_time = \
        (float(token) for token in line.split(','))

        total_metadata_processing_time += metadata_processing_time
        total_metadata_download_time += metadata_download_time
        total_target_download_and_processing_time += \
          target_download_and_processing_time
        total_install_time += install_time
        line_counter += 1

    avg_metadata_processing_time = \
      total_metadata_processing_time / line_counter
    avg_metadata_download_time = \
      total_metadata_download_time / line_counter
    avg_target_download_and_processing_time = \
      total_target_download_and_processing_time / line_counter
    avg_install_time = total_install_time / line_counter

    times[number_of_bins] = {
      'avg_metadata_processing_time': avg_metadata_processing_time,
      'avg_metadata_download_time': avg_metadata_download_time,
      'avg_target_download_and_processing_time': \
        avg_target_download_and_processing_time,
      'avg_install_time': avg_install_time
    }

  return times


def plot_times(minimum_bin_exponent, maximum_bin_exponent, times):
    # finally, draw the stacked bar plot
    # http://matplotlib.org/examples/api/barchart_demo.html
    # http://matplotlib.org/examples/pylab_examples/bar_stacked.html
    # the x locations for the groups
    ind = np.arange(maximum_bin_exponent-minimum_bin_exponent+1)
    width = 0.5 # the width of the bars
    fig, ax = plt.subplots()

    keys = ['avg_metadata_processing_time', 'avg_metadata_download_time',
            'avg_target_download_and_processing_time', 'avg_install_time']
    colors = ['y', 'r', 'g', 'b']

    assert len(keys) == len(colors)

    # Build stack for each column (number of bins)
    bottom = [0] * (maximum_bin_exponent - minimum_bin_exponent + 1)

    # Build each stack across keys
    for i in xrange(len(keys)):
        key = keys[i]
        color = colors[i]
        values = []

        # Each stack varies across number of bins
        for j in xrange(minimum_bin_exponent, maximum_bin_exponent + 1):
            number_of_bins = 2**j
            values.append(times[number_of_bins][key])

        # Draw this stack of times across number of bins
        ax.bar(ind, values, width, color=color, bottom=bottom)

        # the next stack builds upon the heights of the previous stack
        #print('bottom: {}'.format(bottom))
        #print('{} : {}'.format(key, values))
        for l in xrange(maximum_bin_exponent - minimum_bin_exponent + 1):
            bottom[l] += values[l]

    # add title, labels, ticks, legends
    ax.set_title('Average time to download and install a package of average ' \
                 'size (345,055 bytes)', fontsize=10)
    ax.set_ylabel('Seconds')
    ax.set_xlabel('Number of unclaimed bins')
    ax.set_xticks(ind+(width/2))
    ax.set_xticklabels(['2^{}'.format(i) for i in \
                       xrange(minimum_bin_exponent, maximum_bin_exponent + 1)],
                       fontsize=8)

    # write the actual plot
    plt.savefig('hashed-delegation-times.png')


if __name__ == '__main__':
  minimum_bin_exponent = 1
  maximum_bin_exponent = 15
  times = measure_times(minimum_bin_exponent, maximum_bin_exponent)
  plot_times(minimum_bin_exponent, maximum_bin_exponent, times)


