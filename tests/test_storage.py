import json
import os
from typing import List  # noqa: UP035
import unittest
from unittest.mock import mock_open, patch

from library_manager.book import Book
from library_manager.storage import load_books, save_books


class TestStorage(unittest.TestCase):
    """Тесты для загрузки и сохранения книг в файл."""

    def setUp(self) -> None:
        """Настройка тестов, создаем экземпляры книг и тестовый файл.

        :return: None
        """
        self.books: List[Book] = [
            Book("Book One", "Author One", 2000),
            Book("Book Two", "Author Two", 2010),
        ]
        self.storage_file: str = "test_books.json"

    def test_load_books_file_not_found(self) -> None:
        """Тест на случай, когда файл не найден.

        :return: None
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            books = load_books(self.storage_file)
            self.assertEqual(books, [])

    def test_load_books_json_decode_error(self) -> None:
        """Тест на ошибку декодирования JSON.

        :return: None
        """
        with patch("builtins.open", mock_open(read_data="invalid json")):
            books = load_books(self.storage_file)
            self.assertEqual(books, [])

    def test_load_books_success(self) -> None:
        """Тест на успешную загрузку книг из файла.

        :return: None
        """
        book_data: str = json.dumps(
            [
                {
                    "id": str(book.id),
                    "title": book.title,
                    "author": book.author,
                    "year": book.year,
                    "status": book.status,
                }
                for book in self.books
            ],
            ensure_ascii=False,
            indent=4,
        )

        with patch("builtins.open", mock_open(read_data=book_data)):
            books = load_books(self.storage_file)
            self.assertEqual(len(books), 2)
            self.assertEqual(books[0].title, "Book One")
            self.assertEqual(books[1].title, "Book Two")

    def test_save_books(self) -> None:
        """Тест на успешное сохранение книг в файл.

        :return: None
        """
        with patch("builtins.open", mock_open()) as mock_file:
            save_books(self.books, self.storage_file)
            mock_file.assert_called_once_with(self.storage_file, "w", encoding="utf-8")
            write_calls = mock_file().write.call_count
            self.assertGreater(
                write_calls, 0, "Функция write не была вызвана или вызвана 0 раз."
            )

    def test_save_books_exception(self) -> None:
        """Тест на ошибку при сохранении данных в файл.

        :return: None
        """
        with patch("builtins.open", side_effect=Exception("File write error")):
            with self.assertRaises(Exception) as context:
                save_books(self.books, self.storage_file)

            self.assertTrue("File write error" in str(context.exception))

    def tearDown(self) -> None:
        """Очистка после тестов (удаление тестового файла).

        :return: None
        """
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)


if __name__ == "__main__":
    unittest.main()
