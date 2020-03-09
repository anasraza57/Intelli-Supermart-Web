from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin1@mysingleserver:Tempass12@mysingleserver.postgres.database.azure.com:5432/intellisupermart'
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
    description = db.Column(db.String(1000))
    picture_id = db.Column(db.Integer)
    product_quantity = db.Column(db.String(20))
    prod_subcategory_id = db.Column(db.Integer)


@app.route('/')
def index():
    products = Product.query.all()
    print(len(products))
    return render_template('index.html')


@app.route('/about-us')
def about_us():
    return render_template('about-us.html')


@app.route('/careers')
def careers():
    return render_template('careers.html')


@app.route('/cart')
def cart():
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


@app.route('/my-account')
def my_account():
    return render_template('my-account.html')


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@app.route('/product-details')
def product_details():
    return render_template('product-details.html')


@app.route('/return-n-refunds')
def return_n_refunds():
    return render_template('return-n-refunds.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/terms-n-conditions')
def terms_n_conditions():
    return render_template('terms-n-conditions.html')


@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')


if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)