import datetime
import inspect
import sys


def log(*args, sep=' ', end='\n', file=sys.stdout, flush=False):
    (frame, filename, line_number, function_name, lines, index) = \
        inspect.getouterframes(inspect.currentframe())[1]
    print("[%s] [%s,%s,%s]" % (
        datetime.datetime.strftime(
            datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'
        ), filename, line_number, function_name),
        sep=sep, end=end, file=file, flush=flush)
    print(*args, sep=sep, end=end, file=file, flush=flush)
