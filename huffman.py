class Node:
    def __init__(self, char, freq):
        self.left = None
        self.right = None
        self.father = None
        self.char = char
        self.freq = freq

    def is_left(self):
        return self.father.left == self

    def is_right(self):
        return self.father.right == self


class Huffman:
    @staticmethod
    def count_freq(text):
        freq_map = {}
        for c in text:
            if c not in freq_map:
                freq_map[c] = (text.count(c), '')
        return freq_map

    @staticmethod
    def create_huffman_tree(nodes):
        queue = nodes[:]
        while len(queue) > 1:
            queue.sort(key=lambda item: item.freq)
            node_left = queue.pop(0)
            node_right = queue.pop(0)
            node_father = Node(None, node_left.freq + node_right.freq)
            node_father.left = node_left
            node_father.right = node_right
            node_left.father = node_father
            node_right.father = node_father
            queue.append(node_father)
        queue[0].father = None
        return queue[0]

    @staticmethod
    def huffman_encoding(nodes, root, freq_map):
        for i, n in enumerate(nodes):
            node_tmp = n
            while node_tmp != root:
                if node_tmp.is_left():
                    freq_map[n.char] = (freq_map[n.char][0], '0' + freq_map[n.char][1])
                else:
                    freq_map[n.char] = (freq_map[n.char][0], '1' + freq_map[n.char][1])
                node_tmp = node_tmp.father
        return freq_map

    @staticmethod
    def encode(text, freq_map):
        huffman_str = ''
        for char in text:
            huffman_str += freq_map[char][1]
        return huffman_str

    @staticmethod
    def decode(huffman_str, freq_map):
        origin_str = ''
        while huffman_str != '':
            # TODO
            for index, item in enumerate(freq_map):
                if item in huffman_str and huffman_str.index(item) == 0:
                    origin_str += freq_map[index][0]
                    huffman_str = huffman_str[len(item):]
        return origin_str

    def huffman(self, text):
        freq_map = self.count_freq(text)
        nodes = [Node(c, t[0]) for c, t in freq_map.items()]
        root = self.create_huffman_tree(nodes)
        freq_map = self.huffman_encoding(nodes, root, freq_map)
        encoded_str = self.encode(text, freq_map)
        # decoded_str = self.decode(encoded_str, freq_map)
        return freq_map, root, nodes, encoded_str
