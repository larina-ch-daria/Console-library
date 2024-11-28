import unittest
from unittest.mock import patch, mock_open
from main import load_books, save_books, add_book, delete_book, search_books, change_status

class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print(f"{test._testMethodName} прошёл успешно.")
    def addFailure(self, test, err):
        print(f"\n{test._testMethodName} завершился с ошибкой:\n{err[0].__name__}: {err[1]}\n")

    def addError(self, test, err):
        print(f"\n{test._testMethodName} завершился с ошибкой: {err[0].__name__}: {err[1]}\n")

class CustomTestRunner(unittest.TextTestRunner):
    resultclass = CustomTestResult

class TestBookFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_books = [
            {'id': 1, 'title': '1984', 'author': 'George Orwell', 'year': '1949', 'status': 'в наличии'},
            {'id': 2, 'title': 'Brave New World', 'author': 'Aldous Huxley', 'year': '1932', 'status': 'в наличии'}
        ]

    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": 1, "title": "1984", "author": "George Orwell", "year": "1949", "status": "в наличии"}]')
    @patch('os.path.exists', return_value=True)
    def test_load_books_success(self, mock_exists, mock_file):
        books = load_books('mock_file_path')
        expected_books = [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'year': '1949', 'status': 'в наличии'}]
        self.assertEqual(books, expected_books)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_books(self, mock_json_dump, mock_file):
        save_books('mock_file_path', self.mock_books)
        mock_file.assert_called_once_with('mock_file_path', 'w')
        mock_json_dump.assert_called_once_with(self.mock_books, mock_file(), indent=4)

    @patch('builtins.print')
    @patch('main.load_books')
    @patch('main.save_books')
    def test_add_new_book(self, mock_save_books, mock_load_books, mock_print):
        mock_load_books.return_value = []
        add_book('mock_file_path', '1984', 'George Orwell', '1949')
        mock_save_books.assert_called_once()
        self.assertEqual(mock_save_books.call_args[0][1], [self.mock_books[0]])
        mock_print.assert_called_once_with("\nКнига '1984' автора George Orwell добавлена в библиотеку. ID книги: 1.")

    @patch('builtins.print')
    @patch('main.load_books')
    @patch('main.save_books')
    def test_add_book_already_exists(self, mock_save_books, mock_load_books, mock_print):
        mock_load_books.return_value = [self.mock_books[0]]
        add_book('mock_file_path', '1984', 'George Orwell', '1949')
        mock_save_books.assert_not_called()
        mock_print.assert_called_once_with("Книга '1984' автора George Orwell уже есть в библиотеке. ID книги: 1.")

    @patch('builtins.print')
    @patch('main.load_books')
    @patch('main.save_books')
    @patch('builtins.input', side_effect=['да'])
    def test_delete_existing_book(self, mock_input, mock_save_books, mock_load_books, mock_print):
        mock_load_books.return_value = [self.mock_books[0]]
        delete_book('mock_file_path', 1)
        mock_save_books.assert_called_once()
        self.assertEqual(mock_save_books.call_args[0][1], [])
        mock_print.assert_called_once_with("Книга '1984' удалена из библиотеки.")

    @patch('builtins.print')
    @patch('main.load_books')
    @patch('main.save_books')
    def test_delete_non_existing_book(self, mock_save_books, mock_load_books, mock_print):
        mock_load_books.return_value = [self.mock_books[0]]
        delete_book('mock_file_path', 2)
        mock_save_books.assert_not_called()
        mock_print.assert_called_once_with("Книга с ID 2 не найдена.")

    @patch('main.load_books')
    def test_search_by_title(self, mock_load_books):
        mock_load_books.return_value = self.mock_books
        results = search_books('mock_file_path', '1984')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], '1984')

    @patch('main.load_books')
    def test_search_no_results(self, mock_load_books):
        mock_load_books.return_value = self.mock_books
        results = search_books('mock_file_path', 'Nonexistent Book')
        self.assertEqual(len(results), 0)

    @patch('main.load_books')
    @patch('main.save_books')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['нет'])
    def test_change_status_not_wanted(self, mock_input, mock_print, mock_save_books, mock_load_books):
        mock_load_books.return_value = self.mock_books
        change_status('mock_file_path', 1)
        mock_save_books.assert_not_called()
        mock_print.assert_any_call("\nТекущий статус книги '1984': в наличии.")
        mock_input.assert_called_with("Хотите его изменить? (да/нет): ")
        mock_print.assert_any_call("Статус книги '1984' остался прежним: в наличии.")

    @patch('main.load_books')
    @patch('main.save_books')
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['да'])
    def test_change_status_wanted(self, mock_input, mock_print, mock_save_books, mock_load_books):
        mock_load_books.return_value = self.mock_books
        change_status('mock_file_path', 1)
        mock_save_books.assert_called()
        mock_print.assert_any_call("\nТекущий статус книги '1984': в наличии.")
        mock_input.assert_called_with("Хотите его изменить? (да/нет): ")
        mock_print.assert_any_call("Статус книги '1984' с ID 1 изменён на 'выдана'.")

if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner(), verbosity=2)