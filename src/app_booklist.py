from flask import Flask, request, jsonify
import mysql.connector

# Версия приложения
APP_VERSION = "1.0.0"

# Подключение к базе данных
def get_db_connection():
    db = mysql.connector.connect(
        host="192.168.202.5",
        port=3306,
        user="root",
        password="book",
        database="book_catalog"
    )
    return db

# Создание таблицы, если она еще не существует
def create_table_if_not_exists():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            year INT NOT NULL
        )
    """)
    db.commit()
    db.close()

# Добавление книги
def add_book(title, author, year):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
    db.commit()
    book_id = cursor.lastrowid
    db.close()
    return book_id

# Удаление книги
def delete_book(book_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    db.commit()
    db.close()

# Получение списка книг
def get_book_list():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    db.close()
    
    book_list = []
    for book in books:
        book_list.append({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'year': book[3]
        })
    return book_list

app = Flask(__name__)

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data['title']
    author = data['author']
    year = data['year']
    book_id = add_book(title, author, year)
    return jsonify({'message': 'Book added successfully', 'id': book_id}), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    delete_book(book_id)
    return jsonify({'message': 'Book deleted successfully'}), 200

@app.route('/books', methods=['GET'])
def list_books():
    book_list = get_book_list()
    response = {
        'version': APP_VERSION,
        'books': book_list
    }
    return jsonify(response)

if __name__ == '__main__':
    create_table_if_not_exists()
    app.run(debug=True)