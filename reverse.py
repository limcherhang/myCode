s = "words and 987"
def myAtoi(s: str) -> int:
    words = [i for i in range(97, 123)] + [i for i in range(65, 91)]# ascii
    numbers = [i for i in range(48, 58)]

    index_word = None
    index_number = None
    for i, ss in enumerate(s):
        if ord(ss) in words:
            index_word = i
            break
    for i, ss in enumerate(s):
        if ord(ss) in numbers:
            index_number = i
            break

    
    if index_word is not None and index_number is not None:
        print(index_number, index_word)
        if index_word < index_number:
            return 0
    
    s = s.replace(" ", '_')
    signed = 1

    if '-' in s:
        signed = -1
    
    new_s = ''
    start_index = None
    for i in range(len(s)):
        if ord(s[i]) in (48, 49, 50, 51, 52, 53, 54, 55, 56, 57):
            start_index = i
            break
    
    if start_index is None:
        return 0
    
    s = s[start_index:]
    for ss in s:
        if ord(ss) not in (46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57):
            break
        else:
            new_s += ss

    if '.' in new_s:
        ans = signed*float(int(new_s))
        if ans > 2**31-1:
            ans = 2**31-1
        elif ans < -2**31:
            ans = -2**31
    else:
        ans = signed*int(new_s)
        if ans > 2**31-1:
            ans = 2**31 - 1
        elif ans < -2**31:
            ans = -2**31
    
    return ans

print(myAtoi(s))