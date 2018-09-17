import glob
import os
import os.path
import sys
import math
import random

ClASSFILE = './breakfirstTrainTestList/classInd.txt';
TESTFILE = './breakfirstTrainTestList/testlist01.txt';
VALFILE = './breakfirstTrainTestList/validationlist01.txt';
TRAINFILE = './breakfirstTrainTestList/trainlist01.txt'
OUTPUT = './output'

def checkDataFolder():
	try:
		os.stat('./breakfirstTrainTestList')
	except:
		os.mkdir('./breakfirstTrainTestList/')

def checkOutput():
	try:
	    os.stat(OUTPUT)
	except:
	    os.mkdir(OUTPUT)

def writeClassFile(categories):
	#earse content file
	with open(ClASSFILE, 'w'): pass
	#write content file
	with open(ClASSFILE, 'a') as f:
		for i, key in enumerate(categories.keys()):
			line = str(i+1) + ' ' +key+'\n';
			f.write(line)
	f.close
	print('write class file done')

def writeOutputFile(list, file):
	#earse content file
	with open(file, 'w'): pass
	#write content file
	with open(file, 'a') as f:
		for filepath in list:
			filename = os.path.basename(filepath)
			cat = filename.split('.')[0]
			cat = cat.split('_')[1]
			line = cat + '/' + filename + '\n'
			f.write(line)
	f.close
	print('write file done')

def scan():
	#init categories dictonary to store list videos
	categories = dict()

	for root, dirs, files in os.walk("./vid"):
		if root.find('/cam01') != -1:
			for file in files:
				filename = file.split('.')[0]
				filename = filename.split('_')
				person = filename[0]
				cat = filename[1]

				if cat in categories:
					categories[cat].append(root+'/'+file)
				else:
					categories[cat] = [root+'/'+file]

	val_list = []
	test_list = []
	train_list = []

	for key in categories.keys():
		total = len(categories[key]);
		val_total = math.ceil(total*(1/10));
		test_total = math.ceil(total*(3/10));
		train_total = total - val_total - test_total;

		val_list = val_list + random.sample(categories[key], val_total)
		test_list = test_list + random.sample(set(categories[key]) - set(val_list), test_total);
		train_list = train_list + list(set(categories[key]) - set(val_list) - set(test_list));

	writeOutputFile(val_list, VALFILE);
	writeOutputFile(test_list, TESTFILE);
	writeOutputFile(train_list, TRAINFILE);
	#write class to file
	writeClassFile(categories)

	return categories

def main():
    """
    Extract images from videos and build a new file that we
    can use as our data input file. It can have format:

    [train|test], class, filename, nb frames
    """
    #check data folder existed or not
    #if not -> create
    checkDataFolder()
    #check output folder existed or not
	#if not -> create
	checkOutput()
	#scan video from vid folder
	#write validation, train, test list and action class to file
    categories = scan()
    #process videos
    #read 

if __name__ == '__main__':
    main()