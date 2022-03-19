import User
import Dog
import Dog_Walker
import Dog_Owner
#import Walk
from datetime import date
import datetime

#example:
"""user1 = User.User()
user1.First_Name = "ex"
user1.Last_Name=  "ex"
user1.Phone_Number = "053666665"
user1.User_eMail = "example@example.com"
user1.insertToDb()"""
#examples:
"""
walker1 = Dog_Walker.Dog_Walker()
walker1.User_eMail = "harrypotter@hogwarts.com"
walker1.make_premium(datetime.datetime.strptime("2018-11-02",'%Y-%m-%d'), 0.05)"""
"""walker1.First_Name = "Harry"
walker1.Last_Name = "Potter"
walker1.Phone_Number = "0586000000"
walker1.City_of_residence = "London"
walker1.Street = "somwwhere"
walker1.House_Number = 9
walker1.Registration_date_as_Regular = datetime.datetime.strptime("2018-11-02",'%Y-%m-%d')
walker1.Monthly_Commission_Rate=float(0.1)
walker1.Walk_Cost_Large_Dog=60
walker1.Walk_Cost_Medium_Dog=50
walker1.Walk_Cost_Small_Dog=40
walker1.Availability = {'sunday' : {'morning' :False, 'noon': False, 'evening': False}, 'monday': {'morning' :False, 'noon': False, 'evening': False}, 'tuesday' : {'morning' :True, 'noon': False, 'evening': True}, 'wednesday' : {'morning' :True, 'noon': True, 'evening': True}, 'thursday' : {'morning' :False, 'noon': True, 'evening': False}, 'friday' : {'morning' :False, 'noon': False, 'evening': True}, 'saturday' : {'morning' :True, 'noon': False, 'evening': False}}
walker1.insertToDb()"""
"""owner1 = Dog_Owner.Dog_Owner()
owner1.User_eMail = "p@mail.com"
owner1.First_Name = "example"
owner1.Last_Name = "example"
owner1.Phone_Number = "0546000000"
owner1.City_of_residence = "Petah tikva"
owner1.Date_of_Birth = date.today()
owner1.insertToDb()"""
"""dog1 = Dog.Dog()
dog1.Dog_Name="Alpha"
dog1.Date_of_Birth= date.today()
dog1.Dog_Number=1
dog1.Dog_Owner_eMail="p@mail.com"
dog1.Dog_Size="medium"
dog1.Gender="female"
dog1.is_Friendly=True
dog1.is_Vaccinated=False
dog1.insertToDb()"""