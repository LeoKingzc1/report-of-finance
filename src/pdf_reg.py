import os
import cv2
import fitz
import pdfplumber
import numpy as np
import pandas as pd
from paddleocr import PPStructure, draw_structure_result, save_structure_res

#需要创立两个文件夹pdf2imagepath，no_seal_image_path
pdf2imagepath = './image/'
no_seal_image_path = './no_seal/'

table_engine = PPStructure(show_log=False)

def pdf_reg_test(pdf_path, pages):
  # pdf2imagepath = pdf2imagepath
  # pages = [int(pages)]
  pages = pages
  path_prefix = 'pic'
  # no_seal_image_path = no_seal_image_path
  pdf_image(pdf_path, pdf2imagepath, pages, path_prefix)
  # print("-----------将pdf指定页码转换为图片 End---------")
  # 读取pdf转换的图片，去除印章后放在某个目录下
  # print("---------------去除印章 Start---------------")
  files = os.listdir(pdf2imagepath)
  # print(files)
  for pg in pages:
      file_path = os.path.join(pdf2imagepath, path_prefix + str(pg) + ".png")
      image1 = file_path
      # print(file_path)
      if os.path.isfile(file_path):
          seal_remove(file_path)
  # print("---------------去除印章 End---------------")
  # 读取除印章的图片后，OCR识别excel内容
  # print("---------------图片OCR Start-------------")
  files = os.listdir(no_seal_image_path)
  table_engine = PPStructure(show_log=True)
  df_empty = pd.DataFrame()
  for pg in pages:
      file_path = os.path.join(no_seal_image_path, path_prefix + str(pg) + ".png")
      image2 = file_path
      if os.path.isfile(file_path):
          # save_folder = '/content/save'
          img = cv2.imread(file_path)
          result = table_engine(img)
          res1 = result[0]
          df = pd.read_html(res1['res']['html'],header=0)[0]
          df_empty = df_empty.append(df)
  # print(df_empty)

  return df_empty

def pdf_image(pdfPath, imgPath, pages, path_prefix ,rotation_angle=0):
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    zoom_x = 2.5
    zoom_y = 2.5
    # 逐页读取PDF
    for pg in range(0, pdf.page_count):
        if pg in pages:
            page = pdf[pg]
            # 设置缩放和旋转系数
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
            pm = page.get_pixmap(matrix=trans, alpha=False)
            # 这是括号里面的一个参数 matrix=trans,
            # 开始写图像
            pm.writePNG(imgPath + path_prefix + str(pg) + ".png")
    pdf.close()

def seal_remove(imagepath):
    imgs = cv2.imread(imagepath)
    filename = os.path.basename(imagepath)
    image = imgs.copy()
    images = imgs.copy()
    rows, cols = image.shape[:2]
    red_minus_blue = image[:, :, 2] - image[:, :, 0]
    red_minus_green = image[:, :, 2] - image[:, :, 1]

    red_minus_blue = red_minus_blue >= 10
    red_minus_green = red_minus_green >= 10

    red = image[:, :, 2] >= np.mean(image[:, :, 2]) / 1.2

    mask = red_minus_green & red_minus_blue & red
    # print(mask)
    images[mask, :] = 255
    mask = (1 - mask).astype(np.bool)
    # print(mask)
    image[mask, :] = 255

    cv2.imwrite(no_seal_image_path + filename, images)

    cv2.waitKey()

