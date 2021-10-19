import string

def decrypt(txt='', key=''):
    # universe = [c for c in (chr(i) for i in range(32,127))]
    universe = string.ascii_lowercase
    uni_len = len(universe)
    if not txt:
        print('Needs text.')
        return
    if not key:
        print('Needs key.')
        return
    if any(t not in universe for t in key):
        print('Invalid characters in the key. Must only use ASCII symbols.')
        return
    ret_txt = ''
    k_len = len(key)
    for i, l in enumerate(txt):
        if l not in universe:
            ret_txt += l
        else:
            txt_idx = universe.index(l)
            k = key[i % k_len]
            key_idx = -1 * universe.index(k)
            code = universe[(txt_idx + key_idx) % uni_len]
            ret_txt += code
    # print(ret_txt)
    return ret_txt

def encrypt(txt='', key=''):
    # universe = [c for c in (chr(i) for i in range(32,127))]
    universe = string.ascii_lowercase
    uni_len = len(universe)
    if not txt:
        print('Needs text.')
        return
    if not key:
        print('Needs key.')
        return
    if any(t not in universe for t in key):
        print('Invalid characters in the key. Must only use ASCII symbols.')
        return
    ret_txt = ''
    k_len = len(key)
    for i, l in enumerate(txt):
        if l not in universe:
            ret_txt += l
        else:
            txt_idx = universe.index(l)
            k = key[i % k_len]
            key_idx = universe.index(k)
            code = universe[(txt_idx + key_idx) % uni_len]
            ret_txt += code
    # print(ret_txt)
    return ret_txt
