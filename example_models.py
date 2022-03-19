# Adding fixed variables for usage:
WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
PARTS_OF_DAY = ['Morning', 'Noon', 'Evening']

# The following are constants which have been used to simulate objects which are recieved from the DB via SQL queries, and passed to the FE.

OWNERS = [
    {
        'name': 'Benny Gantz',
        'phone': '0509876543',
        'email': 'b@gmail.com'
    },
    {
        'name': 'Deddy Daddon',
        'phone': '0501111111',
        'email': 'dd@gmail.com'
    },
    {
        'name': 'Django Jones',
        'phone': '0504561230',
        'email': 'django@gmail.com'
    }
]

DOGS = [
    {
        'name': 'Fluffy',
        'id': '12a1da5d6',
        'gender': 'Male',
        'size': 'Large',
        'age': 7,
        'friendly': True,
        'vaccinated': True,
        'owner': OWNERS[0]
    },
    {
        'name': 'Bonny',
        'id': 'as8765132asd',
        'gender': 'Female',
        'size': 'Medium',
        'age': 8,
        'friendly': False,
        'vaccinated': True,
        'owner': OWNERS[0]
    },
    {
        'name': 'Pitzi',
        'id': '123456jhgx',
        'gender': 'Female',
        'size': 'Small',
        'age': 17,
        'friendly': False,
        'vaccinated': True,
        'owner': OWNERS[1]
    },
    {
        'name': 'Miflezet',
        'id': 'uiasd78u4',
        'gender': 'Male',
        'size': 'Large',
        'age': 3,
        'friendly': False,
        'vaccinated': False,
        'owner': OWNERS[2]
    },
]

WALKERS = [
    {
        'name': 'Avi Cohen',
        'phone': '0501234567',
        'email': 'a@gmail.com',
        'price': '150'
    },
    {
        'name': 'Benny Bohen',
        'phone': '0501234567',
        'email': 'a@gmail.com',
        'price': '120'
    },
]

OWNER_WALKS = [
    {
        'dog_name': DOGS[0]['name'],
        'day': WEEKDAYS[0],
        'part': PARTS_OF_DAY[0],
        'walker': WALKERS[0],
        'status': 'Accepted',
    },
    {
        'dog_name': DOGS[1]['name'],
        'day': WEEKDAYS[3],
        'part': PARTS_OF_DAY[2],
        'walker': WALKERS[1],
        'status': 'Declined',
    },
]

WALKER_WALKS = [
    {
        'dog': DOGS[0],
        'day': WEEKDAYS[0],
        'part': PARTS_OF_DAY[0],
    },
    {
        'dog': DOGS[1],
        'day': WEEKDAYS[0],
        'part': PARTS_OF_DAY[2],
    },
    {
        'dog': DOGS[1],
        'day': WEEKDAYS[3],
        'part': PARTS_OF_DAY[2],
    },
    {
        'dog': DOGS[2],
        'day': WEEKDAYS[3],
        'part': PARTS_OF_DAY[0],
    },
    {
        'dog': DOGS[3],
        'day': WEEKDAYS[5],
        'part': PARTS_OF_DAY[1],
    },
]

REQUESTS = [
    {
        'id': 'huasjbnasd12',
        'day': WEEKDAYS[0],
        'part': PARTS_OF_DAY[0],
        'dog': DOGS[2]
    },
    {
        'id': 'jlkuijk31',
        'day': WEEKDAYS[3],
        'part': PARTS_OF_DAY[1],
        'dog': DOGS[3]
    },
]