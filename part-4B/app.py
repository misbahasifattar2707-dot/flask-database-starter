# from flask import Flask, jsonify, request, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # ------------------ MODELS ------------------

# class Author(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     country = db.Column(db.String(100))

#     books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete")

# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     year = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

# # ------------------ UI ROUTE ------------------

# @app.route('/')
# def home():
#     search = request.args.get('search')
#     if search:
#         books = Book.query.join(Author).filter(
#             (Book.title.ilike(f"%{search}%")) | (Author.name.ilike(f"%{search}%"))
#         ).all()
#     else:
#         books = Book.query.all()

#     authors = Author.query.all()
#     return render_template('index.html', books=books, authors=authors)

# # ------------------ AUTHOR ROUTES ------------------

# @app.route('/author/add', methods=['POST'])
# def add_author():
#     name = request.form['name']
#     country = request.form.get('country')
#     author = Author(name=name, country=country)
#     db.session.add(author)
#     db.session.commit()
#     return jsonify(success=True)

# @app.route('/author/delete/<int:id>', methods=['DELETE'])
# def delete_author(id):
#     author = Author.query.get_or_404(id)
#     db.session.delete(author)
#     db.session.commit()
#     return jsonify(success=True)

# # ------------------ BOOK ROUTES ------------------

# @app.route('/book/add', methods=['POST'])
# def add_book():
#     title = request.form['title']
#     year = request.form.get('year')
#     author_name = request.form['author']

#     author = Author.query.filter_by(name=author_name).first()
#     if not author:
#         author = Author(name=author_name)
#         db.session.add(author)
#         db.session.commit()

#     book = Book(title=title, year=year, author_id=author.id)
#     db.session.add(book)
#     db.session.commit()
#     return jsonify(success=True)

# @app.route('/book/delete/<int:id>', methods=['DELETE'])
# def delete_book(id):
#     book = Book.query.get_or_404(id)
#     db.session.delete(book)
#     db.session.commit()
#     return jsonify(success=True)

# # ------------------ API ROUTES ------------------

# @app.route('/api/books', methods=['GET'])
# def api_get_books():
#     books = Book.query.all()
#     data = []
#     for book in books:
#         data.append({
#             "id": book.id,
#             "title": book.title,
#             "year": book.year,
#             "author": book.author.name if book.author else None,
#             "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S")
#         })
#     return jsonify(data)

# @app.route('/api/authors', methods=['GET'])
# def api_get_authors():
#     authors = Author.query.all()
#     data = []
#     for author in authors:
#         data.append({
#             "id": author.id,
#             "name": author.name,
#             "country": author.country,
#             "books": [book.title for book in author.books]
#         })
#     return jsonify(data)

# @app.route('/api/book/<int:id>', methods=['GET'])
# def api_get_book(id):
#     book = Book.query.get_or_404(id)
#     return jsonify({
#         "id": book.id,
#         "title": book.title,
#         "year": book.year,
#         "author": book.author.name if book.author else None,
#         "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S")
#     })

# @app.route('/api/author/<int:id>', methods=['GET'])
# def api_get_author(id):
#     author = Author.query.get_or_404(id)
#     return jsonify({
#         "id": author.id,
#         "name": author.name,
#         "country": author.country,
#         "books": [book.title for book in author.books]
#     })

# # ------------------ INIT DB ------------------

# with app.app_context():
#     db.create_all()

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ MODELS ------------------

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))

    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

# ------------------ UI ROUTE ------------------

@app.route('/')
def home():
    search = request.args.get('search', '').strip()

    if search:
        # Search by book title OR author name
        books = Book.query.options(joinedload(Book.author)).join(Author).filter(
            (Book.title.ilike(f"%{search}%")) | (Author.name.ilike(f"%{search}%"))
        ).all()
    else:
        books = Book.query.options(joinedload(Book.author)).all()

    authors = Author.query.all()
    return render_template('index.html', books=books, authors=authors, search=search)

# ------------------ AUTHOR ROUTES ------------------

@app.route('/author/add', methods=['POST'])
def add_author():
    name = request.form['name']
    country = request.form.get('country')
    author = Author(name=name, country=country)
    db.session.add(author)
    db.session.commit()
    return jsonify(success=True)

@app.route('/author/delete/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify(success=True)

# ------------------ BOOK ROUTES ------------------

@app.route('/book/add', methods=['POST'])
def add_book():
    title = request.form['title']
    year = request.form.get('year')
    author_name = request.form['author']

    author = Author.query.filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

    book = Book(title=title, year=year, author_id=author.id)
    db.session.add(book)
    db.session.commit()
    return jsonify(success=True)

@app.route('/book/delete/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify(success=True)

# ------------------ API ROUTES ------------------

@app.route('/api/books', methods=['GET'])
def api_get_books():
    books = Book.query.options(joinedload(Book.author)).all()
    data = []
    for book in books:
        data.append({
            "id": book.id,
            "title": book.title,
            "year": book.year,
            "author": book.author.name if book.author else None,
            "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(data)

@app.route('/api/authors', methods=['GET'])
def api_get_authors():
    authors = Author.query.all()
    data = []
    for author in authors:
        data.append({
            "id": author.id,
            "name": author.name,
            "country": author.country,
            "books": [book.title for book in author.books]
        })
    return jsonify(data)

@app.route('/api/book/<int:id>', methods=['GET'])
def api_get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        "id": book.id,
        "title": book.title,
        "year": book.year,
        "author": book.author.name if book.author else None,
        "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/author/<int:id>', methods=['GET'])
def api_get_author(id):
    author = Author.query.get_or_404(id)
    return jsonify({
        "id": author.id,
        "name": author.name,
        "country": author.country,
        "books": [book.title for book in author.books]
    })

# ------------------ INIT DB ------------------

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
