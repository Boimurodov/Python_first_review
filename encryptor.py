import string
import json
from collections import Counter
from itertools import cycle
import sys
from contextlib import contextmanager


russian_alphabeth = 'йцукенгшщзхъфывапролджэячсмитьбюё'
russian_alphabeth += 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
symbols = {0 : ',', 1 : '.', 2 : '?', 3 : '!', 4 : ' '}
symbols1 = {',' : 0, '.' : 1, '?' : 2, '!' : 3, ' ' : 4}
@contextmanager
def get_stream(stream, mode):
    if stream == sys.stdin:
        file = sys.stdin
    elif stream == sys.stdout:
        file = sys.stdout
    else:
        file = open(stream, mode)
    try:
        yield file
    finally:
        file.close()


def next_symbol(symbol, step):
    if symbol in string.ascii_letters:
        if symbol.isupper():
            return chr(ord('A') + (ord(symbol) - ord('A') + step) % 26)
        else:
            return chr(ord('a') + (ord(symbol) - ord('a') + step) % 26)
    elif symbol in russian_alphabeth:
        if symbol.isupper():
            return chr(ord('А') + (ord(symbol) - ord('А') + step) % 33)
        else:
            return chr(ord('а') + (ord(symbol) - ord('а') + step) % 33)
    elif symbol in symbols1:
        return symbols[(symbols1[symbol] + step) % 5]
    else:
        return symbol


def caesar(text, key, is_encode):
    text1 = ''
    for symbol in text:
        text1 += next_symbol(symbol, key if is_encode else -key)
    return text1


def vigenere(text, key, is_encode):
    text1 = ''

    for symbol, key1 in zip(text, cycle(key)):
        if key1 in string.ascii_letters:
            ord1 = ord(key1.lower()) - ord('a')
        elif symbol in russian_alphabeth:
            ord1 = ord(key1.lower()) - ord('а')
        elif symbol in symbols:
            ord1 = symbols1[symbol]
        text1 += next_symbol(symbol, ord1 if is_encode else -ord1)
    return text1


def vernam(text, text_key, is_encode):
    text1 = ''
    for symbol, key1 in zip(text, text_key):
        ord1 = ord(key1.lower()) - ord('a')
        text1 += next_symbol(symbol, ord1 if is_encode else -ord1)
    return text1


def code_and_decode(cipher, key, input_, output_, is_encode):
    with get_stream(input_, 'r') as input_file:
        text = input_file.read()
    if cipher == 'caesar':
        text = caesar(text, int(key), is_encode)
    if cipher == 'vigenere':
        text = vigenere(text, key, is_encode)
    if cipher == 'vernam':
        with get_stream(key, 'r') as text1:
            text = vernam(text, text1.read(), is_encode)
    with get_stream(output_, 'w') as output_file:
        output_file.write(text)


if sys.argv[1] == 'encode':
    code_and_decode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                    is_encode=True)
if sys.argv[1] == 'decode':
    code_and_decode(sys.argv[2], sys.argv[3],
                    sys.argv[4], sys.argv[5], is_encode=False)


def count(text):
    count_1 = dict(Counter(symbol.lower() for symbol in text if symbol
                           in string.ascii_letters or symbol in russian_alphabeth
                           or symbol in symbols1))
    sum_1 = sum(count_1.values())
    if sum_1:
        for l in count_1.keys():
            count_1[l] /= sum_1
    return count_1


def train(text_, model_):
    with get_stream(text_, 'r') as text_file:
        text = text_file.read()
    with open(model_, 'w') as model_file:
        json.dump(count(text), model_file)


if sys.argv[1] == 'train':
    train(sys.argv[2], sys.argv[3])


def diff(step, mod, count):
    sum_2 = 0
    for symbol in count:
        sum_2 += abs(mod[next_symbol(symbol, step)] - count[symbol])
    return sum_2


def hack(input_, output_, model_):
    with open(model_, 'r') as model_file:
        value_in_model_file = json.load(model_file)
    with get_stream(input_, 'r') as input_file:
        text = input_file.read()
    min_step = min(range(26), key=lambda step:
                   diff(step, value_in_model_file, count(text)))
    text = caesar(text, min_step, True)
    with get_stream(output_, 'w') as output_file:
        output_file.write(text)


if sys.argv[1] == 'hack':
    hack(sys.argv[2], sys.argv[3], sys.argv[4])
