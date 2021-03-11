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
brand_dict = collections.defaultdict(int)

for document in documents:
	if 'brand' not in document.keys():
		continue

	brand = document['brand']

	brand_dict[brand] += 1

top_10_items = sorted(brand_dict.items(), reverse=True, key=lambda item: item[1])[:10]
top_10_total = sum(v for k, v in top_10_items)

print(top_10_items)
print(top_10_total)
print([k for k, v in top_10_items])
