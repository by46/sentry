def hex_representation(binary_str):
    return '[{0}]'.format(' '.join(['{0:02x}'.format(ord(x)) for x in binary_str]))
