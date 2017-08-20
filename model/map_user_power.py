import model
from service import Service
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


class MapUserPower(declarative_base()):
    __tablename__ = 'map_user_power'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    power = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def get_user_power_list(user_id):
        powers = (yield from Service.select([
            model.MapUserPower
        ]).where(
            model.MapUserPower.user_id == user_id
        ).execute())
        return [power['power'] for power in powers]
