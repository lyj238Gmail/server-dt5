#coding=utf-8

def expedition(tree,track,tree_map,calssify_attribute):
	#探索当前节点与节点的分支
	#print tree
	firstSides = list(tree.keys()) #得到含有根节点的列表，如根节点为A，则得到[A]
	firstStr = firstSides[0] #得到根节点名称 如A;(和上一行注释一起看)
	secondDict = tree[firstStr] #获得根节点的子树，子树是字典类型
	#探索部分结束，获得当前节点名称firstStr，和当前节点分支secondDict
	
	#判断各个分支的情况（其实就两条，true与false）
	for key in secondDict.keys(): #遍历子树，即子树的两个分支
		if type(secondDict[key]) != dict: #分支下的节点不是中间节点(字典)就是叶子节点(字符串‘false’或‘true’),这里是叶子的情况
			new_track = track[:];
			new_track.append(firstStr + ' = ' + key) #加入新路径
			#new_track.append(calssify_attribute + ' = ' + secondDict[key])
			#tree_map.append(new_track)
			if ' | ' in secondDict[key]: #用于处理叶子结点中包含多个属性的情景
				attribute_class_list = secondDict[key].split(' | ')
				for member in attribute_class_list:
					new_track_temp = new_track[:]
					new_track_temp.append(calssify_attribute + ' = ' + member)
					tree_map.append(new_track_temp)
			else:
				new_track_temp = new_track[:]
				new_track_temp.append(calssify_attribute + ' = ' + secondDict[key])
				tree_map.append(new_track_temp)
		else: #分支下是字典(中间节点)，需要继续探索
			#更新足迹
			new_track_2 = track[:]
			new_track_2.append(firstStr + ' = ' + key)
			#足迹更新完毕，继续探索
			expedition(secondDict[key],new_track_2,tree_map,calssify_attribute)

def editor2(tree_map): #用于将收集到的路径拼接成结果（假设不变式）
	result = ''
	for original_path in tree_map:
		#将路径列表用‘&’连接起来
		result_path = '' #用于储存用‘ & ’连接好的路径
		for member in original_path:
			if result_path =='':
				result_path = member
			else:
				result_path = result_path + ' & ' + member
		#合成连接好的路径	
		if result == '':
			result = '(' + result_path + ')'
		else:
			result = result + '\n' + '(' + result_path + ')'
	return result


def treeGeography2(tree,calssify_attribute): #从决策树中合成假设不变式
	tree_map = [] #记录所有从根节点到达‘false’叶子节点的路径
	track = [] #用于记录之前走过的路径
	#print(tree)
	expedition(tree,track,tree_map,calssify_attribute) #寻找决策树中的路径，其中路径指从根节点到‘false’叶子节点的路径
	#print(tree_map)
	result = editor2(tree_map) #利用找到的路径合成假设不变式
	return result

	
def grabTree(filename): #读取决策树的函数
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)

def syn_path(tree,save_name,calssify_attribute):  #使用函数实现主函数的功能，即产生决策树路径
	result = treeGeography2(tree,calssify_attribute)
	with open(save_name,'w') as f:
		f.write(result)
		f.close()
	


if __name__ == "__main__": #用于测试的主函数
	tree = grabTree('tree_youxian.txt')
	result = treeGeography2(tree)
	print(result)
	with open('result_youxian.txt','w') as f:
		f.write(result)
