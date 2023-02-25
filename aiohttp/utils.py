import bcrypt


def hash_pw(password):
    return (bcrypt.hashpw(password.encode(), bcrypt.gensalt())).decode()


def check_pw(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
