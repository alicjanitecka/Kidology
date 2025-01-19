from ...exceptions import ValidationError, NotFoundError, PermissionError

class ArticleService:


    def __init__(self, repository):
        self.repository = repository

    def _is_admin(self, user):
        """Sprawdzanie uprawnień administratora"""
        return user.is_staff or user.is_superuser

    def _validate_article_data(self, article_data):
        """Walidacja danych artykułu"""
        required_fields = ['title', 'content', 'categories', 'age_groups']

        # Sprawdź czy wszystkie wymagane pola są obecne
        if not all(field in article_data for field in required_fields):
            return False

        # Sprawdź czy tytuł nie jest pusty
        if not article_data['title'].strip():
            return False

        # Sprawdź czy treść nie jest pusta
        if not article_data['content'].strip():
            return False

        # Sprawdź czy wybrano przynajmniej jedną kategorię i grupę wiekową
        if not article_data['categories'] or not article_data['age_groups']:
            return False

        return True
    def get_articles(self, filters=None, user=None):
        """
        Pobieranie artykułów z uwzględnieniem filtrów i uprawnień użytkownika
        """
        if not user or not user.is_authenticated:
            raise PermissionError("Dostęp tylko dla zalogowanych użytkowników")

        return self.repository.get_filtered_articles(filters)

    def search_articles(self, query, search_params):
        """
        Wyszukiwanie artykułów według różnych kryteriów
        """
        search_in_title = search_params.get('search_in_title', True)
        search_in_content = search_params.get('search_in_content', False)
        categories = search_params.get('categories', [])
        age_groups = search_params.get('age_groups', [])

        return self.repository.search_articles(
            query=query,
            search_in_title=search_in_title,
            search_in_content=search_in_content,
            categories=categories,
            age_groups=age_groups
        )

    def create_article(self, article_data, author):
        """
        Tworzenie nowego artykułu z walidacją uprawnień i danych
        """
        if not self._is_admin(author):
            raise PermissionError("Tylko administrator może dodawać artykuły")

        if not self._validate_article_data(article_data):
            raise ValidationError("Nieprawidłowe dane artykułu")

        if not article_data.get('categories') or not article_data.get('age_groups'):
            raise ValidationError("Artykuł musi mieć przypisaną kategorię i grupę wiekową")

        return self.repository.create_article(article_data)

    def update_article(self, article_id, article_data, author):
        """
        Aktualizacja artykułu z walidacją uprawnień
        """
        if not self._is_admin(author):
            raise PermissionError("Tylko administrator może edytować artykuły")

        article = self.repository.get_by_id(article_id)
        if not article:
            raise NotFoundError("Artykuł nie istnieje")

        if not self._validate_article_data(article_data):
            raise ValidationError("Nieprawidłowe dane artykułu")

        return self.repository.update_article(article_id, article_data)

    def delete_article(self, article_id, author):
        """
        Usuwanie artykułu z walidacją uprawnień
        """
        if not self._is_admin(author):
            raise PermissionError("Tylko administrator może usuwać artykuły")

        article = self.repository.get_by_id(article_id)
        if not article:
            raise NotFoundError("Artykuł nie istnieje")

        self.repository.delete_article(article_id)

    def _is_admin(self, user):
        """
        Sprawdzanie czy użytkownik jest administratorem
        """
        return user.is_staff or user.is_superuser

    def _validate_article_data(self, article_data):
        """
        Walidacja danych artykułu
        """
        required_fields = ['title', 'content', 'categories', 'age_groups']
        return all(field in article_data for field in required_fields)
