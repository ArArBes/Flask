from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from flask_login import UserMixin


Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    phone_number = Column(String(20), unique=True)
    password_hash = Column(String(256))

    reviews = relationship('Review', back_populates='review_author')
    cart_items = relationship('CartItem', back_populates='user')
    orders = relationship('Order', back_populates='user')


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    author = Column(String(256))
    price = Column(Float)
    genre = Column(String(80))
    cover_url = Column(String(256))
    description = Column(String(1024))
    rating = Column(Float)
    year = Column(Integer)

    reviews = relationship('Review', back_populates='reviewed_book')
    order_items = relationship('OrderItem', back_populates='book')
    cart_items = relationship('CartItem', back_populates='book')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    count = Column(Integer)
    
    user = relationship('User', back_populates='cart_items')
    book = relationship('Book', back_populates='cart_items')

    def __repr__(self):
        return f"id={self.id}, book_id={self.book_id}, user_id={self.user_id}, count={self.count}"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime)
    order_status = Column(String(50))
    address = Column(String(512))
    # list_books = Column(Text)

    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    book_id = Column(Integer, ForeignKey("books.id"))
    count = Column(Integer)
    price = Column(Float)

    order = relationship('Order', back_populates='order_items')
    book = relationship('Book', back_populates='order_items')


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    review = Column(Text)
    review_author_id = Column(Integer, ForeignKey('users.id')) 
    review_book_id = Column(Integer, ForeignKey('books.id'))  
    rating = Column(Float)

    review_author = relationship('User', back_populates='reviews')
    reviewed_book = relationship('Book', back_populates='reviews')
