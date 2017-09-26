def search(t, p):
    # partial match table
    k = [0]
    for i in range(1, len(p)):
        j = k[i - 1]
        while j > 0 and p[j] != p[i]:
            j = k[j - 1]
        k.append(j + 1 if p[j] == p[i] else j)

    result = []
    m = 0
    for i, char in enumerate(t):
        while m > 0 and char != p[m]:  # if m mismatches, move forward k[m-1] and restart
            m = k[m - 1]
        if char == p[m]:  # m matches, move forward 1
            m += 1
        if m == len(p):  # fully matches
            result.append(i - (m - 1))
            m = k[m - 1]

    return result


def replace(c, t, r, s, results):
    delta, count = 0, 0
    for i in results:
        t = t[:i + delta] + r + t[i + delta + len(s):]
        delta += len(r) - len(s)
        count += 1
        if count >= c != -1:
            break
    return t
