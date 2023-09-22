import re
import hanlp
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)

def post_data_processing(df):
    df = df
    columns = df.columns.values.tolist()
    df_empty = pd.DataFrame(columns=columns)

    for i in range(len(df)):
        row = df.iloc[i]
        # print(row)
        if not pd.isna(df.iloc[i][0]) and df.iloc[i][0][-1] != '：':
            # row = df.iloc[i]
            text = row[0].strip()
            text = re.sub(r'[^\u4e00-\u9fa5、：（）]', '', text)
            text = re.sub(r'^\W+', '', text)
            text = text.replace(' ', '')
            row[0] = text
        if not pd.isna(df.iloc[i][-2]):
            num1 = re.sub('[^0-9.-]', '', str(row[-2]))
            if len(num1) == 0:
              num1 = '-'
            else:
              row[-2] = num1.strip()
        if not pd.isna(df.iloc[i][-1]):
            num2  = re.sub('[^0-9.-]', '', str(row[-1]))
            if len(num2) == 0:
              num2 = '-'
            else:
              row[-1] = num2.strip()
        df_empty = df_empty.append(row, ignore_index=True)  # Update df_empty here
    return df
#new method
def match_sts(name, subject):
  data = name
  subject = subject
  tot_match = []
  no_match = []
  sus1_match = []
  sus2_match = []
  tem_key = {}
  for i in subject:
    tem_key[i] = [0]

  for i in range(len(data)):

    score = process.extract(data[i],subject, limit=1,scorer=fuzz.token_set_ratio)
    sub_name = score[0][0]
    if score[0][1] >= 80:
      #2-匹配，0代表不匹配，1代表疑似
      tot_match.append([data[i],sub_name,2])
      tem_key[sub_name][0] += 1
      tem_key[sub_name].append(data[i])
    elif score[0][1] < 50:
      no_match.append([data[i],sub_name,0])
    else:
      sus1_match.append([data[i],sub_name,1])
  #tem_key反向检查，检查其是否大于1

  #二次检查
  for i in sus1_match:
    sub_name = i[1]
    times = tem_key[sub_name][0]
    if times != 0:
      no_match.append(i)
    else:
      if sts([(sub_name,i[0])])[0] >= 0.985:
        tot_match.append(i)
      else:
        sus2_match.append(i)

  return tot_match, sus2_match, no_match

def table(df,subject):
  #OCR提取数据后处理
  df = df
  # print(type(df))
  # print(df)
  df = post_data_processing(df)
  # for i in range(len(df)):
  #   if not pd.isna(df.iloc[i][0]):
  #     text = df.iloc[i][0]
  #     cleaned_text = re.sub(r'^\W+', '', text)
  #     df.iloc[i][0] = cleaned_text
  subject = subject
  #建立模版表格
  #创建一个带有列名的空的DataFrame
  columns = df.columns.values.tolist()
  columns.insert(1,'匹配程度')
  df_empty = pd.DataFrame(columns = columns, index = subject)
  # df_empty = template

  #将dataframe录入到list里面,col表示改行内容，test表示每行名称
  col = {}
  name = []
  for i in range(len(df)):
    # if not pd.isna(df.iloc[i][0]) and df.iloc[i][0][-1] != ':':
    if not pd.isna(df.iloc[i][0]):
      col[df.iloc[i][0]] = df.iloc[i]
      name.append(df.iloc[i][0])

  tot_match, sus_match, no_match = match_sts(name,subject)

  ##写入空的dataframe
  for i in tot_match:
    input_id = i[1]
    col_input_id = i[0]
    row = col[col_input_id].tolist()
    row.insert(1,'匹配')
    df_empty.loc[input_id] = row

  for i in sus_match:
    input_id = i[1]
    col_input_id = i[0]
    row = col[col_input_id].tolist()
    row.insert(1,'疑似')
    df_empty.loc[input_id] = row

  df_empty.insert(1, '模版科目', df_empty.index)

  return df_empty



def fin_table_re(option, data):
  tem_name = option+'_data_tok.txt'
  with open('./fin_templates/'+tem_name,'r') as f:
    fin_tem = f.readlines()

  subject = [line.strip() for line in fin_tem]

  df = data
  df_new = table(df,subject)


  return df_new
