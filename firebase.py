import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import json
import random

cred = credentials.Certificate('dragon.json')
firebase_admin.initialize_app(cred)

class Collection:
    def __init__(self):
        self.db = firestore.client()

    def dataup(self):
        doc_ref = self.db.collection(u'users').document(u'alovelace')
        doc_ref.set({
            u'first': u'Ada',
            u'last': u'Lovelace',
            u'born': 1815
        })

    def readit(self):
        commands_ref = self.db.collection(u'commands')
        docs = commands_ref.get()

        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

    def create_sub(self, command_id, gyro_data):
        print("Create sub g data", gyro_data)
        new_id = self.generate_random_id()
        command_a_ref = self.db.collection(u'commands').document(command_id)
        command_a_ref.collection(u'attempts').document(new_id).set({
            u'measurements': json.dumps(gyro_data),
            u'timestamp': str(datetime.datetime.utcnow().isoformat())+"Z"
        })

        return new_id
        
    def generate_random_id(self):
        return "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for x in range(20)])
