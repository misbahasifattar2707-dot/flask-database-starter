from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from models import db, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --------------------------------------------------
# EXISTING UI ROUTES (UNCHANGED)
# --------------------------------------------------

@app.route('/')
def index():
    authors = Author.query.all()
    books = Book.query.options(joinedload(Book.author)).all()
    return render_template('index.html', authors=authors, books=books)

@app.route('/add-author', methods=['POST'])
def add_author():
    name = request.form['name']
    db.session.add(Author(name=name))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add-book', methods=['POST'])
def add_book():
    title = request.form['title']
    year = request.form['year']
    author_id = request.form['author_id']

    db.session.add(Book(title=title, year=year, author_id=author_id))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-book/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete-author/<int:id>')
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('index'))

# --------------------------------------------------
# DASHBOARD API
# --------------------------------------------------
@app.route('/api/dashboard')
def dashboard_api():
    return jsonify({
        "total_books": Book.query.count(),
        "total_authors": Author.query.count()
    })

# --------------------------------------------------
# BOOK API (PAGINATION + SORTING)
# --------------------------------------------------
# /api/books?page=1&per_page=5&sort=title&order=asc

@app.route('/api/books')
def books_api():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    column = getattr(Book, sort, Book.id)
    if order == 'desc':
        column = column.desc()

    pagination = Book.query.options(joinedload(Book.author)) \
        .order_by(column) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": pagination.total,
        "page": page,
        "books": [
            {
                "id": b.id,
                "title": b.title,
                "year": b.year,
                "author": b.author.name if b.author else "-"
            }
            for b in pagination.items
        ]
    })

# --------------------------------------------------
# ✅ AUTHOR API (THIS WAS MISSING)
# --------------------------------------------------

# 1️⃣ Get all authors
@app.route('/api/authors')
def authors_api():
    authors = Author.query.all()
    return jsonify([
        {
            "id": a.id,
            "name": a.name,
            "total_books": len(a.books)
        }
        for a in authors
    ])

# 2️⃣ Get authors with pagination
# /api/authors?page=1&per_page=5
@app.route('/api/authors/paginated')
def authors_paginated_api():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    pagination = Author.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "total": pagination.total,
        "page": page,
        "authors": [
            {
                "id": a.id,
                "name": a.name,
                "total_books": len(a.books)
            }
            for a in pagination.items
        ]
    })

# --------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
