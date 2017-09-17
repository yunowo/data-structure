class Node:
    def __init__(self, item):
        self.left = None
        self.right = None
        self.father = None
        self.char = item[0]
        self.freq = item[1]

    def is_left(self):
        return self.father.left == self

    def is_right(self):
        return self.father.right == self


class Huffman:
    @staticmethod
    def count_freq(text):
        chars = []
        freq_map = []
        for c in text:
            if c not in chars:
                chars.append(c)
                freq = (c, text.count(c))
                freq_map.append(freq)
        return freq_map

    @staticmethod
    def create_huffman_tree(nodes):
        queue = nodes[:]
        while len(queue) > 1:
            queue.sort(key=lambda item: item.freq)
            node_left = queue.pop(0)
            node_right = queue.pop(0)
            node_father = Node((None, node_left.freq + node_right.freq))
            node_father.left = node_left
            node_father.right = node_right
            node_left.father = node_father
            node_right.father = node_father
            queue.append(node_father)
        queue[0].father = None
        return queue[0]

    @staticmethod
    def huffman_encoding(nodes, root):
        codes = [''] * len(nodes)
        for i in range(len(nodes)):
            node_tmp = nodes[i]
            while node_tmp != root:
                if node_tmp.is_left():
                    codes[i] = '0' + codes[i]
                else:
                    codes[i] = '1' + codes[i]
                node_tmp = node_tmp.father
        return codes

    @staticmethod
    def encode(text, freq_map, codes):
        huffman_str = ''
        for char in text:
            for index, item in enumerate(freq_map):
                if char == item[0]:
                    huffman_str += codes[index]
        return huffman_str

    @staticmethod
    def decode(huffman_str, freq_map, codes):
        origin_str = ''
        while huffman_str != '':
            for index, item in enumerate(codes):
                if item in huffman_str and huffman_str.index(item) == 0:
                    origin_str += freq_map[index][0]
                    huffman_str = huffman_str[len(item):]
        return origin_str

    def huffman(self, text):
        freq_map = self.count_freq(text)
        nodes = [Node(item) for item in freq_map]
        root = self.create_huffman_tree(nodes)
        codes = self.huffman_encoding(nodes, root)
        encoded_str = self.encode(text, freq_map, codes)
        decoded_str = self.decode(encoded_str, freq_map, codes)
        return freq_map, encoded_str, decoded_str, root, nodes
