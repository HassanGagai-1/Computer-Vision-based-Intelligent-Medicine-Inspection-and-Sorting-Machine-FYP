from extensions import db
    
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer(),  nullable=False, default=2)
    is_deleted = db.Column(db.Boolean(), nullable=True, default=False)
    
    machines = db.relationship(
        'Machine',
        secondary = 'user_machine',
        backref='users'
    )
    
    
    def __repr__(self):
        return f'<User {self.email} {self.id}>'
    
    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role_id = 2
        self.is_deleted = False
    
    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "role_id": self.role_id,
            "is_deleted": self.is_deleted  # Include deletion status
        }