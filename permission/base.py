from utils.form import form_validation
from utils.log import log


class Base:

    def __init__(self):
        self.form_validation = form_validation
        self.log = log
