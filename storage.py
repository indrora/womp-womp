import dbm 
import json
import xid
import datetime


class Cardfile:
    def __init__(self, filename):
        self.filename = filename
        self.db = dbm.open(filename, 'c')

    def fetch(self, key) -> dict[any, any] | None:
        if key not in self.db:
            return None
        data = json.loads(self.db[key])

        return data

    def insert(self, value) -> str:
        key = xid.XID().string()
        self.db[key] = json.dumps({
                'value': value,
                'id': key,
                'timestamp': datetime.datetime.now().isoformat()
            })
        return key

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
