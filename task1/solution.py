def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        # Проверка позиционных аргументов
        for arg_name, arg_value in zip(annotations.keys(), args):
            expected_type = annotations[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                                f"но получил {type(arg_value).__name__}.")

        # Проверка именованных аргументов
        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(f"Аргумент '{arg_name}' должен быть типа {expected_type.__name__}, "
                                    f"но получил {type(arg_value).__name__}.")

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
try:
    print(sum_two(1, 2.4))  # >>> TypeError
except TypeError as e:
    print(e)

# Проверка именованного аргумента
try:
    print(sum_two(a=1, b=2.4))  # >>> TypeError
except TypeError as e:
    print(e)