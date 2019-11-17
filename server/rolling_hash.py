# rolling_hash.py

modulo = (1e9) + 7
base = 107

def rolling_hash(s):
    s = s[15:]
    ans = 0
    for c in s:
        ans = (ans * base + ord(c)) % modulo
    return int(ans)