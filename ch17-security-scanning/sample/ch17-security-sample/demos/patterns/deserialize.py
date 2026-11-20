"""pickle and yaml.load run code from the data they read."""

import os
import pickle

import yaml


class Payload:
    def __reduce__(self):
        return (print, ("pickle.loads() just called print() for the sender",))


data = pickle.dumps(Payload())
pickle.loads(data)

doc = "!!python/object/apply:os.getcwd []"
print("yaml.load(UnsafeLoader) called os.getcwd():", yaml.load(doc, Loader=yaml.UnsafeLoader) == os.getcwd())
try:
    yaml.safe_load(doc)
except yaml.constructor.ConstructorError as error:
    print("yaml.safe_load ->", type(error).__name__, error.problem)
try:
    yaml.load(doc)
except TypeError as error:
    print("yaml.load(doc) ->", type(error).__name__, error)
