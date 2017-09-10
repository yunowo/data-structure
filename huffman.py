class Node:
    def __init__(self, freq):
        self.left = None
        self.right = None
        self.father = None
        self.freq = freq

    def is_left(self):
        return self.father.left == self

    def is_right(self):
        return self.father.right == self


class Huffman:
    # 统计字符出现频率，生成映射表
    def count_freq(self, text):
        chars = []
        freq_map = []
        for c in text:
            if c not in chars:
                chars.append(c)
                freq = (c, text.count(c))
                freq_map.append(freq)
        return freq_map

    # 创建叶子节点
    def create_nodes(self, freqs):
        return [Node(freq) for freq in freqs]

    # 创建Huffman树
    def create_huffman_tree(self, nodes):
        queue = nodes[:]
        while len(queue) > 1:
            queue.sort(key=lambda item: item.freq)
            node_left = queue.pop(0)
            node_right = queue.pop(0)
            node_father = Node(node_left.freq + node_right.freq)
            node_father.left = node_left
            node_father.right = node_right
            node_left.father = node_father
            node_right.father = node_father
            queue.append(node_father)
        queue[0].father = None
        return queue[0]

    # Huffman编码
    def huffman_encoding(self, nodes, root):
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

    # 编码整个字符串
    def encode(self, text, freq_map, codes):
        huffman_str = ''
        for char in text:
            for index, item in enumerate(freq_map):
                if char == item[0]:
                    huffman_str += codes[index]
        return huffman_str

    # 解码整个字符串
    def decode(self, huffman_str, freq_map, codes):
        origin_str = ''
        while huffman_str != '':
            for index, item in enumerate(codes):
                if item in huffman_str and huffman_str.index(item) == 0:
                    origin_str += freq_map[index][0]
                    huffman_str = huffman_str[len(item):]
        return origin_str

    def huffman(self, text):
        freq_map = self.count_freq(text)
        nodes = self.create_nodes([item[1] for item in freq_map])
        root = self.create_huffman_tree(nodes)
        codes = self.huffman_encoding(nodes, root)
        encoded_str = self.encode(text, freq_map, codes)
        deocded_str = self.decode(encoded_str, freq_map, codes)
        return freq_map, encoded_str, deocded_str
