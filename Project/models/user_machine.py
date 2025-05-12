from extensions import db

class UserMachine(db.Model):
    __tablename__ = 'userMachine'
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),  nullable=False)
    machine_id = db.Column(db.Integer(), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
    
    def __repr__(self):
        return f'<UserMachine {self.id}>'
    
    def __init__(self, user_id, machine_id, is_deleted = False):
        self.user_id = user_id
        self.machine_id = machine_id
        self.is_deleted = is_deleted
        
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "machine_id": self.machine_id,
            "is_deleted": self.is_deleted
        }