from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship, BooleanProperty, DateTimeProperty, \
    EmailProperty
from apps.relations.models.pages import Page
from apps.relations.models.posts import Posts


class User(StructuredNode):
    __label__ = 'USER'

    uuid = StringProperty(unique_index=True)
    email = EmailProperty(unique_index=True)
    first_name = StringProperty()
    last_name = StringProperty()
    is_active = BooleanProperty(default=True)
    is_staff = BooleanProperty(default=False)
    is_superuser = BooleanProperty(default=False)
    date_joined = DateTimeProperty(default_now=True)
    friends = Relationship('User', 'FRIENDS')
    posts = RelationshipTo(Posts, 'POSTS')
    likes = Relationship(Posts, 'LIKES')
    page_follows = RelationshipTo(Page, 'FOLLOWS_PAGE')
