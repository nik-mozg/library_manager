import uuid
from typing import Optional


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        status: str = "в наличии",
        id: Optional[str] = None,
    ) -> None:
        """Инициализирует новый объект книги.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги, по умолчанию 'в наличии'.
        Возможные значения: 'в наличии', 'выдана'.
        :param id: Уникальный идентификатор книги.
        Если не передан, генерируется автоматически.
        """
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self) -> str:
        """Возвращает строковое представление книги.

        :return: Строка, содержащая информацию о книге (ID, название,
        автор, год и статус).
        """
        return (
            f"ID: {self.id} | "
            f"Title: {self.title} | "
            f"Author: {self.author} | "
            f"Year: {self.year} | "
            f"Status: {self.status}"
        )

    def update_status(self, new_status: str) -> None:
        """Обновляет статус книги.

        Проверяет, что новый статус является допустимым значением.

        :param new_status: Новый статус книги ('в наличии' или 'выдана').
        :raises ValueError: Если новый статус не является 'в наличии' или 'выдана'.
        """
        if new_status not in ["в наличии", "выдана"]:
            raise ValueError("Статус может быть только 'в наличии' или 'выдана'.")
        self.status = new_status
