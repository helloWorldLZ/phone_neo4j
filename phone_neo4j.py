import pymongo
import tools

from py2neo import Graph, Node, Relationship


def get_series_type(brand_product, productName):
	stop_words = ['【', 'GB']

	productName = productName.split('：')[-1]

	index_0 = productName.find('【')
	if index_0 == 0:
		index_0 = productName.find('】')
		productName = productName[index_0 + 1:]

	name_list = productName.split()

	results = []
	cut_flag = False

	for word in name_list:

		if tools.is_chiese_word(word) and name_list.index(word) > 0:
			break

		for stop_word in stop_words:
			if stop_word in word:
				cut_flag = True
				break

		if cut_flag:
			break

		results.append(word)

	productName = ' '.join(results)

	if productName.startswith(brand_product):
		productName = productName.replace(brand_product, '')

	index_0 = brand_product.find('（')
	brand_hanzi = ''
	if index_0 > -1:
		brand_hanzi = brand[:index_0]

	if productName.startswith(brand_hanzi):
		productName = productName.replace(brand_hanzi, '')

	return productName


client = pymongo.MongoClient("localhost", 27017)
db = client.jd
current_collection = db.phone
documents = current_collection.find({}, {'imgs': 0, 'comments': 0, '_id': 0})

phone_graph = Graph(host='localhost', user='neo4j', password='123')

top_10_brands = ['华为（HUAWEI）', 'OPPO', 'Apple', '小米（MI）', 'vivo', '纽曼（Newman）', 'realme', '天语（K-TOUCH）', '飞利浦（PHILIPS）', '三星（SAMSUNG）']

# root_phone_node = Node('Root_phone', name='手机', productId='001')
# for top_10_brand in top_10_brands:
# 	brand_node = Node('Brand', name=top_10_brand)
# 	root_2_top_brand = Relationship(root_phone_node, 'INCLUDES', brand_node)
# 	phone_graph.create(root_2_top_brand)

for document in documents:
	attrs = ['brand', 'shopName', 'parameterList', 'productId']
	missing_attr_flag = False
	for attr in attrs:
		if attr not in document.keys():
			missing_attr_flag = True
			break

	if missing_attr_flag:
		continue

	brand = document['brand']
	shopName = document['shopName']
	productId = document['productId']
	parameterList = document['parameterList']

	if brand not in top_10_brands:
		continue

	node_name = get_series_type(brand, parameterList[0])
	if node_name == '':
		continue

	shop_node = phone_graph.nodes.match('Shop', name=shopName).first()
	brand_node = phone_graph.nodes.match('Brand', name=brand).first()
	phone_node = phone_graph.nodes.match('Phone', productId=productId).first()

	if shop_node is None:
		shop_node = Node('Shop', name=shopName)
		phone_graph.create(shop_node)

	if phone_node is None:
		phone_node = Node('Phone', name=get_series_type(brand, parameterList[0]), productId=productId)
		phone_graph.create(phone_node)

	brand_2_shop = Relationship(brand_node, 'SELLER', shop_node)
	shop_2_phone = Relationship(shop_node, 'ON_SALE', phone_node)
	phone_2_brand = Relationship(phone_node, 'BRAND', brand_node)

	phone_graph.create(brand_2_shop | shop_2_phone | phone_2_brand)
