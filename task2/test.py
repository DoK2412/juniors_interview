import unittest
from unittest.mock import patch, Mock
import requests
from juniors_interview.task2.solution import fetch_html, process_page, get_next_url, animals_count

class TestAnimalCount(unittest.TestCase):

    @patch('juniors_interview.task2.solution.requests.get')
    def test_fetch_html_success(self, mock_get):
        # Мокируем успешный ответ
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><body><p>Animal</p></body></html>'
        mock_get.return_value = mock_response

        result = fetch_html("http://mockurl.com")
        self.assertEqual(result, b'<html><body><p>Animal</p></body></html>')
        mock_get.assert_called_once_with("http://mockurl.com")

    @patch('juniors_interview.task2.solution.requests.get')
    def test_fetch_html_failure(self, mock_get):
        # Мокируем сетевую ошибку
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = fetch_html("http://mockurl.com")
        self.assertIsNone(result)

    def test_process_page(self):
        html_content = b'<html><body><p>Animal 1</p><p>Animal 2</p></body></html>'
        result = process_page(html_content)
        # Предполагаем, что функция process_page возвращает количество найденных животных
        self.assertEqual(result, 2)  # Здесь нужно заменить на ваше реальное ожидаемое значение

    def test_get_next_url(self):
        current_url = "http://mockurl.com/page=1"
        result = get_next_url(current_url)
        # Проверяем, как функция генерирует следующий URL
        self.assertEqual(result, "http://mockurl.com/page=2")  # Убедитесь, что предполагаемый URL верный

    @patch('juniors_interview.task2.solution.fetch_html')
    @patch('juniors_interview.task2.solution.process_page')
    def test_animals_count(self, mock_process_page, mock_fetch_html):
        mock_fetch_html.return_value = b'<html><body><p>Animal</p></body></html>'
        mock_process_page.return_value = 1

        result = animals_count("http://mockurl.com")
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()