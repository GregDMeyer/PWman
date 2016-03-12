
from Crypto.Random.random import choice, sample
from string import printable, ascii_lowercase, ascii_letters, digits
from math import log, ceil


def make_pass(pool='chars',
              min_entropy=20,
              min_length=8,
              max_length=30):

    if min_length > max_length:
        raise Exception('min_length must be <= max_length.')

    if pool == 'chars':
        pool = printable.strip()

    elif pool == 'lowercase':
        pool = lowercase

    elif pool == 'alphanumeric':
        pool = ascii_letters + digits

    ind_entropy = log(len(pool), 2)
    min_length = max( int(ceil(min_entropy/ind_entropy)), min_length )

    # no reason to limit entropy by not allowing repeats (thus I use choice() instead of sample() )
    element_lst = [choice(pool) for i in xrange(min_length)]

    return ''.join(element_lst)

