import model
from service import Service


class Session:

    def signin_by_token(req, data={}):
        user = (yield from Service.select([
            model.User
        ]).where(
            model.User.token == data['token']
        ).execute())
        if len(user) == 0:
            return ((400, 'User not exist'), None)
        user = user[0]
        return (None, user)
