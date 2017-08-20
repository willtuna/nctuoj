from utils.include import include


class Form:
    pass


include(
    cls=Form,
    dir='./form/',
    all_path=False,
    ignore=['base.py'],
    isObject=True,
)
