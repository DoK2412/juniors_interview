import requests
from bs4 import BeautifulSoup
import csv

# URL для стартовой страницы категории "Животные по алфавиту"
base_url = "https://ru.wikipedia.org"
start_url = f"{base_url}/wiki/Категория:Животные_по_алфавиту"

# Словарь для хранения количества животных на каждую букву
animals_count = {}


def process_page(url):
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Получаем все элементы списка на странице
        animal_list_items = soup.select('div#mw-pages div.mw-category a')
        for item in animal_list_items:
            animal_name = item.get_text()
            first_letter = animal_name[0].upper()
            if first_letter in animals_count:
                animals_count[first_letter] += 1
            else:
                animals_count[first_letter] = 1
        # Поиск ссылки на следующую страницу
        next_page_link = soup.find('a', href=True, string='Следующая страница')
        # Обновление URL для следующей страницы, или выход из цикла если следующая страница не найдена
        if next_page_link:
            url = base_url + next_page_link['href']
        else:
            url = None


process_page(start_url)

with open('animals_count.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Буква', 'Количество']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for letter, count in sorted(animals_count.items()):
        writer.writerow({'Буква': letter, 'Количество': count})

print("Результаты сохранены в файл animals_count.csv")