from math import *
from random import randint

from flask import *
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://plbsmnpyhgnfkx:900ff23b99965614d20deeb707307f2add036274c83463f95e64dbff0384968b@ec2-107-20-234-175.compute-1.amazonaws.com:5432/d1hntjbagjg4ro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

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
    customer_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)
    total_cost = db.Column(db.String(200))


@app.route('/')
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

    return render_template('index.html', categories=categories, pictures=pictures, products=products,
                           best_seller_products_categories=best_seller_products_categories,
                           index=best_seller_products_cat_index,
                           best_seller_products=best_seller_products,
                           best_seller_products_images=best_seller_products_images)


@app.route('/about-us')
def about_us():
    return render_template('about-us.html')


@app.route('/careers')
def careers():
    return render_template('careers.html')


@app.route('/cart/<int:prod_id>', methods=['GET', 'POST'])
def cart(prod_id):
    if request.method == 'POST':
        return
        # products = Cart.query.all()
        # cart = Cart(customer_id=1, product_id=prod_id, product_quantity=1, total_cost=100)
        # db.session.add(cart)
        # db.session.commit()
        # print(len(products))
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/compare')
def compare():
    return render_template('compare.html')


@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')


@app.route('/delivery')
def delivery():
    return render_template('delivery.html')


@app.route('/faqs')
def faqs():
    return render_template('faqs.html')


@app.route('/how-to-order')
def how_to_order():
    return render_template('how-to-order.html')


@app.route('/how-to-pay')
def how_to_pay():
    return render_template('how-to-pay.html')


@app.route('/login-register')
def login_register():
    return render_template('login-register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect('/my-account')
    return render_template('login-register.html')


@app.route('/my-account')
def my_account():
    return render_template('my-account.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


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

    return render_template('product-details.html', product=product, picture=pic, category=category,
                           subcategory=subcategory)


@app.route('/return-n-refunds')
def return_n_refunds():
    return render_template('return-n-refunds.html')


@app.route('/shop/<string:cate_slug>')
def shop(cate_slug):
    category = Category.query.filter_by(slug=cate_slug).first()
    subcategories = Subcategory.query.filter_by(category_id=category.category_id).all()
    products = Product.query.all()
    pictures = Picture.query.all()

    print("Category: ", category)
    print("Subcategories: ", subcategories)

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

    print(len(cate_products), len(cate_products_pics))
    total_prods = len(cate_products)
    per_page = 9
    number_of_pages = ceil(len(cate_products) / per_page)
    print(number_of_pages)
    if not number_of_pages == 1:
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

    return render_template('shop.html', category=category, subcategories=subcategories, products=cate_products,
                           pictures=cate_products_pics, number_of_pages=number_of_pages, total_prods=total_prods,
                           start_val=start_val, end_val=end_val)


@app.route('/terms-n-conditions')
def terms_n_conditions():
    return render_template('terms-n-conditions.html')


@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')


if __name__ == '__main__':
    # manager.run()
    app.run(host='localhost', port=8080, debug=True)
