from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship, BooleanProperty, DateTimeProperty


class Page(StructuredNode):
    __label__ = 'PAGE'

    uuid = StringProperty(unique_index=True)
    name = StringProperty()
    description = StringProperty()
    is_active = BooleanProperty(default=True)
    date_joined = DateTimeProperty(default_now=True)
    followers = Relationship('User', 'FOLLOWS_PAGE')
    posts = RelationshipTo('Post', 'POSTS')
    likes = Relationship('Post', 'LIKES')
