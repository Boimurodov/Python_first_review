import collections
import itertools
import pickle
import string


from alphabets import russian_alphabeth, symbols, symbols1
from encode_and_decode import vigenere
from get_stream import get_stream
from hack_and_train import count, diff


def suitable_step(text, model_):
    with open(model_, 'rb') as model_file:
        value_in_model_file = pickle.load(model_file)
    min_step = 26 - min(range(26), key=lambda step:
                        diff(step, value_in_model_file, count(text)))
    return min_step


def coincident_index(text: str) -> float:
    len_1 = 0
    for symbol in text:
        if symbol in string.ascii_letters:
            len_1 += 1
    count_1 = dict(collections.Counter(symbol.lower() for symbol in text if symbol in
                   itertools.chain(string.ascii_letters,
                                   russian_alphabeth, symbols1)))
    sum_1 = 0
    for symbol in string.ascii_lowercase:
        if symbol not in count_1:
            continue
        sum_1 += count_1[symbol] * (count_1[symbol] - 1) / (len_1 * (len_1 - 1))
    return sum_1


def len_key(text: str) -> int:
    n = 0
    for symbol in text:
        if symbol in string.ascii_letters:
            n += 1
    len_ = (0.027 * n) / ((n - 1) * coincident_index(text) + 0.065 - 0.038 * n)
    return int(len_) + 1


def find_key(text: str, len_key_text: int, model_) -> str:
    key = ''
    for i in range(len_key_text):
        key += chr(ord('a') + suitable_step(text[i::len_key_text], model_) % 26)
    return key


def hack_vigenere(input_, output_, model_):
    with get_stream(input_, 'r') as input_file:
        text = input_file.read()
    key = find_key(text, len_key(text), model_)
    text = vigenere(text, key, is_encode=False)
    with get_stream(output_, 'w') as output_file:
        output_file.write(text)