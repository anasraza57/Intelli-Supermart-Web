from datetime import datetime
from math import *
from random import randint

from flask import *
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://plbsmnpyhgnfkx:900ff23b99965614d20deeb707307f2add036274c83463f95e64dbff0384968b@ec2-107-20-234-175.compute-1.amazonaws.com:5432/d1hntjbagjg4ro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='bitf16a022@gmail.com',
    MAIL_PASSWORD='Tempass@123'
)

mail = Mail(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200))
    product_description = db.Column(db.String(1000))
    product_price = db.Column(db.String(200))
    picture_id = db.Column(db.Integer)
    product_quantity = db.Column(db.String(20))
    prod_subcategory_id = db.Column(db.Integer)
    slug = db.Column(db.String(200))


class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200))
    picture_id = db.Column(db.Integer)
    slug = db.Column(db.String(200))


class Subcategory(db.Model):
    __tablename__ = 'subcategory'
    subcategory_id = db.Column(db.Integer, primary_key=True)
    subcategory_name = db.Column(db.String(200))
    category_id = db.Column(db.Integer)
    slug = db.Column(db.String(200))


class Picture(db.Model):
    __tablename__ = 'picture'
    picture_id = db.Column(db.Integer, primary_key=True)
    picture_url = db.Column(db.String(200))


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(200))
    product_id = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)


class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    wishlist_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(200))
    product_id = db.Column(db.Integer)


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.String(200), primary_key=True)
    customer_phone = db.Column(db.String(200))


class CustomerInfo(db.Model):
    __tablename__ = 'customer_info'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(200))
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    gender = db.Column(db.String(200))
    address = db.Column(db.String(200))
    city = db.Column(db.String(200))
    zipcode = db.Column(db.String(200))


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(200))
    order_amount = db.Column(db.Integer)
    order_at = db.Column(db.DateTime)
    order_quantity = db.Column(db.Integer)
    order_status = db.Column(db.String(200))


class OrderPlaced(db.Model):
    __tablename__ = 'order_placed'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(200))
    product_id = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)
    order_at = db.Column(db.DateTime)


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    message = db.Column(db.String(1000))
    name = db.Column(db.String(200))
    subject = db.Column(db.String(200))


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    products = Product.query.all()
    no_of_prod = len(products)
    categories = Category.query.all()
    subcategories = Subcategory.query.all()
    pictures = Picture.query.all()
    best_seller_products_cat_index = [7, 6, 5, 4, 3, 2, 1, 0]

    best_seller_products = []
    if no_of_prod > 0:
        for i in range(0, 8):
            rand_index = randint(0, no_of_prod - 1)
            rand_row = products[rand_index]
            best_seller_products.append(rand_row)

    best_seller_products_images = []
    for product in best_seller_products:
        for picture in pictures:
            if product.picture_id == picture.picture_id:
                best_seller_products_images.append(picture)

    best_seller_products_categories = []
    for item in best_seller_products:
        for subcategory in subcategories:
            if item.prod_subcategory_id == subcategory.subcategory_id:
                for category in categories:
                    if subcategory.category_id == category.category_id:
                        best_seller_products_categories.append(category)

    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Home"
    return render_template('index.html', categories=categories, pictures=pictures, products=products,
                           best_seller_products_categories=best_seller_products_categories,
                           index=best_seller_products_cat_index, grand_total=grand_total,
                           best_seller_products=best_seller_products, title=title,
                           best_seller_products_images=best_seller_products_images, count=cart_count,
                           wishlist_count=wishlist_count)


@app.route('/cart', methods=['GET', 'POST', 'DELETE'])
def cart():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        if 'user' in session:
            cart_prod = Cart.query.filter_by(product_id=product_id, customer_id=session['user']).first()
            if not cart_prod:
                cart = Cart(customer_id=session['user'], product_id=product_id, product_quantity=quantity)
                db.session.add(cart)
                db.session.commit()
                return "success"
            else:
                return "duplicate"
        else:
            DictItems = {product_id: {'quantity': quantity}}
            if 'Shoppingcart' in session:
                if product_id in session['Shoppingcart']:
                    return "duplicate"
                else:
                    session['Shoppingcart'] = mergeDict(session['Shoppingcart'], DictItems)
                    return "success"
            else:
                session['Shoppingcart'] = DictItems
                return "success"

    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0 and 'user' not in session:
        return redirect('/')
    else:
        pictures = Picture.query.all()
        subcategories = Subcategory.query.all()
        categories = Category.query.all()
        category = categories[0]
        products = []
        quantities = []
        if 'user' in session:
            cart_products = Cart.query.filter_by(customer_id=session['user']).all()
            if not cart_products:
                return redirect('/')
            else:
                for prod in cart_products:
                    product = Product.query.filter_by(product_id=prod.product_id).first()
                    products.append(product)
                    quantities.append(prod.product_quantity)
        else:
            for key, item in session['Shoppingcart'].items():
                quantity = item['quantity']
                quantities.append(quantity)
                product = Product.query.filter_by(product_id=key).first()
                products.append(product)
        products.reverse()
        cart_products_pics = []
        for product in products:
            for pic in pictures:
                if product.picture_id == pic.picture_id:
                    cart_products_pics.append(pic)

        cart_count, total, grand_total = cartItemsAndPrice()
        wishlist_count = wishListCount()
        title = "Cart"
        return render_template('cart.html', products=products, pictures=cart_products_pics, category=category,
                               subcategories=subcategories, categories=categories, quantities=quantities, title=title,
                               total=total, grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/updateCart', methods=['PUT'])
def updateCart():
    if request.method == 'PUT':
        quantity = int(request.form['quantity'])
        id = int(request.form['id'])
        total_prod_price = 0
        total_price_of_all_prods = []
        if 'user' in session:
            cart_prod = Cart.query.filter_by(product_id=id, customer_id=session['user']).first()
            cart_prod.product_quantity = quantity
            db.session.commit()
            product = Product.query.filter_by(product_id=id).first()
            total_prod_price = product.product_price * quantity
            cart_prods = Cart.query.filter_by(customer_id=session['user']).all()
            for prod in cart_prods:
                product = Product.query.filter_by(product_id=prod.product_id).first()
                res = prod.product_quantity * product.product_price
                total_price_of_all_prods.append(res)
        else:
            for key, item in session['Shoppingcart'].items():
                if int(key) == id:
                    session.modified = True
                    item['quantity'] = quantity
                    product = Product.query.filter_by(product_id=id).first()
                    total_prod_price = product.product_price * quantity
                product = Product.query.filter_by(product_id=key).first()
                res = int(item['quantity']) * product.product_price
                total_price_of_all_prods.append(res)
        grand_total = sum(total_price_of_all_prods)
        return jsonify(
            total=total_prod_price,
            grand_total=grand_total,
        )


@app.route('/deleteFromCart', methods=['DELETE'])
def deleteFromCart():
    if request.method == 'DELETE':
        id = int(request.form['product_id'])
        try:
            if 'user' in session:
                cart = Cart.query.filter_by(product_id=id, customer_id=session['user']).first()
                db.session.delete(cart)
                db.session.commit()
                return "Deleted"
            if 'Shoppingcart' in session:
                session.modified = True
                for key, item in session['Shoppingcart'].items():
                    if int(key) == id:
                        session['Shoppingcart'].pop(key, None)
                        return "Deleted"
        except Exception as e:
            print(e)


@app.route('/wishlist', methods=['GET', 'POST', 'DELETE'])
def wishlist():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        if 'user' in session:
            wishlist_prod = Wishlist.query.filter_by(product_id=product_id, customer_id=session['user']).first()
            if not wishlist_prod:
                wishlist = Wishlist(customer_id=session['user'], product_id=product_id)
                db.session.add(wishlist)
                db.session.commit()
                return "success"
            else:
                return "duplicate"
        else:
            ListItems = [product_id]
            if 'Wishlist' in session:
                if product_id in session['Wishlist']:
                    return "duplicate"
                else:
                    session['Wishlist'] = mergeDict(session['Wishlist'], ListItems)
                    return "success"
            else:
                session['Wishlist'] = ListItems
                return "success"
    if 'Wishlist' not in session or len(session['Wishlist']) <= 0 and 'user' not in session:
        return redirect('/')
    else:
        pictures = Picture.query.all()
        subcategories = Subcategory.query.all()
        categories = Category.query.all()
        category = categories[0]  # for layout.html
        products = []
        if 'user' in session:
            wishlist_prod = Wishlist.query.filter_by(customer_id=session['user']).all()
            if not wishlist_prod:
                return redirect('/')
            else:
                for prod in wishlist_prod:
                    product = Product.query.filter_by(product_id=prod.product_id).first()
                    products.append(product)
        else:
            for key in session['Wishlist']:
                product = Product.query.filter_by(product_id=key).first()
                products.append(product)
        products.reverse()
        wishlist_products_pics = []
        for product in products:
            for pic in pictures:
                if product.picture_id == pic.picture_id:
                    wishlist_products_pics.append(pic)

        cart_count, totals, grand_total = cartItemsAndPrice()
        wishlist_count = wishListCount()
        title = "Wishlist"
        return render_template('wishlist.html', products=products, pictures=wishlist_products_pics, title=title,
                               subcategories=subcategories, category=category, categories=categories,
                               grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/deleteFromWishlist', methods=['DELETE'])
def deleteFromWishlist():
    if request.method == 'DELETE':
        id = int(request.form['product_id'])
        try:
            if 'user' in session:
                wishlist = Wishlist.query.filter_by(product_id=id, customer_id=session['user']).first()
                db.session.delete(wishlist)
                db.session.commit()
                return "Deleted"
            if 'Wishlist' in session:
                session.modified = True
                for key in session['Wishlist']:
                    if int(key) == id:
                        session['Wishlist'].remove(key)
                        return "Deleted"
        except Exception as e:
            print(e)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        gender = request.form['gender']
        address = request.form['address']
        city = request.form['city']
        zipCode = request.form['zipCode']
        grandTotal = int(request.form['grandTotal'])
        info = CustomerInfo.query.filter_by(customer_id=session['user']).first()
        if not info:
            info = CustomerInfo(customer_id=session['user'], first_name=firstName, last_name=lastName, email=email,
                                gender=gender, address=address, city=city, zipcode=zipCode)
            db.session.add(info)
        else:
            is_changed = False
            if info.first_name != firstName:
                info.first_name = firstName
                is_changed = True
            if info.last_name != lastName:
                info.last_name = lastName
                is_changed = True
            if info.email != email:
                info.email = email
                is_changed = True
            if info.gender != gender:
                info.gender = gender
                is_changed = True
            if info.address != address:
                info.address = address
                is_changed = True
            if info.city != city:
                info.city = city
                is_changed = True
            if info.zipcode != zipCode:
                info.zipcode = zipCode
                is_changed = True
            if is_changed:
                db.session.commit()
        cart_prods = Cart.query.filter_by(customer_id=session['user']).all()
        order_quantity = len(cart_prods)

        now = datetime.now()
        dt_string = now.strftime("%b %d, %Y, %I:%M %p")
        order = Order(customer_id=session['user'], order_amount=grandTotal, order_quantity=order_quantity,
                      order_status="Pending", order_at=dt_string)
        db.session.add(order)
        db.session.commit()
        for prod in cart_prods:
            order_placed = OrderPlaced(customer_id=prod.customer_id, product_id=prod.product_id,
                                       product_quantity=prod.product_quantity, order_at=dt_string)
            db.session.add(order_placed)
            db.session.delete(prod)
        db.session.commit()
        return "Success"
    if 'user' not in session:
        return redirect('/')
    else:
        info = CustomerInfo.query.filter_by(customer_id=session['user']).first()
        categories = Category.query.all()
        category = categories[0]
        cart_products = Cart.query.filter_by(customer_id=session['user']).all()
        if not cart_products:
            return redirect('/')
        else:
            products = []
            quantities = []
            for prod in cart_products:
                product = Product.query.filter_by(product_id=prod.product_id).first()
                products.append(product)
                quantities.append(prod.product_quantity)
            products.reverse()

        cart_count, total, grand_total = cartItemsAndPrice()
        wishlist_count = wishListCount()
        title = "Checkout"
        return render_template('checkout.html', products=products, quantities=quantities, category=category,
                               grand_total=grand_total, count=cart_count,info=info,
                               title=title, wishlist_count=wishlist_count, total=total)


@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['customerName']
        email = request.form['customerEmail']
        subject = request.form['contactSubject']
        message = request.form['contactMessage']
        info = Contact(email=email, message=message, name=name, subject=subject)
        db.session.add(info)
        db.session.commit()
        mail.send_message(subject,
                          sender=email,
                          recipients=["bitf16a022@gmail.com"],
                          body=message + '\n\nRegards,' + '\n' + name + '\n' + email + '\n\nThanks!')
        return "Sent"
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Contact Us"
    return render_template('contact-us.html', category=category, grand_total=grand_total, count=cart_count, title=title,
                           wishlist_count=wishlist_count)


@app.route('/phone-verification', methods=['GET', 'POST'])
def phone_verification():
    if 'user' in session:
        return redirect('/')
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        customer_phone = request.form['phone']
        if customer_id and customer_phone:
            customer = Customer.query.filter_by(customer_id=customer_id).first()
            if not customer:
                customer = Customer(customer_id=customer_id, customer_phone=customer_phone)
                db.session.add(customer)
                db.session.commit()
            session['user'] = customer_id
            # Check for cart in session if it has products then add them in DB
            check_cart_in_session()
            # Check for wishlist in session if it has products then add them in DB
            check_wishlist_in_session()
            return "Success"
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Phone Verification"
    return render_template('phone-verification.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user')
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect('/my-account')
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Register"
    return render_template('phone-verification.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/my-account')
def my_account():
    if 'user' not in session:
        return redirect('/phone-verification')
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "My Account"
    return render_template('my-account.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/product-details/<string:prod_slug>')
def product_details(prod_slug):
    product = Product.query.filter_by(slug=prod_slug).first()
    subcategory = Subcategory.query.filter_by(subcategory_id=product.prod_subcategory_id).first()
    category = Category.query.filter_by(category_id=subcategory.category_id).first()
    pictures = Picture.query.all()

    pic = ""
    for picture in pictures:
        if product.picture_id == picture.picture_id:
            pic = picture

    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Product Details"
    return render_template('product-details.html', product=product, picture=pic, category=category,
                           subcategory=subcategory, grand_total=grand_total, count=cart_count, title=title,
                           wishlist_count=wishlist_count)


@app.route('/shop/<string:cate_slug>')
def shop(cate_slug):
    category = Category.query.filter_by(slug=cate_slug).first()
    subcategories = Subcategory.query.filter_by(category_id=category.category_id).all()
    products = Product.query.all()
    pictures = Picture.query.all()

    cate_products = []
    for subcategory in subcategories:
        for product in products:
            if product.prod_subcategory_id == subcategory.subcategory_id:
                cate_products.append(product)

    cate_products_pics = []
    for product in cate_products:
        for pic in pictures:
            if product.picture_id == pic.picture_id:
                cate_products_pics.append(pic)

    total_prods = len(cate_products)
    per_page = 9
    number_of_pages = ceil(len(cate_products) / per_page) + 1
    if number_of_pages == 1:
        number_of_pages += 1
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    start_val = (page - 1) * per_page
    end_val = ((page - 1) * per_page) + per_page
    if end_val > total_prods:
        end_val = total_prods
    cate_products = cate_products[start_val:end_val]
    if not len(products) == 0:
        start_val += 1
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Shop"
    return render_template('shop.html', category=category, subcategories=subcategories, products=cate_products,
                           pictures=cate_products_pics, number_of_pages=number_of_pages, total_prods=total_prods,
                           start_val=start_val, end_val=end_val, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/subshop/<string:cate_slug>/<string:subcate_slug>')
def Shopwithsubcategory(cate_slug, subcate_slug):
    category = Category.query.filter_by(slug=cate_slug).first()
    subcategories = Subcategory.query.filter_by(category_id=category.category_id).all()
    subcategory = Subcategory.query.filter_by(slug=subcate_slug).first()
    products = Product.query.filter_by(prod_subcategory_id=subcategory.subcategory_id).all()
    pictures = Picture.query.all()

    subcate_products_pics = []
    for product in products:
        for pic in pictures:
            if product.picture_id == pic.picture_id:
                subcate_products_pics.append(pic)

    total_prods = len(products)
    per_page = 9
    number_of_pages = ceil(len(products) / per_page) + 1
    if number_of_pages == 1:
        number_of_pages += 1
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    start_val = (page - 1) * per_page
    end_val = ((page - 1) * per_page) + per_page
    if end_val > total_prods:
        end_val = total_prods
    products = products[start_val:end_val]
    if not len(products) == 0:
        start_val += 1
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Shop"
    return render_template('subshop.html', category=category, subcategories=subcategories, subcategory=subcategory,
                           products=products, pictures=subcate_products_pics, number_of_pages=number_of_pages,
                           total_prods=total_prods, start_val=start_val, end_val=end_val, grand_total=grand_total,
                           count=cart_count, wishlist_count=wishlist_count, title=title)


@app.route('/privacy-policy')
def privacy_policy():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Privacy Policy"
    return render_template('privacy-policy.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/about-us')
def about_us():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "About Us"
    return render_template('about-us.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/careers')
def careers():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Careers"
    return render_template('careers.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/return-n-refunds')
def return_n_refunds():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Return n Refunds"
    return render_template('return-n-refunds.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/delivery')
def delivery():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Delivery"
    return render_template('delivery.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/faqs')
def faqs():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "FAQs"
    return render_template('faqs.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/how-to-order')
def how_to_order():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "How to Order"
    return render_template('how-to-order.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/how-to-pay')
def how_to_pay():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "How to Pay"
    return render_template('how-to-pay.html', category=category, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count, title=title)


@app.route('/terms-n-conditions')
def terms_n_conditions():
    categories = Category.query.all()
    category = categories[0]
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    title = "Terms and Conditions"
    return render_template('terms-n-conditions.html', category=category, grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count, title=title)


def mergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


def cartItemsAndPrice():
    if 'Shoppingcart' in session:
        cart_count = len(session['Shoppingcart'])
        if len(session['Shoppingcart']) <= 0:
            return 0, 0, 0
        else:
            total_price_of_all_prods = []
            for key, item in session['Shoppingcart'].items():
                product = Product.query.filter_by(product_id=key).first()
                res = int(item['quantity']) * product.product_price
                total_price_of_all_prods.append(res)
            grand_total = sum(total_price_of_all_prods)
            return cart_count, total_price_of_all_prods, grand_total
    else:
        return 0, 0, 0


def wishListCount():
    if 'Wishlist' in session:
        wishlist_count = len(session['Wishlist'])
        if len(session['Wishlist']) <= 0:
            return 0
        else:
            return wishlist_count
    else:
        return 0


def check_cart_in_session():
    if 'Shoppingcart' in session:
        prods = []
        quantities = []
        for key, item in session['Shoppingcart'].items():
            quantity = item['quantity']
            quantities.append(quantity)
            product = Product.query.filter_by(product_id=key).first()
            prods.append(product)
        session.pop('Shoppingcart')
        for index in range(0, len(prods)):
            cart = Cart.query.filter_by(product_id=prods[index].product_id, customer_id=session['user']).first()
            if not cart:
                cart = Cart(customer_id=session['user'], product_id=prods[index].product_id,
                            product_quantity=quantities[index])
                db.session.add(cart)
                db.session.commit()


def check_wishlist_in_session():
    if 'Wishlist' in session:
        prods = []
        for product_id in session['Wishlist']:
            product = Product.query.filter_by(product_id=product_id).first()
            prods.append(product)
        session.pop('Wishlist')
        for prod in prods:
            wishlist = Wishlist.query.filter_by(product_id=prod.product_id, customer_id=session['user']).first()
            if not wishlist:
                wishlist = Wishlist(customer_id=session['user'], product_id=prod.product_id)
                db.session.add(wishlist)
                db.session.commit()




@app.route('/mobileCart', methods=['GET', 'POST', 'DELETE'])
def mobileCart():
    if request.method == "POST":
        total_products = request.form.get['total_products']
        sub_total = request.form.get['sub_total']
        delivery_charges = request.form.get['delivery_charges']
        prod_id = request.form.get['prod_id']
        show_Items = {prod_id: {'total_products': total_products}}

        if 'MyCart' in session:
            if prod_id in session['MyCart']:
                print("Product already exists")
            if len(session['MyCart']) <= 0:
                return redirect('/')
        else:
            session['MyCart'] = show_Items

        mob_pictures = Picture.query.all()
        mob_products = []
        total_quantity = []
        for key, product in session['MyCart'].product():
            total_quantities = product['quantity']
            total_quantity.append(total_quantities)
            mob_product = Product.query.filter_by(prod_id=key).first()
            mob_products.append(mob_product)
        cart_pictures = []
        for product in mob_products:
            for pic in mob_pictures:
                if product.picture_id == pic.picture_id:
                    cart_pictures.append(pic)
        return jsonify(total_quantity=total_products, grand_total=sub_total, delivery_charges=delivery_charges,
                       pic=mob_pictures, product=mob_products)



@app.route('/DeletefromMobCart', methods=['DELETE'])
def DeletefromMobCart():
    if request.method == 'DELETE':
        prod_id = request.form.get['product_id']
        print(session['MyCart'])
        try:
            session.modified = True
            for key, product in session['MyCart'].product():
                if key == prod_id:
                    session['MyCart'].remove(key)
                    return "Product Removed"
        except Exception as e:
            print(e)


@app.route('/mobileMainCtaegory', methods=['GET'])
def mobileMainCategory():
    categories = Category.query.all()
    pictures = Picture.query.all()
    category_images = []
    for category in categories:
        for picture in pictures:
            if category.picture_id == picture.picture_id:
                category_images.append(picture)
    cart_count, totals, grand_total = cartItemsAndPrice()
    return jsonify(categories=categories, pictures=pictures, category_images=category_images, grand_total=grand_total,
                   count=cart_count)


@app.route('/mobileProduct/<string:cate_slug>')
def mobileProduct(cate_slug):
    category = Category.query.filter_by(slug=cate_slug).first()
    subcategories = Subcategory.query.filter_by(category_id=category.category_id).all()
    products = Product.query.all()
    pictures = Picture.query.all()

    cate_products = []
    for subcategory in subcategories:
        for product in products:
            if product.prod_subcategory_id == subcategory.subcategory_id:
                cate_products.append(product)

    cate_products_pics = []
    for product in cate_products:
        for pic in pictures:
            if product.picture_id == pic.picture_id:
                cate_products_pics.append(pic)

    total_prods = len(cate_products)
    cart_count, totals, grand_total = cartItemsAndPrice()
    return jsonify(category=category, subcategories=subcategories, products=cate_products,
                   pictures=cate_products_pics, total_prods=total_prods, grand_total=grand_total, count=cart_count)


@app.route('/mobileProduct-details/<string:prod_slug>')
def mobileProduct_details(prod_slug):
    product = Product.query.filter_by(slug=prod_slug).first()
    subcategory = Subcategory.query.filter_by(subcategory_id=product.prod_subcategory_id).first()
    category = Category.query.filter_by(category_id=subcategory.category_id).first()
    pictures = Picture.query.all()

    pic = ""
    for picture in pictures:
        if product.picture_id == picture.picture_id:
            pic = picture

    cart_count, totals, grand_total = cartItemsAndPrice()

    return jsonify(product=product, picture=pic, category=category,
                   subcategory=subcategory, grand_total=grand_total, count=cart_count)


@app.route('/mobileLogin', methods=['POST'])
def mobileLogin():
    customer_phone = request.form.get('PhoneNo')
    customer = Customer.query.filter_by(PhoneNo=customer_phone)
    if customer:
        flash('Number Already Exists')
        cart_count, totals, grand_total = cartItemsAndPrice()
        return jsonify('/main.xml', grand_total=grand_total, count=cart_count)
    else:
        return jsonify('/verification.xml')


if __name__ == '__main__':
    # manager.run()
    app.run(host='localhost', port=8080, debug=True)
