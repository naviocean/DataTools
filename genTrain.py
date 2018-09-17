import sys  
import os
import re

FILEINPUT = 'org_trainlist03.txt'
VAL = ['g22', 'g23', 'g24']
TRAINFILE = 'trainlist03.txt'
VALFILE = 'validationlist03.txt'

def writeFile(filepath,datalist):
	#earse content file
	with open(filepath, 'w'): pass
	#write content file
	with open(filepath, 'a') as f:
		for line in datalist:
			f.write(line)
	f.close
	print('write file done')

def main():
	trainlist = []
	validationlist = []
	with open(FILEINPUT) as fp:
		for cnt, line in enumerate(fp):
			match = re.search(r'g\d{2}', line)
			if match.group(0) in VAL:
				validationlist.append(line)
			else:
				trainlist.append(line)
	fp.close()
	print(len(trainlist))
	writeFile(TRAINFILE,trainlist)
	print(len(validationlist))
	writeFile(VALFILE,validationlist)
			# else:
				# print("not found: %s" % line)
if __name__ == '__main__':  
   main()