from sqlalchemy.ext.declarative import declarative_base

from models import Session

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = Session()

    def get_all(self, **criteria):
        return [obj.as_json() for obj in self.session.query(self.__class__).filter_by(**criteria).all()]

    def get(self, id):
        return self.session.query(self.__class__).filter_by(id=id).one().as_json()

    def insert(self, **attr):
        obj = self.__class__(**attr)
        self.session.add(obj)
        self.session.commit()
        return obj.as_json()

    def update(self, id, **attr):
        obj = self.session.query(self.__class__).filter_by(id=id).one()
        for (k, v) in attr.items():
            setattr(obj, k, v)
        self.session.commit()
        return obj.as_json()

    def delete(self, id):
        obj = self.session.query(self.__class__).filter_by(id=id).one()
        self.session.delete(obj)
        self.session.commit()
        return obj.as_json()

    def as_json(self):
        raise Exception("Please override me")
