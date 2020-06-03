from .model import CategoryModel
from database import session_scope


class CategoryGateway:
    def __init__(self):
        self.category = CategoryModel

    def get_all_categories(self):
        with session_scope() as session:
            return session.query(CategoryModel).all()
