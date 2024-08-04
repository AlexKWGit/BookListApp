from flask import Flask, request, jsonify
import mysql.connector

# Версия приложения
APP_VERSION = "1.0.0"

# Подключение к базе данных
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="book_catalog"
)

app = Flask(__name__)

# Создание таблицы, если она еще не существует
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

# Добавление книги
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data['title']
    author = data['author']
    year = data['year']
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
    db.commit()
    
    return jsonify({'message': 'Book added successfully'}), 201

# Удаление книги
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    db.commit()
    
    return jsonify({'message': 'Book deleted successfully'}), 200

# Получение списка книг
@app.route('/books', methods=['GET'])
def get_books():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    response = {
        'version': APP_VERSION,
        'books': []
    }
    
    for book in books:
        response['books'].append({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'year': book[3]
        })
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)