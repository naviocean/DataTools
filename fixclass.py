from random import shuffle
import glob
import os


class FixClass(object):
    class_list = []
    train_file = './trainlist01.txt'
    class_file = './classInd.txt'

    def __init__(self):
        super(FixClass, self).__init__()
        # self.readFile()
        # self.writeClassFile()
        self.reScan()

    def readFile(self):
        with open(self.train_file) as fin:
            for row in list(fin):
                class_name = row.strip().split('/')[0]
                if class_name not in self.class_list:
                    self.class_list.append(class_name)
        self.class_list.sort()
        print(len(self.class_list))

    def writeOutputFile(self, list, file):
        # earse content file
        with open(file, 'w'):
            pass
        # write content file
        with open(file, 'a') as f:
            for row in list:
                line = row + '\n'
                f.write(line)
        f.close
        print('write file done')

    def shuffeFile(self):
        files = ['./trainlist01.txt', 'testlist01.txt', 'validationlist01.txt']

        for i in range(len(files)):
            file = files[i]
            with open(file) as fin:
                rows = [row.strip() for row in list(fin)]

            shuffle(rows)
            # earse content file
            with open(file, 'w'):
                pass
            # write content file
            with open(file, 'a') as f:
                for row in rows:
                    line = row + '\n'
                    f.write(line)
            f.close
            print('write file done')

    def get_labels(self):
        label_dict = {}
        with open('./classInd.txt') as fin:
            for row in list(fin):
                row = row.replace("\n", "").split(" ")
                # -1 because the index of array is start from 0
                label_dict[row[1]] = int(row[0])
        return label_dict

    def reScan(self):
        folders = ['../train/', '../test/', '../validation/']
        classes = self.get_labels()
        trains = []
        tests = []
        validations = []

        for folder in folders:
            class_folders = glob.glob(folder + '*')
            for class_folder in class_folders:
                label_folders = glob.glob(class_folder + '/*')
                for vid_class in label_folders:
                    class_files = glob.glob(vid_class + '/*.jpg')
                    total = len(class_files)
                    file_path = vid_class.replace(folder, '')
                    label = file_path.split('/')[0]
                    row = file_path + ' ' + \
                        str(total) + ' ' + \
                        str(classes[label])
                    if folder == '../train/':
                        trains.append(row)
                    if folder == '../test/':
                        tests.append(row)
                    if folder == '../validation/':
                        validations.append(row)

        if len(trains) > 0:
            self.writeOutputFile(trains, './trainlist01.txt')
        if len(tests) > 0:
            self.writeOutputFile(tests, './testlist01.txt')
        if len(validations) > 0:
            self.writeOutputFile(validations, './validationlist01.txt')


FixClass()
