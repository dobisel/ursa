from restfulpy.orm import DBSession

from ursa.models import Admin


def insert():  # pragma: no cover
    admin = Admin()
    admin.user_name = 'admin'
    admin.password = '123456'
    DBSession.add(admin)

    DBSession.commit()
