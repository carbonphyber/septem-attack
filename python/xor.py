import itertools

# Decrypt an xor data string using string key
def decrypt(data, key):
    bytes_array = bytearray(''.encode('ascii'))
    for b, k in zip(data, itertools.cycle(key.encode('ascii'))):
        bytes_array.extend(bytes((b ^ k,)))
    return bytes_array
