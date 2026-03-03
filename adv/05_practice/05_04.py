from functools import wraps

command_registry = {}
def registry(func):
    command_registry[f"{func.__name__}"] = func

def run_command(func_name):
    return command_registry[f"{func_name}"]

@registry
def func(a, b):
    return a+b

# def func(a, b):
#   return a+b
#
#func = registry(func)

print(run_command("func")(1, 2))