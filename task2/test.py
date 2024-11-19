import unittest
from unittest.mock import patch, Mock
import csv
from task2.solution import process_page

base_url = "https://ru.wikipedia.org"
start_url = f"{base_url}/wiki/Категория:Животные_по_алфавиту"

animals_count = {}


class TestAnimalPageProcessor(unittest.TestCase):

    @patch('requests.get')
    def test_process_page_single_page(self, mock_get):
        html_content = '''
        <div id="mw-pages">
            <div class="mw-category">
                <a href="/wiki/Альфа" title="Альфа">Альфа</a>
                <a href="/wiki/Бета" title="Бета">Бета</a>
                <a href="/wiki/Бетта" title="Бетта">Бетта</a>
                <a href="/wiki/Гамма" title="Гамма">Гамма</a>
            </div>
        </div>
        '''
        mock_get.return_value.content = html_content

        global animals_count
        animals_count = {}

        process_page("mocked_url")

        self.assertEqual(animals_count['А'], 1)
        self.assertEqual(animals_count['Б'], 2)
        self.assertEqual(animals_count['Г'], 1)

    @patch('requests.get')
    def test_process_page_multiple_pages(self, mock_get):
        html_content_page1 = '''
        <div id="mw-pages">
            <div class="mw-category">
                <a href="/wiki/Альфа" title="Альфа">Альфа</a>
                <a href="/wiki/Бета" title="Бета">Бета</a>
            </div>
            <a href="/wiki/NextPage" title="Следующая страница">Следующая страница</a>
        </div>
        '''

        html_content_page2 = '''
        <div id="mw-pages">
            <div class="mw-category">
                <a href="/wiki/Гамма" title="Гамма">Гамма</a>
                <a href="/wiki/Дельта" title="Дельта">Дельта</a>
            </div>
        </div>
        '''

        def side_effect(url):
            if url == 'mocked_url':
                mock_get.return_value.content = html_content_page1
            else:
                mock_get.return_value.content = html_content_page2
            return mock_get.return_value

        mock_get.side_effect = side_effect

        global animals_count
        animals_count = {}

        process_page("mocked_url")

        self.assertEqual(animals_count['А'], 1)
        self.assertEqual(animals_count['Б'], 1)
        self.assertEqual(animals_count['Г'], 1)
        self.assertEqual(animals_count['Д'], 1)

    @patch('builtins.open')
    @patch('csv.DictWriter')
    def test_csv_output(self, mock_dict_writer, mock_open):
        # Simulate CSV writing
        global animals_count
        animals_count = {'А': 2, 'Б': 3, 'В': 1}

        mock_writer = Mock()
        mock_dict_writer.return_value = mock_writer

        csvfile = Mock()
        mock_open.return_value.__enter__.return_value = csvfile

        with open('animals_count.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Буква', 'Количество']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for letter, count in sorted(animals_count.items()):
                writer.writerow({'Буква': letter, 'Количество': count})

        mock_writer.writeheader.assert_called_once()
        self.assertEqual(mock_writer.writerow.call_count, 3)
        mock_writer.writerow.assert_any_call({'Буква': 'А', 'Количество': 2})
        mock_writer.writerow.assert_any_call({'Буква': 'Б', 'Количество': 3})
        mock_writer.writerow.assert_any_call({'Буква': 'В', 'Количество': 1})

if __name__ == '__main__':
    unittest.main()