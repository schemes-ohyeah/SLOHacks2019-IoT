import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Collection:
    def __init__(self):
        cred = credentials.Certificate('service.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def dataup(self):
        doc_ref = self.db.collection(u'users').document(u'alovelace')
        doc_ref.set({
            u'first': u'Ada',
            u'last': u'Lovelace',
            u'born': 1815
        })
