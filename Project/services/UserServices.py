import dal.UserRepository as UserRepository

def get_all_users():
    return UserRepository.get_all_users()

def insert_user(firstname, lastname, email, password):
    return UserRepository.insert_user(firstname, lastname, email, password)

