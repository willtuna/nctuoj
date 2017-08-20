from permission.base import Base


class Judge(Base):

    def get(self, req):
        if (len(req.user) == 0) or (1 not in req.user['power']):
            return (403, 'Permission Denied.')
