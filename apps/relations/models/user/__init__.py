from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship, BooleanProperty, DateTimeProperty, \
    EmailProperty


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
    friends = Relationship('apps.relations.models.user.User', 'FRIENDS')
    posts = RelationshipTo('apps.relations.models.posts.Posts', 'POSTS')
    likes = Relationship('apps.relations.models.posts.Posts', 'LIKES')
    page_follows = RelationshipTo('apps.relations.models.pages.Page', 'FOLLOWS_PAGE')
