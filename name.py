import pymongo
import collections
import tools


def is_chiese_word(word):
	flag = True

	for char in word:
		cp = ord(char)

		if not ((cp >= 0x4E00 and cp <= 0x9FFF) or  #
				(cp >= 0x3400 and cp <= 0x4DBF) or  #
				(cp >= 0x20000 and cp <= 0x2A6DF) or  #
				(cp >= 0x2A700 and cp <= 0x2B73F) or  #
				(cp >= 0x2B740 and cp <= 0x2B81F) or  #
				(cp >= 0x2B820 and cp <= 0x2CEAF) or
				(cp >= 0xF900 and cp <= 0xFAFF) or  #
				(cp >= 0x2F800 and cp <= 0x2FA1F)):  #

			flag = False
			break

	return flag


client = pymongo.MongoClient("localhost", 27017)
db = client.jd
current_collection = db.phone
# current_collection = db.laptop
# current_collection = db.camera
documents = current_collection.find({}, {'imgs': 0, 'comments': 0, '_id': 0})

productName_dict = collections.defaultdict(int)
stop_words = ['【', 'G', '万', '全']
# stop_words = ['【', '拍', '移', '网', '+']

for document in documents:
	if 'parameterList' not in document.keys():
		continue

	productName = document['parameterList'][0]
	productName = productName.split('：')[-1]

	index_0 = productName.find('【')
	if index_0 == 0:
		index_0 = productName.find('】')
		productName = productName[index_0 + 1:]

	name_list = productName.split()

	results = []
	cut_flag = False

	for word in name_list:

		# 处理【 （ 符号
		if is_chiese_word(word) and name_list.index(word) > 0:
			break

		for stop_word in stop_words:
			if stop_word in word:
				cut_flag = True
				break

		if cut_flag:
			break

		results.append(word)

	productName = ' '.join(results)

	# if len(productName) < 1:
	# 	print(document['productId'])

	productName_dict[productName] += 1

total = 0
for k, v in productName_dict.items():
	print(k, '  ', v)

	if len(k) < 1:
		print('-'*20 + k + '-'*20)

	total += v

# print(total)
