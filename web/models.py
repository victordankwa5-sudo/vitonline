from web import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256))
    date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    
    cart_items = db.relationship('Cart', backref=db.backref('user', lazy=True))
    orders = db.relationship('Order', backref=db.backref('user', lazy=True))
    personal_info = db.relationship('Payment', backref=db.backref('user', lazy=True))
    
    #customer
    
    def __str__(self):
        return '<User %r>' % User.id #prints the value of customer
    
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(1000), nullable=False)
    image2 = db.Column(db.String(1000), nullable=False)
    image3 = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    shipping_fee = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    flash_sale = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    
    carts = db.relationship('Cart', backref=db.backref('product', lazy=False))
    orders = db.relationship('Order', backref=db.backref('product', lazy=False))
    
    # Product
    
    def __str__(self):
        return '<Product %r>' % self.name

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    #cart
    
    def __str__(self):
        return '<Cart %r>' % self.id
    

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    #wishlist
    
    def __str__(self):
        return '<Wishlist %r>' % self.id
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_status = db.Column(db.String(1000), nullable=False)
    payment_id = db.Column(db.String(1000), unique=True, nullable=False)
    order_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    payment_link = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    
    # order
    
    def __str__(self):
        return '<Order %r>' % self.id


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    momo_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    
    order_link = db.relationship('Order', backref=db.backref('payment', lazy=True))
    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Payment infornamation
    
    def __str__(self):
        return '<Payment %r>' % self.id
    
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(100), nullable=False)
    store_email = db.Column(db.String(100), nullable=False)
    store_phone = db.Column(db.String(20), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    
    #admin settings
    
    def __str__(self):
        return '<Settings %r>' % self.id

class Brands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __str__(self):
        return '<Brands %r>' % self.id