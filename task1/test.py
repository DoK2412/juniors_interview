import unittest
from task1.solution import sum_two


class TestStrictDecorator(unittest.TestCase):

    def test_valid_types(self):
        # тестируем с валидными аргументами
        self.assertEqual(sum_two(1, 2), 3)
        self.assertEqual(sum_two(10, 20), 30)

    def test_invalid_type_first_arg(self):
        # тестируем с невалидным первым аргументом
        with self.assertRaises(TypeError) as context:
            sum_two(1.5, 2)
        self.assertEqual(str(context.exception), "Argument 'a' must be of type int, but got float.")

    def test_invalid_type_second_arg(self):
        # тестируем с невалидным вторым аргументом
        with self.assertRaises(TypeError) as context:
            sum_two(1, "2")
        self.assertEqual(str(context.exception), "Argument 'b' must be of type int, but got str.")

    def test_invalid_args_count(self):
        # тестируем на неправильное количество аргументов
        with self.assertRaises(TypeError):
            sum_two(1)

        with self.assertRaises(TypeError):
            sum_two(1, 2, 3)

    def test_invalid_arg_types(self):
        # тестируем другие типы данных
        with self.assertRaises(TypeError) as context:
            sum_two([], 2)  # передаем список вместо int
        self.assertEqual(str(context.exception), "Argument 'a' must be of type int, but got list.")

        with self.assertRaises(TypeError) as context:
            sum_two(2, {})  # передаем словарь вместо int
        self.assertEqual(str(context.exception), "Argument 'b' must be of type int, but got dict.")

if __name__ == '__main__':
    unittest.main()