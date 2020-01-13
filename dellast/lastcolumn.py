#coding=utf-8

import csv


def del_last_col(fname, newfname):
	with open(fname) as csvin, open(newfname, 'wb+') as csvout:
		reader = csv.reader(csvin)
		writer = csv.writer(csvout)
		count = 0
		data = []
		for row in reader:
			newrow = row[:-1]
			data.append(newrow)
		for member in data:
			writer.writerow(member)
	csvout.close()


if __name__ == "__main__":
	del_last_col('data.csv','ndata.csv')
