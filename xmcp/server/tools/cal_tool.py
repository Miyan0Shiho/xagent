from pydantic import BaseModel, Field
from typing import Optional

# 工具参数模型
class SumToolParams(BaseModel):
    """工具参数模型"""
    # 计算类型
    type: str = Field(..., description="计算类型")
    # 数字1
    num1: Optional[float] = Field(None, description="数字1")
    # 数字2
    num2: Optional[float] = Field(None, description="数字2")
    # 计算结果
    result: Optional[float] = Field(None, description="计算结果")

def calculate_sum(num1: float, num2: float) -> float:
    """计算两个数字的和"""
    return num1 + num2
def calculate_difference(num1: float, num2: float) -> float:
    """计算两个数字的差"""
    return num1 - num2
def calculate_product(num1: float, num2: float) -> float:
    """计算两个数字的积"""
    return num1 * num2
def calculate_quotient(num1: float, num2: float) -> float:
    """计算两个数字的商"""
    if num2 == 0:
        raise ValueError("除数不能为零")
    return num1 / num2
def calculate_square(num: float) -> float:
    """计算一个数字的平方"""
    return num ** 2
def calculate_square_root(num: float) -> float:
    """计算一个数字的平方根"""
    if num < 0:
        raise ValueError("不能计算负数的平方根")
    return num ** 0.5
def calculate_power(num: float, exponent: float) -> float:
    """计算一个数字的幂"""
    return num ** exponent
def calculate_modulus(num1: float, num2: float) -> float:
    """计算两个数字的模"""