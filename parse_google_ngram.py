#!/usr/bin/env python
#
# Copyright 2012 B. J. Potter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Process Google ngram data.

Google ngram data can be found at
http://books.google.com/ngrams/datasets
This was used to generate the word list included with this code. It
generates a list of the most commonly used words in the chosen set by
inputing 1-gram files from Google. This can be used to generate other
word lists suitable for use in making passphrases.

Example usage:

google_ngram.py -o word_list.txt googlebooks-eng-fiction-all-1gram-*
processing: googlebooks-eng-fiction-all-1gram-20120701-a
Reading line   1 million
Reading line   2 million
Reading line   3 million
Reading line   4 million
Reading line   5 million
Reading line   6 million
Reading line   7 million
Reading line   8 million
Reading line   9 million
Reading line  10 million
processing: googlebooks-eng-fiction-all-1gram-20120701-b
Reading line   1 million
Reading line   2 million
Reading line   3 million
Reading line   4 million
Reading line   5 million
Reading line   6 million
Reading line   7 million
Reading line   8 million
Reading line   9 million

This will write 'ngram_processed.txt' with all of the words from the
input ngram files and the 'word_list.txt' with only the top 10,000
words, excluding words less than three letters and those with
punctuation.
"""

import os
import sys
import string
from optparse import OptionParser
from operator import itemgetter

# Don't analyze words from books before this year
START_YEAR = 1980
# How many words in the output file
MAX_WORDS = 10000
# Exclude words shorter than this from the final list
MIN_WORD_LENGTH = 3


def unwanted_characters_in_word(word):
    """Return boolean indicating unwanted characters in the word."""
    for letter in word:
        if ((letter in string.punctuation) or
            (letter not in string.letters)):
            return True
    return False


def process_ngram_file(file_name, word_list):
    """Process a Google ngram file to make a word list.

    The ngram data comes from http://books.google.com/ngrams/datasets"""
    line_count = 0
    for line in open(file_name):
        line_count += 1
        if line_count % 1000000 == 0:
            print "Reading line {0:3d} million".format(line_count / 1000000)
        line = line.split()
        word = line[0].lower()
        year = int(line[1])
        occurances = int(line[2])
        if (year < START_YEAR or
            unwanted_characters_in_word(word)):
            continue
        word_list[word] = word_list.get(word, 0) + occurances


def build_word_list(input_word_list, word_list_file_name):
    """Write final list of words from processed ngram words.

    input_word_list: The given list has the most frequent words at the
    beginning and less frequent words later.
    word_list_file_name: The file to be written to. It will contain just
    the most common MAX_WORDS."""
    final_word_list = []
    for word in input_word_list:
        word = word[0]
        if len(final_word_list) >= MAX_WORDS:
            break
        if len(word) < MIN_WORD_LENGTH:
            continue
        final_word_list.append(word)
    out_file = open(word_list_file_name, 'w')
    for word in final_word_list:
        out_file.write('{0}\n'.format(word))


# Running from command line (main)
usage = "usage: %prog -o word_list.txt input_ngram_file[s]"
parser = OptionParser(usage)
parser.add_option("-o", "--out", default='',
    help="Output file name")
(options, args) = parser.parse_args()
if len(args) == 0:
    print 'ERROR: Must have an input file'
    sys.exit(1)
if options.out == '':
    print ('ERROR: Must have an output file  "-o word_list.txt"')
    sys.exit(1)
word_list = {}
for file_name in args:
    print 'processing:', file_name
    assert os.path.isfile(file_name)
    process_ngram_file(file_name, word_list)
sorted_list = sorted(word_list.iteritems(), key=itemgetter(1), reverse=True)
build_word_list(sorted_list, options.out)
