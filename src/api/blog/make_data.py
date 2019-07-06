from collections import Counter, defaultdict
from typing import (
    Dict,
    Tuple,
    List,
)
import random

from janome.tokenizer import Tokenizer


def get_three_words_list(sentence: str) -> List[Tuple[int, str]]:
    t = Tokenizer()
    words = ['__BEGIN__'] + t.tokenize(sentence, wakati=True) + ['__END__']
    three_words_list = []
    for i in range(len(words) -2 ):
        three_words_list.append(tuple(words[i:i+3]))
    return three_words_list


def get_three_words_count(sentences: List[str]) -> Counter:
    three_words_list = []
    for sentence in sentences:
        three_words_list += get_three_words_list(sentence)
    three_words_count = Counter(three_words_list)
    return three_words_count

def generate_markov_dict(three_words_count: Counter) -> Dict:
    """マルコフ連鎖で文章生成用の辞書データを生成する
    """
    markov_dict = dict()
    for three_words, count in three_words_count.items():
        two_words = three_words[:2]
        next_word = three_words[2]
        if two_words not in markov_dict:
            markov_dict[two_words] = {'words': [], 'weights': []}
        markov_dict[two_words]['words'].append(next_word)
        markov_dict[two_words]['weights'].append(count)
    return markov_dict


def get_first_word_and_count(three_word_count: Counter) -> Dict:
    first_word_count = defaultdict(int)
    for three_words, count in three_word_count.items():
        if three_words[0] == '__BEGIN__':
            next_word = three_words[1]
            first_word_count[next_word] += count
    return first_word_count


def get_first_word_weights(three_word_count: Counter) -> Tuple[List[str]]:
    first_word_count = get_first_word_and_count(three_word_count)
    words = []
    weights = []
    for word, count in first_word_count.items():
        words.append(word)
        weights.append(count)
    return words, weights


def generate_text(first_words: List[str], first_weights: List[str], markov_dict: Dict):
    first_word = random.choices(first_words, weights=first_weights)[0]
    generate_words = ['__BEGIN__', first_word]
    while True:
        pair = tuple(generate_words[-2:])
        words = markov_dict[pair]['words']
        weights = markov_dict[pair]['weights']
        next_word = random.choices(words, weights=weights)[0]
        if next_word == '__END__':
            break
        generate_words.append(next_word)
    return ''.join(generate_words[1:])
