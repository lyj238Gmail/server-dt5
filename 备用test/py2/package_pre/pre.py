#coding=utf-8
import csv
import random
#由于变量的取值不仅限于true和false因此pre预处理程序存在漏洞
'''
新代码思路
1.读取scv文件，并构建数组（列表形式）
2.使用列表解析读取一列元素
3.记录2中读取到的元素（除Undefined外）
4.循环2-3知道读取完n-1列（n为总列数）
5.读取scv中的每行，如果该行中存在Undefined这将其随机替换为其他可取值
'''
'''
def pre(inName,outName):
	with open(inName,'r') as inCsvFile, open(outName,'w+',encoding = 'utf-8',newline='')as outCsvFile:
		writeCSV = csv.writer(outCsvFile)
		readCSV = csv.reader(inCsvFile, delimiter=',')
		count  = 1
		for line in readCSV:
			if count == 1:
				count += 1
				writeCSV.writerow(line)
				continue
			for i in range(len(line)):
				if line[i] == 'Undefined':
					flag = random.randint(0,1)
					if flag == 0:
						line[i] = 'TRUE'
					else:
						line[i] = 'FALSE'
			writeCSV.writerow(line)
		inCsvFile.close()
		outCsvFile.close()
'''
def read(inName):
	data = []
	with open(inName,'r') as inCsvFile:
		readCSV = csv.reader(inCsvFile, delimiter=',')
		for line in readCSV:
			data.append(line)
	inCsvFile.close()
	return data

def addDataRange(data,column_len):
	data_range = []
	for i in range(column_len):
		temp = set([line[i] for line in data])
		if 'Undefined' in temp:
			temp.remove('Undefined')
		data_range.append(list(temp))
	return data_range

def pre(data,data_range,column_len):
	for line in data:
		for i in range(column_len):
			if line[i] == 'Undefined':
				if(len(data_range[i]) == 0) or (len(data_range[i]) == 1):
					number = random.randint(0,1)
					if number == 0:
						line[i] = 'DATA_1'
					else:
						line[i] = 'DATA_2'
				else:
					current_len = len(data_range[i])
					number = random.randint(0,current_len)
					line[i] = data_range[i][number - 1]

def write(outName,data):
	with open(outName,'wb+')as outCsvFile:
		writeCSV = csv.writer(outCsvFile)
		for line in data:
			writeCSV.writerow(line)
		outCsvFile.close()

def output_pre(infileName,outfileName):
	data = read(infileName)
	column_len = len(data[0])
	data_range = addDataRange(data[1:],column_len)
	pre(data,data_range,column_len)
	write(outfileName,data)
	
	
def readValueSetTxt(filename): #读取valueset.txt 获得各个属性的可取值。并以字典的形式返回
	f = open(filename)
	lines = f.readlines()
	value_set_dict = {}
	count = 1
	temp = ''
	for line in lines:
		if count%2 == 1:
			temp = line.strip()
		else:
			temp_list = line.strip().split(',')
			value_set_dict[temp] = temp_list
		count = count + 1
	return value_set_dict
	

def pre2(data,value_set_dict):
	title = data[0]
	column_len = len(title)
	for line in data:
		for i in range(column_len):
			if line[i] == 'Undefined':
				value_list = value_set_dict[title[i]]
				value_number = len(value_list)
				if(value_number == 0):
					print 'error value number 0!'
				random_number = random.randint(0,value_number - 1)
				line[i] = value_list[random_number]
	
	

	
def output_pre2(infileName,outfileName): #undefined的预处理，输入为待处理文件名与生成文件名
	data = read(infileName) #读取待处理数据
	value_set_dict = readValueSetTxt('valueset.txt')
	pre2(data,value_set_dict)
	write(outfileName,data)
	
	
if __name__ == "__main__":
	#infileName = 'data_part.csv'
	#infileName = 'data.csv'
	#outfileName = 'pre.csv'
	#data = read(infileName)
	#column_len = len(data[0])
	#data_range = addDataRange(data[1:],column_len)
	#pre(data,data_range,column_len)
	#write(outfileName,data)
	#print(data)
	#print readValueSetTxt('valueset.txt')
	output_pre2('ndata.csv','pre.csv')
	
