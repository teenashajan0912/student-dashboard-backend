from models import User

def get_user_by_username(db,username):
    return db.query(User).filter(
        User.username == username
    ).first()


def get_all_users(db):
    return db.query(User).all()


def get_user_by_id(db,user_id):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def create_user(db,user_data):
    user = User(**user_data)
    db.add(user)
    db.commit()
    return user


def delete_user_db(db,user):
    db.delete(user)
    db.commit()