import hcl2
import importlib
import pkgutil


def load_hcl(path):
    # Walk the path and load all HCL files
    for finder, name, ispkg in pkgutil.iter_modules([path]):
        module = importlib.import_module(f"tests.tf.{name}")
        for attr in dir(module):
            if attr.endswith('.tf'):
                with open(f"{path}/{attr}", 'r') as file:
                    yield hcl2.load(file)
    