import firebase_admin
from firebase_admin import credentials, db
import time

cred = credentials.Certificate('attendanceapp-e4818-firebase-adminsdk-kxu8r-539f2e763d.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://attendanceapp-e4818-default-rtdb.firebaseio.com/'})

ref = db.reference('attendanceTaken')
while True:
    command = ref.get()
    if command == 1:
        exec(open('mm.py').read())
        print('Script executed successfully')
        ref.set(0) 
    time.sleep(1)
