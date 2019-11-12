import random


numbers = [10, 20, 30, 40, 50]
print ("Original list:  ", numbers )
print('\n')
random.seed(0)
random.shuffle(numbers)
print("reshuffled list ", numbers)

numbers = [10, 20, 30, 40, 50]
random.seed(1)
random.shuffle(numbers)
print("reshuffled list ", numbers)

numbers = [10, 20, 30, 40, 50]
random.seed(2)
random.shuffle(numbers)
print("reshuffled list ", numbers)

numbers = [10, 20, 30, 40, 50]
random.seed(3)
random.shuffle(numbers)
print("reshuffled list ", numbers)

numbers = [10, 20, 30, 40, 50]
random.seed(4)
random.shuffle(numbers)
print("reshuffled list ", numbers)

numbers = [10, 20, 30, 40, 50]
random.seed(5)
random.shuffle(numbers)
print("reshuffled list ", numbers)