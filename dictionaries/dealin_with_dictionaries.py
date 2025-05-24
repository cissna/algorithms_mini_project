"""Dealin with dictionaries"""


def read_wordlist(filename: str):
    """Input: File name
    Output: set of words in file"""
    words = set()
    with open(filename) as f:
        for word in f:
            word = word.strip().lower()
            if word:
                words.add(word)
    return words


def all_set(d, skip=None, operation='&'):
    """uh oh"""
    lst = [d[key] for key in d if key != skip]
    set1 = lst.pop().copy()
    for st in lst:
        exec(f'set1 {operation}= st')
    return set1


joe_less = read_wordlist('less_word.txt')
joe_more = read_wordlist('lots_word.txt')
nltk = read_wordlist('nltk_words.txt')
nltk.add('feet')
for word in nltk.copy():
    nltk.add(word + 's')
    nltk.add(word + 'es')
    nltk.add(word[:-1] + 'ies')

    nltk.add(word + 'ed')
    nltk.add(word + 'd')
    nltk.add(word + word[-1] + 'ed')
    nltk.add(word[:-1] + 'ied')

    nltk.add(word + 'ing')
    nltk.add(word[:-1] + 'ing')

    nltk.add(word + 'er')
    nltk.add(word[:-1] + 'ier')

    nltk.add(word + 'est')
    nltk.add(word[:-1] + 'iest')
    nltk.add(word[:-1] + 'iest')
    
    nltk.add(word + 'ly')

sowpods = read_wordlist('sowpods.txt')
# wiktionary = read_wordlist('wiktionary100k.txt')  # unreliable, missing many words, many extra words

each = {'joe_less': joe_less, 'joe_more': joe_more, 'nltk': nltk, 'sowpods': sowpods}  # , 'wiktionary': wiktionary}
all_sets_no_sowpods_over_15 = {word for word in all_set(each, skip='sowpods') if len(word) > 15}
all_sets = all_set(each) | all_sets_no_sowpods_over_15
all_sets_no_nltk = all_set(each, skip='nltk')
for key in each:
    print(key, len(each[key]), sep=':\t')
print('all:', len(all_sets), sep='\t\t')
print('no nltk:', len(all_sets_no_nltk), sep='\t')

print(all_sets_no_nltk - all_sets)

# print('quickest' in nltk)