class LexicoGraphPermu:
    def __init__(self, _arr):
        self.arr = _arr


# next_permutation method implementation
def next_permutation(L):
    n = len(L)
    i = n - 2
    while i >= 0 and L[i] >= L[i + 1]:
        i -= 1

    if i == -1:
        return False

    j = i + 1
    while j < n and L[j] > L[i]:
        j += 1
    j -= 1

    L[i], L[j] = L[j], L[i]

    left = i + 1
    right = n - 1

    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1

    return True

# Function to print nth permutation
# using next_permute()


def nPermute(string, n):
    # string = list(string)
    string = string
    new_string = []

    # Sort the string in lexicographically
    # ascending order
    string.sort()
    j = 2

    # Keep iterating until
    # we reach nth position
    while next_permutation(string):
        new_string = string

        # check for nth iteration
        if j == n:
            break
        j += 1

    # print string after nth iteration
    # print(''.join(new_string))
    print(new_string)


arr = [1,2,3,4,5,6,7,8,9,10,11,12,13]
n = 6000000
nPermute(arr, n)
