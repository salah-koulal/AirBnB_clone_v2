#!/usr/bin/python3
"""AirBnB cloned v2 data storage class"""
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class save instances to a mysql db and
    get instances from the db
    Attributes:
        __engine: create the interfaces of comunication with db
        __session: open a comunication with the db
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes new instances of DBStorage.
        """
        try:
            user = os.environ.get('HBNB_MYSQL_USER')
            password = os.environ.get('HBNB_MYSQL_PWD')
            host = os.environ.get('HBNB_MYSQL_HOST')
            db = os.environ.get('HBNB_MYSQL_DB')
            env = os.environ.get('HBNB_ENV')
            attributes = [user, password, host, db]
            for attribute in attributes:
                if attribute is None:
                    print("Missing attributes env var")

            conn_str = "mysql+mysqldb://{}:{}@{}/{}".format(
                user, password, host, db)
            # create engine and session object with connection string
            self.__engine = create_engine(conn_str, pool_pre_ping=True)

            # drop all tables in DB if test env
            if env == 'test':
                Base.metadata.drop_all(bind=self.__engine, checkfirst=True)
        except Exception as E:
            print("raised exception in init")
            print(E)

    def all(self, cls=None):
        """show all the instances"""
        instances = {}
        if cls is None:
            all_cls = ["State", "City", "User", "Place", "Review", "Amenity"]

            for cl in all_cls:
                objs = self.__session.query(eval(cl))
                for obj in objs:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    instances[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                instances[key] = obj
        return instances

    def new(self, obj):
        """add an object into the database"""
        if obj and self.__session:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session"""
        try:
            self.__session.delete(obj)
        except Exception:
            pass

    def reload(self):
        """ reload all the objs"""
        try:
            Base.metadata.create_all(self.__engine)
            Session = scoped_session(sessionmaker(
                bind=self.__engine, expire_on_commit=False))
            self.__session = Session()
        except Exception as Err:
            print(Err)

    def close(self):
        """Close session"""
        self.__session.close()
