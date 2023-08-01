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
        assert name in collector.get_books_genre()

    def test_add_new_book_invalid_name(self, collector):
        # Попытка добавить книгу с недопустимым названием (символов > 40)
        invalid_name = "A" * 41
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.books_genre

    # Тесты для метода set_book_genre
    # Убрала параметризацию и использую только один тест для проверки этого метода
    def test_set_book_genre(self, collector):
        name, genre = test_books[0]
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    def test_set_book_genre_invalid_genre(self, collector):
        # Попытка установить жанр, который отсутствует в списке genre
        name, invalid_genre = "Book 7", "Сказки"
        collector.add_new_book(name)
        collector.set_book_genre(name, invalid_genre)
        assert collector.get_book_genre(name) != invalid_genre

    def test_get_books_with_specific_genre(self, collector):
        # Добавляем две книги с жанром "Фантастика"
        collector.add_new_book("Book 1")
        collector.set_book_genre("Book 1", "Фантастика")
        collector.add_new_book("Book 2")
        collector.set_book_genre("Book 2", "Фантастика")

        # Получаем список книг с жанром "Фантастика"
        books_with_specific_genre = collector.get_books_with_specific_genre("Фантастика")

        # Проверяем, что список содержит ровно две книги, и все они имеют жанр "Фантастика"
        assert len(books_with_specific_genre) == 2 and all(
            collector.get_book_genre(book) == "Фантастика" for book in books_with_specific_genre)

    def test_get_books_for_children_genre(self, collector):
        # Добавляем две книги с жанром "Фантастика"
        collector.add_new_book("Book 1")
        collector.set_book_genre("Book 1", "Фантастика")
        collector.add_new_book("Book 2")
        collector.set_book_genre("Book 2", "Фантастика")

        # Добавляем одну книгу с жанром "Для детей"
        collector.add_new_book("Book 3")
        collector.set_book_genre("Book 3", "Для детей")

        # Получаем список книг с жанром "Для детей"
        books_for_children = collector.get_books_with_specific_genre("Для детей")

        # Проверяем, что в списке книг для детей нет книг с жанрами из genre_age_rating
        assert all(collector.get_book_genre(book) not in collector.genre_age_rating for book in books_for_children)

    # Тест для метода add_book_in_favorites с невалидным названием книги
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