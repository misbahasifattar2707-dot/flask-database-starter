from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ MODELS ------------------

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))

    books = db.relationship('Book', backref='author', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country
        }

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
           "author": self.author.name if self.author else None
           #"created_at": self.created_at.isoformat()

        }

# ------------------ UI ------------------

@app.route('/')
def home():
    return render_template('index.html')

# ------------------ AUTHOR APIs ------------------

@app.route('/api/authors', methods=['GET'])
def get_authors():
    return jsonify([a.to_dict() for a in Author.query.all()])

@app.route('/api/authors', methods=['POST'])
def add_author():
    data = request.get_json()
    author = Author(name=data['name'], country=data.get('country'))
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_dict()), 201

# ------------------ BOOK APIs ------------------

@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify([b.to_dict() for b in Book.query.all()])

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = Book(
        title=data['title'],
        year=data.get('year'),
        author_id=data['author_id']
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

# @app.route('/api/books', methods=['POST'])
# def add_book():
#     data = request.get_json()

#     author_name = data.get('author')

#     if not author_name:
#         return jsonify({"error": "Author name is required"}), 400

#     # 🔍 Check if author already exists
#     author = Author.query.filter_by(name=author_name).first()

#     # ➕ Create author if not exists
#     if not author:
#         author = Author(name=author_name)
#         db.session.add(author)
#         db.session.commit()

#     book = Book(
#         title=data['title'],
#         year=data.get('year'),
#         author_id=author.id
#     )

#     db.session.add(book)
#     db.session.commit()

#     return jsonify(book.to_dict()), 201

# ------------------ INIT DB ------------------

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
