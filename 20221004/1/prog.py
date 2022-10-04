def bin_search(str1, str2):
    n = len(str2)
    if n > 0:
        if str1 == str2[int(n/2)]:
            return True
        elif str1 > str2[int(n/2)]:
            return bin_search(str1, str2[int(n/2):])   
        else:
            return bin_search(str1, str2[:int(n/2)])
    else:
        return False

str1, str2 = eval(input())
print(bin_search(str1, str2))