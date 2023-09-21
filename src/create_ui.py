import gradio as gr
from src.ui_fun import *

def create_ui():
    with gr.Blocks() as demo:
        gr.Markdown(
        """
        # 智能财报分析系统
        """)

        file = gr.File(label="请上传PDF文件", file_types=['pdf'])
        with gr.Row(equal_height=True):
          with gr.Column():
            with gr.Row():
              with gr.Column():
                p_s_profit = gr.Textbox(label = '利润表起始页码', info="请输入起始页码")
                p_e_profit = gr.Textbox(label = '终止页码', info="请输入终止页码(如果是单页，请输入相同页码即可)")
              with gr.Column():
                p_s_balance = gr.Textbox(label = '资产负债表起始页码', info="请输入起始页码")
                p_e_balance = gr.Textbox(label = '终止页码', info="请输入终止页码(如果是单页，请输入相同页码即可)")
              with gr.Column():
                p_s_flow = gr.Textbox(label = '现金流量表起始页码', info="请输入起始页码")
                p_e_flow = gr.Textbox(label = '终止页码', info="请输入终止页码(如果是单页，请输入相同页码即可)")

        button1 = gr.Button("匹配")
        with gr.Column():
          with gr.Row(equal_height=True) :
            # profit_options = gr.CheckboxGroup(label = '请选择需要列')
            profit_dataframe = gr.HTML(scale=2)

          with gr.Row(equal_height=True) :
            # balance_options = gr.CheckboxGroup(label = '请选择需要的列')
            balance_dataframe = gr.HTML()

          with gr.Row(equal_height=True) :
            # flow_options = gr.CheckboxGroup(label = '请选择需要列')
            flow_dataframe = gr.HTML()

          numbers = gr.CheckboxGroup(label = '选择需要列的序号')
          numbers = gr.Textbox(label = '请选择需要列的序号', info="从1开始计数")
          button2 = gr.Button("下载")
          csv = gr.File(interactive=False, visible=False)

        button1.click(mock_ocr, [file,p_s_profit, p_e_profit,p_s_balance, p_e_balance, p_s_flow, p_e_flow], [profit_dataframe,balance_dataframe,flow_dataframe])
        button2.click(export_csv, [profit_dataframe, balance_dataframe, flow_dataframe,numbers], csv)
      
    return demo
