
from bae.core import const
import pymongo


def getdb():
    db_name = 'nnYUvEvZFuvtqfzDkWnJ'
    con = pymongo.Connection(host = const.MONGO_HOST, port = int(const.MONGO_PORT))
    db = con[db_name]
    db.authenticate(const.MONGO_USER, const.MONGO_PASS)
    return con, db


def save(data, table):
    """data: [{'a': 1, 'b': 2}, {'a': 2, 'b': 1}]"""
    con, db = getdb()
    ware = db[table]
    result = ware.insert(data)
    con.disconnect()
    return result


def fetch(restrict, table):
    assert(isinstance(restrict, dict))

    con, db = getdb()
    ware = db[table]
    result = ware.find_one(restrict)
    con.disconnect()
    return result

