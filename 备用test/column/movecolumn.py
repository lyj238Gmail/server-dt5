#coding=utf-8

import csv
import sys
import os

def move_cvs_col(fname, newfname, index,target_column):
	with open(fname) as csvin, open(newfname, 'wb+') as csvout:
		reader = csv.reader(csvin)
		writer = csv.writer(csvout)
		count = 0
		data = []
		for row in reader:
			newrow = row[:index] + row[index + 1:]
			#print('1')
			newrow.append(target_column[count])
			data.append(newrow)
			count = count + 1
		for member in data:
			writer.writerow(member)
	csvout.close()
		
def read_column(fname,index):
	with open(fname) as csvin:
		reader = csv.reader(csvin)
		target_column = [row[index] for row in reader]
		return target_column

def move(fname,newfname,index):
	target_column = read_column(fname,index)
	dir_path = os.getcwd() +'/csvpathfile/'
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	newfname_temp = dir_path + newfname
	move_cvs_col(fname,newfname_temp,index,target_column)
	return newfname_temp #传回生成文件的位置

#读取csv文件，返回表头和内容（列表形式）
def readCsvHead(fileName):
	count = 1
	with open(fileName,'r') as infile:
		readCSV = csv.reader(infile, delimiter=',')
		for line in readCSV:
			if count == 1:
				title = line
				break
		infile.close()
		return title

def newCsv(fname,newfname,attribute_name):
	title = readCsvHead(fname)
	count = 0
	position = -1
	for member in title:
		if member.replace('NODE_','').lower() == attribute_name.lower():
			position = count
			break
		count = count + 1
	if position == -1:
		print('no attribute')
		sys.exit(1)
	else:
		result = move(fname,newfname,position)
		return result
		
		
def findPosition(title,attribute_list): #找到属性列表中的属性位于title中的位置
	result_list = []
	for member in attribute_list:
		position = title.index(member.lower())
		result_list.append(position)
	return result_list
		
def completePath(newfname):
	dir_path = os.getcwd() +'/csvpathfile/'
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	newfname_complete = dir_path + newfname
	return newfname_complete



#用于读取原协议的属性列表
def read_txt(filename):
	f = open(filename)
	lines = f.readlines()
	for line in lines:
		temp = line
		break
	f.close()
	result_list = temp.split(',')
	#print result_list
	return result_list[:-1]

		
def newAttributeCsv(fname,newfname,classify_attribute_name,attribute_list): #建立只含查询不变式属性的csv
	#title = readCsvHead(fname)
	#print title
	title = read_txt('title.txt')
	#print title2
	#print title2
	newfname_complete = completePath(newfname) #生成新csv的位置
	for i in range(len(title)): #去除对称规约对属性名称的影响
		title[i] = title[i].replace('NODE_','').lower()
		
	#print title	
	
	position_list = findPosition(title,attribute_list) #查询不变式中属性在title中的位置
	classify_attribute_pisition = title.index(classify_attribute_name.lower()) #分类属性在查询不变式中的位置
	with open(newfname_complete, 'wb+') as csvout:
		writer = csv.writer(csvout)
		data_set_column = []
		#print(position_list)
		for number in position_list:
			if number != classify_attribute_pisition: #先加入非分类属性的属性
				attribute_column = read_column(fname,number)
				data_set_column.append(attribute_column)
		classify_attribute_column = read_column(fname,classify_attribute_pisition)
		data_set_column.append(classify_attribute_column) #加入分类属性
		data_set_row=[[r[col] for r in data_set_column] for col in range(len(data_set_column[0]))] #列表行转列
		#print(data_set_row)
		for member in data_set_row: #生成新的csv
			writer.writerow(member)
	csvout.close()
	return newfname_complete #返回新csv的位置
		
		
	
	
	




if __name__ == "__main__":
	#move_cvs_col('data.csv', 'new.csv', 0)
	#print(read_column('data.csv',0))
	#move('data.csv', 'new.csv', 0)
	#newCsv('data.csv', 'new.csv', 'Cache[1].Data')
	#test = 'Cache[NODE_1].Data'
	#print(test.replace('NODE_',''))
	'''
	test = ['ctf','ctf1','ctf3']
	result = test[0:0]
	result.extend(test[1:2])
	print(result)
	'''
	fname = 'data.csv'
	newfname =  'new.csv'
	attribute_list = ['Cache[1].Data','ExGntd','MemData']
	classify_attribute_name = 'ExGntd'
	print newAttributeCsv(fname,newfname,classify_attribute_name,attribute_list)
	
