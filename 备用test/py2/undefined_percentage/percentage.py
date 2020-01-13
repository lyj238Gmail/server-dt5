#coding=utf-8
import csv
import csvOperation

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

if __name__ == "__main__":
	result = percentage('data.csv')
	print(result)
