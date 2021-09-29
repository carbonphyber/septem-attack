#!/usr/bin/python3

import json
import re
import string
import sys

VERBOSE = False
most_desirable_chars_regex = re.compile(b'^[A-Za-z0-9]+$')
plaintext_preable_sample_length = 120

def _file_iterator(f):
    byte = f.read(1)
    while byte:
        yield byte[0]
        byte = f.read(1)

def file(value):
    f = open(value, 'rb')
    return _file_iterator(f)

# when executed as a program (as opposed to a library)
if __name__ == '__main__':
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
    if VERBOSE:
        print(bip39_english_words)
        print("\n")

    # the universe of characters to test as part of the XOR key
    all_chars = list(string.printable)

    # read in the STDIN as the XOR ciphertext
    data = _file_iterator(sys.stdin.buffer)
    data_byte_array = bytearray(data)
    j = 0
    i = 0
    matches = list()
    for this_char in data_byte_array:
        matches.insert(i, list())
        if VERBOSE:
            sys.stdout.buffer.write(("** %s **\n" % (hex(this_char))).encode('ascii'))
        for letter1 in all_chars:
            key_char = letter1.encode('ascii')
            xor_result = bytes((this_char ^ int(key_char[0]),))
            key_col = "%20s: " % (key_char)
            if most_desirable_chars_regex.match(xor_result):
                matches[i].append(letter1)
                if VERBOSE:
                    sys.stdout.buffer.write(("%s\t%s (0x%s) => %s (0x%s)\n" % (key_col.encode('ascii'), key_char, bytes.hex(key_char), xor_result, bytes.hex(xor_result))).encode('ascii'))
                    sys.stdout.buffer.write(re.sub(b'[^a-zA-Z.,: ]', '.'.encode('ascii'), bytes(xor_result)))
                    sys.stdout.buffer.write(b"\n")
            j += 1
            if j % 10 == 0:
                sys.stdout.buffer.flush()
        if VERBOSE:
            print('matches[%i]: %s' % (i, matches[i]))
        i += 1

    if VERBOSE:
        print(json.dumps(list(map(lambda x: int(x), data_byte_array[:plaintext_preable_sample_length])), indent=4, sort_keys=True))
