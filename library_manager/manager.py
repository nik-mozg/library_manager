import re
from typing import List, Optional

from library_manager.book import Book
from library_manager.storage import load_books, save_books


def get_search_query() -> str:
    """Запрашивает ввод пользователя для поиска с дополнительной проверкой.

    Функция запрашивает у пользователя ввод для поиска книги по названию, автору или году.
    Запрещает вводить строку меньше 2 символов или строку, состоящую только
    из пробелов и знаков препинания.

    :return: Строка с запросом пользователя.
    """
    while True:
        query = input(
            "Название, автор или год для поиска содержит (минимум 2 символа): "
        ).strip()
        if len(query) < 2:
            print("Ошибка: Запрос должен содержать хотя бы 2 символа. Повторите!")
        elif re.match(r"^[\W\s]+$", query):
            print(
                "Ошибка: Запрос не может состоять только из пробелов или "
                + "знаков препинания. Повторите! "
            )

        else:
            return query


def validate_year() -> Optional[int]:
    """Проверка года: он должен быть целым числом от 1800 до 2030.

    Повторный ввод при ошибке.
    Функция запрашивает у пользователя ввод года и проверяет, что год
    находится в допустимом диапазоне.
    При неверном вводе запрашивает ввод снова.
    :return: Целое число, год издания.
    """
    while True:
        year = input("Введите год издания: ")
        try:
            year = int(year)
            if 1800 <= year <= 2030:
                return year
            else:
                print("Ошибка: Год должен быть в диапазоне от 1800 до 2030.")
        except ValueError:
            print("Ошибка: Введите целое число для года.")


def get_status_input() -> str:
    """Запрашивает ввод статуса книги и проверяет, чтобы это было '1' или '2'.

    Функция запрашивает у пользователя ввод статуса и проверяет, что он
    соответствует одному из двух возможных значений.
    В случае некорректного ввода запрашивает новый ввод.

    :return: Строка, содержащая статус книги: 'в наличии' или 'выдана'.
    """
    while True:
        status_input = input(
            "Введите новый статус (1 - 'в наличии', 2 - 'выдана'): "
        ).strip()
        if status_input == "1":
            return "в наличии"
        elif status_input == "2":
            return "выдана"
        else:
            print("Ошибка: Введите '1' для 'в наличии' или '2' для 'выдана'.")


class LibraryManager:
    def __init__(self, storage_file: str = "data/books.json") -> None:
        """Инициализация менеджера библиотеки.

        Загружает книги из указанного файла.

        :param storage_file: Путь к файлу для загрузки и сохранения данных.
        """
        self.storage_file = storage_file
        self.books: List[Book] = load_books(self.storage_file)

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавление новой книги в библиотеку.

        Функция проверяет наличие книги с таким же названием и автором в библиотеке.
        Если такая книга уже есть, она не добавляется.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        """
        if any(book.title == title and book.author == author for book in self.books):
            print(
                f"Ошибка: Книга '{title}' авторства '{author}' уже есть в библиотеке."
            )
            return

        new_book = Book(title, author, year)
        self.books.append(new_book)
        save_books(self.books, self.storage_file)
        print(f"Книга '{title}' добавлена в библиотеку.")

    def remove_book(self, book_id: str) -> None:
        """Удаление книги по ID.

        Функция удаляет книгу по указанному ID, если она найдена.

        :param book_id: Идентификатор книги.
        """
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            save_books(self.books, self.storage_file)
            print(f"Книга с ID {book_id} была удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_books(self, query: str) -> List[Book]:
        """Поиск книг по названию, автору или году.

        Функция ищет книги, соответствующие запросу в названии, авторе или годе.

        :param query: Строка для поиска.
        :return: Список книг, соответствующих запросу.
        """
        results = [
            book
            for book in self.books
            if query.lower() in book.title.lower()
            or query.lower() in book.author.lower()
            or query in str(book.year)
        ]
        return results

    def display_books(self) -> None:
        """Отображение всех книг.

        Функция выводит информацию о всех книгах в библиотеке.

        Если библиотека пуста, выводится сообщение о том, что книги не найдены.
        """
        if not self.books:
            print("Библиотека пуста.")
        for book in self.books:
            print(book)

    def update_book_status(self, book_id: str, new_status: str) -> None:
        """Изменение статуса книги по ID.

        Функция обновляет статус книги по указанному ID, если книга найдена.

        :param book_id: Идентификатор книги.
        :param new_status: Новый статус книги ('в наличии' или 'выдана').
        """
        book_to_update = next((book for book in self.books if book.id == book_id), None)
        if book_to_update:
            try:
                book_to_update.update_status(new_status)
                save_books(self.books, self.storage_file)
                print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
            except ValueError as e:
                print(f"Ошибка: {e}")
        else:
            print(f"Книга с ID {book_id} не найдена.")
