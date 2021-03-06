import psycopg2
import psycopg2.extras

MAX_WAIT_SECOND_BEFORE_SHUTDOWN = 3
PORT = 3019

TORNADO_SETTING = {}
TORNADO_SETTING['debug'] = True
TORNADO_SETTING['cookie_secret'] = 'cookie secret!'
TORNADO_SETTING['compress_response'] = True
TORNADO_SETTING['autoescape'] = 'xhtml_escape'
TORNADO_SETTING['xheaders'] = True
TORNADO_SETTING['password_salt'] = 'asdf'

DB_SETTING = {}
DB_SETTING['dsn'] = 'dbname=testpython user=willvegapunk password=topscientist host=localhost port=5432'
DB_SETTING['size'] = 1
DB_SETTING['max_size'] = 10
DB_SETTING['setsession'] = ("SET TIME ZONE +8",)
DB_SETTING['raise_connect_errors'] = False
DB_SETTING['cursor_factory'] = psycopg2.extras.RealDictCursor
