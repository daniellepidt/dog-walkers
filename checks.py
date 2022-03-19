import db_handler

# Functions to check if the user exist in db in two ways: as Dog Owner or as Dog Walker.

def check_if_owner(email):
    # Using db_handler - to connect to the DB
    u_DbHandler=db_handler.DbHandler()
    cursor = u_DbHandler.getCursor()
    cursor.execute('SELECT dog_owner_email FROM Dog_Owner WHERE dog_owner_email="'+email+'"')
    check_owner = cursor.fetchall()
    if check_owner:
        return True
    return False

def check_if_walker(email):
    # Using db_handler - to connect to the DB
    u_DbHandler=db_handler.DbHandler()
    cursor = u_DbHandler.getCursor()
    cursor.execute('SELECT dog_walker_email FROM Dog_Walker WHERE dog_walker_email="'+email+'"')
    check_owner = cursor.fetchall()
    if check_owner:
        return True
    return False
