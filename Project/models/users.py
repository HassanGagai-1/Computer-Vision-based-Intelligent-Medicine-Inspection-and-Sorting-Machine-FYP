from extensions import db
    
    
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    totp_secret = db.Column(db.String(255), nullable=True)
    
    reset_token = db.Column(db.String(255), nullable=True) 
    reset_token_expiry = db.Column(db.DateTime(), nullable=True)
    
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
    
    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }