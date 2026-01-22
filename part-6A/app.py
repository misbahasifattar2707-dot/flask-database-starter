# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # =========================
# # MODEL
# # =========================
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)

# with app.app_context():
#     db.create_all()

# # =========================
# # ROUTES
# # =========================

# @app.route('/')
# def index():
#     products = Product.query.all()
#     return render_template('index.html', products=products)

# @app.route('/add', methods=['GET', 'POST'])
# def add_product():
#     if request.method == 'POST':
#         product = Product(
#             name=request.form['name'],
#             quantity=int(request.form['quantity']),
#             price=float(request.form['price'])
#         )
#         db.session.add(product)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('add.html')

# @app.route('/edit/<int:id>', methods=['GET', 'POST'])
# def edit_product(id):
#     product = Product.query.get_or_404(id)

#     if request.method == 'POST':
#         product.name = request.form['name']
#         product.quantity = int(request.form['quantity'])
#         product.price = float(request.form['price'])

#         db.session.commit()
#         return redirect(url_for('index'))

#     return render_template('edit.html', product=product)

# @app.route('/delete/<int:id>')
# def delete_product(id):
#     product = Product.query.get_or_404(id)
#     db.session.delete(product)
#     db.session.commit()
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# MODEL
# =========================
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

# =========================
# WEB ROUTES
# =========================

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            quantity=int(request.form['quantity']),
            price=float(request.form['price'])
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = int(request.form['quantity'])
        product.price = float(request.form['price'])
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', product=product)

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

# =========================
# API ROUTE (JSON)
# =========================

@app.route('/api/products', methods=['GET'])
def get_products_api():
    products = Product.query.all()

    data = []
    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "price": p.price
        })

    return jsonify({
        "status": "success",
        "count": len(data),
        "products": data
    })

# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)
