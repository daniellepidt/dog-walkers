# -------------------------------------------------------------------------------
# User
# -------------------------------------------------------------------------------
# A class to manage the users - create and save in the DB
#-------------------------------------------------------------------------
# Author: Almog Asraf, Daniel Pidtylok, Nir Levanon
# Last updated: 04.01.2021
#-------------------------------------------------------------------------

# import logging so we can write Owner to the log
import logging
# import the class DbHandler to interact with the database
import db_handler


class User():
    
    def __init__(self):
        logging.info('Initializing User')
        self.u_DbHandler=db_handler.DbHandler()
        # Creates data members of the class Dog
        self.user_email = ""
        self.first_name = ""
        self.last_name = ""
        self.phone_number = ""
        self.city_of_residence = ""

    def insertToDb(self):
        # Inserting the object of user to the DB
        self.u_DbHandler.connectToDb()
        cursor = self.u_DbHandler.getCursor()
        sql = """INSERT INTO Users(user_email,first_Name,last_Name,phone_number,city_of_residence) VALUES(%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (self.user_email, self.first_name, self.last_name, self.phone_number, self.city_of_residence))
        self.u_DbHandler.commit()
        self.u_DbHandler.disconnectFromDb()
        return