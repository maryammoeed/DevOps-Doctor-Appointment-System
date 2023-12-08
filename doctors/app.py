from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://mongodb:27017/')  # Replace with your MongoDB connection string
db = client['doctors_db']
doctors_collection = db['doctors']

# Initial bootstrapping
initial_doctors = [
    {'id': "1", 'firstName': "Muhammad Ali", 'lastName': "Kahoot", 'speciality': "DevOps"},
    {'id': "2", 'firstName': "Good", 'lastName': "Doctor", 'speciality': "Test"},
    {'id': "3", 'firstName': "Areeba", 'lastName': "Ahsan", 'speciality': "Dermotology"},
    {'id': "4", 'firstName': "Daud", 'lastName': "Tariq", 'speciality': "Cardiology"},
    {'id': "5", 'firstName': "Maryam", 'lastName': "Moeed", 'speciality': "Data Science"}
]

# Insert initial values if the collection is empty
if doctors_collection.count_documents({}) == 0:
    doctors_collection.insert_many(initial_doctors)

@app.route('/hello')
def hello():
    greeting = "Hello world!"
    return greeting

@app.route('/doctors', methods=["GET"])
def get_doctors():
    doctors_list = list(doctors_collection.find({}, {'_id': False}))
    return jsonify(doctors_list)

@app.route('/doctor/<doctor_id>', methods=["GET"])
def get_doctor(doctor_id):
    doctor = doctors_collection.find_one({'id': doctor_id}, {'_id': False})
    if doctor:
        return jsonify(doctor)
    else:
        return jsonify({'error': 'Doctor not found'}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
