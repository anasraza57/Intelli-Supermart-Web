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
    product_id = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)


def cartItemsAndPrice():
    return 0,0,0
    # cart_count = len(session['Shoppingcart'])
    # if len(session['Shoppingcart']) <= 0:
    #     return 0, 0, 0
    # else:
    #     total_price_of_all_prods = []
    #     for key, item in session['Shoppingcart'].items():
    #         product = Product.query.filter_by(product_id=key).first()
    #         res = int(item['quantity']) * product.product_price
    #         total_price_of_all_prods.append(res)
    #     grand_total = sum(total_price_of_all_prods)
    #     return cart_count, total_price_of_all_prods, grand_total


def wishListCount():
    wishlist_count = len(session['Wishlist'])
    if len(session['Wishlist']) <= 0:
        return 0
    else:
        return wishlist_count


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
    return render_template('index.html', categories=categories, pictures=pictures, products=products,
                           best_seller_products_categories=best_seller_products_categories,
                           index=best_seller_products_cat_index, grand_total=grand_total,
                           best_seller_products=best_seller_products,
                           best_seller_products_images=best_seller_products_images, count=cart_count,
                           wishlist_count=wishlist_count)


@app.route('/about-us')
def about_us():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('about-us.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/careers')
def careers():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('careers.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


def mergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


# @app.route('/cart', methods=['GET', 'POST', 'DELETE'])
# def cart():
#     if request.method == 'POST':
#         product_id = request.form['product_id']
#         quantity = request.form['quantity']
#         DictItems = {product_id: {'quantity': quantity}}
#
#         if 'Shoppingcart' in session:
#             if product_id in session['Shoppingcart']:
#                 print("This product is already in cart!")
#             else:
#                 session['Shoppingcart'] = mergeDict(session['Shoppingcart'], DictItems)
#             # return redirect(request.referrer)
#         else:
#             session['Shoppingcart'] = DictItems
#             # return redirect(request.referrer)
#
#     if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
#         return redirect('/')
#     else:
#         pictures = Picture.query.all()
#         subcategories = Subcategory.query.all()
#         categories = Category.query.all()
#         category = categories[0]
#
#         products = []
#         quantities = []
#         for key, item in session['Shoppingcart'].items():
#             quantity = item['quantity']
#             quantities.append(quantity)
#             product = Product.query.filter_by(product_id=key).first()
#             products.append(product)
#         products.reverse()
#         cart_products_pics = []
#         for product in products:
#             for pic in pictures:
#                 if product.picture_id == pic.picture_id:
#                     cart_products_pics.append(pic)
#
#         cart_count, total, grand_total = cartItemsAndPrice()
#         wishlist_count = wishListCount()
#         return render_template('cart.html', products=products, pictures=cart_products_pics, category=category,
#                                subcategories=subcategories, categories=categories, quantities=quantities,
#                                total=total, grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)
#
#
# @app.route('/updateCart', methods=['PUT'])
# def updateCart():
#     if request.method == 'PUT':
#         quantity = int(request.form['quantity'])
#         id = int(request.form['id'])
#         session.modified = True
#         total_price_of_all_prods = []
#         total_prod_price = 0
#         for key, item in session['Shoppingcart'].items():
#             if int(key) == id:
#                 item['quantity'] = quantity
#                 product = Product.query.filter_by(product_id=id).first()
#                 total_prod_price = product.product_price * quantity
#             product = Product.query.filter_by(product_id=key).first()
#             res = int(item['quantity']) * product.product_price
#             total_price_of_all_prods.append(res)
#         grand_total = sum(total_price_of_all_prods)
#         return jsonify(
#             total=total_prod_price,
#             grand_total=grand_total,
#         )
#
#
# @app.route('/deleteFromCart', methods=['DELETE'])
# def deleteFromCart():
#     if request.method == 'DELETE':
#         id = int(request.form['product_id'])
#         print(session['Shoppingcart'])
#         print(id)
#         try:
#             session.modified = True
#             for key, item in session['Shoppingcart'].items():
#                 if int(key) == id:
#                     session['Shoppingcart'].pop(key, None)
#                     return "Deleted"
#         except Exception as e:
#             print(e)


@app.route('/wishlist', methods=['GET', 'POST', 'DELETE'])
def wishlist():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        ListItems = [product_id]
        if 'Wishlist' in session:
            if product_id in session['Wishlist']:
                print("This product is already in wishList!")
            else:
                session['Wishlist'] = mergeDict(session['Wishlist'], ListItems)
        else:
            session['Wishlist'] = ListItems
    if 'Wishlist' not in session or len(session['Wishlist']) <= 0:
        return redirect('/')
    else:
        pictures = Picture.query.all()
        subcategories = Subcategory.query.all()
        categories = Category.query.all()
        category = categories[0]  # for layout.html
        products = []
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
    return render_template('wishlist.html', products=products, pictures=wishlist_products_pics,
                           subcategories=subcategories, category=category, categories=categories,
                           grand_total=grand_total,
                           count=cart_count, wishlist_count=wishlist_count)


@app.route('/deleteFromWishlist', methods=['DELETE'])
def deleteFromWishlist():
    if request.method == 'DELETE':
        id = int(request.form['product_id'])
        try:
            session.modified = True
            for key in session['Wishlist']:
                if int(key) == id:
                    session['Wishlist'].remove(key)
                    return "Deleted"
        except Exception as e:
            print(e)


@app.route('/checkout')
def checkout():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('checkout.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/compare')
def compare():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('compare.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/contact-us')
def contact_us():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('contact-us.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/delivery')
def delivery():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('delivery.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/faqs')
def faqs():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('faqs.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/how-to-order')
def how_to_order():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('how-to-order.html', grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


@app.route('/how-to-pay')
def how_to_pay():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('how-to-pay.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/login-register')
def login_register():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('login-register.html', grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect('/my-account')
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('login-register.html', grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


@app.route('/my-account')
def my_account():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('my-account.html', grand_total=grand_total, count=cart_count, wishlist_count=wishlist_count)


@app.route('/privacy-policy')
def privacy_policy():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('privacy-policy.html', grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


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
    return render_template('product-details.html', product=product, picture=pic, category=category,
                           subcategory=subcategory, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


@app.route('/return-n-refunds')
def return_n_refunds():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('return-n-refunds.html', grand_total=grand_total, count=cart_count,
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
    return render_template('shop.html', category=category, subcategories=subcategories, products=cate_products,
                           pictures=cate_products_pics, number_of_pages=number_of_pages, total_prods=total_prods,
                           start_val=start_val, end_val=end_val, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


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
    return render_template('subshop.html', category=category, subcategories=subcategories, subcategory=subcategory, products=products,
                           pictures=subcate_products_pics, number_of_pages=number_of_pages, total_prods=total_prods,
                           start_val=start_val, end_val=end_val, grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


@app.route('/terms-n-conditions')
def terms_n_conditions():
    cart_count, totals, grand_total = cartItemsAndPrice()
    wishlist_count = wishListCount()
    return render_template('terms-n-conditions.html', grand_total=grand_total, count=cart_count,
                           wishlist_count=wishlist_count)


if __name__ == '__main__':
    # manager.run()
    app.run(host='localhost', port=8080, debug=True)
