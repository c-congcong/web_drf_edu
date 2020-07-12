import random


def get_random_code():
    code = "%06d" % random.randint(0, 999999)
    print(code)
    return code


def get_random_name():
    name = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 5))
    print(name)
    return name


if __name__ == '__main__':
    get_random_name()
    get_random_code()
