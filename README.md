## 使用 python 来对作图数据预处理

> 本质是数据清洗，并输出初步的图像

文件夹`plain_data`中的是原始数据，里面需要用的是`[LC Chromatogram(Detector A-Ch1)]`这个下面的表格数据
第一列需要乘以一个`0.4`或者`0.5`的系数，需做成可配参数，第二列除以 1000 即可

执行脚本名称为：index.py

`python3 transData.js *(X轴系数)`

默认会处理`plain_data`文件夹下的所有原始数据，然后通过绘图处理出基本结果, 保存在result文件夹下

依赖：`python3` | `pandas` | `matplotlib`
安装依赖包命令：`pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas matplotlib --user`
