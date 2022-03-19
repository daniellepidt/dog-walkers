# -------------------------------------------------------------------------------
# DbHandler
# -------------------------------------------------------------------------------
# A class to interact with the database
#-------------------------------------------------------------------------
# Author: Almog Asraf, Daniel Pidtylok, Nir Levanon
# Last updated: 04/01/2021
#-------------------------------------------------------------------------


# import logging so we can write messages to the log
import logging
import os
#import DB library
import MySQLdb

# Database connection parameters 
DB_USER_NAME='db_team07'
DB_PASSWORD='uhjdkecc'
DB_DEFALUT_DB='db_team07'

class DbHandler():
    def __init__(self):
        logging.info('Initializing DbHandler new')
        self.d_user=DB_USER_NAME
        self.d_password=DB_PASSWORD
        self.d_default_db=DB_DEFALUT_DB
        self.d_charset='utf8'
        self.d_host='34.122.221.36'
        self.d_port=3306
        self.d_DbConnection=None

    def connectToDb(self):
        logging.info('In ConnectToDb')
        # we will connect to the DB only once
        if self.d_DbConnection is None:
            # connect to the DB
            self.d_DbConnection = MySQLdb.connect(
            host=self.d_host,
            db=self.d_default_db,
            port=self.d_port,
            user= self.d_user,
            passwd=self.d_password,
            charset=self.d_charset)

    def disconnectFromDb(self):
        logging.info('In DisconnectFromDb')
        if self.d_DbConnection:
            self.d_DbConnection.close()
            
    def commit(self):
        logging.info('In commit')
        if self.d_DbConnection:
            self.d_DbConnection.commit()
            
    def getCursor(self):
        logging.info('In DbHandler.getCursor')
        self.connectToDb()
        return (self.d_DbConnection.cursor())