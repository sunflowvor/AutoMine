import numpy as np
import cv2
import os
import sys

#data_set path
automine_img_path = '/home/ivan/Desktop/3Dbox-2/split_1/test/image/'
automine_label_path = '/home/ivan/Desktop/3Dbox-2/split_1/test/label/'

#transformed lables path
automine_label_tosave_path = './labels2coco/'

#the real ptah of your data set
automine_data_real_path = '/home/ivan/Desktop/3Dbox-2/split_1/test/'

index = 0
cvfont = cv2.FONT_HERSHEY_SIMPLEX

automine_names = open('automine.names','r')
automine_names_contents = automine_names.readlines()                
automine_images = os.listdir(automine_img_path)
automine_labels = os.listdir(automine_label_path)

automine_images.sort()
automine_labels.sort()

automine_names_dic_key = []
for class_name in automine_names_contents:
    automine_names_dic_key.append(class_name.rstrip())
values = range(len(automine_names_dic_key))
automine_names_num = dict(zip(automine_names_dic_key,values))


#创建训练集图片的List
f = open('test-automine.txt','w')
for img in automine_images:
    f.write(automine_data_real_path+img+'\n')
f.close()

#数据集 相对坐标 转换为绝对坐标
for indexi in range(len(automine_images)):
    automine_img_totest_path = automine_img_path + automine_images[indexi]
    automine_label_totest_path = automine_label_path + automine_labels[indexi]
    #print(automine_label_totest_path,automine_img_totest_path)
    
    automine_img_totest = cv2.imread(automine_img_totest_path)
    img_height, img_width = automine_img_totest.shape[0],automine_img_totest.shape[1]
    
    automine_label_totest = open(automine_label_totest_path,'r')
    
    label_contents = automine_label_totest.readlines()
    #print(label_contents)
    real_label = open(automine_label_tosave_path + automine_labels[indexi],'w')
    
    for line in label_contents:
        line = line.strip("\n")
        if line[-4:] == ".txt":
            continue
        data = line.split(' ')
        x=y=w=h=0
        if(len(data) == 16):
            class_str = data[0]
            if(class_str != 'DontCare'):
                # for calls is a string
                # trans this to number by using automine.names
                #(x,y) center (w,h) size
                x1 = float(data[3])
                y1 = float(data[4])
                x2 = float(data[5])
                y2 = float(data[6])
                
                intx1 = int(x1)
                inty1 = int(y1)
                intx2 = int(x2)
                inty2 = int(y2)

                bbox_center_x = float( (x1 + (x2 - x1) / 2.0) / img_width)
                bbox_center_y = float( (y1 + (y2 - y1) / 2.0) / img_height)
                bbox_width = float((x2 - x1) / img_width)
                bbox_height = float((y2 - y1) / img_height)

                #print(automine_names_contents[class_num])
                # cv2.putText()
                # 输入参数为图像、文本、位置、字体、大小、颜色数组、粗细
                #cv2.putText(automine_img_totest, class_str, (intx1, inty1+3), cvfont, 2, (0,0,255), 1)
                # cv2.rectangle()
                # 输入参数分别为图像、左上角坐标、右下角坐标、颜色数组、粗细
                #cv2.rectangle(automine_img_totest, (intx1,inty1), (intx2,inty2), (0,255,0), 2)
                line_to_write = str(automine_names_num[class_str]) + ' ' + str(bbox_center_x)+ ' ' + str(bbox_center_y)+ ' ' + str(bbox_width)+ ' ' + str(bbox_height) +'\n'

                real_label.write(line_to_write)
                sys.stdout.write(str(int((indexi/len(automine_images))*100))+'% '+'*******************->' "\r" )
                sys.stdout.flush()

    #cv2.imshow(str(indexi)+' kitti_label_show',kitti_img_totest)    
    #cv2.waitKey()
    real_label.close()
automine_names.close()
print("Labels tranfrom finished!")
