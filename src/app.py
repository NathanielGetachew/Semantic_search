from flask import Flask, render_template, request, jsonify
from search_engine import search_products, get_user_search_history

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_id = data.get('user_id', 'guest')
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query cannot be empty'}), 400
    
    results = search_products(user_id, query)
    history = get_user_search_history(user_id)
    
    return jsonify({'results': results, 'history': history})

@app.route('/chat', methods=['GET'])
def get_chat_history():
    user_id = request.args.get('user_id', 'guest')
    history = get_user_search_history(user_id)
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True)
