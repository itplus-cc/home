def makeSecret():
    import random, string
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(random.randint(10, 16)))
    return password
