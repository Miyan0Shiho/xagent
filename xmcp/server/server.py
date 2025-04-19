"""
mcp server服务端实现

提供以下工具：

事实以及知识获取：
    获取制定位置在制定时区上的时间
    获取制定位置的新闻
    获取指定位置的股票信息
    获取指定位置的汇率信息


    RAG 部分：
        获取指定学科的知识
        获取指定范围的知识
        通过将和用户的对话以及过往经验以向量形式存储在数据库中
        通过向量数据库进行检索和用户的对话、过往的经验和记忆等

数据转换：
    通过文本生成图片
    从图片中提取文本
    处理pdf, markdown, html等文件
    处理excel, csv等表格文件
    处理json, xml等数据文件

网页操作：
    自动化操作网页
    自动化操作浏览器


"""

from mcp.server.fastmcp import FastMCP
import os
import sys
# 获取当前工作目录并添加到模块路径
current_dir = os.getcwd()
sys.path.insert(0, os.path.join(current_dir,'xmcp/server'))  # 添加当前目录到模块路径
from tools.cal_tool import calculate_sum,  calculate_difference, calculate_product, calculate_quotient, calculate_square        
from pydantic import create_model

mcp = FastMCP("TestServer")
# 事实及知识获取
# 数据转换
# 网页操作
# 数据计算
@mcp.tool()
def calculateSum_tool(num1: float, num2: float) -> float:
    """计算两个数字的和"""
    return calculate_sum(num1, num2)



if __name__ == "__main__":
    mcp.run()

