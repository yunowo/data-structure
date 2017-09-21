class KMP:
    @staticmethod
    def partial(pattern):
        """ Calculate partial match table: String -> [Int]"""
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret

    def search(self, t, p):
        """
        KMP search main algorithm: String -> String -> [Int]
        Return all the matching position of pattern string P in S
        """
        partial, ret, j = self.partial(p), [], 0

        for i in range(len(t)):
            while j > 0 and t[i] != p[j]:
                j = partial[j - 1]
            if t[i] == p[j]:
                j += 1
            if j == len(p):
                ret.append(i - (j - 1))
                j = 0

        return ret
