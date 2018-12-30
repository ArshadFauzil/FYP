import pymongo
import os
import pprint

myclient = pymongo.MongoClient(os.getenv('MONGO_CLIENT'))
pc_db = myclient[os.getenv('MONGO_DB')]

mydict = {"name": "Arshad", "address": "20 Dehiwala"}


# x = mycol.insert_one(mydict)


def insert_pseudocode_into_db(pseudocode):
    coll_name = pc_db["pseudocodes"]
    pc = {"PseudoCode": pseudocode}

    coll_name.insert_one(pc)


def get_pseudocode_from_db():
    coll_name = pc_db["pseudocodes"]
    records = list(coll_name.find({}))
    lines = []
    for x in records:
        lines.append(x['PseudoCode'])
        # print(len(x['PseudoCode']))
    print(lines)


def delete_all_documents(collection):
    coll_name = pc_db[collection]
    coll_name.remove({})


if __name__ == '__main__':
    get_pseudocode_from_db()
    delete_all_documents('pseudocodes_temp')
