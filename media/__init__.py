import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool

# 生成示例数据
df = pd.DataFrame({
    'timestamp1': np.arange(900, 946),
    'timestamp2': np.arange(900, 946),
    'timestamp3': np.arange(900, 946),
    'timestamp4': np.arange(900, 946),
    'min1': np.random.randint(20, 80, size=(46,)),
    'min2': np.random.randint(25, 70, size=(46,)),
    'min3': np.random.randint(30, 90, size=(46,)),
    'min4': np.random.randint(35, 100, size=(46,)),
})

# 定义不同颜色
colors = ['#CAB2D6','#FF9F7F','#B5EAD7','#F7DD72']

# 循环生成四个数据源
sources = []
for i in range(1, 5):
    x_col = 'timestamp{}'.format(i)
    y_col = 'min{}'.format(i)
    sources.append(ColumnDataSource(data=dict(
        x= df[x_col],
        y= df[y_col],
        color=[colors[i-1]] * len(df),
        label=['timestamp{}'.format(i)] * len(df),  # 添加新的label列到数据源
    )))

# 创建图形对象
p = figure(width=800, height=400)

# 循环生成四条折线，并对每条线添加一个HoverTool
for i in range(4):
    line = p.line(x='x', y='y', source=sources[i], line_width=2, color=colors[i], legend_label='@label[0]', name='line{}'.format(i+1))
    hover = HoverTool(tooltips=[('Line', '@label'), ('X', '@x'), ('Value', '@y')], renderers=[line])
    p.add_tools(hover)

# 展示图形
output_file('four_lines_hover.html')
show(p)
