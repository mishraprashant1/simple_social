from django.core.management.base import BaseCommand
from apps.relations.models import User
from neomodel import db
from django.conf import settings


class Command(BaseCommand):
    help = 'Build friend recommendations in redis'

    def handle(self, *args, **options):
        redis_conn = settings.REDIS_CONNECTION
        users = User.nodes.all()
        for user in users:
            query = '''
            MATCH (A:USER)-[:FRIENDS]->(B:USER)-[:FRIENDS]->(C:USER)
            WHERE not (A)-[:FRIENDS]->(C) and A.uuid <> C.uuid and A.uuid="{user_uuid}"
            RETURN C
            '''.format(user_uuid=user.uuid)
            results, meta = db.cypher_query(query)
            recommendations = set([user[0]['uuid'] for user in results])
            print(f"recommendation:{user.uuid}", len(recommendations))
            if len(recommendations) > 0:
                redis_conn.lpush(f"recommendation:{user.uuid}", *recommendations)
        self.stdout.write(self.style.SUCCESS('Successfully built friend recommendations'))
