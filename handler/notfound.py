import tornado
import tornado.gen

from req import ApiRequestHandler


class NotFound(ApiRequestHandler):

    @tornado.gen.coroutine
    def get(self):
        self.render((404, "NotFound"))
