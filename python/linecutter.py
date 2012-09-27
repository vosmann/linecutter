#!/usr/bin/python

import os
import sys
import argparse
import codecs
DEFAULT_LINE_LENGTH = 80

# Implementation TODOs
# Leave empty lines as they were.
# Don't touch whitespace at line beginnings.
# When breaking a line, the leading whitespace needs to be added to the
# the beginning of the added new line.


# Prepare the arguments.
parser = argparse.ArgumentParser(description="Cut a file's lines to a shorter \
        length.")
parser.add_argument('filename', type=str, help="Path to the file.")
parser.add_argument('-l', action='store', dest='length',
        help="Longest allowed line length.")
parser.add_argument('-k', action='store_true', dest='keep', default=False,
        help="Keep the old file.")
args = parser.parse_args()

if args.length == None:
    max_line_length = DEFAULT_LINE_LENGTH
else:
    max_line_length = args.length

# Print some starting info.
print "___Linecutter___"
print "Working on file: " + args.filename
print "Max line length: " + str(max_line_length)

# Business time.
try:
    # Open the files.
    orig_file = open(args.filename, mode='r')
    new_file = open(args.filename + ".new", mode='w')
    #orig_file = codecs.open(args.filename, encoding='utf-8', mode='r')
    #new_file = codecs.open(args.filename + ".new", encoding='utf-8', mode='w')

    # Process segments of text delimited by an empty line (or more).
    still_same_segment = True
    segment_lines = []
    for line in orig_file:
        segment_lines.append(line)
        if not line.strip():
            # Segment end. Make the new lines.
            words = segment_lines.split()
            print words
            new_line = ""
            for word in words:
                print word
                if len(new_line) == 0:
                    # The first word of the line. First in the file actually.
                    new_line = new_line + word
                    print "\tFIRST word of line."
                elif len(new_line) + 1 + len(word) <= max_line_length:
                    # Not the first word of the line, but still fits into the
                    # line.
                    new_line = new_line + " " + word
                    print "\tadding another word"
                else:
                    # Write the right-sized line into another file.
                    new_file.write(new_line)
                    new_file.write(u'\n')
                    print "\tCOULDN'T fit. Writing the line."
                    new_line = ""
                    new_line = new_line + word
                    print "\tFIRST word of line. (It couldn't fit into the \
                            last one.)"
            segment_lines = []

    # Everyone needs closure.
    orig_file.close()
    new_file.close()
    # If the script wasn't run with a switch to keep it, delete old file.
    if not args.keep:
        print "UUU, deleting old file."
except IOError as (errno, strerror):
    print "I/O error({0}): {1}. Aborting execution.".format(errno, strerror)
    raise
except:
    print "Unexpected error; aborting execution. Info: ", sys.exc_info()[0]
    raise
