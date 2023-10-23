from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship, BooleanProperty, DateTimeProperty


class Page(StructuredNode):
    __label__ = 'PAGE'

    uuid = StringProperty(unique_index=True)
    name = StringProperty()
    description = StringProperty()
    is_active = BooleanProperty(default=True)
    date_joined = DateTimeProperty(default_now=True)
    followers = Relationship('apps.relations.models.user.User', 'FOLLOWS_PAGE')
    posts = RelationshipTo('apps.relations.models.posts.Posts', 'POSTS')
    likes = Relationship('apps.relations.models.posts.Posts', 'LIKES')
