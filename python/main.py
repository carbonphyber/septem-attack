#!/usr/bin/python3

import argparse
import itertools
import json
import re
import string
import sys

most_desirable_chars_regex = re.compile(b'^[A-Za-z0-9]+$')
lesser_desirable_chars_regex = re.compile(b'^[\-., ;:?!]+$')
plaintext_preable_sample_length = 120

#
def _file_iterator(f):
    byte = f.read(1)
    while byte:
        yield byte[0]
        byte = f.read(1)

#
def file(value):
    f = open(value, 'rb')
    return _file_iterator(f)

#
def _parse_arguments():
    parser = argparse.ArgumentParser(
        description='decrypt an xor data stream without knowledge of the full key',
        formatter_class=argparse.RawTextHelpFormatter,
        )

    # A hint should be formatted like:
    # "**foobar****"
    # where "foobar" is the known substring (both in content and location)
    # and the asterixes are unknown key bytes.
    def hint(value):
        return value

    parser.add_argument(
        '--hint',
        dest='hint',
        metavar='STRING',
        type=hint,
        default='************',
        help='give a hint to about the XOR decryption key'
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


#
def onlyKeepHighScoresThenSort(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition otherwise remove from dictObj
        if callback((key, value)):
            newDict[key] = value
    newList = [k for k, v in sorted(newDict.items(), key=lambda item: item[1])]
    return newList


# when executed as a program (as opposed to a library)
if __name__ == '__main__':
    args = _parse_arguments()
    hint = args.hint
    period_len = len(hint)
    verbose = args.verbose
    if verbose:
        print("hint: %s\n" % hint)
        print("period_len: %s\n" % period_len)

    #
    # Python installs some signal handlers that raise Python exceptions
    # These lines restore normal UNIX behaviour for SIGINT/SIGPIPE
    # - Ctrl+C will now work as expected
    # - xcat ... | head will also work as expected
    #
    import signal
    try:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

    # Load English BIP-39 words from a local file
    bip39_english_words = list()
    with open('./english.txt') as f:
        while (word := f.readline().rstrip()):
            bip39_english_words.append(word)
    if verbose:
        print(bip39_english_words)
        print("\n")

    # the universe of characters to test as part of the XOR key
    all_chars = list(string.printable)

    # read in the STDIN as the XOR ciphertext
    data = args.data
    data_byte_array = bytearray(data)
    j = 0
    i = 0
    matches = list()
    for this_char in data_byte_array:
        matches.insert(i, list())
        # if verbose:
        #     sys.stdout.buffer.write(("** %s **\n" % (hex(this_char))).encode('ascii'))
        for this_letter in all_chars:
            key_char = this_letter.encode('ascii')
            xor_result = bytes((this_char ^ int(key_char[0]),))
            key_col = "%20s: " % (key_char)
            if most_desirable_chars_regex.match(xor_result):
                matches[i].append([this_letter, 1.0])
            elif lesser_desirable_chars_regex.match(xor_result):
                matches[i].append([this_letter, 0.8])
                # if verbose:
                #     sys.stdout.buffer.write(("%s\t%s (0x%s) => %s (0x%s)\n" % (key_col.encode('ascii'), key_char, bytes.hex(key_char), xor_result, bytes.hex(xor_result))).encode('ascii'))
                #     sys.stdout.buffer.write(re.sub(b'[^a-zA-Z.,: ]', '.'.encode('ascii'), bytes(xor_result)))
                #     sys.stdout.buffer.write(b"\n")
            j += 1
            if verbose and j % 10 == 0:
                sys.stdout.buffer.flush()
        if verbose:
            print('matches[%i]: %s' % (i, matches[i]))
        i += 1

    if verbose:
        print(json.dumps(list(map(lambda x: int(x), data_byte_array[:plaintext_preable_sample_length])), indent=4, sort_keys=True))

    # reduce to only the highest scoring matches
    most_likely_chars = list()
    for i in range(0, period_len):
        most_likely_chars.append(dict())

    for i in range(0, len(matches)):
        for j in matches[i]:
            # print(json.dumps(j, indent=4, sort_keys=True))
            key = j[0]
            score = j[1]
            partition_num = i % period_len
            if key not in most_likely_chars[partition_num]:
                most_likely_chars[partition_num][key] = 0.0
            most_likely_chars[partition_num][key] += score

    # filter, sort, and convert dict to list of the dict.key
    filtered_chars = list()
    for i in range(0, period_len):
        if hint[i] == '*':
            max_value = max(most_likely_chars[i].values())
            # Only retain key bytes which decryp to at least 90% of desirable plaintext characters
            filter_threshold = max_value * 0.9
            filtered_chars.append(onlyKeepHighScoresThenSort(most_likely_chars[i], lambda d : d[1] >= filter_threshold))
        else:
            # use the character from the hint
            filtered_chars.append(list(hint[i]))

    if verbose:
        print(json.dumps(filtered_chars, indent=4, sort_keys=True))

    for this_combo in itertools.islice(itertools.product(*filtered_chars), 999999999):
        sys.stdout.buffer.write((b"%s\n" % (''.join(this_combo).encode('ascii'))))
    sys.stdout.flush()
