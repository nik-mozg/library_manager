import json

from library_manager.book import Book


def load_books(storage_file: str) -> list[Book]:
    """
    Загружает список книг из файла.

    Эта функция открывает указанный файл и пытается загрузить данные книг. Если файл
    не найден или данные повреждены, возвращается пустой список. Если данные успешно
    загружены, они преобразуются в список объектов `Book`.

    :param storage_file: Путь к файлу, из которого необходимо загрузить книги.
    :return: Список объектов Book, загруженных из файла.
    """
    try:
        with open(storage_file, encoding="utf-8") as file:
            data = json.load(file)
            books = [Book(**book_data) for book_data in data]
            return books
    except FileNotFoundError:
        print(f"Файл '{storage_file}' не найден. Создан новый.")
        return []
    except json.JSONDecodeError:
        print("Ошибка при чтении данных из файла. Возможно, файл поврежден.")
        return []


def save_books(books: list[Book], storage_file: str) -> None:
    """
    Сохраняет список книг в файл.

    Эта функция принимает список объектов `Book` и сохраняет
    их в указанный файл в формате JSON.

    :param books: Список объектов Book, которые необходимо сохранить.
    :param storage_file: Путь к файлу, в который необходимо сохранить данные.
    :return: None
    """
    data = [book.__dict__ for book in books]
    try:
        with open(storage_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл: {e}")
        raise
