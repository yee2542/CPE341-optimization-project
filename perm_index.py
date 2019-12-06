def permutationIndex(permutation):
        index = 0
        position = 2  # position 1 is paired with factor 0 and so is skipped
        factor = 1
        for p in range(len(permutation) - 2, -1, -1):
            successors = 0
            for q in range(p + 1, len(permutation)):
                if permutation[p] > permutation[q]:
                    successors += 1

            index += (successors * factor)
            factor *= position
            position += 1

        return index
# print(permutationIndex([2,1,5,6,7,5,4,3,4,13,9,5,1,0]))