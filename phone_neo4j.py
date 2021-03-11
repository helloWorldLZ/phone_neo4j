import pymongo
import tools

from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher


client = pymongo.MongoClient("localhost", 27017)
db = client.jd
current_collection = db.phone
documents = current_collection.find({}, {'imgs': 0, 'comments': 0, '_id': 0})

phone_graph = Graph(host='localhost', user='neo4j', password='123')

shop_set = set()
top_10_brands = ['华为（HUAWEI）', 'OPPO', 'Apple', '小米（MI）', 'vivo', '纽曼（Newman）', 'realme', '天语（K-TOUCH）', '飞利浦（PHILIPS）', '三星（SAMSUNG）']
# for top_10_brand in top_10_brands:
# 	brand_node = Node('Brand', name=top_10_brand)
# 	phone_graph.create(brand_node)

for document in documents:
	attrs = ['brand', 'shopName', 'parameterList']
	missing_attr_flag = False
	for attr in attrs:
		if attr not in document.keys():
			missing_attr_flag = True
			break

	if missing_attr_flag:
		continue

	brand = document['brand']
	if brand not in top_10_brands:
		continue

	shopName = document['shopName']
	if shopName not in shop_set:
		shop_node = Node('Shop', name=shopName)

		brand_nodes = NodeMatcher('Brand')




		phone_graph.create(shop_node)

		shop_set.add(shopName)

