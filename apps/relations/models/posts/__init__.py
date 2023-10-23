from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, BooleanProperty, DateTimeProperty


class Posts(StructuredNode):
    __label__ = 'POST'

    uuid = StringProperty(unique_index=True)
    text_content = StringProperty()
    share_with = StringProperty()
    is_active = BooleanProperty(default=True)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    deleted_at = DateTimeProperty(default_now=True)

    user = RelationshipFrom('apps.relations.models.user.User', 'POSTS')
    page = RelationshipFrom('apps.relations.models.pages.Page', 'POSTS')
    images = RelationshipTo('PostImage', 'HAS_IMAGE')
    tags = RelationshipTo('PostTags', 'HAS_TAG')
    likes = RelationshipTo('apps.relations.models.pages.Page', 'LIKES')


class PostImage(StructuredNode):
    __label__ = 'POST_IMAGE'

    uuid = StringProperty(unique_index=True)
    image = StringProperty()
    post = RelationshipFrom('Posts', 'HAS_IMAGE')


class PostTags(StructuredNode):
    __label__ = 'POST_TAGS'

    uuid = StringProperty(unique_index=True)
    tag = StringProperty()
    type = StringProperty()
    post = RelationshipFrom('Posts', 'HAS_TAG')
