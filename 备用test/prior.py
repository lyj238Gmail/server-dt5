#coding=utf-8
#用于测试优先级筛选（指定用于分类的属性，获得优先级高的属性列表）、优先级决策树生成\
#决策树不变式（路径）合成、z3判断的整合

#qinv ：询问不变式
#读取qinv，将每一行的inv的小写形式存入列表并返回

import csv
import column.movecolumn
import py2.treemain
import path.inv_synthesizer
import z3check.check
import os



csvclassattribute = []
g_number = 0


#读取原协议的属性列表
def read_txt_title(filename):
	f = open(filename)
	lines = f.readlines()
	for line in lines:
		temp = line
		break
	f.close()
	result_list = temp.split(',')
	
	if 'isgood\n' in result_list:
		result_list.remove('isgood\n')
		
	for i in range(len(result_list)):
		result_list[i] = result_list[i].lower()
	#print result_list
	return result_list


def readQInv(filename):
	result = []
	f = open(filename)
	lines = f.readlines() #读取全部内容以列表形式返回
	for line in lines:
		result.append(line.lower())
	return result
	
#读取csv文件，返回表头和内容（列表形式）,将NODE_1变为1
def readCsvHead(fileName):
	count = 1
	with open(fileName,'r') as infile:
		readCSV = csv.reader(infile, delimiter=',')
		for line in readCSV:
			if count == 1:
				title = line
				break
		infile.close()
	for i in range(len(title)):
		if 'NODE_' in title[i]:
			title[i] = title[i].replace('NODE_','')
	result_title = [member.lower() for member in title]
	return result_title

#找出qinv中的属性
def analysisQinv(q_inv,title):
	attribute_result = []
	q_inv_temp = q_inv.replace('(','')
	q_inv_temp = q_inv_temp.replace(')','')
	q_inv_temp = q_inv_temp.replace('!','')
	q_inv_part_list = q_inv_temp.split(' & ')
	for member in q_inv_part_list:
		temp_list = member.split(' = ')
		for attribute in temp_list:
			attribute_temp = attribute.strip()
			#print(attribute_temp)
			#print(title)
			if (attribute_temp in title) and (attribute_temp not in attribute_result):
				attribute_result.append(attribute_temp)
	#print attribute_result
	return attribute_result





#生成优先级字典
def priorDicr(title,attribute_list):
	result = {}
	for member in title:
		if member in attribute_list:
			result[member] = 0
		else:
			result[member] = 0.1
	return result




#用于生成对应的决策树
def creatTree(origin_csv,attribute_list,prior_dict):
	#print attribute_list
	classify_attribute = py2.treemain.chooseClassifyAttribute(origin_csv,attribute_list) #添加属性筛选机制，避免分类属性只含一种状态
	new_csv_name = classify_attribute + '.csv'
	new_csv_name_temp = column.movecolumn.newAttributeCsv(origin_csv,new_csv_name,classify_attribute,attribute_list) #生成新的csv文件,并找到生成文件的位置
	tree = py2.treemain.creatDTree(new_csv_name_temp,prior_dict)
	return tree,classify_attribute

def saveStr(filename,strtarget):
	with open(filename,'w') as f:
		f.write(strtarget)
		f.close()



# handle scalarset
def analysisQinv2(q_inv,title,scalarset_list):
	q_inv_temp = q_inv.replace('(','')
	q_inv_temp = q_inv_temp.replace(')','')
	q_inv_temp = q_inv_temp.replace('!','')
	q_inv_part_list = q_inv_temp.split(' & ')
	for member in q_inv_part_list:
		temp_list = member.split(' = ')
		att_temp_list = []
		for attribute in temp_list:
			attribute_temp = attribute.strip()
			if (attribute_temp in title):
				att_temp_list.append(attribute_temp)
		if len(att_temp_list) == 1:
			if att_temp_list[0] in scalarset_list:
				return 'notinv'
	return 'mayinv'


def read_txt(filename):
	result_list = []
	f = open(filename)
	lines = f.readlines()
	for line in lines:
		result_list.append(line.strip().replace('\n',''))
	f.close()
	return result_list


def handleScalarset(qinv,attribute_list,title):
	#german scalarset_list
	'''
	scalarset_list = ['memdata','auxdata,cache[1].data','cache[2].data','chan1[1].data','chan1[2].data','chan2[1].data','chan2[2].data','chan3[1].data','chan3[2].data',\
	'curptr']
	'''
	# read scalarset_list
	scalarset_list = read_txt('sca.txt')
	scalarset_list_temp = []
	for member in scalarset_list:
		temp = member.lower()
		scalarset_list_temp.append(temp)
	
	
	
	if len(attribute_list) == 1:  # only one formula
		if attribute_list[0] in scalarset_list_temp:
			return 'notinv'
		else:
			#print attribute_list
			#print 'mayinv'
			return 'mayinv'
	#many formula
	#result = analysisQinv2(qinv,title,scalarset_list_temp)
	#return result
	return 'mayinv'

'''
def handleSingleAttribute(tree,classify_attribute): #查询不变式只有单个属性，而该属性却又多种取值，tree是字符型（str），如 A | B | C 其中A、B、C是属性可能取的值（状态）,需要手工合成路径
	value_list = tree.split(' | ')
	result = ''
	countmax = len(value_list)
	count = 1
	for member in value_list:
		if result == '':
			result = classify_attribute + ' = ' + member + '\n'
		else:
			if count == countmax:
				result = result + classify_attribute + ' = ' + member
			else:
				result = result + classify_attribute + ' = ' + member +'\n'
		count = count + 1
	return result
'''	

	

#输入为原始csv的数据、查询不变式，输出为z3的判定结果
def decisionTreeZ3(o_csvname,qinv,z3):
	global g_number
	#title = readCsvHead(o_csvname)
	title = read_txt_title('title.txt')
	attribute_list = analysisQinv(qinv,title)
	
	#由于convert函数的改善，可能不需要这步了
	'''
	#handle scalarset
	result_handle = handleScalarset(qinv,attribute_list,title)
	#print result_handle
	if result_handle == 'notinv':
		return 'sat'
	'''
	prior_dict = priorDicr(title,attribute_list) #生成优先级字典 1008虽然用不上优先级，但是在生成决策树时需要用到其中的元素，因此保留
	#classify_attribute = attribute_list[0]
	#print(prior_dict)
	dir_path = os.getcwd() +'/pathfile/'
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	result_save_name = dir_path + str(g_number) + '.txt'
	g_number = g_number + 1
	tree,classify_attribute = creatTree(o_csvname,attribute_list,prior_dict) #获得优先级树
	if type(tree) != dict: #无法分类，直接传回分类
		if ' | ' in tree: #单个属性多种取值（状态）
			return 'sat'
		else:
			saveStr(result_save_name,tree)
	else:
		path.inv_synthesizer.syn_path(tree,result_save_name,classify_attribute) #合成路径
	result = z3check.check.z3Checker(result_save_name,qinv,z3)
	return result

'''		
def priorTest(datafname,qfname):
	q_inv_list = readQInv(qfname) #读取qinv列表
	#print(analysisQinv('!((!(Cache[1].State = i)) & (!(Cache[1].Data = AuxData)))',title))
	#print(title)
	for member in q_inv_list:
		#attribute_list = analysisQinv(member,title)
		#print(attribute_list)
		result = decisionTreeZ3(datafname,member)
		if result == 'unsat':
			print member + ' : ' + 'is inv!'
		else:
			print member + ' : ' + 'is not inv!'
'''
'''
def test(datafname,qfname):
	q_inv_list = readQInv(qfname)
	decisionTreeZ3(datafname,q_inv_list[0])
'''


def convert(q_inv_low):
	q_inv_low_temp = q_inv_low.replace('[1]','[3]')
	q_inv_low_temp = q_inv_low_temp.replace('[2]','[4]')
	q_inv_low_temp = q_inv_low_temp.replace('[3]','[2]')
	q_inv_low_temp = q_inv_low_temp.replace('[4]','[1]')
	q_inv_low_temp = q_inv_low_temp.replace('= 1','= 3')
	q_inv_low_temp = q_inv_low_temp.replace('= 2','= 4')
	q_inv_low_temp = q_inv_low_temp.replace('= 4','= 1')
	q_inv_low_temp = q_inv_low_temp.replace('= 3','= 2')
	q_inv_low_temp = q_inv_low_temp.replace('1 =','3 =')
	q_inv_low_temp = q_inv_low_temp.replace('2 =','4 =')
	q_inv_low_temp = q_inv_low_temp.replace('4 =','1 =')
	q_inv_low_temp = q_inv_low_temp.replace('3 =','2 =')
	return q_inv_low_temp
	



def Test(q_inv,z3):
	
	q_inv_low = q_inv.lower()
	'''
	if 'home' in q_inv_low:
		q_inv_low_normal = q_inv_low.replace('home','1')
		#q_inv_low_temp = convert(q_inv_low)
		result = decisionTreeZ3('pre.csv',q_inv_low_normal,z3)
		if result == 'unsat':
			return 'true'
		else:
			return 'false'			
	else:
		result = decisionTreeZ3('pre.csv',q_inv_low,z3)
		if result == 'unsat':
			#return 'true'
			q_inv_low_convert = convert(q_inv_low) #对称化，即‘1’变‘2’，‘2’变‘1’
			result2 = decisionTreeZ3('pre.csv',q_inv_low_convert,z3)
			if result2 == 'unsat':
				return 'true'
			else:
				return 'false'
		else:
			return 'false'
	'''
	'''
	result = decisionTreeZ3('ndata.csv',q_inv_low,z3)
	if result == 'unsat':
		#return 'true'
		q_inv_low_convert = convert(q_inv_low) #对称化，即‘1’变‘2’，‘2’变‘1’
		result2 = decisionTreeZ3('ndata.csv',q_inv_low_convert,z3)
		if result2 == 'unsat':
			return 'true'
		else:
			return 'false'
	else:
		return 'false'
	'''

	'''
	q_inv_low = q_inv.lower()
	q_inv_low_convert = convert(q_inv_low)
	q_inv_strong = q_inv_low +' & ' + q_inv_low_convert
	result = decisionTreeZ3('pre.csv',q_inv_strong,z3)
	if result == 'unsat':
		return 'true'
	else:
		return 'false'
	'''
	#1008加入可对称判断，缩短不可对称不变式的判断时间
	
	if ('[1]' in q_inv_low) or ('[2]' in q_inv_low) or ('= 1' in q_inv_low) or ('= 2' in q_inv_low) or ('1 =' in q_inv_low) or ('2 =' in q_inv_low):
		result = decisionTreeZ3('ndata.csv',q_inv_low,z3)
		if result == 'unsat':
			q_inv_low_convert = convert(q_inv_low) #对称化，即‘1’变‘2’，‘2’变‘1’
			result2 = decisionTreeZ3('ndata.csv',q_inv_low_convert,z3)
			if result2 == 'unsat':
				return 'true'
			else:
				return 'false'
		else:
			return 'false'
	else:
		result = decisionTreeZ3('ndata.csv',q_inv_low,z3)
		if result == 'unsat':
			return 'true'
		else:
			return 'false'
		

'''
def testcheckinv():
	qinv_list = readQInv('qinv.txt')
	for member in qinv_list:
		print 'checking' + member
'''	

if __name__ == "__main__":
	q_inv = '(!((ExGntd = TRUE) & (ShrSet[1] = TRUE) & (CurCmd = empty)))'
	#result = Test(q_inv)
	#print result
	result = convert(q_inv.lower())
	print result
