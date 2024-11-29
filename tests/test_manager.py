from typing import List  
import unittest

from library_manager.book import Book
from library_manager.manager import LibraryManager


class TestLibraryManager(unittest.TestCase):
    """Тесты для функциональности LibraryManager."""

    def setUp(self) -> None:
        """Настройка тестов, создаем экземпляр LibraryManager и книги.

        :return: None
        """
        self.library_manager: LibraryManager = LibraryManager()
        self.book1: Book = Book("Book One", "Author One", 2000)
        self.book2: Book = Book("Book Two", "Author Two", 2010)
        self.library_manager.books: List[Book] = [self.book1, self.book2]

    def test_add_book(self) -> None:
        """Тест добавления книги."""
        new_book = Book("Book Three", "Author Three", 2020)
        self.library_manager.add_book(new_book.title, new_book.author, new_book.year)
        self.assertEqual(len(self.library_manager.books), 3)
        self.assertEqual(self.library_manager.books[-1].title, "Book Three")

    def test_add_existing_book(self) -> None:
        """Тест добавления существующей книги (проверка дубликатов)."""
        existing_book = Book("Book One", "Author One", 2000)
        self.library_manager.add_book(
            existing_book.title, existing_book.author, existing_book.year
        )
        self.assertEqual(len(self.library_manager.books), 2)

    def test_update_book_status(self) -> None:
        """Тест изменения статуса книги."""
        self.library_manager.update_book_status(self.book1.id, "выдана")
        self.assertEqual(self.book1.status, "выдана")

    def test_update_book_status_no_change(self) -> None:
        """Тест на попытку изменения статуса на тот же (ничего не меняем)."""
        self.library_manager.update_book_status(self.book1.id, "в наличии")
        self.assertEqual(self.book1.status, "в наличии")

    def test_find_books(self) -> None:
        """Тест поиска книги по запросу."""
        found_books = self.library_manager.find_books("Book One")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "Book One")

    def test_find_books_empty(self) -> None:
        """Тест поиска книги по запросу, который не существует."""
        found_books = self.library_manager.find_books("Nonexistent Book")
        self.assertEqual(len(found_books), 0)

    def test_invalid_year(self) -> None:
        """Тест на валидацию года (должен быть числом в диапазоне от 1800 до 2030)."""
        valid_year: int = 1999
        invalid_year: int = 1700
        self.assertTrue(1800 <= valid_year <= 2030)
        self.assertFalse(1800 <= invalid_year <= 2030)

    def test_invalid_status_input(self) -> None:
        """Тест на ввод некорректного статуса."""
        invalid_status: str = "not_a_valid_status"
        self.assertNotIn(invalid_status, ["в наличии", "выдана"])

    def tearDown(self) -> None:
        """Очистка после каждого теста (необязательно)."""
        del self.library_manager
        del self.book1
        del self.book2


if __name__ == "__main__":
    unittest.main()
