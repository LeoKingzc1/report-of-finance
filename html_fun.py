from HTMLTable import HTMLTable

def df_html(title, df):
  df = df
  head = tuple(df.columns.values)
  rows = []
  for i in range(len(df)):
    rows.append(tuple(df.iloc[i]))
  rows = tuple(rows)

  # 标题
  table = HTMLTable(caption = title)
  # 表头行
  table.append_header_rows(((head),))
  # 数据行
  table.append_data_rows(rows)

    # 标题样式
  table.caption.set_style({
      'font-size': '22px',
  })
  # 表格样式，即<table>标签样式
  table.set_style({
      'border-collapse': 'collapse',
      'word-break': 'keep-all',
      'white-space': 'nowrap',
      'font-size': '12px',
  })
  # 统一设置所有单元格样式，<td>或<th>
  table.set_cell_style({
      'border-color': '#000',
      'border-width': '1px',
      'border-style': 'solid',
      'padding': '5px',
  })
  # 表头样式
  table.set_header_row_style({
      'color': '#fff',
      'background-color': '#48a6fb',
      'font-size': '18px',
  })
  # 覆盖表头单元格字体样式
  table.set_header_cell_style({
      'padding': '8px',
  })
  # 调小次表头字体大小
  table[1].set_cell_style({
      'padding': '8px',
      'font-size': '8px',
  })
  # 遍历数据行，如果增长量为负，标红背景颜色
  for row in table.iter_data_rows():
      if row[2].value == '疑似':
          row.set_style({
              'background-color': '#ffdddd',
          })

  return table.to_html()

def highlight_row(s):
    # c = 'background-color: green' if int(s[1]) > 20 else ''
    c = 'background-color: red' if s['匹配程度'] == '疑似' else ''
    return [c] * len(s)