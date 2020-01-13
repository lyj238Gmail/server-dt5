#coding=utf-8
import csv

#读取csv文件，返回表头和内容（列表形式）
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

#读取txt文件中的原子公式，以列表的形式返回
def txtToList(file_name):
	result = []
	with open(file_name,'r') as infile:
		for line in infile:
			temp = line.strip()
			if temp != '':
				result.append(temp)
		infile.close()
	return result
	
#输入为原子公式列表，将每个原子公式的等号左值以列表的形式返回	
def getLeft(atom_list):
	left_list = []
	for member in atom_list:
		temp = member.split('=')
		left_list.append(temp[0].strip())
	return left_list

#输入为原子公式列表，将每个原子公式的等号右值以列表的形式返回
def getRight(atom_list):
	right_list = []
	for member in atom_list:
		temp = member.split('=')
		right_list.append(temp[1].strip())
	return right_list


#找到成员在列表中的位置，输入依次为目标列表和目标成员
def findPosition(target_list,target):
	count = 0
	for member in target_list:
		if member == target:
			return count
		else:
			count = count + 1		
	return 'error'


#生成转换列表，用于可达集csv到原子公式csv的转换，产生出列表包含原子公式与可达集表头的对应关系，依次输入为可达集表头和原子公式左值列表
def getConvertList(origin_list,left_list):
	convert_list = []
	for member in left_list:
		position = findPosition(origin_list,member)
		if position == 'error':
			print('target not found ' + member)
			return 'false'
		else:
			convert_list.append(position)
	return convert_list

#转换函数，用于可达集csv内容（不包括表头的部分）到原子公式csv内容的转换
#输入依次为原子公式内容（列表）、转换列表、原子公式右值列表、可达集表头
def dataSetToAtomDataSet(origin_dataset,convert_list,right_list,origin_title):
	atom_dataset = []
	for member in origin_dataset:
		temp = []
		for i in range(len(right_list)):
			if right_list[i] in origin_title:
				right_position = findPosition(origin_title,right_list[i])
				if(member[right_position].lower() == 'undefined' or member[convert_list[i]].lower() == 'undefined'):
					temp.append('undefined')
				else:
					if member[right_position].lower() == member[convert_list[i]].lower():
						temp.append('true')
					else:
						temp.append('false')
			else:
				if(right_list[i].lower() == 'undefined' or member[convert_list[i]].lower() == 'undefined'):
					temp.append('undefined')
				else:	
					if right_list[i].lower() == member[convert_list[i]].lower():
						temp.append('true')
					else:
						temp.append('false')
		atom_dataset.append(temp)
	return atom_dataset

#用于生成原子公式的csv，以列表的形式返回表头和内容，输入依次为原子公式csv的表头、内容和可达集csv的内容（用于添加isgood项）	
def creatAtomCsv(atom_list,atom_dataset,origin_dataSet):
	newtitle = atom_list
	newtitle.append('isgood')
	for i in range(len(atom_dataset)):
			atom_dataset[i].append(list(origin_dataSet[i])[-1])
	return newtitle,atom_dataset		

#创建csv文件，输入一次为表头和内容
def creatCsv(title,dataset,atom_csv):
	with open(atom_csv,'w',newline='') as outfile:
		writer = csv.writer(outfile)
		writer.writerow(title)
		for member in dataset:
			writer.writerow(member)
	outfile.close()

#对于判断变量等于变量的情况，返回公式中变量的取值。输入依次为，原子公式csv的表头、用于判断的原子公式组合的左值列表、右值列表和变量在左值列表中的位置
def findValue(title,list_left,list_right,position):
	for i in range(len(list_left)):
		if list_left[i] == list_left[position]:
			if list_right[i] in title:
				continue
			else:
				return list_right[i]
	return 'notfound'

#用于将给定的原子公式组合转换为，以原子公式为基准的矢量（用于决策树的判断）
def toVec(atom_title,target): #target like n[1] = T & n[2] = C
	target_vec = []
	if '&' in target:
		target_list = target.split('&')
	else:
		target_list = []
		target_list.append(target)
	target_list_left = getLeft(target_list[:])
	target_list_right = getRight(target_list[:])
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
	
