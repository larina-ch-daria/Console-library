import json
import os
from typing import List, Dict, Optional

Book = Dict[str, Optional[str]]

# Константы для статусов книг
STATUS_AVAILABLE = 'в наличии'
STATUS_CHECKED_OUT = 'выдана'

def load_books(file_path: str) -> List[Book]:
    '''Функция загружает книги из файла библиотеки.'''
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        return json.load(file)

def save_books(file_path: str, books: List[Book]) -> None:
    '''Функция сохраняет книги в файл библиотеки.'''
    with open(file_path, 'w') as file:
        json.dump(books, file, indent=4)

def find_book_by_title_and_author(books: List[Book], title: str, author: str) -> Optional[Book]:
    '''Функция находит книгу по названию и автору.'''
    return next((book for book in books if book['title'] == title and book['author'] == author), None)

def add_book(file_path: str, title: str, author: str, year: str) -> None:
    '''Добавляет книгу в библиотеку, если она еще не существует.'''
    books = load_books(file_path)
    existing_book = find_book_by_title_and_author(books, title, author)

    if existing_book:
        print(f"Книга '{title}' автора {author} уже есть в библиотеке. ID книги: {existing_book['id']}.")
        return
    
    book_id = books[-1]['id'] + 1 if books else 1
    new_book: Book = {
        'id': book_id,
        'title': title,
        'author': author,
        'year': year,
        'status': STATUS_AVAILABLE
    }
    books.append(new_book)
    save_books(file_path, books)
    print(f"\nКнига '{title}' автора {author} добавлена в библиотеку. ID книги: {book_id}.")

def delete_book(file_path: str, book_id: int) -> None:
    '''Удаляет книгу из библиотеки по ID.'''
    books = load_books(file_path)
    requested_book = next((book for book in books if book['id'] == book_id), None)
    
    if not requested_book:
        print(f"Книга с ID {book_id} не найдена.")
        return
    
    decision = input(f"\nПо этому ID найдена книга '{requested_book['title']}'. Вы хотите её удалить? (да/нет): ").lower()
    if decision == 'да':
        books.remove(requested_book)
        save_books(file_path, books)
        print(f"Книга '{requested_book['title']}' удалена из библиотеки.")
    else:
        print(f"Книга '{requested_book['title']}' осталась в библиотеке.")

def search_books(file_path: str, query: str) -> List[Book]:
    '''Ищет книги по запросу.'''
    books = load_books(file_path)
    return [book for book in books if (query in book['title'] or query in book['author'] or query in str(book['year']))]

def display_books(file_path: str) -> None:
    '''Отображает все книги в библиотеке.'''
    books = load_books(file_path)
    if not books:
        print("Нет книг в библиотеке.")
        return
    
    print(f"\nПолный каталог библиотеки:")
    for book in books:
        print(f"{book['id']}. '{book['title']}'\nАвтор: {book['author']}\nГод написания: {book['year']}\nТекущий статус: {book['status']}")

def change_status(file_path: str, book_id: int) -> None:
    '''Изменяет статус книги по ID.'''
    books = load_books(file_path)
    book = next((book for book in books if book['id'] == book_id), None)

    if not book:
        print(f"Книга с ID {book_id} не найдена.")
        return

    print(f'''\nТекущий статус книги '{book["title"]}': {book["status"]}.''')
    new_status = input("Хотите его изменить? (да/нет): ").lower()

    if new_status == 'да':
        book['status'] = STATUS_CHECKED_OUT if book['status'] == STATUS_AVAILABLE else STATUS_AVAILABLE
        save_books(file_path, books)
        print(f"Статус книги '{book['title']}' с ID {book_id} изменён на '{book['status']}'.")            
    else:
        print(f"Статус книги '{book['title']}' остался прежним: {book['status']}.")

def main(file_path: str) -> None:
    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("\nВведите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            add_book(file_path, title, author, year)
        elif choice == '2':
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                delete_book(file_path, book_id) 
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите числовой ID.")
        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            results = search_books(file_path, query)
            if results:
                print(f"\nПо вашему запросу нашлись следующие книги:")
                for book in results:
                    print(f"{book['id']}. '{book['title']}'\nАвтор: {book['author']}\nГод написания: {book['year']}\nТекущий статус: {book['status']}")
            else:
                print("\nКниги не найдены.")
        elif choice == '4':
            display_books(file_path)
        elif choice == '5':
            try:
                book_id = int(input("\nВведите ID книги для изменения статуса: "))
                change_status(file_path, book_id)
            except ValueError:
                print("\nНекорректный ввод. Пожалуйста, введите числовой ID.")
        elif choice == '0':
            break
        else:
            print("\nНекорректный ввод. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    file_path = 'database.json'
    main(file_path)

