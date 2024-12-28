from extensions import db

class UserMachine(db.Model):
    __tablename__ = 'user_machine'
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    machine_id = db.Column(db.Integer(), db.ForeignKey('machines.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f'<UserMachine {self.id}>'
    
    def __init__(self, user_id, machine_id):
        self.user_id = user_id
        self.machine_id = machine_id
        
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "machine_id": self.machine_id
        }