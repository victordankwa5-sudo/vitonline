from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Cart, Payment, Order, Settings
from werkzeug.security import generate_password_hash, check_password_hash
from web import db, mail
from random import *
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message

auth = Blueprint("auth",__name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_name = request.form.get('email')
        password = request.form.get('password')
        checkbox = request.form.get('remember')
        
        user = User.query.filter_by(email=email_name).first()
        
        if user:
            if check_password_hash(user.password, password):
                if checkbox == 'ON':
                    login_user(user, remember=True)
                    flash("Logged in successfuly.", 'success')
                    if current_user.id == 1:
                        return redirect(url_for('admin.index'))
                    else:
                        return redirect(url_for('views.index'))
                else:
                    login_user(user, remember=False)
                    flash('logged in successfuly', 'success')
                    if current_user.id == 1:
                        return redirect(url_for('admin_views.admin_index'))
                    else:
                        return redirect(url_for('views.index'))
            else:
                flash("Password incorrect.", 'error')
        else:
            flash("Email does not exist.", 'error')
    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout successful', 'success')
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email_name = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email_name).first()

        if user:
            flash('Username already exists', 'error')
        elif user_email:
            flash('Email already exists', 'error')
        elif len(username) < 2 :
            flash("Username cannot be less than 2 characters", 'error')
        elif len(email_name) < 2 :
            flash("Email is too short", 'error')
        elif len(password1) < 8 :
            flash("password too short!", 'error')
        elif password1 != password2 :
            flash("Passwords don't match!", 'error')
        else:
            new_user = User(username=username, email=email_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfuly', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template("signup.html", user=current_user)


@auth.route("/forgotpass", methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'POST':
        
        def get_email():
            return request.form.get('email')
        global email
        email = get_email()
        
        msg_subject = 'PASSWORD RECOVERY'
        msg_body = f'This is your account recovery code\n do not share this code with anyone, it is confidential and should be kept private.'
        
        #Function to generate 4-digit code
        def generate_code():
            code_array = []
            for code_num in range(4):
                code_num = randint(0, 9)
                code_array.append(code_num)
            code_combine = f'{code_array[0]}{code_array[1]}{code_array[2]}{code_array[3]}'
            code = int(code_combine)
            return code
        
        global verification_code
        verification_code = generate_code()
        print(verification_code)
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            try:
                msg = Message(subject=msg_subject, sender='victordankwa5@gmail.com', recipients=[email])
                msg.body = f"{msg_body}\n\n {verification_code}"
                mail.send(msg)
                flash(f'A 4-digit code was sent to {user.email}', 'success')
                return redirect(url_for('auth.verify_code'))
            except:
                flash('Could not send code!', 'error')
            
        else:
            flash('Email does not exist!', 'error')
        
    return render_template("forgotpass_getcode.html", user=current_user)


@auth.route("/verify-code", methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
         code = request.form.get('code-entry')
         
         if code.isdigit():
            code = int(code)
            if code != verification_code:
                flash('Wrong code!, try again.', 'error')
            else:
                flash('Verification successful!', 'success')
                return redirect(url_for('auth.change_password'))
         else:
             flash("The code can only be numbers!", 'error')
    
    return render_template("forgotpass_entercode.html", user=current_user)


@auth.route('change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        new_password = request.form.get('new-password')

        if len(new_password) < 8:
            flash('password cannot be less than 8 characters', 'error')
        else:
            try:
                User.query.filter_by(email=email).update(dict(
                    password=generate_password_hash(new_password, method='pbkdf2:sha256')
                ))
                db.session.commit()
                flash('You have successfuly changed your password', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                flash('An error occured', 'error')
        
    return render_template('change-password.html', user=current_user)
    

@auth.route('/personal-info', methods=['GET', 'POST'])
@login_required
def personal_info_form():
    order = Order.query.filter_by(customer_link=current_user.id).first()
    customer_detail = Payment.query.filter_by(customer_link=current_user.id).first()
    
    if customer_detail:
        flash('You have already setted your details, visit profile to edit')
        return redirect(url_for('views.index'))
    else:
        if request.method == 'POST':
            full_name = request.form.get('fullname')
            momo_name = request.form.get('momo-name')
            phone_number = request.form.get('phone-number')
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
                phone_number = int(phone_number)
                new_payment_detail = Payment()
                new_payment_detail.full_name = full_name
                new_payment_detail.momo_name = momo_name
                new_payment_detail.phone_number =   phone_number
                new_payment_detail.region = region
                new_payment_detail.town = town
                new_payment_detail.address = address
                new_payment_detail.postal_code =    postal_code
                new_payment_detail.country = country
                new_payment_detail.payment_method =     payment_method
                new_payment_detail.customer_link = current_user.id
                db.session.add(new_payment_detail)
                db.session.commit()
                
                flash('You have successfuly created your Delivery info', 'success')
                return redirect(url_for('pay.checkout'))
            
        return render_template('personal_info_form.html', user=current_user, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [], order=order)

# @auth.route('/verify-payment', methods=['GET', 'POST'])
# @login_required
# def verify_payment():
#     if request.method == 'POST':
#         return redirect(url_for('payment.payment_callback'))
        
#     return render_template('verify-payment.html', user=current_user, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [])

# @auth.route('/place-order')
# @login_required
# def place_order():
#     customer_cart = Cart.query.filter_by(customer_link=current_user.id)
        
#     if customer_cart:
#         try:
#             amount = 0
            
#             for item in customer_cart:
#                 amount += item.product.current_price * item.quantity
            
#             total = amount + 200
            
#             for item in customer_cart:
#                 new_order = Order()
#                 new_order.quantity = item.quantity
#                 new_order.price = item.product.current_price
#                 new_order.status = 'Pending'
#                 new_order.payment_id = 'PFO#01'
#                 new_order.total = total

#                 new_order.product_link = item.product_link
#                 new_order.customer_link = item.customer_link
                
#                 customer_payment = Payment.query.filter_by(customer_link=current_user.id).first()
                
#                 new_order.payment_link = customer_payment.id

#                 db.session.add(new_order)

#                 product = Product.query.get(item.product_link)

#                 product.stock -= item.quantity
#                 db.session.delete(item)
#                 db.session.commit()

#             flash('Order placed successfuly')

#             return redirect(url_for('views.products'))
            
#         except Exception as e:
#             flash('could not place order', 'error')
#             return redirect(url_for('views.cart'))
#     else:
#         flash('Your cart is empty', 'error')
#         return redirect(url_for('views.products'))
