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
    """复合增长率
    """
    r = (current_value / start_value) ** (1 / years) - 1
    if desc:
        return percent(r, degree)
    else:
        return round(r, degree) 

def percent(value, degree=2):
    change = '下降' if value < 0 else '增长'
    value = abs(value) * 100
    value = round(value, degree)
    return f'{change}{value}%'

