from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    """Returns all messages ordered by created_at ascending"""
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_list = [message.to_dict() for message in messages]
    return make_response(jsonify(messages_list), 200)

@app.route('/messages', methods=['POST'])
def create_message():
    """Creates a new message"""
    data = request.get_json()
    
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return make_response(jsonify(new_message.to_dict()), 201)

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    """Updates a message's body"""
    message = Message.query.get(id)
    
    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)
    
    data = request.get_json()
    
    if 'body' in data:
        message.body = data['body']
        message.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return make_response(jsonify(message.to_dict()), 200)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    """Deletes a message"""
    message = Message.query.get(id)
    
    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)
    
    db.session.delete(message)
    db.session.commit()
    
    return make_response(jsonify({"message": "Message deleted successfully"}), 200)

if __name__ == '__main__':
    app.run(port=5555)