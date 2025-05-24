"""DFS graph traverser to win Letter Boxed"""

def reverse_d(d):
    reversed_d = {}
    for key in d if type(d) == dict else range(len(d)):
        for value in d[key]:
            if value in reversed_d:
                reversed_d[value].add(key)
            else:
                reversed_d[value] = {key}
    return reversed_d


def has_consecutive_same_numbers(numbers):
    for i in range(len(numbers) - 1):
        if numbers[i] == numbers[i + 1]:
            return True
    return False


def make_words_set():
    with open('dictionaries/less_word.txt', 'r') as f:
        less_word = {x.strip().lower()for x in f.read().split('\n')}
    return {x for x in less_word if len(x)>2}


def make_letter_boxed_graph(sides: [{str, str, str}, {str, str, str}, {str, str, str}, {str, str, str}], return_words=False):
    fair_letters = set(sides[0] | sides[1] | sides[2] | sides[3])
    words = {word for word in make_words_set() if not set(word) - fair_letters}
    mapper = reverse_d(sides)
    words = {word for word in words if not has_consecutive_same_numbers([mapper[char] for char in word])}
    if return_words:
        return words

    graph = {word: {word2 for word2 in words if word[-1] == word2[0]} for word in words}
    return graph, fair_letters


def solve_letter_boxed_2(G, fair_letters):
    results = []
    for key in G:
        for value in G[key]:
            if not (fair_letters - set(key)) - set(value):
                results.append((key, value))
    return results

def solve(G):
    new = sorted([(len(set(x)), x) for x in G.keys()])
    E = set()
    answer = [new[-1]]
    start = new.pop()
    for n in start[1]:
            E.add(n)
    while len(E) < 12:        
        all_words = []
        for i in new:
            if i[1][0] == start[1][-1]:
                all_words.append((len(E|set(i[1])), i[1]))
        all_words = sorted(all_words)
        start = all_words.pop()
        index = -1
        for j in new:
            index += 1
            if j[1] == start[1]:
                break
        answer.append(new[index])
        new.pop(index)
        for n in start[1]:
            E.add(n)
    return [item[1] for item in answer]

def text2sides(text):
    return [set(x.lower().strip()) for x in text.split() if x.lower().strip()]


def letter_boxed_solver(letters):
    """Format should be:
    'WUH LTR PYI AXG'
    """
    sides = text2sides(letters)
    graph = make_letter_boxed_graph(sides)[0]
    return solve(graph)
