import json
import os
from typing import List, Dict, Optional

Book = Dict[str, Optional[str]]

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

def add_book(file_path: str, title: str, author: str, year: str) -> None:
    '''
    Функция получает название, автора и год книги.
    Проверяет библиотеку на наличие дубляжа и добавляет, если книги ещё нет.
    '''
    books = load_books(file_path)

    existing_book = next((book for book in books if book['title'] == title and book['author'] == author), None)   
    if existing_book:
        print(f"Книга '{title}' автора {author} уже есть в библиотеке. ID книги: {existing_book['id']}.")
        return
    
    book_id = books[-1]['id']+1 if books else 1
    new_book: Book = {
        'id': book_id,
        'title': title,
        'author': author,
        'year': year,
        'status': 'в наличии'
    }
    books.append(new_book)
    save_books(file_path, books)  # Передаем file_path
    print(f"\nКнига '{title}' автора {author} добавлена в библиотеку. ID книги: {book_id}.")

def delete_book(file_path: str, book_id: int) -> None:
    '''
    Функция получает ID книги для удаления.
    Удаляет книгу из библиотеки.
    '''
    books = load_books(file_path)
    if not any(book['id'] == book_id for book in books):
        print(f"Книга с ID {book_id} не найдена.")
        return
    
    requested_book = [book for book in books if (book_id == book['id'])]
    if requested_book:
        decision = input(f"\nПо этому ID найдена книга '{requested_book[0]['title']}'.\nВы хотите её удалить? (да/нет): ").lower()
        if decision == 'да':
            books = [book for book in books if book['id'] != book_id]
            save_books(file_path, books)
            print(f"Книга '{requested_book[0]['title']}' удалена из библиотеки.")
        else:
            print(f"Книга '{requested_book[0]['title']}' осталась в библиотеке.")
        return

def search_books(file_path: str, query: str) -> List[Book]:
    '''Функция ищет книгу в файле библиотеки.'''
    books = load_books(file_path)
    results = [book for book in books if (query in book['title'] or query in book['author'] or query in str(book['year']))]
    return results

def display_books(file_path: str) -> None:
    '''Функция отображает все книги из файла библиотеки.'''
    books = load_books(file_path)
    if not books:
        print("Нет книг в библиотеке.")
        return
    else:
        print(f"\nПолный каталог библиотеки:")
        for book in books:
            print(f"{book['id']}. '{book['title']}'\nАвтор: {book['author']}\nГод написания:{book['year']}\nТекущий статус: {book['status']}")

def change_status(file_path: str, book_id: int) -> None:
    '''
    Функция запрашивает ID книги, которой надо поменять статус ("в наличии"/"выдана").
    Пользователь может отказаться менять статус и вернуться к меню.
    '''
    books = load_books(file_path)
    for book in books:
        if book['id'] == book_id:
            print(f'''\nТекущий статус книги '{book["title"]}': {book["status"]}.''')
            new_status = input("Хотите его изменить? (да/нет): ").lower()

            if new_status == 'да':
                book['status'] = 'выдана' if book['status'] == 'в наличии' else 'в наличии'
                save_books(file_path, books)
                print(f"Статус книги '{book['title']}' с ID {book_id} изменён на '{book['status']}'.")            
            else:
                print(f"Статус книги '{book['title']}' остался прежним: {book['status']}.")
            return
    print(f"Книга с ID {book_id} не найдена.")

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

