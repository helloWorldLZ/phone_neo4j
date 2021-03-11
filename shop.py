import pymongo
import collections
import tools


client = pymongo.MongoClient("localhost", 27017)
db = client.jd
current_collection = db.phone
# current_collection = db.laptop
# current_collection = db.camera
documents = current_collection.find({}, {'imgs': 0, 'comments': 0, '_id': 0})

# labels = []
shop_dict = collections.defaultdict(int)

for document in documents:
	if 'shopName' not in document.keys():
		continue

	shopName = document['shopName']

	shop_dict[shopName] += 1

top_10_item = sorted(shop_dict.items(), reverse=True, key=lambda item: item[1])[:10]
top_10_total = sum(v for k, v in top_10_item)

print(top_10_item)
print(top_10_total)
