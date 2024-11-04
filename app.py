from flask import *
from peewee import *

db = SqliteDatabase('store.db')





class User(Model):
    username=CharField(unique=True)
    password=TextField()

    class Meta:
        database=db
        db_table='کاربران'



class Product(Model):
    name=CharField(unique=True)
    price=FloatField()

    class Meta:
        database=db
        db_table='کالا'

        

class Cart(Model):
    user=ForeignKeyField(User,backref='carts')
    product=ForeignKeyField(Product,backref='carts')

    class Meta:
        database=db
        db_table='خرید ها'



with db:
    db.create_tables([User,Product,Cart])
    

app = Flask(__name__)
app.secret_key = '1'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create(username=username, password=password)
        return redirect(url_for('log_in'))
    return render_template('sign in.html')

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_or_none(User.username == username, User.password == password)
        if user:
            session['user_id'] = user.id
            if username == 'kourosh' and password == '123':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('products'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        Product.create(name=name, price=price)
    products = Product.select()
    return render_template('admin.html', products=products)

@app.route('/products')
def products():
    products = Product.select()
    return render_template('products.html', products=products)


@app.route('/delete_product', methods=['GET', 'POST'])
def deletep():
    if request.method == 'POST':
        product_id=request.form['product_id']
        product=Product.get_or_none(Product.id==product_id)
        if product:
            product.delete_instance()
        return redirect(url_for('index'))    
    return render_template('delete product.html')



@app.route('/delete_user', methods=['GET', 'POST'])
def deleteu():
    if request.method == 'POST':
        user_id=request.form['user_id']
        user=User.get_or_none(User.id==user_id)
        if user:
            user.delete_instance()
        return redirect(url_for('index'))    
    return render_template('delete user.html')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' in session:
        user = User.get(User.id == session['user_id'])
        product = Product.get(Product.id == product_id)
        Cart.create(user=user, product=product)
        return redirect(url_for('products'))
    return redirect(url_for('log_in'))

if __name__ == '__main__':
    app.run(debug=True)
