import cv2
import os
import numpy as np

def YoloLine2BndBox(classIndex, xcen, ycen, w_box, h_box, width,height):
    cx, cy, w, h = float(xcen * width),float(ycen * height), w_box * width, h_box * height

    xmin = round(cx - float(w / 2))
    xmax = round(cx + float(w / 2))
    ymin = round(cy - float(h / 2))
    ymax = round(cy + float(h / 2))

    return classIndex, xmin, ymin, xmax, ymax

if __name__ == '__main__':
    ANNOTATIONS_PATH = 'C:/annotations/'
    IMAGES_PATH = 'C:/images/'
    
    for annot_file in os.listdir(ANNOTATIONS_PATH):

        annot_path = os.path.join(ANNOTATIONS_PATH,annot_file)
        img_file = annot_file.replace('.txt','.jpg')
        img_path = os.path.join(IMAGES_PATH,img_file)
        img_name = img_file.replace('.jpg','')

        data = open(annot_path,'r')
        annot_data = data.read().rstrip()
        annot_data = list(annot_data.split())
        annot_data = [float(num) for num in annot_data]
        
        img = cv2.imread(img_path)
        height, width, depth = img.shape[0],img.shape[1],img.shape[2]
        imgSize = (height,width)
        _class, xmin, ymin, xmax, ymax = YoloLine2BndBox(annot_data[0],
                                                        annot_data[1],
                                                        annot_data[2],
                                                        annot_data[3],
                                                        annot_data[4],
                                                        width,
                                                        height)
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        cv2.line(img, (xmax,ymax), (xmin,ymax), (0, 255, 0), 2)
        cv2.line(img, (xmin,ymin), (xmin,ymax), (0, 255, 0), 2)
        cv2.line(img, (xmin,ymin), (xmax,ymin), (0, 255, 0), 2)
        cv2.line(img, (xmax,ymax), (xmax,ymin), (0, 255, 0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(0)

        xml_file = open(IMAGES_PATH + img_name + '.xml','w' )
        xml_file.write('<annotation>\n')
        xml_file.write('	<folder>'+str(int(_class))+'</folder>\n')
        xml_file.write('	<filename>'+img_file+'</filename>\n')
        # xml_file.write('	<path>'+img_path.replace('/','\\')+'</path>\n')
        xml_file.write('	<path>'+img_path+'</path>\n')
        xml_file.write('	<source>\n		<database>Unknown</database>\n	</source>\n	<size>\n' )
        xml_file.write('		<width>'+str(width)+'</width>\n' )
        xml_file.write('		<height>'+str(height)+'</height>\n' )
        xml_file.write('		<depth>'+str(depth)+'</depth>\n' )
        xml_file.write('	</size>\n	<segmented>0</segmented>\n	<object>\n')
        xml_file.write('		<name>'+str(int(_class))+'</name>\n')
        xml_file.write('		<pose>Unspecified</pose>\n')
        xml_file.write('		<truncated>0</truncated>\n')
        xml_file.write('		<difficult>0</difficult>\n		<bndbox>\n')
        xml_file.write('			<xmin>'+str(xmin)+'</xmin>\n')
        xml_file.write('			<ymin>'+str(ymin)+'</ymin>\n')
        xml_file.write('			<xmax>'+str(xmax)+'</xmax>\n')
        xml_file.write('			<ymax>'+str(ymax)+'</ymax>\n')
        xml_file.write('		</bndbox>\n	</object>\n</annotation>\n')
        xml_file.close()
