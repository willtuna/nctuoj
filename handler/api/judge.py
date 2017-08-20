import model
import tornado
from req import ApiRequestHandler
from service import Service


class Judge(ApiRequestHandler):

    @tornado.gen.coroutine
    def get(self):
        mission = (yield from Service.delete(
            model.Mission
        ).where(
            model.Mission.id.in_(Service.select(
                [model.Mission.id]
            ).order_by(
                model.Mission.id.asc()
            ).limit(1))
        ).returning(
            model.Mission.id,
            model.Mission.payload
        ).execute())
        if len(mission) == 0:
            self.render()
        else:
            self.render(mission[0])
