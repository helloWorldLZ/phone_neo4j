import pymongo
import collections
import tools


client = pymongo.MongoClient("localhost", 27017)
db = client.jd
current_collection = db.phone
# current_collection = db.laptop
# current_collection = db.camera
documents = current_collection.find({}, {'imgs': 0, 'comments': 0, '_id': 0})

cpu_dict = collections.defaultdict(list)
# stop_words = ['GB', '【']
stop_words = []

for document in documents:
	if 'parameterList' not in document.keys():
		continue

	parameterList = document['parameterList']

	cpu = ''
	for parameter in parameterList:
		if 'CPU' in parameter:
			cpu = parameter
			break

	cpu_type = cpu.split('：')[-1]
	cpu_dict[cpu_type].append(0)

total = 0
for k, v in cpu_dict.items():
	num = len(v)

	# if num < 3:
	# 	continue

	print(k, '  ', num)

	total += num

print(total)
