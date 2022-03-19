# -------------------------------------------------------------------------------
# Dog Owner
# -------------------------------------------------------------------------------
# A class to manage the owners - create and save in the DB
#-------------------------------------------------------------------------
# Author: Almog Asraf, Daniel Pidtylok, Nir Levanon
# Last updated: 09.12.2020
#-------------------------------------------------------------------------


# import logging so we can write Owner to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
#import master class User
from user import User


class Dog_Owner(User):

    def __init__(self):
        logging.info('Initializing Owner')
        self.o_DbHandler=db_handler.DbHandler()
        # Creates data members of the class Owner
        User.__init__(self)
        self.date_of_birth = ""

    def insertToDb(self):
        # First, we check if the walker already exists as a User
        self.u_DbHandler=db_handler.DbHandler()
        cursor = self.u_DbHandler.getCursor()
        cursor.execute('SELECT User_eMail FROM Users where User_eMail="'+self.user_email+'"')
        checker = cursor.fetchall()
        if not checker:
            # Inserting the values of object walker to the DB
            User.insertToDb(self)
        # Inserting the object of owner to the DB
        self.o_DbHandler.connectToDb()
        cursor = self.o_DbHandler.getCursor()
        sql = """INSERT INTO Dog_Owner(date_of_birth, dog_owner_email) VALUES(%s,%s)"""
        cursor.execute(sql, (self.date_of_birth, self.user_email))
        self.o_DbHandler.commit()
        self.o_DbHandler.disconnectFromDb()
        return
