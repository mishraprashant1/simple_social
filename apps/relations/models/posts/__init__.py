from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, BooleanProperty, DateTimeProperty


class Posts(StructuredNode):
    __label__ = 'POST'

    uuid = StringProperty(unique_index=True)
    user = RelationshipFrom('User', 'POSTS')
    page = RelationshipFrom('Page', 'POSTS')
    text_content = StringProperty()
    share_with = StringProperty()
    is_active = BooleanProperty(default=True)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    deleted_at = DateTimeProperty(default_now=True)
    images = RelationshipTo('PostImage', 'HAS_IMAGE')
    tags = RelationshipTo('PostTags', 'HAS_TAG')
    likes = RelationshipTo('User', 'LIKES')
