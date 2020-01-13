#coding=utf-8
import id3
import csv
import treePlotter
def readCsv(fileName):
	dataSet = []
	count = 1
	with open(fileName,'r') as infile:
		readCSV = csv.reader(infile, delimiter=',')
		for line in readCSV:
			if count == 1:
				title = line
				count += 1
			else:
				dataSet.append(line)
		infile.close()
		return title,dataSet
		
def test(title,fileName,target):
	with open(fileName,'r') as infile:
		readCSV = csv.reader(infile, delimiter=',')
		count  = 1
		for line in readCSV:
			if count == target:
				infile.close()
				return line
			count += 1
		infile.close()
		return 0
		
def txtToList(file_name):
	result = []
	with open(file_name,'r') as infile:
		for line in infile:
			temp = line.strip()
			if temp != '':
				result.append(temp)
	return result

def getLeft(atom_list):
	left_list = []
	for member in atom_list:
		temp = member.split('=')
		left_list.append(temp[0].strip())
	return left_list

def findPosition(target_list,target):
	count = 0
	for member in target_list:
		if member == target:
			return count
		else:
			count = count + 1		
	return 'error'
	
def getConvertList(atom_list,left_list):
	convert_list = []
	for member in left_list:
		position = findPosition(atom_list,member)
		if position == 'error':
			print('target not found ' + member)
			return 'false'
		else:
			convert_list.append(position)
	return convert_list
			
def getRight(atom_list):
	right_list = []
	for member in atom_list:
		temp = member.split('=')
		right_list.append(temp[1].strip())
	return right_list

def dataSetToAtomDataSet(origin_dataset,convert_list,right_list,origin_title):
	atom_dataset = []
	for member in origin_dataset:
		temp = []
		for i in range(len(right_list)):
			if right_list[i] in origin_title:
				right_position = findPosition(origin_title,right_list[i])
				if member[right_position].lower() == member[convert_list[i]].lower():
					temp.append('true')
				else:
					temp.append('false')
			else:	
				if right_list[i].lower() == member[convert_list[i]].lower():
					temp.append('true')
				else:
					temp.append('false')
		atom_dataset.append(temp)
	return atom_dataset

def creatAtomCsv(atom_list,atom_dataset,origin_dataSet):
	newtitle = atom_list
	newtitle.append('isgood')
	for i in range(len(atom_dataset)):
			atom_dataset[i].append(list(origin_dataSet[i])[-1])
	return newtitle,atom_dataset		

def creatCsv(title,dataset):
	with open('atom.csv','w',newline='') as outfile:
		writer = csv.writer(outfile)
		writer.writerow(title)
		for member in dataset:
			writer.writerow(member)
	outfile.close()


def findValue(title,list_left,list_right,position):
	for i in range(len(list_left)):
		if list_left[i] == list_left[position]:
			if list_right[i] in title:
				continue
			else:
				return list_right[i]
	return 'notfound'



def toVec(atom_title,target): #target like n[1] = T & n[2] = C
	target_vec = []
	if '&' in target:
		target_list = target.split('&')
	else:
		target_list = []
		target_list.append(target)
	print(target_list)
	target_list_left = getLeft(target_list[:])
	print(target_list_left)
	target_list_right = getRight(target_list[:])
	print(target_list_right)
	print(atom_title)
	atom_title_left = getLeft(atom_title[:])
	atom_title_right = getRight(atom_title[:])
	for i in range(len(atom_title_left)):
		find_flag = 'false'
		for j in range(len(target_list_left)):
			if atom_title_left[i] == target_list_left[j]:
				find_flag = 'true'
				if atom_title_right[i] in atom_title_left:
					if atom_title_right[i] in target_list_left:
						position = findPosition(target_list_left,atom_title_right[i])
						find_flag_part = 'true'
						print(j)
						print(target_list_left)
						print(target_list_right)
						value_left = findValue(atom_title,target_list_left,target_list_right,j)
						if value_left == 'notfound':
							find_flag_part = 'false'
						value_right = findValue(atom_title,target_list_left,target_list_right,position)
						if value_right == 'notfound':
							find_flag_part = 'false'
						if find_flag_part == 'true':
							print(value_left)
							print(value_right)
							if value_left.lower() == value_right.lower():
								target_vec.append('true')
							else:
								target_vec.append('false')
						else:
							target_vec.append('undefinded')			
					else:
						target_vec.append('undefinded')
				else:
					if target_list_right[j].lower() == atom_title_right[i].lower():
						target_vec.append('true')
					else:
						target_vec.append('false')
		if find_flag == 'false':
			target_vec.append('undefinded')
	return target_vec
	




if __name__ == "__main__":
	#convert part
	
	atom_list = txtToList('atom.txt')
	#print(atom_list)
	origin_title,origin_dataSet = readCsv('mutual_data.csv')
	left_list = getLeft(atom_list[:])
	#print(left_list)
	#print(origin_title)
	convert_list = getConvertList(origin_title,left_list)
	#print(convert_list)
	right_list = getRight(atom_list[:])
	#print(right_list)
	atom_dataset = dataSetToAtomDataSet(origin_dataSet,convert_list,right_list,origin_title)
	#print(atom_dataset)
	newtitle,newdataset = creatAtomCsv(atom_list[:],atom_dataset[:],origin_dataSet)
	creatCsv(newtitle,newdataset)
	
	#decision tree part
	
	title,dataSet = readCsv('atom.csv')
	print(title[:-1])
	myTree = id3.createTree(dataSet,title[:-1])
	treePlotter.createPlot(myTree)
	
	'''
	#recive some message like n[1] = T & n[2] = C
	title,dataSet = readCsv('atom.csv')
	message = 'n[1] = T'
	message_vec = toVec(title[:-1],message)
	print(message_vec)
	'''
	'''
	#test 18 5 11
	title,dataSet = readCsv('atom.csv')
	myTree = id3.createTree(dataSet,title[:-1])
	message = 'n[1] = T & n[2] = T & x = true'
	message_vec = toVec(title[:-1],message)
	result = id3.classify2(myTree,title[:-1],message_vec)
	print(result)
	'''
	
	
	'''
	tree = id3.grabTree("mutual_tree.txt")
	print(tree)
	treePlotter.createPlot(tree)
	fileName = 'mutual_data.csv'
	title,dataSet = readCsv(fileName)
	myTree = id3.createTree(dataSet,title[:])
	treePlotter.createPlot(myTree)
	#id3.storeTree(myTree,'mutual_tree.txt')
	#testline = test(title,fileName,800)
	#result = id3.classify(myTree,title,testline)
	#print(result)
	
	testSet = []
	for i in range(103,955):
		temp = test(title,fileName,i)
		testSet.append(temp)
	for line in testSet:
		result = id3.classify(myTree,title,line)
		if result != 'TRUE':
			print('false')
	'''

	
		
		
