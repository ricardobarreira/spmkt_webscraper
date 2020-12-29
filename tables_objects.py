from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

Base = declarative_base()


class Store(Base):
    __tablename__ = 'stores'

    store_id = Column(Integer(), primary_key=True)
    store_name = Column(String(50))


class Urls(Base):
    __tablename__ = 'URLs'

    url_id = Column(Integer(), primary_key=True)
    url_string = Column(String(255))
    category = Column(String(255))
    store_id = Column(Integer(), ForeignKey('stores.store_id'))

    store = relationship("Store", backref=backref('URLs', order_by=store_id))


class Html(Base):
    __tablename__ = 'HTML_elements'

    element_id = Column(Integer(), primary_key=True)
    element_string = Column(String(255))
    h_level = Column(Integer())
    type = Column(String(55))
    store_id = Column(Integer(), ForeignKey('stores.store_id'))

    store = relationship("Store", backref=backref('HTML_elements', order_by=store_id))


class Headers(Base):
    __tablename__ = 'Headers'

    header_id = Column(Integer(), primary_key=True)
    header_type = Column(String(55))
    header_string = Column(String(255))
    store_id = Column(Integer(), ForeignKey('stores.store_id'))

    store = relationship("Store", uselist=False)


class Cookies(Base):
    __tablename__ = 'Cookies'

    cookie_id = Column(Integer(), primary_key=True)
    cookie_string = Column(String(10000))
    store_id = Column(Integer(), ForeignKey('stores.store_id'))

    store = relationship("Store", uselist=False)


class Products(Base):
    __tablename__ = 'Products'

    product_id = Column(Integer(), primary_key=True)
    product_name = Column(String(255))
    product_quantity = Column(String(55), nullable=False)


class Offers(Base):
    __tablename__ = 'Offers'

    offer_id = Column(Integer(), primary_key=True)
    offer_price = Column(String(255))
    offer_date = Column(DateTime(), default=datetime.now)
    offer_discount = Column(String(55))

    product_id = Column(Integer(), ForeignKey('Products.product_id'))
    store_id = Column(Integer(), ForeignKey('stores.store_id'))

    product = relationship("Products", uselist=False)
    store = relationship("Store", uselist=False)
