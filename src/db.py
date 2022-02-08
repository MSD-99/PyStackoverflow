import pymongo

host = 'local'
port = 27017
client = pymongo.MongoClient(host= host, port=port)
mongodb = client.Pystackoverflowbot