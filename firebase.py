import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime


class Collection:
    def __init__(self):
        cred = credentials.Certificate('dragon.json')
        firebase_admin.initialize_app(cred)
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
        command_a_ref = self.db.collection(u'commands').document(command_id)
        return command_a_ref.collection(u'attempts').add({
            u'measurements': gyro_data,
            u'timestamp': datetime.datetime.now().isoformat()
        })
