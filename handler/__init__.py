from utils.include import include


class Handler:
    pass


include(
    cls=Handler,
    dir='./handler/',
    all_path=False,
)
