import os
import sys
import glob
import untangle
import matplotlib.pyplot as plt
import cv2


class Satudora(object):
    """docstring for Satudora"""
    labels_folder = '../Satudora/replace_worker'
    images_folder = '../Satudora/Worker_Dataset_v2.0'
    output_folder = './output'

    def __init__(self, size, padding=0.1):
        super(Satudora, self).__init__()
        self.size = size
        self.padding = padding
        # check output folder
        self.checkAndMakeFolder(self.output_folder)

        self.scanLabelsFolder()

    def checkAndMakeFolder(self, folderPath):
        try:
            os.stat(folderPath)
        except:
            os.mkdir(folderPath)

    def scanLabelsFolder(self):
        cam_folders = glob.glob(self.labels_folder + '/*')
        for cam_folder in cam_folders:
            cam_name = cam_folder.replace(self.labels_folder, '')
            label_folders = glob.glob(cam_folder + '/*')
            for label_folder in label_folders:
                xml_files = glob.glob(label_folder + '/*.xml')
                for xml_file in xml_files:
                    # xml_file = os.path.join(
                    #     self.labels_folder, '27', '27_1', '20180502095500_0065.xml')
                    obj = self.parserXML(xml_file)
                    img_path = label_folder.replace(
                        self.labels_folder, self.images_folder)

                    img_file = os.path.join(
                        img_path, 'images', obj['file_name'])
                    # img_file = os.path.join(
                    #     self.images_folder, '27/27_1/images/20180502095500_0065.jpg')
                    exists = os.path.isfile(img_file)
                    if exists:
                        img = plt.imread(img_file)
                        count = 0
                        # plt.figure(0)
                        # plt.imshow(img)
                        for person in obj['persons']:
                            label = person['name']
                            count += 1
                            width = int(obj['width'])
                            height = int(obj['height'])

                            xmin = int(person['xmin'])
                            xmax = int(person['xmax'])
                            ymin = int(person['ymin'])
                            ymax = int(person['ymax'])

                            y_padding = (self.padding * (ymax - ymin))
                            x_padding = (self.padding * (xmax - xmin))

                            xmin, xmax, ymin, ymax = self.resizeSquare(
                                xmin, xmax, ymin, ymax, width, height)
                            # print(xmin, xmax, ymin, ymax)
                            img_crop = img[ymin:ymax, xmin:xmax]
                            plt.figure(1)
                            plt.imshow(img_crop)

                            # padding
                            xmin_p, xmax_p, ymin_p, ymax_p = self.resize(
                                xmin, xmax, ymin, ymax, width, height, x_padding, y_padding)
                            inside = self.checkOtherInside(
                                obj['persons'], person, xmin_p, xmax_p, ymin_p, ymax_p)
                            # print(xmin, xmax, ymin, ymax,
                            #       (xmax - xmin), (ymax - ymin))
                            # img_crop = img[ymin:ymax, xmin:xmax]
                            # plt.figure(2)
                            # plt.imshow(img_crop)
                            # print(inside)
                            if inside == True:
                                img_crop = img[ymin:ymax, xmin:xmax]
                                plt.figure(2)
                                plt.imshow(img_crop)
                            else:
                                xmin, xmax, ymin, ymax = self.resizeSquare(
                                    xmin_p, xmax_p, ymin_p, ymax_p, width, height)
                                img_crop = img_crop = img[ymin:ymax, xmin:xmax]
                                # resize
                                # i_width = xmax_p - xmin_p
                                # i_height = ymax_p - ymin_p
                                # if max(i_width, i_height) > self.size:
                                #     if i_width > i_height:
                                #         x_size = 0
                                #         y_size = i_width - i_height
                                #     else:
                                #         y_size = 0
                                #         x_size = i_height - i_width
                                # else:
                                #     x_size = self.size - i_width
                                #     y_size = self.size - i_height

                                # xmin_r, xmax_r, ymin_r, ymax_r = self.resize(
                                #     xmin_p, xmax_p, ymin_p, ymax_p, width, height, x_size, y_size)

                                # # check others inside box
                                # inside = self.checkOtherInside(
                                #     obj['persons'], person, xmin_r, xmax_r, ymin_r, ymax_r)
                                # # print(inside)
                                # if inside == True:
                                #     xmin, xmax, ymin, ymax = self.resizeSquare(
                                #         xmin_p, xmax_p, ymin_p, ymax_p, width, height)
                                #     img_crop = img_crop = img[ymin:ymax, xmin:xmax]
                                # else:
                                #     # print(xmin, xmax, ymin, ymax, i_width,
                                #     #       i_height, x_size, y_size)
                                #     img_crop = img[ymin_r:ymax_r,
                                #                    xmin_r:xmax_r]
                                plt.figure(2)
                            # plt.imshow(img_crop)
                            img_name = obj['file_name'].split('.')[0]
                            des_path = os.path.join(self.output_folder, label)
                            self.checkAndMakeFolder(des_path)

                            plt.imsave(
                                '{}/{}-{}-{:04d}.jpg'.format(des_path, cam_name, img_name, count), img_crop)
                            # plt.show()
                    else:
                        pass
                    # exit()

    def checkOtherInside(self, objects, current, xmin, xmax, ymin, ymax):
        inside = False
        for person in objects:
            if person is not current:
                xmin1 = int(person['xmin'])
                xmax1 = int(person['xmax'])
                ymin1 = int(person['ymin'])
                ymax1 = int(person['ymax'])
                iou = self.getIO((xmin, ymin, xmax, ymax),
                                 (xmin1, ymin1, xmax1, ymax1))
                # print(iou)
                if iou > 0.3:
                    inside = True
                    break
        return inside

    def getIO(self, boxA, boxB):
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        # compute the area of intersection rectangle
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / boxBArea
        # return the intersection over union value
        return iou

    def resizeSquare(self, xmin, xmax, ymin, ymax, width, height):
        i_width = xmax - xmin
        i_height = ymax - ymin
        if i_width > i_height:
            x_size = 0
            y_size = i_width - i_height
        else:
            y_size = 0
            x_size = i_height - i_width

        return self.resize(xmin, xmax, ymin, ymax, width, height, x_size, y_size)

    def resize(self, xmin, xmax, ymin, ymax, width, height, x_size, y_size):
        x_size = x_size / 2
        y_size = y_size / 2
        if xmin - x_size < 0:
            x_size = 2 * x_size - xmin
            xmin = 0
            xmax = xmax + x_size

        if xmax + x_size > width:
            x_size = 2 * x_size - (width - xmax)
            xmax = width
            xmin = xmin - x_size

        if xmin - x_size >= 0 and xmax + x_size <= width:
            xmin = xmin - x_size
            xmax = xmax + x_size

        if ymin - y_size < 0:
            y_size = 2 * y_size - ymin
            ymin = 0
            ymax = ymax + y_size

        if ymax + y_size > height:
            y_size = 2 * y_size - (height - ymax)
            ymax = height
            ymin = ymin - y_size

        if ymin - y_size >= 0 and ymax + y_size <= height:
            ymin = ymin - y_size
            ymax = ymax + y_size

        return (int(xmin), int(xmax), int(ymin), int(ymax))

    def parserXML(self, file_path):
        print(file_path)
        parser = untangle.parse(file_path)
        objects = parser.annotation.object
        print(len(objects))
        result = {
            'file_name': parser.annotation.filename.cdata,
            'width': parser.annotation.size.width.cdata,
            'height': parser.annotation.size.height.cdata
        }
        persons = []
        for obj in objects:
            person = {
                'name': obj.name.cdata,
                'xmin': obj.bndbox.xmin.cdata,
                'ymin': obj.bndbox.ymin.cdata,
                'xmax': obj.bndbox.xmax.cdata,
                'ymax': obj.bndbox.ymax.cdata,
            }
            persons.append(person)
        result['persons'] = persons
        return result


if __name__ == '__main__':
    Satudora(size=224)
