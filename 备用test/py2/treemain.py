#coding=utf-8

import csv
import socket

import id3
import treePlotter
import csvOperation
import package_pre.pre

#将可达集csv转换为原子公式csv，参数为可达集csv名称、原子公式存放的txt文件的名称,输出为atom.csv
def convert(origin_csv,atom_txt,atom_csv):
	atom_list = csvOperation.txtToList(atom_txt)
	origin_title,origin_dataSet = csvOperation.readCsv(origin_csv)
	left_list = csvOperation.getLeft(atom_list[:])
	convert_list = csvOperation.getConvertList(origin_title,left_list)
	right_list = csvOperation.getRight(atom_list[:])
	atom_dataset = csvOperation.dataSetToAtomDataSet(origin_dataSet,convert_list,right_list,origin_title)
	newtitle,newdataset = csvOperation.creatAtomCsv(atom_list[:],atom_dataset[:],origin_dataSet)
	csvOperation.creatCsv(newtitle,newdataset,atom_csv)

#生成决策树，输入为原子公式csv文件（训练集）
def createTree(atom_csv,undefined_percentage):     #输入为处理过的可达集、优先级字典
	title,dataSet = csvOperation.readCsv(atom_csv)
	#add 0822 for only one class  可能返回字符串，而不是字典
	classList = [example[-1] for example in dataSet]
	if len(set(classList)) == 1:
		return '(' + title[-1] + ' = ' + classList[0] + ')'
	else:
		myTree = id3.createTree(dataSet,title[:-1],undefined_percentage) #0726,修改函数id3.createTree，加入优先级判定依据，即undefined_percentage
		return myTree

#绘制决策树的图片
def printTree(tree):
	treePlotter.createPlot(tree)
	
#保存决策树，输入为决策树（字典）、保存文件的名称
def saveTree(tree,filename):
	id3.storeTree(tree,filename)

#读取使用saveTree保存的树，返回树（字典），输入为存有树的文件名称	
def loadTree(filename):
	tree = id3.grabTree(filename)
	return tree

#使用决策树判断原子公式组合（字符串），输入为决策树（字典）、原子公式的表头（含有isgood项）、原子公式组合（字符串，使用&连接）
def classify(tree,atom_title,message):
	message_vec = csvOperation.toVec(atom_title[:-1],message)
	result = id3.classify3(tree,atom_title[:-1],message_vec)
	return result

'''
#20180726用于计算各个属性中undefined的概率，返回是字典形式，字典内容为： 属性名：包含undefined概率
def percentage(csvfile):
	title,dataSet = csvOperation.readCsv(csvfile)
	undefined_percentage_dict = {}
	number_of_data = len(dataSet)
	for i in range(len(title)):
		undefined_counter = 0  #初始化计数器
		for j in range(number_of_data):
			if dataSet[j][i].lower() == 'undefined':         #j代表行数，i代表列数
				undefined_counter = undefined_counter + 1
		undefined_percentage_dict[title[i]] = undefined_counter/number_of_data
	return 	undefined_percentage_dict
'''

def priority_test(csvfile):
	result = {}
	title,dataSet = csvOperation.readCsv(csvfile)
	for member in title:
		if  member ==  'Chan2[NODE_1].Cmd' or member ==  'ExGntd' or member ==  'ShrSet[NODE_1]' or member ==  'CurCmd':
			result[member] = 0
			print('1')
		else:
			result[member] = 0.1
	return result
	


#teacher 使用可达集csv、原子公式txt、生成的原子公式csv名称、存储树的文件的名称，生成决策树，并打印
def teacher(origin_csv,atom_txt,atom_csv,tree_save_file):
	'''
	convert(origin_csv,atom_txt,atom_csv)             #0726 获得原子公式为表头的训练数据
	undefined_percentage = percentage(atom_csv)    #0726 获得训练数据的undefined概率（优先级），undefined概率越大优先级越底
	package_pre.pre.output_pre(atom_csv,'pre.csv') #0726 对训练数据进行预处理
	tree = createTree('pre.csv',undefined_percentage) #0726 修改createTree函数，加入优先级标准，即undefined_percentage
	'''
	undefined_percentage = priority_test(origin_csv)
	package_pre.pre.output_pre(origin_csv,'pre.csv')
	tree = createTree('pre.csv',undefined_percentage)
	saveTree(tree,tree_save_file)
	#printTree(tree)
	return tree

#assistant 在teacher生成过树后，读取存储树的文件，打印并返回树，输入为存储决策树的文件的名字
def assistant(tree_save_file):
	tree = loadTree(tree_save_file)
	printTree(tree)
	return tree

'''
def student(tree,atom_title):
	HOST='localhost'
	PORT=1307
	BUFFER_SIZE=1024
	flag = '1'
	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_address=(HOST,PORT)
	sock.bind(server_address)
	print('Waiting for message ...')
	sock.listen(1)
	while(flag == '1'):
		client_socket,client_address=sock.accept()
		print("Connected %s successfully"%str(client_address))
		data = ''
		target_len = 0
		current_rec_len = 0
		while (current_rec_len < target_len) or target_len == 0:
			try:
				temp = client_socket.recv(BUFFER_SIZE)
				if target_len == 0:
					temp = temp.decode().split(',')
					target_len = int(temp[0])
					data += ','.join(temp[1:])
				else:
					data += temp
				current_rec_len = len(data)
			except socket.timeout as e:
				pass
		print('recive:')
		print(data)
		result = classify(tree,atom_title,data)
		client_socket.sendall(result.encode())
		flag = input('input 1 to continue:')
	sock.close()
'''		
	
def creatDTree(origin_csv,prior_dict):
	#package_pre.pre.output_pre(origin_csv,'pre.csv') #预处理
	tree = createTree(origin_csv,prior_dict) #生成树
	saveTree(tree,'tree_save.txt') #存储树
	return tree




#读取原协议的属性列表
def read_txt(filename):
	f = open(filename)
	lines = f.readlines()
	for line in lines:
		temp = line
		break
	f.close()
	result_list = temp.split(',')
	if 'isgood\n' in result_list:
		result_list.remove('isgood\n')
	#print result_list
	return result_list
	
	


#选择分类属性，避免分类属性只含一种状态
def chooseClassifyAttribute(origin_csv,attribute_list):
	title1,dataSet = csvOperation.readCsv(origin_csv)
	title = read_txt('title.txt')
	result = attribute_list[0]  #默认返回第一属性，防止所有属性包含的状态种类数均为1
	for i in range(len(title)):
		title[i] = title[i].replace('NODE_','').lower()
	if len(attribute_list) == 1: #只有一种属性
		return attribute_list[0]
	else: #有多种属性
		for member in attribute_list:
			if member not in title:
				print 'error treemain 153 member not in title!!!!!!!!'
				print 'memeber :' + member
				print 'title :' + title
			else:
				position = title.index(member)
				temp_list = [example[position] for example in dataSet] #找到数据集中该位置的所有取值
				temp_set = set(temp_list)
				temp_set_list = list(temp_set)
				if len(temp_set_list) != 1: #该属性包含的状态不只一个，选择该属性作为分类属性
					result = member
					break
	return result
			
	
	
if __name__ == "__main__":
	origin_csv = 'data_2.csv'
	atom_txt = 'atom.txt'
	atom_csv = 'atom.csv'
	tree_save_file = 'tree_youxian.txt'
	command = 0 #0调用用teacher，表示已经生成过树、非0代表调用assistant，代表读取已生成的树
	if command == 0:
		tree = teacher(origin_csv,atom_txt,atom_csv,tree_save_file)
	else:
		tree = assistant(tree_save_file)
	#title,dataSet = csvOperation.readCsv(atom_csv)
	#student(tree,title)
	'''
	#test classify
	testVec = 'n[1] = T & n[2] = T'
	result = classify(tree,title,testVec)
	print(result)
	'''
	#print (priority_test(origin_csv))
	
	
	

