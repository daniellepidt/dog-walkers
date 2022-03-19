# -------------------------------------------------------------------------------
# Walk
# -------------------------------------------------------------------------------
# A class to manage the walks - create and save in the DB
#-------------------------------------------------------------------------
# Author: Almog Asraf, Daniel Pidtylok, Nir Levanon
# Last updated: 04.01.2021
#-------------------------------------------------------------------------


# import logging so we can write Walk to the log
import logging
# import the class DbHandler to interact with the database
import db_handler

class Walk():

    def __init__(self):
        logging.info('Initializing Owner')
        self.wk_DbHandler=db_handler.DbHandler()
        # Creates data members of the class Walk
        self.request_id = ""
        self.request_date = ""
        self.request_status = ""
        self.day_in_the_week = ""
        self.part_of_day = ""
        self.response_date = ""
        self.cancelation_date = ""
        self.dog_number = ""
        self.dog_walker_email = ""
        
    def insertToDb(self):
        # Inserting the object of walk to the DB
        self.wk_DbHandler.connectToDb()
        cursor = self.wk_DbHandler.getCursor()
        sql = """INSERT INTO Walk(request_date,request_status,day_in_the_week,part_of_day,dog_number,dog_walker_email) VALUES(%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (self.request_date, self.request_status, self.day_in_the_week, self.part_of_day, self.dog_number, self.dog_walker_email))
        self.wk_DbHandler.commit()
        self.wk_DbHandler.disconnectFromDb()
        return