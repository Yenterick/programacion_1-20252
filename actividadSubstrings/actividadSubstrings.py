def checkSubstrings(strCheck, check):
    substrings = []
    left = 0

    for i in range(len(strCheck)):
        for j in range(i, len(strCheck) + 1):
            string = strCheck[left:j]
            if check is True:
                if strCheck[left] in "aeiou" and string != "":
                    substrings.append(string)
            else:
                if strCheck[left] not in 'aeiou' and string != "":
                    substrings.append(string)
        left += 1

    return len(substrings),substrings     

def game(stringCheck):
    substringA = checkSubstrings(stringCheck, True)
    substringB = checkSubstrings(stringCheck, False)

    return f"A {substringA[0]} - {substringA[1]}" if substringA[0] >= substringB[0] else f"B {substringB[0]} - {substringB[1]}"

print(game("murcielago"))
    