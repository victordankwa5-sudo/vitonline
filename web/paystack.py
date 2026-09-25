from flask import Blueprint, jsonify, redirect, render_template, flash, url_for, request
from flask_login import login_required, current_user
from .models import Payment, Settings, Cart, Order, Product
import os
import requests
from dotenv import load_dotenv
from web import db

load_dotenv()

pay = Blueprint('pay', __name__)

@pay.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    payment_status = Payment.query.filter_by(customer_link=current_user.id).first()
    settings = Settings.query.filter_by(id=1).first()
    
    if payment_status:
        cart_detail = Cart.query.filter_by(customer_link=current_user.id).all()
            
        amount = 0
        total_shipping_fee = 0
            
        for item in cart_detail:
            amount += item.product.current_price * item.quantity
            total_shipping_fee += item.product.shipping_fee
            
        total = amount + total_shipping_fee
            
        return render_template('checkout.html', user=current_user, cart_detail=cart_detail,amount=amount, total=total, settings=settings, total_shipping_fee=total_shipping_fee, cart_num = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [])
    else:
        flash('Please finish setting up your profile to buy from us!', 'error')
        return redirect(url_for('auth.personal_info_form'))



PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET_KEY")
HEADERS = {"Authorization": f"Bearer {PAYSTACK_SECRET}", "Content-Type": "application/json"}

@pay.route('/api/pay/initialize', methods=['POST'])
def initialize():
    body = request.json
    payload = {
        "email": body['email'],
        "amount": int(float(body['amount']) * 100),
        "currency": "GHS",
        "callback_url": "https://yourdomain.com/success", # change to your live link
        "metadata": {"order_id": body.get('order_id', 'ORDER-1')}
    }
    r = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=HEADERS)
    return jsonify(r.json())

@pay.route('/success')
def success_page():
    return render_template('success.html', user=current_user)

@pay.route('/api/pay/verify/<reference>')
def verify(reference):
    r = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=HEADERS)
    data = r.json()
    if data.get('data', {}).get('status') == 'success':
        # SAVE TO DB HERE - Mark order as paid
        customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0
        shipping_fee = 0
        for item in customer_cart:
            amount += item.product.current_price * item.quantity
            shipping_fee += item.product.shipping_fee
        total = amount + shipping_fee
            
        for item in customer_cart:
            
            new_order = Order()
            new_order.quantity = item.quantity
            new_order.price = item.product.current_price
            new_order.status = 'Pending'
            new_order.payment_status = 'Pending'
            new_order.payment_id = reference
            new_order.total = total
            new_order.product_link = item.product_link
            new_order.customer_link = item.customer_link
            customer_payment = Payment.query.filter_by(customer_link=current_user.id).first()
            new_order.payment_link = customer_payment.id
            
            db.session.add(new_order)
            
            product = Product.query.get(item.product_link)
            product.stock -= item.quantity
            
            db.session.delete(item)
            db.session.commit()
        
        flash(f"Order Paid: {data['data']['metadata']}", "success")
        return jsonify({"status": "success"})
    return jsonify({"status": "failed", "data": data})

# This auto-confirms payment even if user closes browser
@pay.route('/paystack/webhook', methods=['POST'])
def webhook():
    # Verify it's really from Paystack
    # In production, verify signature
    event = request.json
    if event['event'] == 'charge.success':
        reference = event['data']['reference']
        print(f"Webhook: Payment success for {reference}")
        # Update your database here
    return jsonify({"status": "ok"}), 200

@pay.route('/api/pay/config')
def get_config():
    return jsonify({
        "public_key": os.getenv("PAYSTACK_PUBLIC_KEY")
    })