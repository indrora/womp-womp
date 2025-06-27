import json
import datetime
from rocksdict import Rdict
from cyksuid.v2 import ksuid, parse
from card import Troublecard


class Cardfile:
    def __init__(self, filename):
        self.filename = filename
        self.db = Rdict(self.filename)

    def fetch(self, key:str) -> Troublecard | None:
        if key not in self.db:
            return None
        data = json.loads(self.db[key])
        return data

    def insert(self, value:Troublecard) -> str:
        self.db[str(value.id)] = value
        return str(value.id)

    def list_ids(self):
        return [key for key in self.db.keys()]

    def search(self, filterfunc):
        results = []
        for key in self.db.keys():
            data = json.loads(self.db[key])
            if filterfunc(data):
                results.append(data)
        return results

    def delete(self, key):
        if key in self.db:
            del self.db[key]

    def close(self):
        self.db.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        