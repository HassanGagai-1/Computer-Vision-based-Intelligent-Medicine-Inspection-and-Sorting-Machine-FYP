from extensions import db
class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement= False)
    name = db.Column(db.String(50), nullable=False, unique = True)

    
    
    def __repr__(self):
        return f'<role {self.id} {self.name}>'
    
    def __init__(self, name):
        if name.lower() == 'admin':
            self.id = 1
        elif name.lower() == 'customer':
            self.id = 2
        else:
            raise ValueError("Invalid role name")
        self.name = name
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name 
        }
