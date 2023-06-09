from flask import Flask, request, jsonify
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# In-memory data store
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"},
    {"id": 3, "title": "Book 3", "author": "Author 3"}
]

# Create a counter metric for total number of HTTP requests
requests_total = Counter('http_requests_total', 'Total Number of HTTP Requests')

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    requests_total.inc()
    return jsonify(books)

# Route to get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    requests_total.inc()
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

# Route to create a new book
@app.route('/books', methods=['POST'])
def create_book():
    requests_total.inc()
    new_book = {
        'id': len(books) + 1,
        'title': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    return jsonify(new_book), 201

# Route to update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    requests_total.inc()
    for book in books:
        if book['id'] == book_id:
            book['title'] = request.json['title']
            book['author'] = request.json['author']
            return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

# Route to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    requests_total.inc()
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({'message': 'Book deleted'})
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    # Create a WSGI app to serve both the Flask app and Prometheus metrics
    app_dispatch = DispatcherMiddleware(app, {
        '/metrics': make_wsgi_app()
    })
    
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
