# run this file to see the content of frontier.shelve.db, 
# which is the storage for the frontier queue
import shelve

db = shelve.open("frontier.shelve")

for key in db:
    print(key, db[key])

db.close()
