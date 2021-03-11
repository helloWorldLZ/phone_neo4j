import pymongo
import collections
import tools


client = pymongo.MongoClient("localhost", 27017)
db = client.jd
current_collection = db.laptop
documents = current_collection.find({})

# labels = []
# statistics = collections.defaultdict(list)
i = 0
for document in documents:
	# line = ''
	brand = document['brand']
	texts = []

	i += 1
	if i > 200:
		break

	parameterList = document['parameterList']   # 商品介绍
	for item in parameterList:
		results = item.split('：')

		label = tools.get_label(results[0])

		texts.append(results[1])

	print(','.join(texts))

	# tableItem = document['tableItem']   # 规格与包装
	# for item in tableItem:
	
	# 	column1 = item['tableName']
	#
	# 	dlItems = item['dlItems']
	# 	for dlItem in dlItems:
	# 		column2 = dlItem[0]
	# 		column3 = dlItem[1]


# for k, v in statistics.items():
# 	num = len(v)
#
# 	if num > 100:
# 		print(k, '  ', num)
