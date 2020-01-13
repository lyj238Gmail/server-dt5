#coding=utf-8
from math import log
import operator

def calcShannonEnt(dataSet):
	numEntries = len(dataSet) #获取data列表中的元素个数
	labelCounts = {}  #创建空的字典，用于记录每种取值情况的个数，用于计算熵
	for featVec in dataSet:
		currentLabel = featVec[-1]   #取列表中的每一个元素（列表），找到该元素（列表）的最后一个元素的取值（决定该元素的分类），并记录下来
		if currentLabel not in labelCounts.keys():  #如果这种元素的取值还未记录与字典labelCounts中，则在该字典中创建该分类的键值对并初始化为0
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1  #按键值（种类）记录找到的取值
	shannonEnt = 0.0  #初始的香农熵 默认为0
	for key in labelCounts:   #对于labelCounts中的每种元素取值
		prob = float(labelCounts[key])/numEntries   #计算这种取值的概率 ：该类型总数/总数
		shannonEnt -= prob * log(prob,2)  #香浓熵的计算  -p(xi)log2p(xi)的和
	return shannonEnt #返回结果（香农熵）
		
def createDataSet():
	dataSet = [[1,1,'yes'],
	           [1,1,'yes'],
	           [1,0,'no'],
	           [0,1,'no'],
	           [0,1,'no']]
	labels = ['no surfacing','flippers']
	return dataSet, labels
    
def splitDataSet(dataSet,axis,value):   #参数分别为 数据集、特征值的位置、特征值的值
	retDataSet = []
	for featVec in dataSet:  #对于数据集（列表）中的每个元素
		if featVec[axis] == value:   #如果特征值的值等于规定的值
			reducedFeatVec = featVec[:axis]  #创建切片，并移除特征值项（前半部分）
			reducedFeatVec.extend(featVec[axis+1:])  #创建切片，并移除特征值项（后半部分）
			retDataSet.append(reducedFeatVec) #将去除特征值项的元素组成新的列表
	return retDataSet  #返回特征值等于给定值的元素组成的列表，其中特征值项已被删除

''' 原版的ID3选择最佳特征函数
def chooseBestFeatureToSplit(dataSet):   #选择最佳特征，对于ID3算法，选择的是拥有最大信息增益的特征
	numFeatures = len(dataSet[0]) - 1   #找到特征的数量，减一是为了排除最后一项（数据的分类项）
	#baseEntropy = calcShannonEnt(dataSet)  #使用香农熵算法计算未分类时数据集的熵，并将其作为基础熵，用于信息增益的判断
	baseEntropy = 100
	bestInfoGain = 0.0; bestFeature = -1  #最大信息增益基础值（初始化）为0，最佳特征基础值为-1
	for i in range(numFeatures):  #遍历所有的特征
		featList = [example[i] for example in dataSet]  #使用列表解析，将数据集中的每个元素的特征值（i对应的）加入列表中
		uniqueVals = set(featList)  #获得没用重复的取值，也就是所有可能取值的列表
		newEntropy = 0.0  #用于记录按特征划分后的熵，初始化为0
		for value in uniqueVals:  #对于每种取值
			subDataSet = splitDataSet(dataSet,i,value) #找出所有符合取值的元素
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy  #信息增益的计算
		if(infoGain > bestInfoGain):  #如果按第i个特征划分后的信息增益比之前记录的最佳划分的增益要好（大）
			bestInfoGain = infoGain #更新最佳信息增益
			bestFeature = i  #跟新最佳划分（特征）
	return bestFeature #返回最佳特征
'''	
def chooseBestFeatureToSplit(dataSet,labels,undefined_percentage):   #0726 加入新参数labels（标签），undefined_percentage（优先级）
	numFeatures = len(dataSet[0]) - 1   #找到特征的数量，减一是为了排除最后一项（数据的分类项）
	#baseEntropy = calcShannonEnt(dataSet)  #使用香农熵算法计算未分类时数据集的熵，并将其作为基础熵，用于信息增益的判断
	baseEntropy = 100
	bestInfoGain = 0.0; bestFeature = -1  #最大信息增益基础值（初始化）为0，最佳特征基础值为-1
	for i in range(numFeatures):  #遍历所有的特征
		featList = [example[i] for example in dataSet]  #使用列表解析，将数据集中的每个元素的特征值（i对应的）加入列表中
		uniqueVals = set(featList)  #获得没用重复的取值，也就是所有可能取值的列表
		newEntropy = 0.0  #用于记录按特征划分后的熵，初始化为0
		for value in uniqueVals:  #对于每种取值
			subDataSet = splitDataSet(dataSet,i,value) #找出所有符合取值的元素
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy  #信息增益的计算
		if(infoGain > bestInfoGain):  #如果按第i个特征划分后的信息增益比之前记录的最佳划分的增益要好（大）
			bestInfoGain = infoGain #更新最佳信息增益
			bestFeature = i  #跟新最佳划分（特征）
	return bestFeature #返回最佳特征
	
def chooseBestFeatureToSplit2(dataSet):   #选择最佳特征，对于ID3算法，选择的是拥有最大信息增益的特征  使用信息增益比来选取特征，算法C4.5
	numFeatures = len(dataSet[0]) - 1   #找到特征的数量，减一是为了排除最后一项（数据的分类项）
	baseEntropy = calcShannonEnt(dataSet)  #使用香农熵算法计算未分类时数据集的熵，并将其作为基础熵，用于信息增益的判断
	bestInfoGain = 0.0; bestFeature = -1  #最大信息增益基础值（初始化）为0，最佳特征基础值为-1
	bestInfoGainRatio = 0.0 #最佳信息增益比的初始化
	for i in range(numFeatures):  #遍历所有的特征
		featList = [example[i] for example in dataSet]  #使用列表解析，将数据集中的每个元素的特征值（i对应的）加入列表中
		uniqueVals = set(featList)  #获得没用重复的取值，也就是所有可能取值的列表
		newEntropy = 0.0  #用于记录按特征划分后的熵，初始化为0
		splitInfo = 0.0 #用于记录特征的熵
		for value in uniqueVals:  #对于每种取值
			subDataSet = splitDataSet(dataSet,i,value) #找出所有符合取值的元素
			prob = len(subDataSet)/float(len(dataSet)) #用于归一化（消除总数的影响）
			newEntropy += prob * calcShannonEnt(subDataSet)  #把（第i个特征值的）所有取值的熵加载一起
			splitInfo += -prob * log(prob,2)
		infoGain = baseEntropy - newEntropy  #信息增益的计算
		if(splitInfo == 0):
			continue
		infoGainRatio = infoGain / splitInfo #计算信息增益比
		if(infoGainRatio > bestInfoGainRatio):  #如果按第i个特征划分后的信息增益比之前记录的最佳划分的增益要好（大）
			bestInfoGainRatio = infoGainRatio #更新最佳信息增益ratio
			bestFeature = i  #跟新最佳划分（特征）
	return bestFeature #返回最佳特征

def majorityCnt(classList): #返回集合中占比例最大的类 .0823已修改，返回的是叶子节点可能取的值,以A | B | C的字符串形式返回
	'''
	classCount = {}  #用于统计类的字典，初始化为空
	for vote in classList: #对于列表中的元素
		if vote not in classCount.keys(): classCount[vote] = 0  #若字典中没有该种类，向字典中添加该种类，并初始化为0
		classCount[vote] += 1 #对种类的计数
	sortedClassCount = sorted(classCount.items(),\
	key=operator.itemgetter(1),reverse=True)  #对classCount进行排序，并返回计数最大的类型
	return sortedClassCount[0][0]  #返回集合中占比例最大的类
	'''
	class_set = set(classList)
	result = ''
	for member in class_set:
		if result == '':
			result = member
		else:
			result = result + ' | ' + member
	return result

'''	 原版的决策树生成函数
def createTree(dataSet,labels):  #创建树，需要参数：训练集、特征名字的集合
	classList = [example[-1] for example in dataSet]  #收集所有元素的类别，-1是判定类别的值
	if classList.count(classList[0]) == len(classList):   #第一种类别的数量等于总数量，即所有元素都属于一类，则返回该类别
		return classList[0]
	if len(dataSet[0]) == 1:    #特征用完了，只剩最后一个由于判定类别的结果了（列表只剩最后一个元素），则返回结果中占主要成分的类别
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet)  #找到最佳特征
	bestFeatLabel = labels[bestFeat]   #找到最佳特征所对应的名字
	myTree = {bestFeatLabel:{}}  #使用最佳特征创建节点
	del(labels[bestFeat])  #删除特征名字合集中已经使用的标签名
	featValues = [example[bestFeat] for example in dataSet]  #找到最佳特征可能的取值（有重复）
	uniqueVals = set(featValues)   #去掉最佳特征可能取值集中的重复
	for value in uniqueVals:  #对于每种可能的取值
		subLabels = labels[:]  #使用切片复制labels集
		temp = splitDataSet(dataSet, bestFeat, value)
		myTree[bestFeatLabel][value] = createTree(temp,subLabels)   
	return myTree  #返回生成好的树（字典）
'''
#20180825之前的版本
'''
def createTree(dataSet,labels,undefined_percentage): #0706 加入优先级判定依据undefined_percentage
	classList = [example[-1] for example in dataSet]  #收集所有元素的类别，-1是判定类别的值
	if classList.count(classList[0]) == len(classList):   #第一种类别的数量等于总数量，即所有元素都属于一类，则返回该类别
		return classList[0]
	if len(dataSet[0]) == 1:    #特征用完了，只剩最后一个由于判定类别的结果了（列表只剩最后一个元素），则返回结果中占主要成分的类别
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet,labels,undefined_percentage)  #找到最佳特征 0706向函数chooseBestFeatureToSplit加入优先级依据与labels
	bestFeatLabel = labels[bestFeat]   #找到最佳特征所对应的名字
	myTree = {bestFeatLabel:{}}  #使用最佳特征创建节点
	del(labels[bestFeat])  #删除特征名字合集中已经使用的标签名
	featValues = [example[bestFeat] for example in dataSet]  #找到最佳特征可能的取值（有重复）
	uniqueVals = set(featValues)   #去掉最佳特征可能取值集中的重复
	for value in uniqueVals:  #对于每种可能的取值
		subLabels = labels[:]  #使用切片复制labels集
		temp = splitDataSet(dataSet, bestFeat, value)
		myTree[bestFeatLabel][value] = createTree(temp,subLabels,undefined_percentage)   
	return myTree  #返回生成好的树（字典）
'''

def priInEndClassify(dataSet,labels,prior_dict):
	resut_list = []	
	temp_labels = labels[:]
	for i in range(len(temp_labels)):
		temp_labels[i] = temp_labels[i].lower()
	

	for member in prior_dict.keys():
		if member in temp_labels: #存在未被使用的优先属性
			position = temp_labels.index(member) #找到其位于title的位置
			temp_list = [example[position] for example in dataSet] #找到数据集中该位置的所有取值
			temp_set = set(temp_list) #去重复
			temp_set_list = list(temp_set)
			if len(temp_set_list) == 1: #一致的取值，代表可以加入到叶子节点中
				str_temp = member + ' = ' + temp_set_list[0]
				resut_list.append(str_temp)
			'''
			else:
				print member + ':'
				print temp_set
			'''
				
	if len(resut_list) == 0:
		return 'empty'
	else:
		result = ''
		for member in resut_list:
			if result == '':
				result = member
			else:
				result = result + ' & ' + member
		return ' & ' + result
			


def createTree(dataSet,labels,undefined_percentage): #输入为可达集、属性列表、优先级字典
	classList = [example[-1] for example in dataSet]  #收集所有元素的类别，-1是判定类别的值
	if classList.count(classList[0]) == len(classList):   #第一种类别的数量等于总数量，即所有元素都属于一类，则返回该类别 0825 修改，加入查看未使用的优先属性
		pri_attr_union = priInEndClassify(dataSet,labels,undefined_percentage) #查看没有使用的优先属性，如果他们状态唯一则把他们加入到决策树中
		if pri_attr_union == 'empty':
			return classList[0]
		else:
			return classList[0] + pri_attr_union
	if len(dataSet[0]) == 1:    #特征用完了，只剩最后一个由于判定类别的结果了（列表只剩最后一个元素），则返回结果中占主要成分的类别
		return majorityCnt(classList) #majorityCnt已经修改，不再返回主要类别，而是返回所有可能类别的整合
	bestFeat = chooseBestFeatureToSplit(dataSet,labels,undefined_percentage)  #找到最佳特征 加入了属性优先级概念
	bestFeatLabel = labels[bestFeat]   #找到最佳特征所对应的名字
	myTree = {bestFeatLabel:{}}  #使用最佳特征创建节点
	del(labels[bestFeat])  #删除特征名字合集中已经使用的标签名
	featValues = [example[bestFeat] for example in dataSet]  #找到最佳特征可能的取值（有重复）
	uniqueVals = set(featValues)   #去掉最佳特征可能取值集中的重复
	for value in uniqueVals:  #对于每种可能的取值
		subLabels = labels[:]  #使用切片复制labels集
		temp = splitDataSet(dataSet, bestFeat, value)
		myTree[bestFeatLabel][value] = createTree(temp,subLabels,undefined_percentage)   
	return myTree  #返回生成好的树（字典）




'''
#使用决策树判断状态，书上版本		
def classify(inputTree,featLabels,testVec):  #树的使用，即分类函数，所需参数:训练好的树、所有特征名字的合集（与用于训练的一致）、测试样本（包含每个特征取值的样本）
    firstSides = list(inputTree.keys()) #keys()返回字典的所有键，由于是python3.0 keys()返回的值为dict_keys(如dict_keys(['sam', 'tom']))，需要将它转换成列表（结果如['sam', 'tom']）（2.0则直接返回列表）
    firstStr = firstSides[0]  #找到第一个用于分类的特征的名字
    secondDict = inputTree[firstStr] #获得第一个特征的子树（字典形式）
    featIndex = featLabels.index(firstStr)    #获得第一个特征的位置
    for key in secondDict.keys(): #获得第一个特征的每种划分（每种划分所对应的值）
        if testVec[featIndex] == key:   #找到测试样本中该特征（目前正在用来判断的特征）的值，并与目前遍历的分支的值相比较，若相同，则进入该分支
            if type(secondDict[key]) == dict:   #如果该分支下是字典的形式（还存在子树，即还可以继续划分）
                classLabel = classify(secondDict[key],featLabels,testVec) #则使用该子树继续进行划分（递归过程）
            else:
                classLabel = secondDict[key] #分支下是叶子节点，则记录下测试样本的类型，即叶子节点的类型
    return classLabel  #返回结果（类型）
#使用决策树判断状态，遇到undefined返回undefined版本
def classify2(inputTree,featLabels,testVec):  #树的使用，即分类函数，所需参数:训练好的树、所有特征名字的合集（与用于训练的一致）、测试样本（包含每个特征取值的样本）
    firstSides = list(inputTree.keys()) #keys()返回字典的所有键，由于是python3.0 keys()返回的值为dict_keys(如dict_keys(['sam', 'tom']))，需要将它转换成列表（结果如['sam', 'tom']）（2.0则直接返回列表）
    firstStr = firstSides[0]  #找到第一个用于分类的特征的名字
    secondDict = inputTree[firstStr] #获得第一个特征的子树（字典形式）
    featIndex = featLabels.index(firstStr)    #获得第一个特征的位置
    for key in secondDict.keys(): #获得第一个特征的每种划分（每种划分所对应的值）
        if testVec[featIndex] == 'undefinded':
            return 'unknow'
        if testVec[featIndex].lower() == key.lower():   #找到测试样本中该特征（目前正在用来判断的特征）的值，并与目前遍历的分支的值相比较，若相同，则进入该分支
            if type(secondDict[key]) == dict:   #如果该分支下是字典的形式（还存在子树，即还可以继续划分）
                classLabel = classify2(secondDict[key],featLabels,testVec) #则使用该子树继续进行划分（递归过程）
            else:
                classLabel = secondDict[key] #分支下是叶子节点，则记录下测试样本的类型，即叶子节点的类型
    return classLabel  #返回结果（类型）

def classify3(inputTree,featLabels,testVec):
	firstSides = list(inputTree.keys())
	firstStr = firstSides[0]
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)
	result_list = []
	if testVec[featIndex] == 'undefinded':
		for key in secondDict.keys():
			if type(secondDict[key]) == dict:
				classLabel_temp = classify3(secondDict[key],featLabels,testVec)
				result_list.append(classLabel_temp)
			else:
				classLabel_temp = secondDict[key]
				result_list.append(classLabel_temp)
	else:
		 for key in secondDict.keys():
			 if testVec[featIndex] == key: 
				  if type(secondDict[key]) == dict:
					   classLabel_temp = classify3(secondDict[key],featLabels,testVec)
					   result_list.append(classLabel_temp)
				  else:
					  classLabel_temp = secondDict[key]
					  result_list.append(classLabel_temp)
	result_set = list(set(result_list))
	if len(result_set) == 1:
		return result_set[0]
	else:
		return 'unknow'
'''					  
	
def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'wb+')
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)		
