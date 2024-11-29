import sys

from library_manager.manager import (
    LibraryManager,
    get_search_query,
    get_status_input,
    validate_year,
)


def print_menu() -> None:
    """
    Выводит меню для пользователя.

    Эта функция не принимает аргументы и не возвращает значений. Она просто выводит
    меню с доступными действиями для пользователя.
    """
    print("\nМеню управления библиотекой:")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Поиск книги")
    print("4. Отобразить все книги")
    print("5. Изменить статус книги")
    print("6. Выйти")


def main() -> None:
    """
    Главная функция для работы с пользователем через командную строку.

    Эта функция выполняет цикл, в котором пользователю предоставляется меню для
    выполнения различных операций с книгами. В зависимости от выбора пользователя,
    вызываются соответствующие методы для добавления, удаления, поиска, отображения
    книг и изменения их статуса.
    """
    library_manager = LibraryManager()

    while True:
        print_menu()
        choice = input("Выберите действие (1-6): ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            valid_year = validate_year()
            if valid_year is None:
                continue
            existing_book = next(
                (
                    book
                    for book in library_manager.books
                    if book.title == title and book.author == author
                ),
                None,
            )
            if existing_book:
                print(f"Ошибка: Книга '{title}' авторства '{author}' уже есть в базе.")
            else:
                library_manager.add_book(title, author, valid_year)

        elif choice == "2":
            book_id = input("Введите ID книги, которую хотите удалить: ")
            library_manager.remove_book(book_id)

        elif choice == "3":
            query = get_search_query()
            found_books = library_manager.find_books(query)
            if found_books:
                for book in found_books:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library_manager.display_books()

        elif choice == "5":
            book_id = input("Введите ID книги, статус которой хотите изменить: ")
            book = next(
                (book for book in library_manager.books if book.id == book_id), None
            )

            if book:
                print(f"Информация о книге: {book}")
                new_status = get_status_input()
                if book.status == new_status:
                    print(
                        f"Статус книги '{book.title}' уже установлен как '{new_status}'."
                    )
                else:
                    library_manager.update_book_status(book_id, new_status)
            else:
                print(f"Книга с ID {book_id} не найдена.")

        elif choice == "6":
            print("Выход из программы...")
            sys.exit()

        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 6.")


if __name__ == "__main__":
    main()
