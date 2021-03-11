import pypinyin
import pymongo
import collections
import json


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

# def get_first_letters(text):
# 	results = pypinyin.pinyin(text, pypinyin.Style.FIRST_LETTER)
#
# 	# 把拼音结果中的其他字符去掉。例如：'固态硬盘（SSD）'
# 	# before: [['g'], ['t'], ['y'], ['p'], ['（SSD）']]
# 	# after: ['g', 't', 'y', 'p']
# 	letters = [item[0] for item in results if len(item[0]) < 2]
#
# 	res = ''.join(letters)
# 	# print(res)
#
# 	return res
#
#
# def get_label_statistics():
# 	client = pymongo.MongoClient("localhost", 27017)
# 	db = client.jd
# 	current_collection = db.laptop
# 	documents = current_collection.find({})
#
# 	label_statistics = collections.defaultdict(list)
# 	for document in documents:
#
# 		parameterList = document['parameterList']  # 商品介绍
# 		for item in parameterList:
# 			results = item.split('：')
# 			label = get_first_letters(results[0])
#
# 			if len(label_statistics[label]) == 0:
# 				label_statistics[label].extend([results[0], 1])    # [label 对应的的中文名称, 出现次数]
# 			else:
# 				label_statistics[label][-1] += 1
#
# 	res = {k: v for k, v in label_statistics.items() if v[-1] > 300}
#
# 	with open('label_map.json', 'w', encoding='utf-8') as f_obj:
# 		json.dump(res, f_obj, indent=4, ensure_ascii=False)
#
#
# # def get_label_map():
# # 	with open('label_map.json', encoding='utf-8') as f_obj:
# # 		res = json.load(f_obj)
# #
# # 	return res
#
#
# def get_label(text):
# 	label = get_first_letters(text)
#
# 	with open('label_map.json', encoding='utf-8') as f_obj:
# 		res = json.load(f_obj)
#
# 	if label not in res.keys():
# 		label = 'O'
#
# 	return label


# print(pypinyin.pinyin('固态硬盘（SSD）', pypinyin.Style.FIRST_LETTER))

# get_first_letters('商品名称')

# get_label_statistics()

# get_label_map()

# get_label('商品名称')
