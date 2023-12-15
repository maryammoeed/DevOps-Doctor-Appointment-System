from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://mongodb-service:27017/')
db = client['appointments_db']
appointments_collection = db['appointments']

# Initial bootstrapping
initial_appointments = [
    {'id': "1", 'doctor': "1", 'date': "21 Nov 2023", 'rating': "Good"},
    {'id': "2", 'doctor': "1", 'date': "22 Nov 2023", 'rating': "Bad"},
    {'id': "3", 'doctor': "2", 'date': "22 Nov 2023", 'rating': "Good"},
    {'id': "4", 'doctor': "1", 'date': "22 Nov 2023", 'rating': "Bad"},
    {'id': "5", 'doctor': "2", 'date': "22 Nov 2023", 'rating': "Good"},
    {'id': "6", 'doctor': "3", 'date': "23 Nov 2023", 'rating': "Excellent"},
    {'id': "7", 'doctor': "2", 'date': "23 Nov 2023", 'rating': "Good"},
    {'id': "8", 'doctor': "3", 'date': "24 Nov 2023", 'rating': "Bad"},
]

# Insert initial values if the collection is empty
if appointments_collection.count_documents({}) == 0:
    appointments_collection.insert_many(initial_appointments)

@app.route('/hello')
def hello():
    greeting = "HELLO WORLD!"
    return greeting

@app.route('/appointments', methods=["GET"])
def get_appointments():
    appointments_list = list(appointments_collection.find({}, {'_id': False}))
    return jsonify(appointments_list)

@app.route('/appointment/<appointment_id>', methods=["GET"])
def get_appointment(appointment_id):
    appointment = appointments_collection.find_one({'id': appointment_id}, {'_id': False})
    if appointment:
        return jsonify(appointment)
    else:
        return jsonify({'error': 'Appointment not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7070)
