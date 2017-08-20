from utils.include import include


class DataCollector:
    pass


include(
    cls=DataCollector,
    dir='./data_collector/',
    all_path=False,
    ignore=['base.py'],
    isObject=True,
)
