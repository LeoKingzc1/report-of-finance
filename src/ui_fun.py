import re
import gradio as gr
import pandas as pd
from src.html_fun import *
from src.pdf_reg import *
from src.sub_match import *

def read_numbers(df, col_numbers):
    columns = df.columns.values.tolist()
    col_name = []
    for i in col_numbers:
      col_name.append(columns[i])
    return col_name

def mock_ocr(pdf, p_s_profit, p_e_profit,p_s_balance, p_e_balance, p_s_flow, p_e_flow):
    # print(tables)
    profit_pages = []
    balance_pages = []
    flow_pages = []
    for i in range(int(p_s_profit)-1, int(p_e_profit)):
        profit_pages.append(i)
    for i in range(int(p_s_balance)-1, int(p_e_balance)):
      balance_pages.append(i)
    for i in range(int(p_s_flow)-1, int(p_e_flow)):
        flow_pages.append(i)

    profit_data = pdf_reg_test(pdf.name,profit_pages)
    profit_df = fin_table_re('profit', profit_data)
    profit_columns = profit_df.columns.values.tolist()
    profit_df.fillna(value='-', inplace=True)
    profit_output = df_html('利润表',profit_df)

    balance_data = pdf_reg_test(pdf.name,balance_pages)
    balance_df = fin_table_re('balance', balance_data)
    balance_columns = balance_df.columns.values.tolist()
    balance_df.fillna(value='-', inplace=True)
    balance_output = df_html('资产负债表',balance_df)

    flow_data = pdf_reg_test(pdf.name,flow_pages)
    flow_df = fin_table_re('flow', flow_data)
    flow_columns = flow_df.columns.values.tolist()
    flow_df.fillna(value='-', inplace=True)
    flow_output = df_html('现金流量表',flow_df)



    with open('./html_templates/profit_template.html') as f1:
      profit_content = f1.read()
    profit_content = profit_content.replace('<!-- 在这里插入表格 -->', profit_output)

    with open('./html_templates/balance_template.html') as f2:
      balance_content = f2.read()
    balance_content = balance_content.replace('<!-- 在这里插入表格 -->', balance_output)

    with open('./html_templates/flow_template.html') as f3:
      flow_content = f3.read()
    flow_content = flow_content.replace('<!-- 在这里插入表格 -->', flow_output)
    # return content, im2
    return profit_content, balance_content, flow_content

def export_csv(d1,d2,d3,numbers):
    # # get tables
    df1 = pd.read_html(d1,header=0)[0]
    df2 = pd.read_html(d2,header=0)[0]
    df3 = pd.read_html(d3,header=0)[0]

    # 数字正则表达式
    numbers = numbers.replace(' ','')
    pattern = r'\d+'

    numbers = re.findall(pattern, numbers)
    num = []
    for i in numbers:
      num.append(int(i)-1)

    col1 = read_numbers(df1, num)
    col2 = read_numbers(df2, num)
    col3 = read_numbers(df3, num)

    output_path = 'output.xlsx'

    # 创建一个 ExcelWriter 对象
    with pd.ExcelWriter(output_path) as writer:
        # 将每个 DataFrame 写入到不同的工作表中
        df1.style.apply(highlight_row, axis = 1).to_excel(writer, columns=col1 ,sheet_name='利润表', engine='openpyxl', index = False)
        df2.style.apply(highlight_row, axis = 1).to_excel(writer, columns=col2, sheet_name='资产负债表', engine='openpyxl', index = False)
        df3.style.apply(highlight_row, axis = 1).to_excel(writer, columns=col3, sheet_name='现金流量表', engine='openpyxl', index = False)
    return gr.File.update(value="output.xlsx", visible=True)
