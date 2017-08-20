from permission.base import Base


class Missions(Base):

    def post(self, req):
        if len(req.user) == 0:
            print("Hello I am in",'backend/permission/api/mission.py')
            print("Hello I am in",'backend/permission/api/mission.py')
            print("Hello I am in",'backend/permission/api/mission.py')
            return (403, 'Permission Denied.')
