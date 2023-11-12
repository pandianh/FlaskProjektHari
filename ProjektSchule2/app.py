from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Beispiel Daten (könnten durch eine Datenbank ersetzt werden)
books = [
    {"id": 1, "title": "Der Herr der Ringe", "author": "J.R.R. Tolkien", "genre": "Fantasy"},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian"},
    {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction"},
]


# Routen für die Anwendung
@app.route('/')
def home():
    return render_template('home_books.html', books=books)


@app.route('/book/<int:book_id>')
def view_book(book_id):
    book = get_book_by_id(book_id)
    if book:
        return render_template('view_book.html', book=book)
    else:
        return "Book not found"


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        new_book = {"id": len(books) + 1, "title": title, "author": author, "genre": genre}
        books.append(new_book)
        return redirect(url_for('home'))
    return render_template('add_book.html')


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found"

    if request.method == 'POST':
        book['title'] = request.form['title']
        book['author'] = request.form['author']
        book['genre'] = request.form['genre']
        return redirect(url_for('view_book', book_id=book_id))

    return render_template('edit_book.html', book=book)


@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found"

    books.remove(book)
    return redirect(url_for('home'))


def get_book_by_id(book_id):
    for book in books:
        if book['id'] == book_id:
            return book
    return None


if __name__ == '__main__':
    app.run(debug=True)