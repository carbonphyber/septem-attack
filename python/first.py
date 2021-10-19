#!/usr/bin/python3

from analysis import index_of_coincidence
import argparse
import itertools
import json
import re
import signal
import string
import sys
from vigenere import decrypt as vigenere_decrypt
from xor import decrypt as xor_decrypt

# 
most_desirable_chars_regex = re.compile(b'^[A-Za-z0-9 .,]+$')
most_desirable_char_score = 1.0
lesser_desirable_chars_regex = re.compile(b'^[\-;:?!]+$')
lesser_desirable_char_score = 0.0
not_desirable_char_score = 0.0
# a RegEx to replace/substitute all non-alpha characters
clean_nonalpha_regex = re.compile(r"[^a-z]", re.IGNORECASE)

#
def _file_iterator(f):
    byte = f.read(1)
    while byte:
        yield byte[0]
        byte = f.read(1)

# Return a file reader
def file(value):
    f = open(value, 'rb')
    return _file_iterator(f)

# Handle CLI arguments
def _parse_arguments():
    parser = argparse.ArgumentParser(
        description='decrypt an xor data stream without knowledge of the full key',
        formatter_class=argparse.RawTextHelpFormatter,
        )

    parser.add_argument(
        'data',
        nargs='?',
        metavar='FILE',
        type=file,
        default=_file_iterator(sys.stdin.buffer),
        help='input filename [default: use stdin]',
        )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='increase output verbosity'
        )

    return parser.parse_args()


# when executed as a program (as opposed to a library)
if __name__ == '__main__':
    args = _parse_arguments()
    verbose = args.verbose

    #
    # Python installs some signal handlers that raise Python exceptions
    # These lines restore normal UNIX behaviour for SIGINT/SIGPIPE
    # - Ctrl+C will now work as expected
    # - xcat ... | head will also work as expected
    #
    try:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

    # the universe of characters to test as part of the XOR key
    all_chars = list(string.printable)

    num_chars = 120
    # read in the STDIN as the XOR ciphertext
    data = args.data
    data_byte_array = bytearray(data)[:num_chars]
    j = 0
    i = 0
    matches = list()
    likely_matches = list()
    # 16 elements. One for each possible period
    for k in range(0, 16):
        likely_matches.insert(k, list())
        for l in range(0, k + 1):
            likely_matches[k].insert(l, dict())
    for this_char in data_byte_array:
        matches.insert(i, dict())
        for this_letter in all_chars:
            key_char = this_letter.encode('ascii')
            xor_result = bytes((this_char ^ int(key_char[0]),))
            if most_desirable_chars_regex.match(xor_result):
                matches[i][this_letter] = most_desirable_char_score
                for k in range(0, 16):
                    period_offset = i % (k + 1)
                    if this_letter not in likely_matches[k][period_offset]:
                        likely_matches[k][period_offset][this_letter] = 0.0
                    likely_matches[k][period_offset][this_letter] += most_desirable_char_score
            elif lesser_desirable_chars_regex.match(xor_result):
                matches[i][this_letter] = lesser_desirable_char_score
                for k in range(0, 16):
                    period_offset = i % (k + 1)
                    if this_letter not in likely_matches[k][period_offset]:
                        likely_matches[k][period_offset][this_letter] = 0.0
                    likely_matches[k][period_offset][this_letter] += lesser_desirable_char_score
            else:
                matches[i][this_letter] = not_desirable_char_score
                if this_letter not in likely_matches[k][period_offset]:
                    likely_matches[k][period_offset][this_letter] = 0.0
            j += 1
        # if verbose:
        #     print('matches[%i]: %s' % (i, matches[i]))
        i += 1

    # if verbose:
    #     print(json.dumps(matches, indent=4, sort_keys=True))

    # if verbose:
    #     print(json.dumps(likely_matches, indent=4, sort_keys=True))

    intersect_matches = list()
    # a list element for each potential period
    for j in range(0, 12):
        intersect_matches.insert(j, list())
        for k in range(0, max(j, 1)):
            intersect_matches[j].insert(k, dict())
        i = 0
        # for each character in the ciphertext
        for partition in range(0, max(j, 1)):
            # for each potential match we see for this ciphertext character in matches
            for item in likely_matches[j][partition].items():
                l = item[0]
                l_score = item[1]
                if l not in intersect_matches[j][partition]:
                    intersect_matches[j][partition][l] = 0.0
                intersect_matches[j][partition][l] += l_score
            max_value = max(intersect_matches[j][partition].values())
            filtered_dict = dict()
            for item in likely_matches[j][partition].items():
                l = item[0]
                l_score = item[1]
                if l_score / max_value > 0.90:
                    filtered_dict[l] = l_score / max_value
            intersect_matches[j][partition] = filtered_dict
            i += 1
        # print("intersect_matches: %s" % (json.dumps(intersect_matches, indent=4, sort_keys=True)))

    if verbose:
        # print(json.dumps(intersect_matches, indent=4, sort_keys=True))
        # print(json.dumps(intersect_matches[11], indent=4, sort_keys=True))
        print(json.dumps(list(map(lambda x: list(x.keys()), intersect_matches[11])), indent=4, sort_keys=True))

    # letters_per_byte = list(map(lambda byte_matches: clean_nonalpha_regex.sub('', ''.join(list(byte_matches.keys()))), matches))
    # if verbose:
    #     print(json.dumps(letters_per_byte, indent=4, sort_keys=True))

    # if verbose:
    #     print(json.dumps(i, indent=4, sort_keys=True))
    #     print(json.dumps(list(map(lambda z: list(filter(lambda x: x[1] > (i / 16), z.items())), likely_matches[11])), indent=4, sort_keys=True))
    #     # print(json.dumps(likely_matches[11], indent=4, sort_keys=True))
    #     # print(json.dumps(likely_matches, indent=4, sort_keys=True))
