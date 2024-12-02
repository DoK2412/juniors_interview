import requests
from bs4 import BeautifulSoup
import csv

# URL для стартовой страницы категории "Животные по алфавиту"
base_url = "https://ru.wikipedia.org"
start_url = f"{base_url}/wiki/Категория:Животные_по_алфавиту"

# Словарь для хранения количества животных на каждую букву
animals_count = {}


def fetch_html(url):
    """Получает HTML содержимое страницы по указанному URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.content
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


def process_page(url):
    """Обрабатывает страницы категорий животных для подсчета количества по буквам."""
    count = 0
    while url:
        print(count)
        count += 1
        html_content = fetch_html(url)
        if html_content is None:
            break

        soup = BeautifulSoup(html_content, 'html.parser')

        # Получаем все элементы списка на странице
        animal_list_items = soup.select('div#mw-pages div.mw-category a')
        for item in animal_list_items:
            animal_name = item.get_text()
            first_letter = animal_name[0].upper()
            animals_count[first_letter] = animals_count.get(first_letter, 0) + 1

        url = get_next_url(soup)


def get_next_url(soup):
    """Возвращает URL следующей страницы, если он существует."""
    next_page_link = soup.find('a', href=True, string='Следующая страница')
    return base_url + next_page_link['href'] if next_page_link else None


process_page(start_url)

with open('animals_count.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Буква', 'Количество']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for letter, count in sorted(animals_count.items()):
        writer.writerow({'Буква': letter, 'Количество': count})

print("Результаты сохранены в файл animals_count.csv")