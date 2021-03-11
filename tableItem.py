import pymongo
import collections
import tools


client = pymongo.MongoClient("localhost", 27017)
db = client.jd
current_collection = db.phone
# current_collection = db.laptop
# current_collection = db.camera
documents = current_collection.find({}, {'imgs': 0, 'comments': 0, '_id': 0})

name_dict = collections.defaultdict(int)
# stop_words = ['GB', '移动']
stop_words = []

for document in documents:
	if 'tableItem' not in document.keys():
		continue

	tableItem = document['tableItem']   # 规格与包装
	for item in tableItem:

		column1_name = item['tableName']

		if column1_name not in ['主体', '主芯片']:
			continue

		dlItems = item['dlItems']
		for dlItem in dlItems:
			column2_name = dlItem[0]
			column3_name = dlItem[1]

			name_list = column3_name.split()
			results = []
			cut_flag = False

			for word in name_list:

				for stop_word in stop_words:
					if stop_word in word:
						cut_flag = True
						break

				if cut_flag:
					break

				results.append(word)

			productName = ' '.join(results)

			# if column2_name == '品牌':
			if column2_name == '产品名称':
				name_dict[productName] += 1

				# if '全网通' in productName:
				# 	print(document['url'])

print(len(name_dict.items()))

# top_10_item = sorted(name_dict.items(), reverse=True, key=lambda x: x[1])[:10]
# top_10_total = sum(v for k, v in top_10_item)
#
# print(top_10_item)
# print(top_10_total)
