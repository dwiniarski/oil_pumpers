import random


def generate_random_string(length):
    return ''.join(random.choice('0123456789abcdefghijklmnoprstuqwxzv') for i in range(length))
