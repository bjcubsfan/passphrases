#!/usr/bin/env python
#
# Copyright 2017 B. J. Potter
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

"""Command line tool to generate pass phrases.

This outputs sequences of words that can be used as passphrases. It
chooses random words in a good cryptographic way from a given list of
words. The default and suggested usage is to pick a pass phrase of 4
random words from a list of 10,000 words.
"""

from __future__ import print_function
import os
import sys
import random
from optparse import OptionParser


def generate_pass_phrases(
    word_list,
    number_words_in_phrase,
    number_phrases):
    """Generates and prints random pass phrases.

    number_words_in_phrase: how many words per phrase
    number_phrases: how many pass phrases to generate
    prints: string of pass phrases
    """
    # The last word in the list is the
    # max for our random integer.
    integer_max = len(word_list)
    # start with the first (0th) word
    integer_min = 0
    pass_phrases = []
    for _ in range(number_phrases):
        pass_phrase = []
        for _ in range(number_words_in_phrase):
            # SystemRandom is a cryptographically secure way
            # to generate random numbers.
            pass_phrase.append(
                word_list[random.SystemRandom().randint(
                    integer_min, integer_max)])
        pass_phrases.append(pass_phrase)
    return pass_phrases


def print_pass_phrases(pass_phrases):
    for pass_phrase in pass_phrases:
        printable_pass_phrase = ' '.join(pass_phrase)
        print(printable_pass_phrase)


def get_word_list(file_name):
    with open(file_name) as input_file:
        word_list = [line.strip() for line in input_file]
    return word_list


def command_line():
    """Running from command line (main)"""
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    path_to_script = os.path.dirname(os.path.abspath(__file__))
    default_file = os.path.join(path_to_script, 'word_list.txt')
    parser.add_option("-w", "--words", default=4,
        help="Number of words per phrase")
    parser.add_option("-n", "--num", default=5,
        help="Number of phrases")
    parser.add_option("-f", "--file", default=default_file,
        help="Use other than the default word list")
    (options, args) = parser.parse_args()
    if os.path.isfile(options.file):
        word_list = get_word_list(options.file)
    else:
        sys.stdout.write('%s is not a file' % options.file)
        sys.exit(1)
    print_pass_phrases(
        generate_pass_phrases(
            word_list, int(options.words), int(options.num)))

if __name__ == '__main__':
    command_line()
