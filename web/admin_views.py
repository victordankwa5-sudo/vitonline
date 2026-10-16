from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import Order, User, Product, Brands, Settings, Notifications, Revenue
from datetime import datetime

admin_views = Blueprint('admin_views', __name__)

# This code renders the admin
@admin_views.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
def admin_index():
    if current_user.id == 1:
        products = Product.query.order_by(Product.id).all()
        orders = Order.query.order_by(Order.id).all()
        customers = User.query.order_by(User.id).all()
        settings = Settings.query.filter_by(id = 1).first()
        revenue = Revenue.query.order_by(Revenue.date).all()
        
        total_revenue = 0
        for amount in revenue:
            total_revenue += amount
        
        month_rev = Revenue.query.order_by(Revenue.date).all()
        
        current_revenue = 0
        for rev in month_rev:
            if rev.date.strftime('%b') == datetime.today().strftime('%b'):
                current_revenue += rev.amount
                
        this_month_percentage = 0
        if current_revenue and total_revenue:
            this_month_percentage = round((current_revenue / total_revenue) * 100)
        
        total_products = len(products)
        total_orders = len(orders)
        total_customers = len(customers)
        return render_template('admin-dashboard.html', user=current_user, total_products=total_products, total_orders=total_orders, total_customers=total_customers, orders=orders, settings=settings, total_revenue=total_revenue, months_percentage=this_month_percentage)
    else:
        flash("You are not an admin!", "error")
        return redirect(url_for("views.index"))

# This block gets the input of add-product and writes it into json
@admin_views.route('/admin-product', methods=['GET', 'POST'])
@login_required
def admin_products():
    id = current_user.id
    if id == 1:
        num_orders = Order.query.order_by(Order.id).all()
        total_orders = len(num_orders)
            
        products = Product.query.order_by(Product.name).all()
        settings = Settings.query.filter_by(id = 1).first()
        
        return render_template('admin-product.html', user=current_user, products=products, total_orders=total_orders, settings=settings)
    else:
        flash("You are not an admin!", "error")
        return redirect(url_for("views.index"))

@admin_views.route('/admin-orders')
@login_required
def orders():
    if current_user.id == 1:
        orders = Order.query.order_by(Order.id).all()
        settings = Settings.query.filter_by(id = 1).first()
        
        num_orders = Order.query.order_by(Order.id).all()
        total_orders = len(num_orders)
        
        return render_template('admin-orders.html', user=current_user, orders=orders, total_orders=total_orders, settings=settings)
    else:
        flash('You are not an admin!', 'error')
        return redirect(url_for('views.index'))

@admin_views.route('/admin/orders/<int:order_id>/print')
@login_required # your admin check
def admin_print_order(order_id):
    if current_user.id == 1:
        settings = Settings.query.filter_by(id = 1).first()
        order = Order.query.get_or_404(order_id)
        
        customer = User.query.filter_by(id=order.customer_link).first()
        
        # If your cart_detail is related to order
        order_details = Order.query.filter_by(payment_id=order.payment_id).all()
        return render_template('admin_print_order.html', order=order, order_detail=order_details, settings=settings, customer=customer)
    else:
        flash('You are not an admin!', 'error')
        
@admin_views.route('/admin-customers')
@login_required
def customers():
    if current_user.id == 1:
        customers = User.query.order_by(User.date_joined).all()
        settings = Settings.query.filter_by(id = 1).first()
        
        num_orders = Order.query.order_by(Order.id).all()
        total_orders = len(num_orders)
        
        return render_template('admin-customers.html', user=current_user, customers=customers, total_orders=total_orders, settings=settings)
    else:
        flash('You are not an admin!', 'error')
        return redirect(url_for('views.index'))
    
@admin_views.route('/admin-categories')
@login_required
def categories():
    if current_user.id == 1:
        settings = Settings.query.filter_by(id = 1).first()
        num_orders = Order.query.order_by(Order.id).all()
        total_orders = len(num_orders)
        
        laptops = Product.query.filter_by(category='Laptops').all()
        num_laptops = len(laptops)
        
        phones_tablets = Product.query.filter_by(category='Phones/Tablets').all()
        num_phones_tablets = len(phones_tablets)
        
        desktop = Product.query.filter_by(category='Desktop').all()
        num_desktop = len(desktop)
        
        peripharals = Product.query.filter_by(category='Peripharals').all()
        num_peripharals = len(peripharals)
        
        accessories = Product.query.filter_by(category='Accessories').all()
        num_accessories = len(accessories)
        
        gaming = Product.query.filter_by(category='Gaming').all()
        num_gaming = len(gaming)
        
        sound = Product.query.filter_by(category='Sound').all()
        num_sound = len(sound)
        
        security = Product.query.filter_by(category='Security').all()
        num_security = len(security)
        
        
        return render_template('admin-categories.html', user=current_user, total_orders=total_orders, num_laptops=num_laptops, num_phones_tablets=num_phones_tablets, num_desktop=num_desktop, num_peripharals=num_peripharals, num_accessories=num_accessories, num_gaming=num_gaming, num_sound=num_sound, num_security=num_security, settings=settings)
    else:
        flash('You are not an admin!', 'error')
        return redirect(url_for('views.index'))


@admin_views.route('/admin-brands')
@login_required
def admin_brands():
    if current_user.id == 1:
        settings = Settings.query.filter_by(id = 1).first()
        num_orders = Order.query.order_by(Order.id).all()
        total_orders = len(num_orders)
        
        brands = Brands.query.order_by(Brands.name).all()
        
        return render_template('admin-brands.html', user=current_user, brands=brands, total_orders=total_orders, settings=settings)
    else:
        flash('You are not an admin!', 'error')

@admin_views.route('/notifications')
@login_required
def notifications():
    if current_user.id == 1:
        settings = Settings.query.filter_by(id=1).first()
        notifications = Notifications.query.order_by(Notifications.id).all()
        num_orders = Order.query.order_by(Order.id).all()
        total_orders = len(num_orders)
        
        return render_template('admin-notifications.html', user=current_user, settings=settings, notifications=notifications, total_orders=total_orders)
    else:
        flash('You are not an admin!', 'error')
        return redirect(request.referrer)