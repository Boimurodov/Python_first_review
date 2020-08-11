import collections
import itertools
import pickle
import string


from alphabets import russian_alphabeth, symbols, symbols1
from encode_and_decode import caesar, next_symbol
from get_stream import get_stream


def count(text):
    count_1 = dict(collections.Counter(symbol.lower() for symbol in text if symbol in
                                       itertools.chain(string.ascii_letters, russian_alphabeth, symbols1)))
    sum_1 = sum(count_1.values())
    if sum_1:
        for l in count_1.keys():
            count_1[l] /= sum_1
    return count_1


def train(text_, model_):
    with get_stream(text_, 'r') as text_file:
        text = text_file.read()
    with open(model_, 'wb') as model_file:
        pickle.dump(count(text), model_file)


def diff(step, mod, count_):
    sum_2 = 0
    for symbol in count_:
        sum_2 += abs(mod[next_symbol(symbol, step)] - count_[symbol])
    return sum_2


def hack(input_, output_, model_):
    with open(model_, 'rb') as model_file:
        value_in_model_file = pickle.load(model_file)
    with get_stream(input_, 'r') as input_file:
        text = input_file.read()
    min_step = 26 - min(range(26), key=lambda step:
                        diff(step, value_in_model_file, count(text)))
    text = caesar(text, min_step, is_encode=False)
    with get_stream(output_, 'w') as output_file:
        output_file.write(text)
