def gr(a,b, desc=True, degree=2):
    """growth rate
    a相对于b的增长率
    """
    r = (a - b) / b
    if desc:
        return percent(r, degree)
    else:
        return round(r, degree) 

def cagr(current_value, start_value , years, desc=True, degree=2):
    """
    复合增长率
    """
    r = (current_value / start_value) ** (1 / years) - 1
    if desc:
        return percent(r, degree)
    else:
        return round(r, degree) 

def percent(value, degree=2):
    """
    将带正负号的比值(1代表100%)转成“增长/下降xx%”的形式
    """
    from numpy import isnan
    if isnan(value):
        return '无环比'
    else:
        change = '下降' if value < 0 else '增长'
    value = abs(value) * 100
    if degree == 0:
        value = f'{value:.0f}'
    else:
        value = round(value, degree)
    return f'{change}{value}%'

def px2cm(value):
    """
    将像素换算成厘米
    """
    return value/96*2.54

def cm2px(value):
    """
    将厘米换算成像素
    """
    return value/2.54*96
