import numpy as np
import os
import random
import matplotlib.pyplot as plt
import pandas as pd
import re
import pickle

def combine(entry):
	pass

def computeDate(filename):
	results = re.findall(r"^[0-9]{8}$", filename)
	print "filename is: ", filename
	print "results is: ", results
	return results[0]

def dump(filename, obj):
	pickle.dump(obj, filename)

def pdCombine(file, df):
	df = df.concat(file)
	return df

def main(testSampleSize = 10):
	totalTransitionMatrix = np.matrix([[0,0,0], [0,0,0], [0,0,0]])

	limit = testSampleSize
	finished = False
	parse = True
	basepath = '../../alllogs/'

	try:
		os.listdir(basepath)
	except Exception, e:
		print e
		parse = False


	if parse:
		for files in os.listdir(basepath):
			if finished == True:
				break
			path = os.path.join(basepath, files)
			if os.path.isdir(path):
				date = computeDate(path)
				print "Date is: ", date

				for logFile in os.listdir(path):
					if limit == 0:
						finished = True
						break

					actualFilePath = os.join(path, logFile)
					dataFile = pd.read_csv(actualFilePath, sep = ";")
					print dataFile.head()

					limit -= 1
					# print limit
					# print totalTransitionMatrix

if __name__ == '__main__':
	main(10)

# What are the entries I want
# Date, Day of week, 