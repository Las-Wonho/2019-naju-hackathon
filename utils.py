from random import randint


class Singleton:
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)

        return class_._instance


def hash(sample_string):
    # return sample_string + str(randint(0, 100000))
    return sample_string
