# -------------------------------------------------------------------------------
# Dog Walker
# -------------------------------------------------------------------------------
# A class to manage the walkers - create and save in the DB
#-------------------------------------------------------------------------
# Author: Almog Asraf, Daniel Pidtylok, Nir Levanon
# Last updated: 04.01.2021
#-------------------------------------------------------------------------


# import logging so we can write Walker to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
#import master class User
from user import User


class Dog_Walker(User):
    
    def __init__(self):
        logging.info('Initializing Walker')
        self.w_DbHandler=db_handler.DbHandler()
        # create data members of the class Walker
        User.__init__(self)
        self.dog_walker_email = ""
        self.street = ""
        self.house_number = 0
        self.seens_when = ""
        self.walk_cost_large_dog = 0.0
        self.walk_cost_medium_dog = 0.0
        self.walk_cost_small_dog = 0.0
        self.monthly_commission_rate = 0.0
        self.registration_date_as_regular= ""
        self.Availability = {'Sunday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Monday': {'Morning' :False, 'Noon': False, 'Evening': False}, 'Tuesday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Wednesday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Thursday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Friday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Saturday' : {'Morning' :False, 'Noon': False, 'Evening': False}}
        

    def insertToDb(self):
        # First we need to check if we don't have this user as user object
        self.u_DbHandler=db_handler.DbHandler()
        cursor = self.u_DbHandler.getCursor()
        cursor.execute('SELECT user_email FROM Users WHERE user_email="'+self.user_email+'"')
        checker = cursor.fetchall()
        if not checker:
            # Inserting the values of object walker to the DB as user
            User.insertToDb(self)
        #  Inserting the object of walker to the DB
        self.w_DbHandler.connectToDb()
        cursor = self.w_DbHandler.getCursor()
        # Inserting the main information to walker table
        sql = """INSERT INTO Dog_Walker(dog_walker_email,street,house_number,since_when,walk_cost_small_dog,walk_cost_medium_dog,walk_cost_large_dog, monthly_commission_rate,registration_date_as_regular) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (self.user_email,self.street, 
                      self.house_number,self.seens_when,self.walk_cost_small_dog,
                      self.walk_cost_medium_dog,self.walk_cost_large_dog,
                      self.monthly_commission_rate,self.registration_date_as_regular))
        self.w_DbHandler.commit()
        # Inserting the days and parts in days that the walker is able to walk
        cursor2 = self.w_DbHandler.getCursor()
        for day in self.Availability:
            for part in self.Availability[day]:
                if self.Availability[day][part]:
                    sql = """INSERT INTO Availability(dog_walker_email,day_in_the_week,part_of_day) VALUES(%s,%s,%s)"""
                    cursor2.execute(sql,(self.user_email,day,part))
        self.w_DbHandler.commit()
        self.w_DbHandler.disconnectFromDb()
        return
