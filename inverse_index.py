import ast
import re
from os import walk, path


class InverseIndex:
    @staticmethod
    def create():
        result = {}
        paths = [fn for fn in next(walk('docs'))[2]]
        for p in paths:
            with open(path.join('docs', p), 'r') as f:
                original = f.read()
                filtered = re.sub("[\",.?!:;/<>()]", "", original)
                words = filtered.split()
                words_unique = list(set(words))

                for i, w in enumerate(words_unique):
                    index = []
                    for ii, ww in enumerate(words_unique):
                        if ww == w:
                            index.append((p, ii))
                    if w in result:
                        result[w].append(*index)
                    else:
                        result[w] = index

        with open('my_index.txt', 'w') as f:
            f.writelines(str(result))

    @staticmethod
    def search(query):
        with open('my_index.txt', 'r') as f:
            index = ast.literal_eval(f.readlines()[0])
            result = []
            for k in index.keys():
                if query == k:
                    result = [*result, *index[k]]
            return result
