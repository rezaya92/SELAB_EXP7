from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/prescription.db'
db = SQLAlchemy(app)


def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_national_id = db.Column(db.Integer, nullable=False)
    patient_national_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Prescription id: %r>' % self.id
    
    @property
    def serialize(self):
       return {
           'id'         : self.id,
           'doctor_national_id': self.doctor_national_id,
           'patient_national_id': self.patient_national_id,
           'description': self.description,
           'issued_at': dump_datetime(self.issued_at)
       }


if __name__ == "__main__":
    app.run(debug=True, port=9000)
