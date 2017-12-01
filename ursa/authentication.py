from restfulpy.authentication import StatefulAuthenticator
from restfulpy.orm import DBSession

from ursa.models import Member


class Authenticator(StatefulAuthenticator):

    def create_principal(self, member_id=None, session_id=None):
        member = Member.query.filter(Member.id == member_id).one()
        return member.create_jwt_principal(session_id=session_id)

    def create_refresh_principal(self, member_id=None):
        member = Member.query.filter(Member.id == member_id).one()
        return member.create_refresh_principal()

    def validate_credentials(self, credentials):
        user_name, password = credentials
        member = Member.query.filter(Member.user_name == user_name).one_or_none()
        if member is None or not member.validate_password(password):
            return None
        return member
