import random
import math
import sys
import glob
import os
import os.path
from subprocess import call
# from timecode import Timecode


class BreakFirst(object):
    classFile = './breakfastTrainTestList/classInd.txt'
    testFile = './breakfastTrainTestList/testlist01.txt'
    valFile = './breakfastTrainTestList/validationlist01.txt'
    trainFile = './breakfastTrainTestList/trainlist01.txt'
    inputVids = './vid'
    outputVids = './output'
    rawFolder = './lab_raw'
    categories = dict()
    labelFilter = ['SIL', 'walk_in', 'walk_out']
    framerate = 15

    def __init__(self):
        super(BreakFirst, self).__init__()
        self.checkDataFolder()
        self.checkOutputFolder()
        self.scanVideoFiles()
        self.pickRandom()

    def checkOutputFolder(self):
        try:
            os.stat(self.outputVids)
        except:
            os.mkdir(self.outputVids)

    def checkDataFolder(self):
        self.checkAndMakeFolder(folderPath='./breakfastTrainTestList')

    def checkAndMakeFolder(self, folderPath):
        try:
            os.stat(folderPath)
        except:
            os.mkdir(folderPath)

    def writeClassFile(self):
        # earse content file
        with open(self.classFile, 'w'):
            pass
        # write content file
        with open(self.classFile, 'a') as f:
            for i, key in enumerate(self.categories.keys()):
                line = str(i + 1) + ' ' + key + '\n'
                f.write(line)
        f.close
        print('write class file done')

    def writeOutputFile(self, list, file):
        # earse content file
        with open(file, 'w'):
            pass
        # write content file
        with open(file, 'a') as f:
            for filepath in list:
                filename = os.path.basename(filepath)
                cat = filename.split('.')[0]
                cat = cat.split('_')
                cat = cat[len(cat) - 1]
                line = cat + '/' + filename + '\n'
                f.write(line)
        f.close
        print('write file done')

    def checkFileExisted(self, filepath):
        return bool(os.path.exists(filepath))

    def checkAlreadySplit(self):
        return

    def processLabel(self, label):
        labels = label.split('_')
        return ''.join([str(x.capitalize()) for x in labels])

    def spiltVideoByCoarse(self, coarseFilePath, src):
        # read coarse file
        with open(coarseFilePath) as fin:
            filename = os.path.basename(src)
            for row in list(fin):
                frames = row.split(" ")[0]
                # get label
                label = row.split(" ")[1]
                # get start frame
                start_frame = int(frames.split('-')[0])
                start_time = start_frame / 15

                # get end frame
                end_frame = int(frames.split('-')[1])
                # Timecode('15', frames=end_frame)
                end_time = (end_frame - start_frame) / 15

                # filter label
                if not label in self.labelFilter:
                    label = self.processLabel(label)
                    folder = self.outputVids + '/' + label
                    dest_name = filename.split(
                        '.')[0] + '_' + str(start_frame) + '_' + label + '.avi'
                    dest = folder + '/' + dest_name

                    # check folder existed or not
                    self.checkAndMakeFolder(folder)
                    # check split existed?
                    if not self.checkFileExisted(filepath=dest):
                        # trim = 'trim=start_frame=' + \
                            # str(start_frame) + ':end_frame=' + str(end_frame)
                        # call(["ffmpeg", "-i", src, trim, dest])
                        call(["ffmpeg", '-i', src, '-ss',
                              str(start_time), '-t', str(end_time),
                              dest])
                        print("Splited %s" % (src))
                        print(start_frame, end_frame,
                              start_time, end_time, dest)
                    # else:
                        # print("Already splited %s" % (src))
                        # store label, file to dict
                    if label in self.categories:
                        self.categories[label].append(
                            label + '/' + dest_name)
                    else:
                        self.categories[label] = [
                            label + '/' + dest_name]

        # print("%s" % (self.categories))

    # get all video files
    # read coarse file and then split video to multiparts with label
    def scanVideoFiles(self):
        for root, dirs, files in os.walk(self.inputVids):
            if root.find('/cam01') != -1:
                for file in files:
                    if file.endswith(".avi"):
                        aviFilePath = root + '/' + file
                        filename = file.split('.')[0]
                        person = filename.split('_')[0]
                        # generate coarse file path
                        coarseFilePath = self.rawFolder + '/' + person + '/' + filename + '.coarse'
                        # check coarse file existed or not?
                        if self.checkFileExisted(filepath=coarseFilePath):
                            # read coarse file to get label
                            self.spiltVideoByCoarse(
                                coarseFilePath, src=aviFilePath)
                        else:
                            print('not found %s %s' % (root, file))

    def diff(self, li1, li2):
        li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
        return li_dif

    def getRandomList(self, dataList):
        if dataList != []:
            elem = random.choice(dataList)
            dataList.remove(elem)
        else:
            elem = None
            # print(dataList)
        return dataList, elem

    def getNumRandomList(self, datalist, num):
        newlist = []
        for x in range(0, num):
            datalist, item = self.getRandomList(datalist)
            newlist.append(item)
        return datalist, newlist

    def pickRandom(self):
        val_list = []
        test_list = []
        train_list = []
        # print("%s" % (self.categories))
        cats = self.categories
        for key in cats.keys():
            total = len(cats[key])
            if total >= 10:
                val_total = math.trunc(total * (1 / 10))
                if val_total == 0:
                    val_total = 1
                test_total = math.trunc(total * (3 / 10))
                if test_total == 0:
                    test_total = 1
                train_total = total - val_total - test_total
                # print("%s %s %s %s" %
                # (total, val_total, test_total, train_total))
                # val_list = val_list + \
                #     random.sample(cats[key], val_total)
                # cats[key] = self.diff(cats[key], val_list)
                # test_list = test_list + random.sample(cats, test_total)
                # train_list = train_list + self.diff(cats[key], test_list)
                cats[key], tmp_list = self.getNumRandomList(
                    cats[key], val_total)

                val_list = val_list + tmp_list

                cats[key], tmp_list = self.getNumRandomList(
                    cats[key], test_total)
                test_list = test_list + tmp_list
                train_list = train_list + cats[key]
                print(total, val_total, test_total, train_total)
        # print(test_list)
        if len(val_list) > 0:
            self.writeOutputFile(val_list, self.valFile)
        if len(test_list) > 0:
            self.writeOutputFile(test_list, self.testFile)
        if len(train_list) > 0:
            self.writeOutputFile(train_list, self.trainFile)

        self.writeClassFile()


a = BreakFirst()
