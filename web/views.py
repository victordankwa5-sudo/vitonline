from flask import Blueprint, render_template, request, jsonify, flash, redirect, after_this_request, url_for
from flask_login import login_required, current_user
from .models import Product, Cart, Payment, Order, User, Brands, Settings
from . import db
import json
import random

views = Blueprint('views', __name__)

@views.route('/')
def index():
    if current_user.is_authenticated:
        order = Order.query.filter_by(customer_link=current_user.id).first()
    else:
        order=0
    products = Product.query.filter_by(flash_sale=True)
    
    brands = Brands.query.order_by(Brands.name).all()
    settings = Settings.query.filter_by(id=1).first()
    
    return render_template("index.html", user=current_user, products=products, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], order=order, round=round, brands=brands, settings=settings)

@views.route('/about-us')
def landing_page():
    settings = Settings.query.filter_by(id=1).first()
    
    return render_template('landing-page.html', user=current_user, settings=settings)

@views.route('/products')
def products():
    products = Product.query.filter(Product.stock > 0).all()
    settings = Settings.query.filter_by(id=1).first()
    
    return render_template("product.html", user=current_user, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], products=products, settings=settings)

@views.route('/add-to-cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    
    if request.method == 'POST':
        global product_id
        product_id = json.loads(request.data)
        
    else:
        @after_this_request
        def add_header(response):

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        product_id = product_id['product_id']
        product_to_add = Product.query.get(product_id)
        product_exists = Cart.query.filter_by(product_link=product_id, customer_link=current_user.id).first()
        
        if product_exists:
            try:
                product_exists.quantity += 1
                db.session.commit()
                new_cart = Cart.query.filter_by(customer_link=current_user.id).all()
                new_cart_quantity = len(new_cart)
                data = {
                    'flash_message': 'Updated',
                    'new_cart_quantity': new_cart_quantity
                }
                return jsonify(data)
            except Exception as e:
                flash('Product quantity could not be updated', 'error')
                return redirect(request.referrer)
        else:
            new_cart_item = Cart()
            new_cart_item.quantity = 1
            new_cart_item.product_link = product_to_add.id
            new_cart_item.customer_link = current_user.id

            try:
                db.session.add(new_cart_item)
                db.session.commit()
    
                new_cart = Cart.query.filter_by(customer_link=current_user.id).all()

                new_cart_quantity = len(new_cart)

                data = {
                    'new_cart_quantity': new_cart_quantity,
                    'flash_message': 'Added to cart'
                }
                return jsonify(data)
            except Exception as e:
                flash('Could not add product to cart', 'error')
    
    return jsonify({})

@views.route("/cart")
@login_required
def cart():
    order = Order.query.filter_by(customer_link=current_user.id).first()
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    settings = Settings.query.filter_by(id=1).first()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity
    
    return render_template("cart.html", user=current_user, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], cart=cart, amount=amount, total=amount+200, order=order, settings=settings)

@views.route('/plus-cart', methods=['GET', 'POST'])
@login_required
def plus_cart():
    if request.method == 'POST':
        global cart_id
        cart_id = json.loads(request.data)
    
    else:
        @after_this_request
        def add_header(response):

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        cart_id = cart_id['cart_id']
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity += 1
        db.session.commit()
        
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        
        amount = 0
        
        for item in cart:
            amount += item.product.current_price * item.quantity
        
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200,
            'item_total': cart_item.product.current_price * cart_item.quantity
        }
        
        return jsonify(data)
    
    return jsonify({})


@views.route('/minus-cart', methods=['GET', 'POST'])
@login_required
def minus_cart():
    if request.method == 'POST':
        global cart_id
        cart_id = json.loads(request.data)
    
    else:
        @after_this_request
        def add_header(response):

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        cart_id = cart_id['cart_id']
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity -= 1
        db.session.commit()
        
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        
        amount = 0
        
        for item in cart:
            amount += item.product.current_price * item.quantity
        
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200,
            'item_total': cart_item.product.current_price * cart_item.quantity
        }
        
        return jsonify(data)
    
    return jsonify({})


@views.route('/remove-cart', methods=['GET', 'POST'])
@login_required
def remove_cart():
    if request.method == 'POST':
        global cart_id
        cart_id = json.loads(request.data)
    
    else:
        @after_this_request
        def add_header(response):

            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        cart_id = cart_id['cart_id']
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()
        
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        
        amount = 0
        
        for item in cart:
            amount += item.product.current_price * item.quantity
        
        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 200,
            'item_total': cart_item.product.current_price * cart_item.quantity
        }
        
        return jsonify(data)
    
    return jsonify({})


@views.route('/orders')
@login_required
def orders():
    order = Order.query.filter_by(customer_link=current_user.id).all()
    settings = Settings.query.filter_by(id=1).first()
    
    return render_template('order.html', user=current_user, order=order, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], settings=settings)

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.name.ilike(f'%{search_query}%')).all()
        settings = Settings.query.filter_by(id=1).first()
        
        return render_template('search.html', items=items, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], user=current_user, settings=settings)
    
    return render_template('search.html', user=current_user)

@views.route('/view-product/<int:product_id>')
def view_product(product_id):
    product = Product.query.get(product_id)
    settings = Settings.query.filter_by(id=1).first()
    
    return render_template('view-product.html', user=current_user, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], product=product, settings=settings)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        try:
            User.query.filter_by (id=current_user.id).update(dict(
                username=username,
                email=email
            ))
            db.session.commit()
            flash('Log in details updated', 'success')
            return redirect(request.referrer)
        except Exception as e:
            flash('Faild to update profile', 'error')
    
    return render_template('user-profile.html', user=current_user)

@views.route('/edit-personal-info', methods=['GET', 'POST'])
@login_required
def edit_personal_info():
    user_info = Payment.query.filter_by(customer_link=current_user.id).first()
    
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        momo_name = request.form.get('momo-name')
        phone_number = request.form.get('phone-num')
        region = request.form.get('region')
        town = request.form.get('town')
        address = request.form.get('address')
        postal_code = request.form.get('postal-code')
        country = request.form.get('country')
        payment_method = request.form.get('payment-method')
        
        
        if phone_number.isalpha():
            flash('Phone number must be numbers only!', 'error')
        elif len(phone_number) < 10 or len(phone_number) > 10:
            flash('Phone number must be 10 digits', 'error')
        elif phone_number[0] != '0':
            flash('Enter a valid phone number', 'error')
        elif postal_code.isalpha():
            flash('Postal code must be numbers only', 'error')
        else:
            Payment.query.filter_by(customer_link=current_user.id).update(dict(
                full_name=fullname,
                momo_name=momo_name,
                phone_number=phone_number,
                region=region,
                town=town,
                address=address,
                postal_code=postal_code,
                country=country,
                payment_method=payment_method
            ))
            db.session.commit()
            
            flash('Personal info updated', 'success')
            return redirect(request.referrer)
    
    return render_template('edit-personal-info.html', user=current_user, user_info=user_info)

@views.route('/flash-sale', methods=['GET', 'POST'])
def flash_sale():
    flash_sale_products = Product.query.filter_by(flash_sale=True).all()
    settings = Settings.query.filter_by(id=1).first()
    
    return render_template('flash-sale.html', user=current_user, products=flash_sale_products, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], round=round, settings=settings)

@views.route('/brands/<string:brand_name>')
def brand(brand_name):
    brand_items = Product.query.filter_by(brand=brand_name).all()
    settings = Settings.query.filter_by(id=1).first()
    
    return render_template('brands.html', products=brand_items, user=current_user, settings=settings)