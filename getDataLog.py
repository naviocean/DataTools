import os
import re


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


def getData():
    vals_acc = []
    vals_loss = []
    acc = []
    loss = []
    with open('train.log') as fin:
        for row in list(fin):
            row = row.strip()
            if row.find('Accuracy') != -1:
                val_acc = re.findall(r'Accuracy (.*) \s+', row)
                val_loss = re.findall(r'Loss (.*)', row)
                vals_acc.append(val_acc[0])
                vals_loss.append(val_loss[0])
            elif row.find('INFO Epoch') != -1:
                loss_avg = re.findall(r"Loss (.*?)\t", row)
                acc_avg = row.split("Acc ")
                # print(acc_avg[1])
                acc.append(acc_avg[1])
                loss.append(loss_avg[0])
    for i in range(len(loss)):
        line = vals_acc[i] + '|' + acc[i] + '|' + vals_loss[i] + '|' + loss[i]
        print(line)


getData()
