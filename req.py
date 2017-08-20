import datetime
import json
import traceback
import types

import model
import tornado.gen
import tornado.template
import tornado.web
import tornado.websocket
from data_collector import DataCollector
from form import Form
from permission import Permission
from tornado_cors import CorsMixin
from utils.log import log


class DatetimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class RequestHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_METHODS = "GET, POST, PUT, DELETE, OPTIONS"
    CORS_ORIGIN = "*"
    CORS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = 'Content-Type, Authorization, Content-Length, \
    X-Requested-With, X-Prototype-Version, Origin, Allow, *'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = log
        try:
            self.CORS_ORIGIN = self.request.headers['Origin']
        except:
            self.CORS_ORIGIN = '*'
        self.add_header('Access-Control-Allow-Origin', self.CORS_ORIGIN)

    def initialize(self, *args, **kwargs):
        self.start = datetime.datetime.now()

    def get_args(self, name):
        meta = {}
        for n in name:
            try:
                if n[-2:] == "[]":
                    meta[n[:-2]] = self.get_arguments(n)
                elif n[-8:] == "[file][]":
                    n = n[:-8]
                    meta[n] = self.request.files[n]
                elif n[-6:] == "[file]":
                    n = n[:-6]
                    meta[n] = self.request.files[n][0]
                else:
                    meta[n] = self.get_argument(n)
            except:
                meta[n] = None
        return meta

    @tornado.gen.coroutine
    def check_permission(self):
        now = Permission
        for attr in self.path[1:]:
            if hasattr(now, attr):
                now = getattr(now, attr)
            else:
                return None
        method = self.request.method.lower()
        if not hasattr(now, method):
            return None
        res = getattr(now, method)(self)
        if isinstance(res, types.GeneratorType):
            res = yield from res
        if isinstance(res, tuple):
            self.render(res)

    @tornado.gen.coroutine
    def check_form_validation(self):
        now = Form
        for attr in self.path[1:]:
            if hasattr(now, attr):
                now = getattr(now, attr)
            else:
                return None
        method = self.request.method.lower()
        if not hasattr(now, method):
            return None
        res = getattr(now, method)(self.data)
        if isinstance(res, types.GeneratorType):
            res = yield from res
        if isinstance(res, tuple):
            self.render(res)

    @tornado.gen.coroutine
    def get_data(self):
        now = DataCollector
        for attr in self.path[1:]:
            if hasattr(now, attr):
                now = getattr(now, attr)
            else:
                self.data = {}
                return
        method = self.request.method.lower()
        if not hasattr(now, method):
            self.data = {}
            return
        self.data = getattr(now, method)(self, *self.path_args)
        self.path_args = []

    @tornado.gen.coroutine
    def prepare(self):
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = x_real_ip or self.request.remote_ip
        self.remote_ip = remote_ip
        self.log("[%s] %s %s" %
                 (self.request.method, self.request.uri, self.remote_ip))

        def encode(data):
            if isinstance(data, dict):
                for x in data:
                    try:
                        data[x] = encode(data[x])
                    except:
                        pass
            elif isinstance(data, list):
                for x in data:
                    try:
                        x = encode(x)
                    except:
                        pass
            else:
                if isinstance(data, int):
                    data = str(data).encode()
            return data
        try:
            json_data = json.loads(self.request.body.decode())
            json_data = encode(json_data)
            self.request.arguments.update({x: y if isinstance(y, list) else [
                                          y, ] for x, y in json_data.items()})
        except:
            pass

        if not self._finished:
            yield self.get_identity()
        if not self._finished:
            yield self.get_data()
        if not self._finished:
            yield self.check_permission()
        if not self._finished:
            yield self.check_form_validation()

    def on_finish(self):
        super().on_finish()
        self.log("[Finish] [%s ms] [%s] %s %s" % ((
            datetime.datetime.now() - self.start).microseconds // 1000,
            self.request.method, self.request.uri, self.remote_ip))

    @tornado.gen.coroutine
    def get_identity(self):
        try:
            err, self.user = yield from model.Session.signin_by_token(self, {
                'token': self.get_args(['token'])['token']
            })
            if err:
                self.user = {}
        except Exception as e:
            self.user = {}
        if len(self.user):
            self.user['power'] = yield from \
                model.MapUserPower.get_user_power_list(self.user['id'])


class ApiRequestHandler(RequestHandler):

    def render(self, msg=""):
        if isinstance(msg, tuple):
            code, msg = msg
        else:
            code = 200
        self.set_status(code)
        try:
            msg = json.dumps({
                'msg': msg
            }, cls=DatetimeEncoder)
        except:
            msg = str(msg)
        self.finish(msg)

    def write_error(self, err, **kwargs):
        traceback.print_tb(kwargs['exc_info'][2])
        self.render((err, str(err)))


class StaticFileHandler(tornado.web.StaticFileHandler, ApiRequestHandler):

    def initialize(self, *args, **kwargs):
        ApiRequestHandler.initialize(self, *args, **kwargs)
        tornado.web.StaticFileHandler.initialize(self, *args, **kwargs)


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
