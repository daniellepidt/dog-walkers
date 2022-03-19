# -------------------------------------------------------------------------------
# Dog
# -------------------------------------------------------------------------------
# A class to manage the Dogs - create and save in the DB
#-------------------------------------------------------------------------
# Author: Almog Asraf, Daniel Pidtylok, Nir Levanon
# Last updated: 04.01.2021
#-------------------------------------------------------------------------


# import logging so we can write Dog to the log
import logging
# import the class DbHandler to interact with the database
import db_handler

class Dog():

    def __init__(self):
        logging.info('Initializing Dog')
        self.d_DbHandler=db_handler.DbHandler()
        # Creates data members of the class Dog
        self.dog_number = ""
        self.dog_name = ""
        self.gender = ""
        self.date_of_birth = ""
        self.dog_size = ""
        self.is_vaccinated = False
        self.is_friendly = False
        self.dog_owner_email = ""

    def insertToDb(self):
        # Inserting the object of dog to the DB
        self.d_DbHandler.connectToDb()
        cursor = self.d_DbHandler.getCursor()
        sql = """INSERT INTO Dog(dog_name,gender,date_of_birth,dog_size,is_vaccinated,is_friendly,dog_owner_email) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (self.dog_name, self.gender, self.date_of_birth, self.dog_size, self.is_vaccinated, self.is_friendly, self.dog_owner_email))
        self.d_DbHandler.commit()
        self.d_DbHandler.disconnectFromDb()
        return