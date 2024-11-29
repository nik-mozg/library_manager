import unittest
from unittest.mock import patch

from library_manager.manager import get_search_query, get_status_input, validate_year


class TestManagerFunctions(unittest.TestCase):
    """Тесты для функций в менеджере библиотеки."""

    @patch("builtins.input", return_value="Book")
    def test_get_search_query_valid(self, mock_input) -> None:
        """Тест на правильный ввод для поиска.

        В данном тесте проверяется, что функция `get_search_query()`
        правильно обрабатывает
        ввод пользователя и возвращает строку для поиска.

        :param mock_input: Мок для ввода пользователя.
        :return: None
        """
        query: str = get_search_query()
        self.assertEqual(query, "Book")
        mock_input.assert_called_once_with(
            "Название, автор или год для поиска содержит (минимум 2 символа): "
        )

    @patch("builtins.input", side_effect=["2100", "2000"])
    def test_validate_year_invalid_too_large(self, mock_input) -> None:
        """Тест на неверный год (больше 2030).

        Этот тест проверяет, что функция `validate_year()` правильно возвращает год,
        если первый ввод невалидный, а второй — корректный.

        :param mock_input: Мок для ввода пользователя.
        :return: None
        """
        year: int = validate_year()
        self.assertEqual(year, 2000)

    @patch("builtins.input", side_effect=["0", "2"])
    def test_get_status_input_valid(self, mock_input) -> None:
        """Тест на корректный ввод статуса.

        В данном тесте проверяется, что функция `get_status_input()` правильно
        обрабатывает некорректный ввод и затем возвращает правильный статус.

        :param mock_input: Мок для ввода пользователя.
        :return: None
        """
        status: str = get_status_input()
        self.assertEqual(status, "выдана")


if __name__ == "__main__":
    unittest.main()
