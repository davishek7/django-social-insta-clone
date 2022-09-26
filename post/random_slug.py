import string, random

def generate_random_slug():
    return ''.join(random.choice(string.ascii_letters) for _ in range(12))