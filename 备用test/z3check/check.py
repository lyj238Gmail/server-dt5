#coding=utf-8

from z3serv import SMT2


#目标(assert (not (=> (and (= (n 5) C) (= (n 3) C)) (and (= (n 3) C) (= (n 5) C))))):  unsat
#针对决策树不变式的中缀转前缀
def transForDTInv(dtinv): #用于处理来自于决策树的不变式，例如"(x = TRUE & n[1] != C & n[1] != E & n[2] != C & n[2] != E)"
	member_list = []
	strsplit = dtinv[1:-1].split('&')
	for member in strsplit:
		member_temp = member.strip()
		if '=' in member_temp and '!=' not in member_temp: #表达式为 a = b的形式
			parameter_list = member_temp.split(' = ')
			for i in range(len(parameter_list)):
				count = 0
				for j in range(len(parameter_list[i])):
					if parameter_list[i][j] == '[':
						nember_temp = parameter_list[i][j + 1]
						parameter_list[i] = parameter_list[i].replace('[' + nember_temp + ']', '')
						parameter_list[i] = '(' + parameter_list[i] +' ' + nember_temp + ')'
					count = count + 1
			newform = '(' + ' ' + '=' + ' ' + parameter_list[0] + ' ' + parameter_list[1] + ')'
			member_list.append(newform)
		elif '!=' in member_temp: #表达式为 a != b的形式
			parameter_list = member_temp.split(' != ')
			for i in range(len(parameter_list)):
				count = 0
				for j in range(len(parameter_list[i])):
					if parameter_list[i][j] == '[':
						nember_temp = parameter_list[i][j + 1]
						parameter_list[i] = parameter_list[i].replace('[' + nember_temp + ']', '')
						parameter_list[i] = '(' + parameter_list[i] +' ' + nember_temp + ')'
					count = count + 1
			newform = '(not ' + '(' + ' ' + '=' + ' ' + parameter_list[0] + ' ' + parameter_list[1] + ')' + ')'
			member_list.append(newform)
		else:
			print 'error no = or !='
	result = ''
	if len(member_list) == 1:
		result = member_list[0]
	else:
		for member in member_list:
			if result == '':
				result = member
			else:
				result = '(' + 'and ' + result + ' ' + member + ')'
	return result

#针对查询不变式的中缀转前缀，方法为将查询不变式的形式转换为决策树不变式的形式，即（A & B & C），其中A、B、C用‘ = ’或‘ ！= ’连接
def transForQInv(qinv):#用于处理查询的inv
	qinv_temp = qinv[2:-1] #去掉！与第一层括号
	qinv_temp = qinv_temp.replace('(','')
	qinv_temp = qinv_temp.replace(')','')
	qinv_list = qinv_temp.split(' & ')
	for i in range(len(qinv_list)):
		if '!' in qinv_list[i]:
			qinv_list[i] = qinv_list[i].replace('!','')
			temp_list = qinv_list[i].split(' = ')
			qinv_list[i] = temp_list[0] + ' != ' + temp_list[1]
	new_qinv = ''
	for member in qinv_list:
		if new_qinv == '':
			new_qinv = member
		else:
			new_qinv = new_qinv + ' & ' + member
	result = transForDTInv('(' + new_qinv + ')')
	return result
	
#输入查询不变式与决策树不变式，并以中缀的形式将两者连接起来（并且的形式）	
def transDTAndQInv(dtinv,qinv):
	dt_result = transForDTInv(dtinv)
	q_result = transForQInv(qinv)
	result = '(assert (and ' + dt_result + ' ' + q_result +'))'
	return result
#读取决策树不变式（决策树每条通往true的路径，或其他形式的路径），	代码replace(' | \r\n','')可能根据系统不同而不同，该版本为Ubuntu	
def readDTInv(filename):
	result = []
	f = open(filename)
	lines = f.readlines() #读取全部内容以列表形式返回
	for line in lines:
		#print(line)
		result.append(line.replace('\n','').replace('NODE_1','1').replace('NODE_2','2').replace('DATA_1','1').replace('DATA_2','2').lower()) #替换决策树不变式中每条路径多余的部分，不同系统不一样，这种替换在linux——Ubuntu中有效
	return result
#测试用，读取查询不变式
def readQInv(filename):
	result = []
	f = open(filename)
	lines = f.readlines() #读取全部内容以列表形式返回
	for line in lines:
		result.append(line.lower())
	return result
#测试用，检测决策树不变式（其中的一条）与查询不变式的并是否满足（sat），如果是不变式应该为unsat，即res的值。context上下文要根据协议来设置
def check(qinv,dtinv_list):
	smt2 = SMT2('(declare-datatypes () ((state i t c e))) (declare-fun n (Int) state) (declare-fun x () Bool)')
	for member in dtinv_list:
		stm_test = transDTAndQInv(member,qinv)
		#print stm_test
		res = smt2.check(stm_test)
		print res
#测试用，检测决策树不变式（一般有多条）与查询不变式（可以是多条）的并是否满足（sat）。如果是不变式应该为unsat，即res的值。context上下文要根据协议来设置
def check_list(qinv_list,dtinv_list,z3):
	'''
	context = '(declare-datatypes () ((CACHE_STATE I S E)))\
(declare-datatypes () ((MSG_CMD Empty ReqS ReqE Inv InvAck GntS GntE)))(declare-fun Cache.State (Int) CACHE_STATE)\
(declare-fun Cache.Data (Int) Int)\
(declare-fun Chan1.Cmd (Int) MSG_CMD)\
(declare-fun Chan1.Data (Int) Int)\
(declare-fun Chan2.Cmd (Int) MSG_CMD)\
(declare-fun Chan2.Data (Int) Int)\
(declare-fun Chan3.Cmd (Int) MSG_CMD)\
(declare-fun Chan3.Data (Int) Int)\
(declare-fun ShrSet (Int) Bool)\
(declare-fun InvSet (Int) Bool)\
(declare-fun ExGntd () Bool)\
(declare-fun CurCmd () MSG_CMD)\
(declare-fun CurPtr () Int)\
(declare-fun MemData () Int)\
(declare-fun AuxData () Int)'
'''
	#print qinv_list[0]
	#context = '(declare-datatypes () ((state i t c e))) (declare-fun n (Int) state) (declare-fun x () Bool)'
	#context = context.lower()
	#context = context.replace('int','Int').replace('bool','Bool')
	smt2 = z3
	for member in qinv_list:
		#print member + ':'
		for member2 in dtinv_list:
			member2_temp = member2.replace('undefined','3')
			stm_test = transDTAndQInv(member2_temp,member)
			#print(stm_test)
			#print stm_test
			res = smt2.check(stm_test)
			if res == 'sat':
				#print 'sat path : ' + member2 +'\n'
				return 'sat'
	return 'unsat'


def z3Checker(invfile_dt,q_inv,z3):
	dt_inv_list = readDTInv(invfile_dt) #读取优先决策树路径
	qinv_list = []
	qinv_list.append(q_inv)
	result = check_list(qinv_list,dt_inv_list,z3) #检测查询不变式的真伪，如果为真返回值为“unsat”，反之返回“sat”
	return result
	
	
	


if __name__ == '__main__':
	#string_dt = "(x = TRUE & n[1] != C & n[1] != E & n[2] != C & n[2] != E)"
	#stringinv = "(!((n[1] = c) & (x = TRUE)))"
	#print(transForDTInv(string_dt))
	#print(transForQInv(stringinv))
	#print(transDTAndQInv(string_dt,stringinv))
	#inv = '!((n[2] = e) & (n[1] = e))'
	invfile_dt = 'result_youxian.txt'
	invfile_q = 'test.txt'
	dt_inv_list = readDTInv(invfile_dt)
	inv_q_list = readQInv(invfile_q)
	#print dt_inv_list
	#print(dt_inv_list)
	check_list(inv_q_list,dt_inv_list)
