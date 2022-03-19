#-------------------------------------------------------------------------
# Author: Nir Levanon, Daniel Pidtylok, Almog Asraf       
# Last updated: 04.01.2021
# main.py- this file handles all the html pages
#-------------------------------------------------------------------------

# Import webapp2  - Python web framework compatible with Google App Engine
import webapp2
# Import Jinja and os libraries
import jinja2
import os
# Import logging so we can write in the console
import logging
# Import users library - To login with google account
from google.appengine.api import users
# Import all objects of our DB
import db_handler
import user
import dog
import Dog_Owner
import Dog_Walker
import walk
# Import date library - we need it sometimes to insert to DB
from datetime import date
# Example_models contains constants which are used in the different functions
# need?
from example_models import *
# Import checks - contains functions that checks if the user already an owner or walker
from checks import check_if_owner, check_if_walker

# Load Jinja
jinja_environment =jinja2.Environment(loader=
                                      jinja2.FileSystemLoader
                                     (os.path.dirname(__file__)))

# ---------------------------------------------------------
# Main page - Shows the group details and Google login button 
# Handles /
# --------------------------------------------------------
class MainPage(webapp2.RequestHandler):
    def get(self):
        # Create a template object
        main_page_template = jinja_environment.get_template('index.html')
        user = users.get_current_user()
        #if is logged in
        if user:
            logging.info('The user is logged in to google')
            # get the nickname from the user object
            nickname = user.nickname()
            logging.info('nickname is '+ nickname)
            # 
            if check_if_owner(user.email()):
                self.redirect('/owner/walks_and_requests')
            elif check_if_walker(user.email()):
                self.redirect('/walker/walks_and_requests')
            else:
                self.redirect('/first_login')
        # Creating an HTML page and response
        self.response.write(main_page_template.render())


# ------------------------------------------------------
# class to handle /login requests
# will force the user to perform login and redirects to 
# /first_login
# ------------------------------------------------------
class Login(webapp2.RequestHandler):
    def get(self):
        logging.info('In Login.get()')
        user = users.get_current_user()  

        # If the user object exists (the user is logged in to google)
        if user:
            logging.info('The user object exists')
            logging.info('The user is logged in to google. There is nothing to do')
            logging.info('Is the user already an owner?' + str(check_if_owner(user.email())) +"\nIs the user already a walker?" + str(check_if_walker(user.email())))
            if check_if_owner(user.email()):
                self.redirect('/owner/walks_and_requests')
            elif check_if_walker(user.email()):
                self.redirect('/walker/walks_and_requests')
            else:
                self.redirect('/first_login')

        # The user object doesn't exist ( the user is not logged to google)
        # we will ask him to login and
        # provide the URI of the show_status page, to display the status afterwards
        else:      
            logging.info('The user object does not exist')
            logging.info('We will force the user to perform login to google')
            logging.info('Redirecting to /login/first_login_page afterwards but checks if the user in')
            # Forces the user to login and than redirects to /first_login to choose if he is a walker or an owner
            self.redirect(users.create_login_url('/first_login'))

# -----------------------------------------
# class to logout from the google account
# and show main page again
# Handles /logout 
# -----------------------------------------

class Logout(webapp2.RequestHandler):
    def get(self):

        logging.info('In Logout.get()')
        # if the user is logged in - we will perform log out
        user = users.get_current_user()

        if user:
            logging.info('The user is logged in - performing logout ')
            # force the user to logout and redirect him afterward to 
            # Main page
            self.redirect(users.create_logout_url('/'))

        else:
            logging.info('user is now not logged in ')
            logging.info('The user is logged out. There is nothing to do')
            logging.info('Redirecting to main_page')
            self.redirect('/')


# ---------------------------------------------------------
# First Login - Here a new user selects whether he is a Dog
# Owner or a Dog Walker 
# Handles /first_login
# --------------------------------------------------------
class FirstLogin(webapp2.RequestHandler):
    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('login/first_login_page.html')
        user = users.get_current_user()
        # If the user already exist in our DB (owner or walker), he redirects to his homepage
        if user:
            logging.info(user.email()+':'+'\nis the user already an owner?' + str (check_if_owner(user.email())) +"\nis the user already a walker? " + str(check_if_walker(user.email())))
            if check_if_owner(user.email()):
                self.redirect('/owner/walks_and_requests')
            elif check_if_walker(user.email()):
                self.redirect('/walker/walks_and_requests')
        # Else, he needs to choose if he is a walker or owner 
        # Creating an HTML page and response
        self.response.write(first_login_template.render())


# ---------------------------------------------------------
# Dog Owner Register - Here a new Dog Owner fills out his/her details
# Handles /owner/register
# --------------------------------------------------------
class DogOwnerRegister(webapp2.RequestHandler):
    # There is a 'get' funtions to get the form and show it, and a 'post' function to handle what we get from it
    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('owner/register_page.html')
        # Creating an HTML page and response
        self.response.write(first_login_template.render())
    
    def post(self):

        # Retrieve data from the POST request
        user1 = users.get_current_user()
        logging.info('Is the user already an owner?' + str(check_if_owner(user1.email())))
        if not check_if_owner(user1.email()):
            # Using class Dog_Owner - to insert to DB
            owner = Dog_Owner.Dog_Owner()
            owner.user_email = user1.email()
            owner.first_name = str(self.request.get('fname'))
            owner.last_name = str(self.request.get('lname'))
            owner.date_of_birth = self.request.get('birthday')
            owner.phone_number = str(self.request.get('phone'))
            owner.city_of_residence = str(self.request.get('city_of_residence'))
            owner.insertToDb()
        # Redirects to the next page
        self.redirect('/owner/dogs/new_dog')

# ---------------------------------------------------------
# Add first dog for Dog Owner
# Handles /owner/dogs/new_dog
# --------------------------------------------------------
class AddNewDog(webapp2.RequestHandler):

    # There is a 'get' funtions to get the form and show it, and a 'post' function to handle what we get from it.
    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('owner/dogs/new_dog_page.html')
        # Creating an HTML page and response
        self.response.write(first_login_template.render())

    def post(self):

        # Retrieve data from the POST request
        user = users.get_current_user()
        # Using class Dog - to insert to DB
        dog1 = dog.Dog()
        dog1.dog_name = str(self.request.get('dogname'))
        dog1.gender = str(self.request.get('gender'))
        dog1.dog_size = str(self.request.get('size'))
        dog1.date_of_birth = self.request.get('birthday')
        dog1.is_friendly = self.request.get('friendly') == 'friendly'
        dog1.is_vaccinated = self.request.get('vaccinated') == 'vaccinated'
        dog1.dog_owner_email = user.email() 
        dog1.insertToDb()
        # Redirects to the next page
        self.redirect('/owner/dogs/my_dogs')
        
    
# ---------------------------------------------------------
# View all of the Dog Owner's dogs & add new ones.
# Handles /owner/dogs/my_dogs
# --------------------------------------------------------
class MyDogs(webapp2.RequestHandler):
    # function to get the Owner's dogs
    def get(self):

        user = users.get_current_user()
        # Create a template object
        first_login_template = jinja_environment.get_template('owner/dogs/my_dogs_page.html')
        # Getting from the Db all the dogs to show to the owner
        dogs = get_all_dogs(user)
        # Creating an HTML page and response
        self.response.write(first_login_template.render({'dogs': dogs, 'user_type': 'owner'}))

def get_all_dogs(user):
    # Function to get all the dogs of this owner - prevents duplicated code
    # Creates db_handler object - to connect to the DB
    d_DbHandler=db_handler.DbHandler()
    cursor = d_DbHandler.getCursor()
    # Getting all the dogs and their features
    cursor.execute('SELECT * FROM Dog WHERE dog_owner_email="'+user.email()+'"')
    dogs = []
    temps = cursor.fetchall()
    for temp in temps:
        temp_dict = {}
        temp_dict['id'] = str(temp[0])
        temp_dict['name'] = str(temp[1])
        temp_dict['gender'] = str(temp[2])
        temp_dict['size'] = str(temp[4])
        temp_dict['age'] = date.today().year - temp[3].year
        temp_dict['friendly'] = temp[6]
        temp_dict['vaccinated'] = temp[5]
        temp_dict['owner'] = str(temp[7])
        dogs.append(temp_dict)
    d_DbHandler.disconnectFromDb()
    return dogs

# ---------------------------------------------------------
# View all of the Dog Owner's walk requests & set a new walk.
# Handles /owner/walks_and_requests
# --------------------------------------------------------
class OwnerWalkAndRequests(webapp2.RequestHandler):

    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('owner/walks_and_requests/walks_and_requests_page.html')

        user = users.get_current_user()
        dogs = get_all_dogs(user)
        dog_id = str(self.request.get('dogs'))
        #Getting the day and part of day for the walk
        day_in_the_week = str(self.request.get('days'))
        part_of_day = str(self.request.get('parts_of_day'))
        # Creates db_handler object - to connect to the DB
        d_DbHandler=db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        # Creating a list of all the walkers that available on this day, part of day and city of residence
        walkers = []
        # Checks what is the size of the dog
        if dog_id:
            for dog in dogs:
                if str(dog['id']) == dog_id:
                    size = str(dog['size'])
                    break
            #Getting from DB the city of residence of the owner so we can get the right walkers
            sql = """SELECT city_of_residence
                    FROM Users
                    WHERE user_email = '""" + user.email() + "';"
            cursor.execute(sql)
            city_of_residence_temp = cursor.fetchall()
            city_of_residence = str(city_of_residence_temp[0][0])
            #Getting the table of all the walkers that are in the city of residence of the owner and avialible in the particular day and part of day
            #Checking which size so we can 'catch' the right price 
            costs = {
                "Small": "walk_cost_small_dog",
                "Medium": "walk_cost_medium_dog",
                "Large": "walk_cost_large_dog"
            }
            sql = """SELECT first_name, last_name, W.dog_walker_email, phone_number, %s
                    FROM Users AS U JOIN Dog_Walker AS W ON U.user_email = W.dog_walker_email
                        JOIN Availability As A ON W.dog_walker_email = A.dog_walker_email
                    WHERE city_of_residence = "%s" and day_in_the_week = "%s" and part_of_day="%s";"""
            sql = sql % (costs[size],city_of_residence,day_in_the_week,part_of_day)
            cursor.execute(sql)
            temps = cursor.fetchall()
            #Making a list of all the appropriate walkers
            for temp in temps:
                temp_dict = {}
                temp_dict['name'] = str(temp[0]) + " " + str(temp[1])
                temp_dict['phone'] = str(temp[3])
                temp_dict['email'] = str(temp[2])
                temp_dict['price'] = float(temp[4])
                walkers.append(temp_dict)
        
        # Getting all the requests of walks for all the dogs
        sql = """SELECT request_id, dog_name, day_in_the_week, part_of_day, request_status, first_name, last_name, phone_number, dog_walker_email
                FROM Walk AS WK JOIN Dog as D ON WK.dog_number = D.dog_number
				    JOIN Users AS U ON WK.dog_walker_email = U.user_email 
                WHERE D.dog_owner_email = '""" +user.email()+"""'
                ORDER BY FIELD(day_in_the_week, "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"),
		                FIELD(part_of_day, "Morning", "Noon", "Evening");"""
        cursor.execute(sql)
        temps = cursor.fetchall()
        # Creates walks list of all the walks requests of the owner
        walks = []
        for temp in temps:
            temp_dict_main = {}
            temp_dict_walker = {}
            temp_dict_main['id'] = str(temp[0])
            temp_dict_main['dog_name'] = str(temp[1])
            temp_dict_main['day'] = str(temp[2])
            temp_dict_main['part'] = str(temp[3])
            temp_dict_walker['name'] = str(temp[5]) + " " + str(temp[6])
            temp_dict_walker['phone'] = str(temp[7])
            temp_dict_walker['email'] = str(temp[8])
            temp_dict_walker['price'] = 0
            temp_dict_main['walker'] = temp_dict_walker
            temp_dict_main['status'] = str(temp[4])
            walks.append(temp_dict_main)
        
        parameters_for_template = {
            'walks': walks,
            'days': WEEKDAYS,
            'parts_of_day': PARTS_OF_DAY,
            'dogs': dogs,
            'walkers': walkers,
            'chosen_day': day_in_the_week,
            'chosen_part': part_of_day,
            'chosen_dog': dog_id,
            'user_type': 'owner'
        }

        # Creating an HTML page and response
        self.response.write(first_login_template.render(parameters_for_template))


# ---------------------------------------------------------
# Walk Request From Owner - here we insert the walk request
# from the owner to the DB
# Handels /owner/walks_and_requests/insert
# ---------------------------------------------------------
class WalkRequestFromOwner(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        # Using the walk class - to insert to DB
        walk_new = walk.Walk()
        walk_new.request_date = date.today()
        walk_new.day_in_the_week = str(self.request.get('day'))
        walk_new.part_of_day = str(self.request.get('part'))
        walk_new.dog_number = int(self.request.get('dog_id'))
        walk_new.dog_walker_email = str(self.request.get('walker_email')) 
        walk_new.request_status = "pending"
        walk_new.insertToDb()
        # Redirect back to owner's homepage
        self.redirect('/owner/walks_and_requests')
        

# ---------------------------------------------------------
# Cancel Walk - here we cancel the walk request, can be done
# by the owner and the walker
# Handels /walk/cancel
# ---------------------------------------------------------
class CancelWalk(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        # Creates db_handler object - to connect to the DB
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        request_id = self.request.get('id')
        if check_if_owner(user.email()):
            # Cancel the walk
            sql = """UPDATE Walk
                    SET request_status = "canceled", cancelation_date="%s"
                    WHERE request_id = %s;"""
            sql = sql % (date.today(),request_id)
            cursor.execute(sql)
        else:
            # Decline the walk
            sql = """UPDATE Walk
                    SET request_status = "declined", response_date="%s", cancelation_date = "%s"
                    WHERE request_id = %s;"""
            sql = sql % (date.today(),date.today(),request_id)
            cursor.execute(sql)
        d_DbHandler.commit()
        d_DbHandler.disconnectFromDb()
        # Redirects back to homepages
        if check_if_owner(user.email()):
            self.redirect('/owner/walks_and_requests')
        else:
            self.redirect('/walker/walks_and_requests')

# ---------------------------------------------------------
# Accept Walk By Walker - here we deal with accept request of the walker.
# Handles /walker/walks_and_requests/accept
# ---------------------------------------------------------
class AcceptWalkByWalker (webapp2.RequestHandler):

    def get(self):

        # Creates db_handler object - to connect to the DB
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        request_id = self.request.get('id')
        # Accepting the walk
        sql = """UPDATE Walk
                SET request_status = "accepted", response_date="%s"
                WHERE request_id = %s"""
        sql = sql % (date.today(),request_id)
        cursor.execute(sql)
        d_DbHandler.commit()
        d_DbHandler.disconnectFromDb()
        # Redirects back to homepage
        self.redirect('/walker/walks_and_requests')


# ---------------------------------------------------------
# Dog Walker Register - Here a new Dog Walker fills out his/her details
# Handles /walker/register
# --------------------------------------------------------
class DogWalkerRegister(webapp2.RequestHandler):
    # There is a 'get' funtions to get the form and show it, and a 'post' function to handle what we get from it.
    def get(self): 

        # Create a template object
        first_login_template = jinja_environment.get_template('walker/register/register_page.html')
        # Creating an HTML page and response
        parameters_for_template = {
            'days': WEEKDAYS,
            'parts_of_day': PARTS_OF_DAY
        }
        self.response.write(first_login_template.render(parameters_for_template))

    def post(self):

        user = users.get_current_user()
        # Using the Dog_Walker class - to insert to DB
        walker = Dog_Walker.Dog_Walker()
        walker.user_email = user.email()
        walker.first_name = self.request.get('fname')
        walker.last_name = self.request.get('lname')
        walker.seens_when = self.request.get('seniority')
        walker.registration_date_as_regular = date.today()
        walker.phone_number = self.request.get('phone')
        walker.city_of_residence = self.request.get('city_of_residence')
        walker.street = self.request.get('street')
        walker.house_number = self.request.get('house-number')
        walker.monthly_commission_rate = 0.1
        walker.walk_cost_small_dog = self.request.get('price_small')
        walker.walk_cost_medium_dog = self.request.get('price_medium')
        walker.walk_cost_large_dog = self.request.get('price_large')
        dict_temp_days_and_parts = {'Sunday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Monday': {'Morning' :False, 'Noon': False, 'Evening': False}, 'Tuesday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Wednesday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Thursday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Friday' : {'Morning' :False, 'Noon': False, 'Evening': False}, 'Saturday' : {'Morning' :False, 'Noon': False, 'Evening': False}}
        for day in dict_temp_days_and_parts:
            for part in dict_temp_days_and_parts[day]:
                logging.info(self.request.get(day+'-'+part))
                temp_str = day+'-'+part
                temp = self.request.get(temp_str)
                if temp == temp_str:
                    dict_temp_days_and_parts[day][part] = True
                else:
                    dict_temp_days_and_parts[day][part] = False
        walker.Availability = dict_temp_days_and_parts
        walker.insertToDb()
        # Redirects back to hompage
        self.redirect('/walker/walks_and_requests')


# ---------------------------------------------------------
# View all of the Dog Walkers's walk requests & set walks.
# Handles /walker/walks_and_requests
# --------------------------------------------------------
class WalkerWalkAndRequests(webapp2.RequestHandler):

    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('walker/walks_and_requests/walks_and_requests_page.html')
        user = users.get_current_user()

        # Make 'set_walks' into SQL query that gets the set walks.
        # Creates db_handler object - to connect to the DB
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        sql = """SELECT request_id, day_in_the_week, part_of_day,WK.dog_number,
	                    dog_name, dog_size, gender, date_of_birth, is_friendly, is_vaccinated,
                        first_name, last_name, phone_number, user_email
                FROM Walk AS WK JOIN Dog As D ON WK.dog_number = D.dog_number 
			                    JOIN Users As U ON D.dog_owner_email = U.user_email
                WHERE dog_walker_email = '"""+user.email()+"""' AND request_status="accepted"
                ORDER BY FIELD(day_in_the_week, "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"),
		                 FIELD(part_of_day, "Morning", "Noon", "Evening");"""
        cursor.execute(sql)
        temps = cursor.fetchall()
        d_DbHandler.commit()
        # Creates a list of all the set walks
        set_walks = []
        for temp in temps:
            temp_dict = {}
            temp_dict_dog = {}
            temp_dict_owner = {}
            temp_dict_owner['name'] = str(temp[10]) + " " + str(temp[11])
            temp_dict_owner['phone'] = str(temp[12])
            temp_dict_owner['email'] = str(temp[13])
            temp_dict_dog['name'] = str(temp[4])
            temp_dict_dog['id'] = str(temp[3])
            temp_dict_dog['gender'] = str(temp[6])
            temp_dict_dog['size'] = str(temp[5])
            temp_dict_dog['age'] = date.today().year - temp[7].year
            temp_dict_dog['friendly'] = temp[8]
            temp_dict_dog['vaccinated'] = temp[9]
            temp_dict_dog['owner'] = temp_dict_owner
            temp_dict['dog'] = temp_dict_dog
            temp_dict['day'] = str(temp[1])
            temp_dict['part'] = str(temp[2])
            temp_dict['id'] = str(temp[0])
            set_walks.append(temp_dict)
        
        # Create dict with three keys, according to the parts of day
        # Create dict with days of the week as keys, and inside every day insert all parts of day
        walks = dict.fromkeys(WEEKDAYS, {})
        for walk in set_walks:
            if walk['part'] not in walks[walk['day']]:
                walks[walk['day']][walk['part']] = []
            walks[walk['day']][walk['part']].append(walk)
        for day in walks.keys():
            if not walks[day]:
                del walks[day]

        # Show requests that the walker didn't response
        sql = """SELECT request_id, day_in_the_week, part_of_day,WK.dog_number,
	                    dog_name, dog_size, gender, date_of_birth, is_friendly, is_vaccinated,
                        first_name, last_name, phone_number, user_email
                FROM Walk AS WK JOIN Dog As D ON WK.dog_number = D.dog_number 
			                    JOIN Users As U ON D.dog_owner_email = U.user_email
                WHERE dog_walker_email = '"""+user.email()+"""' AND request_status="pending"
                ORDER BY FIELD(day_in_the_week, "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"),
		                 FIELD(part_of_day, "Morning", "Noon", "Evening");"""
        cursor.execute(sql)
        temps = cursor.fetchall()
        d_DbHandler.commit()
        # Creates a list of all those requests
        requests = []
        for temp in temps:
            temp_dict = {}
            temp_dict_dog = {}
            temp_dict_owner = {}
            temp_dict_owner['name'] = str(temp[10]) + " " + str(temp[11])
            temp_dict_owner['phone'] = str(temp[12])
            temp_dict_owner['email'] = str(temp[13])
            temp_dict_dog['name'] = str(temp[4])
            temp_dict_dog['id'] = str(temp[3])
            temp_dict_dog['gender'] = str(temp[6])
            temp_dict_dog['size'] = str(temp[5])
            temp_dict_dog['age'] = date.today().year - temp[7].year
            temp_dict_dog['friendly'] = temp[8]
            temp_dict_dog['vaccinated'] = temp[9]
            temp_dict_dog['owner'] = temp_dict_owner
            temp_dict['dog'] = temp_dict_dog
            temp_dict['day'] = str(temp[1])
            temp_dict['part'] = str(temp[2])
            temp_dict['id'] = str(temp[0])
            requests.append(temp_dict)
        d_DbHandler.disconnectFromDb()

        parameters_for_template = {
            'requests': requests,
            'walks': set_walks,
            'user_type': 'walker'
        }        
        # Creating an HTML page and response
        self.response.write(first_login_template.render(parameters_for_template))
    

# --------------------------------------------------
# Routing
# --------
# /                                 - shows the Home Page
# /login                            - presents the login form
# /logout                           - logs out the user and returns him to the Home Page
# /first_login                      - let's the user decide what type he is on first entry
# /owner/register                   - registeration form for Dog Owner's first entry
# /owner/dogs/new_dog               - form for adding the Dog Owner's first dog
# /owner/dogs/my_dogs               - view all of the Dog Owner's dogs
# /owner/walks_and_requests         - view all of the Dog Owner's set walks & requests
# /walker/register                  - registration form for Dog Walkers's first entry
# /walker/walks_and_requests        - view all of the Dog Walkers's set walks & requests
# /owner/walks_and_requests/insert  - inserting the walk request from owner to DB, and than redirects to walks_and_requests
# /walker/walks_and_requests/accept - accepting the walk request and redirects back to /walker/walks_and_requests/
# /walk/cancel                      - cancels the walk request. Used both for walker and owner.
# --------------------------------------------------
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/login', Login),
                               ('/first_login', FirstLogin),
                               ('/owner/register', DogOwnerRegister),
                               ('/owner/dogs/new_dog', AddNewDog),
                               ('/owner/dogs/my_dogs', MyDogs),
                               ('/owner/walks_and_requests', OwnerWalkAndRequests),
                               ('/walker/register', DogWalkerRegister),
                               ('/walker/walks_and_requests', WalkerWalkAndRequests),
                               ('/owner/walks_and_requests/insert', WalkRequestFromOwner),
                               ('/walker/walks_and_requests/accept', AcceptWalkByWalker),
                               ('/walk/cancel', CancelWalk),
                               ('/logout', Logout)
                               ],
                              debug=True)