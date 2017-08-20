import tornado
import tornado.gen

from req import ApiRequestHandler


class Index(ApiRequestHandler):

    @tornado.gen.coroutine
    def get(self):
        self.render()
