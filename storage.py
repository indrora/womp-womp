import json
import datetime
from rocksdict import Rdict, Options
from cyksuid.v2 import ksuid, parse
from card import Troublecard
import threading


class Cardfile:

    def __init__(self, filename):
        self.lock = threading.Lock()
        with self.lock:
            self.filename = filename
            opts =  Options()
            opts.create_if_missing(True)
            opts.set_keep_log_file_num(5)
            opts.set_inplace_update_locks(32)
            print("Opening", self.filename)
            self.db = Rdict(self.filename, options=opts)

    def insert(self, value:Troublecard) -> str:
        with self.lock:
            self.db[str(value.id)] = value.to_json()
            return str(value.id)

    def list_ids(self):
        return [key for key in self.db.keys()]

    def search(self, filterfunc):
        with self.lock:
            results = []
            for key in self.db.keys():
                data = self.get(key)
                if filterfunc(data):
                    yield data

    def get(self, key):
        # does NOT take a lock because this is threadsafe.
        if key in self.db:
            return Troublecard.from_json(self.db[key])
        else:
            return None
    
    def page(self, after=None, limit=10):
        with self.lock:
            if after is None:
                after = str(ksuid())
            keys = self.db.keys(backwards=True, from_key=after)
            for key in keys:
                if limit <= 0:
                    break
                yield self.get(key)
                limit -= 1

    def most_recent_id(self):
        with self.lock:
            keys = self.db.keys(backwards=True, limit=1)
            if len(keys) > 0:
                return keys[0]
            else:
                return None
    
    

    def delete(self, key):
        with self.lock:
            if key in self.db:
                del self.db[key]

    def close(self):
        self.db.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
       