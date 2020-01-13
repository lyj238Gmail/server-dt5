版本：基于“undefined”的优先级决策树，使用python3运行main.py,该代码的数据集原子German，好坏比例1:1，坏状态使用了距离概念
版本说明：在原有的决策树（ID3）中加入了优先级概念。这里的优先级指某属性的样本数据中包含undefined的概率，
含有undefined概率越底的属性优先级越高。在决策树中，优先级概念被应用于选择属性以分裂数据集。原算法中，选择属性的依据
是“信息增益”，“信息增益”大的属性将会被选中。在基于“undefined”的优先级决策树中，选择属性被分为三种情况，第一种情况为
“当前属性的优先级大于最佳属性”，该情况下会直接替换现有属性为最佳属性。第二种情况为“当前属性的优先级与最佳属性相等”，
该情况下会对比当前属性与最佳属性的“信息增益”，“信息增益”大者为最佳属性。第三种情况为“当前属性的优先级小于于最佳属性”
这种情况不做任何处理。

新加入的函数
1.def percentage(csvfile): 用于计算各个属性的数据中包含undefined的概率
伪代码:位于main.py
def percentage(csvfile): #输入为 csv文件
	获得表头与训练数据
	undefined_percentage_dict = {} #用于返回的字典
	获取训练数据大小
	for 每个属性:
		undefined_counter = 0  #初始化计数器
		for 属性对应的每个样本数据:
			if 样本值 == 'undefined':
				undefined_counter = undefined_counter + 1 #进行计数
		undefined_percentage_dict[属性名称] = undefined_counter/训练数据总数 #保存属性对应的undefined概率
	return undefined_percentage_dict

新加入包：import package_pre.pre
说明：整合了之前的预处理代码，以package_pre.pre包的形式出现

对原版本函数的修改
1.def teacher(origin_csv,atom_txt,atom_csv,tree_save_file): #teacher模块
伪代码：位于main.py
def teacher(origin_csv,atom_txt,atom_csv,tree_save_file):
	生成以原子公式为表头的训练数据  #new
	计算训练数据的优先级字典，即函数percentage得出的结果 #new
	对训练数据进行预处理，对“undefined”项进行随机赋值 #new
	使用预处理过的数据生成决策树 #new
	存储决策树
	打印决策树
	return 决策树

2.def createTree(atom_csv,undefined_percentage):  #teacher中生成决策树的函数
说明：位于main.py。修改调用函数id3.createTree的代码，加入新参数undefined_percentage

3.def createTree(dataSet,labels,undefined_percentage): #0706 加入优先级判定依据undefined_percentage
说明：该函数位于id3.py
	 修改调用函数chooseBestFeatureToSplit的代码，加入新的参数，更新为 chooseBestFeatureToSplit(dataSet,labels,undefined_percentage)
	 修改调用自身的代码，加入新参数，修改为createTree(temp,subLabels,undefined_percentage)

4.def chooseBestFeatureToSplit(dataSet,labels,undefined_percentage): #修改选择用于分裂数据集的属性的方法，加入优先级的判定
伪代码：
def chooseBestFeatureToSplit(dataSet,labels,undefined_percentage):
	numFeatures = len(dataSet[0]) - 1   #找到特征的数量，减一是为了排除最后一项（数据的分类项）
	#baseEntropy = calcShannonEnt(dataSet)  #使用香农熵算法计算未分类时数据集的熵，并将其作为基础熵，用于信息增益的判断
	baseEntropy = 100
	bestInfoGain = 0.0; bestFeature = -1  #最大信息增益基础值（初始化）为0，最佳特征基础值为-1
	best_priority = 1 #定义优先级,优先级越小，优先程度越高，初始化为1，这里指undefined率 NEW！！
	for i in range(numFeatures):  #遍历所有的特征
		featList = [example[i] for example in dataSet]  #使用列表解析，将数据集中的每个元素的特征值（i对应的）加入列表中
		uniqueVals = set(featList)  #获得没用重复的取值，也就是所有可能取值的列表
		newEntropy = 0.0  #用于记录按特征划分后的熵，初始化为0
		for value in uniqueVals:  #对于每种取值
			subDataSet = splitDataSet(dataSet,i,value) #找出所有符合取值的元素
			prob = len(subDataSet)/float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy  #信息增益的计算
#注意！！！上方代码与原算法一样，除了加入最佳优先级best_priority，下方为新代码的伪代码
		if(当前属性的优先级大于最佳属性的优先级):
			替换最佳属性为当前属性
		if(当前属性与最佳属性的优先级相同):
			选择信息增益大的属性为最佳属性
	返回最佳属性
	
