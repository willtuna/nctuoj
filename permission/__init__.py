from utils.include import include


class Permission:
    pass


include(
    cls=Permission,
    dir='./permission/',
    all_path=False,
    ignore=['base.py'],
    isObject=True,
)
