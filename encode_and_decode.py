import string
import itertools


from alphabets import russian_alphabeth, symbols, symbols1
from get_stream import get_stream


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

    for symbol, key1 in zip(text, itertools.cycle(key)):
        if key1 in string.ascii_letters:
            ord1 = ord(key1.lower()) - ord('a')
        elif symbol in russian_alphabeth:
            ord1 = ord(key1.lower()) - ord('а')
        elif symbol in symbols:
            ord1 = symbols1[symbol]
        else:
            ord1 = 0
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