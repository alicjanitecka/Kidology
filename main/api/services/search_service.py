from ..repositories.article_repository import ArticleRepository
from ...exceptions import ValidationError

class SearchService:
    def __init__(self, repository: ArticleRepository):
        self.repository = repository

    def search_articles(self, search_params):

        if not search_params:
            return self.repository.get_all()

        query = search_params.get('search_query')
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

    def validate_search_params(self, params):

        if not isinstance(params.get('search_in_title', True), bool):
            raise Va
