from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'  # Change if needed
app.config['MYSQL_USER'] = 'root'       # Change if needed
app.config['MYSQL_PASSWORD'] = 'root'   # Change if needed
app.config['MYSQL_DB'] = 'book_management_system'  # Change to match your DB name

mysql = MySQL(app)

# Route to view all books (Home Page)
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    return render_template('index.html', books=books)

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    
    # GET request - render the add book form
    return render_template('add_book.html')

# Route to update book details
@app.route('/update_book/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        cur.execute("UPDATE books SET title=%s, author=%s, year=%s WHERE id=%s", (title, author, year, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM books WHERE id=%s", (id,))
    book = cur.fetchone()
    cur.close()
    
    return render_template('update_book.html', book=book)

# Route to delete a book
@app.route('/delete_book/<int:book_id>')
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM books WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# Route to show books list (book_list page)
@app.route('/book_list', methods=['GET', 'POST'])
def book_list():
    # Fetch all books
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()

    # Search functionality if a book ID is provided
    if request.method == 'POST':
        id = request.form['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE id=%s", (id,))
        books = cur.fetchall()
        cur.close()
        return render_template('book_list.html', books=books)
    
    return render_template('book_list.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
