import tornado

import model
from req import ApiRequestHandler
from service import Service


class Missions(ApiRequestHandler):

    @tornado.gen.coroutine
    def post(self):
        missions = []
        for mission in self.data['mission_list']:
            missions.append((yield from Service.insert(
                model.Mission
            ).values(
                payload=mission
            ).returning(
                model.Mission.id, model.Mission.payload
            ).execute())[0])
        self.render(missions)
