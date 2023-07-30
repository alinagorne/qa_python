import pytest
from main import BooksCollector

# Класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# Обязательно указывать префикс Test
class TestBooksCollector:

    # Пример теста:
    # Обязательно указывать префикс test_
    # Дальше идет название метода, который тестируем - test_add_new_book_add_two_books
    def test_add_new_book_add_two_books(self):
        # Создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # Добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # Проверяем, что добавилось именно две
        # Словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # Напиши свои тесты ниже
    # Чтобы тесты были независимыми, в каждом из них создавай отдельный экземпляр класса BooksCollector()

    # Тестовые данные для параметризации тестов
    test_books = [
        ("Book 1", "Фантастика"),
        ("Book 2", "Ужасы"),
        ("Book 3", "Детективы"),
        ("Book 4", "Мультфильмы"),
        ("Book 5", "Комедии"),
        ("Book 6", "Фэнтези"),  # Жанр, отсутствующий в списке genre
    ]

    test_favorites = ["Book 1", "Book 3"]

    # Фикстура, создающая новый экземпляр BooksCollector перед каждым тестом
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # Тесты для метода add_new_book
    @pytest.mark.parametrize("name", [book[0] for book in test_books])
    def test_add_new_book(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.books_genre

    def test_add_new_book_invalid_name(self, collector):
        # Попытка добавить книгу с недопустимым названием (символов > 40)
        invalid_name = "A" * 41
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.books_genre

    # Тесты для метода set_book_genre
    @pytest.mark.parametrize("name, genre", test_books)
    def test_set_book_genre(self, collector, name, genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    def test_set_book_genre_invalid_genre(self, collector):
        # Попытка установить жанр, который отсутствует в списке genre
        name, invalid_genre = "Book 7", "Сказки"
        collector.add_new_book(name)
        collector.set_book_genre(name, invalid_genre)
        assert collector.get_book_genre(name) != invalid_genre

    # Тесты для метода get_books_with_specific_genre
    def test_get_books_with_specific_genre(self, collector):
        for name, genre in test_books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        specific_genre = "Фантастика"
        books_with_specific_genre = collector.get_books_with_specific_genre(specific_genre)
        assert all(collector.get_book_genre(book) == specific_genre for book in books_with_specific_genre)

    # Тесты для метода get_books_for_children
    def test_get_books_for_children(self, collector):
        for name, genre in test_books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        books_for_children = collector.get_books_for_children()
        assert all(collector.get_book_genre(book) not in collector.genre_age_rating for book in books_for_children)

    # Тесты для методов add_book_in_favorites и delete_book_from_favorites
    @pytest.mark.parametrize("name", test_favorites)
    def test_add_and_delete_book_from_favorites(self, collector, name):
        collector.add_new_book(name)
        collector.set_book_genre(name, "Фантастика")  # Добавим валидный жанр, чтобы можно было добавить в избранное
        collector.add_book_in_favorites(name)
        assert name in collector.favorites

        collector.delete_book_from_favorites(name)
        assert name not in collector.favorites

    def test_add_book_in_favorites_invalid_book(self, collector):
        invalid_book = "Invalid Book"
        collector.add_new_book(invalid_book)
        collector.add_book_in_favorites(invalid_book)
        assert invalid_book not in collector.favorites

    # Тест для метода get_list_of_favorites_books
    def test_get_list_of_favorites_books(self, collector):
        for name, genre in test_books:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        for name in test_favorites:
            collector.add_book_in_favorites(name)

        favorites_list = collector.get_list_of_favorites_books()
        assert all(book in favorites_list for book in test_favorites)

    # Тест на получение жанра для несуществующей книги
    def test_get_book_genre_not_exists(self, collector):
        name = "Non-existent Book"
        assert collector.get_book_genre(name) is None

    # Тест на добавление книги в избранное, которая отсутствует в списке жанров
    def test_add_book_in_favorites_genre_not_exists(self, collector):
        name = "Book 10"
        collector.add_new