from extensions import db
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import event
from models.results import Result
class Machine(db.Model):
    __tablename__ = 'machine'

    id = db.Column(db.Integer(), primary_key=True)
    machine_code = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)
    updated_date = db.Column(db.DateTime(), nullable=True)
    updated_by = db.Column(db.Integer(), nullable=True)
    is_deleted = db.Column(db.Boolean(), nullable=True, default=False)
    machine_password = db.Column(db.String(255), nullable=False)
    machine_description = db.Column(db.String(255), nullable=True)
    machine_profile_img = db.Column(db.String(255), nullable=True)
    machine_name = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Machine {self.machine_code} {self.id}>'

    def __init__(self, machine_name,machine_code, created_by,updated_by, machine_password,machine_description,machine_profile_img):
        self.machine_code = machine_code
        self.machine_name = machine_name
        self.created_by = created_by
        self.created_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.updated_by = updated_by
        self.is_deleted = False 
        self.machine_password = machine_password
        self.machine_description = machine_description
        self.machine_profile_img = machine_profile_img

    def to_dict(self):
        return {
            "id": self.id,
            "machine_name": self.machine_name,
            "machine_code": self.machine_code,
            "created_by": self.created_by,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
            "updated_by": self.updated_by,
            "is_deleted": self.is_deleted,
            "machine_description": self.machine_description,
            "machine_profile_img": self.machine_profile_img
        }
        
# @event.listens_for(Machine, 'after_insert')
# def create_result_after_machine_insert(mapper, connection, target):
#     result = Result(
#         machine_id=target.id,
#         created_date=datetime.datetime.now(),
#         is_deleted=False,
#         total_strips=0,
#         faulty_strips=0,
#         non_faulty_strips=0
#     )
#     db.session.add(result)
