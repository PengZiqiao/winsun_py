from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
import pandas as pd
from winsun.date import Week

"""常量"""
ZHU_ZHAI = ['住宅']
SHANG_YE = ['商业']
BAN_GONG = ['办公']
SHANG_BAN = ['商业', '办公']
BIE_SHU = ['独立别墅', '叠加别墅', '联排别墅', '双拼别墅']
SHANG_PIN_ZHU_ZHAI = ['独立别墅', '叠加别墅', '联排别墅', '双拼别墅', '住宅']
QUANSHI_BUHAN_LIGAO = '全市(不含溧水高淳)'


class GisSpider:
    def __init__(self):
        """初始化并登陆GIS
        """
        self.url = 'http://winsun.house365.com/'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 60)

        # 登陆
        self.driver.get(f'{self.url}weixin/login')
        print('>>> 请使用微信扫码登陆')
        try:
            self.wait.until(lambda driver: driver.find_element_by_class_name('logo'))
            print('>>> 成功登陆')
        except TimeoutException:
            print('>>> 登陆超时')

    def gongxiao(self, by, **kwargs):
        """商品房市场-供销走势
        :param 参数均为 string 或 [string,string,...]
            by: year, month, week
            year_start:开始年份 default:最新
            year:结束年份 default:最新
            plate:板块 default:全市
            pq:片区 default:不限
            groupby:分类方式 default:板块
            usg: 功能 default:[住宅]
            item: 输出项 default:[上市面积, 销售面积, 销售套数, 销售均价]
            isSum: 0 逐期 1 累计
        """
        if by == 'year':
            self.driver.get(f'{self.url}stat/wsdbestate/year')
        else:
            self.driver.get(f'{self.url}stat/wsdbestate/{by}trend')
        self.wait.until(lambda driver: driver.find_element_by_id("btnSearch"))

        # 下拉列表的选项们
        for key in ['week_start', 'week', 'month_start', 'month', 'year_start', 'year', 'plate', 'pq', 'groupby',
                    'isSum']:
            if key in kwargs:
                self.select(key, kwargs[key])

        # 功能
        if 'usg' in kwargs:
            self.checkbox('chk_usg', kwargs['usg'])

        # 输出项
        if 'item' in kwargs:
            dic = {
                '上市面积': '0',
                '上市套数': '1',
                '认购面积': '2',
                '认购套数': '3',
                '销售面积': '4',
                '销售套数': '5',
                '销售金额': '6',
                '销售均价': '7',
            }
            value_list = list(dic[key] for key in kwargs['item'])
            self.checkbox('chk_fld[]', value_list)

        # 查询
        self.driver.find_element_by_id("btnSearch").click()
        try:
            self.wait.until_not(lambda driver: driver.find_element_by_class_name('loading'))
            print('>>> 查询成功')
        except TimeoutException:
            print('>>> 超时')
        return self.driver.page_source

    def rank(self, by, plate, usg):
        """当期排行榜
        :param 
            by: week, month
            plate: 板块
            usg: 物业类型
        :return: df的列表,如df[0]为面积排行榜
        """
        self.driver.get(f'{self.url}stat/wsdbestate/{by}rank')
        self.wait.until(lambda driver: driver.find_element_by_id("btnSearch"))

        # 板块、功能
        self.select('plate', plate)
        self.checkbox('chk_usg', usg)

        # 查询
        self.driver.find_element_by_id("btnSearch").click()
        try:
            self.wait.until_not(lambda driver: driver.find_element_by_class_name('loading'))
            print('>>> 查询成功')
        except TimeoutException:
            print('>>> 超时')
        rank_df = pd.read_html(self.driver.page_source, index_col=0, header=0)
        return rank_df

    def select(self, name, value):
        """下拉列表
        :param
            name:表单控件的name
            value:表单的 value 或visible_text
        """
        s = Select(self.driver.find_element_by_name(name))
        try:
            s.select_by_visible_text(value)
        except NoSuchElementException:
            s.select_by_value(value)

    def checkbox(self, name, value_list):
        """多选框
        :param
            name:表单控件的name
            value:表单的 value 或visible_text
        """

        chk = self.driver.find_elements_by_name(name)

        # 取消所有已选项目
        for each in chk:
            if each.is_selected():
                each.click()

        # 根据value选中需要的项目
        for each in chk:
            if each.get_attribute('value') in value_list:
                each.click()

    def current_gxj(self, by, usg, plate, rengou=False):
        """返回一个当期的，以各板块为行，以“供、销、价”为列的表格，含“合计”
        :param 
            by: year, month, week
            usg: 物业类型
            plate: 板块
            rengou: 是否包含认购面积
        :return: df
        """

        item = ['上市面积', '销售面积', '销售均价']
        if rengou:
            item.append('认购面积')

        r = self.gongxiao(by=by, usg=usg, plate=plate, item=item, isSum='1')
        df = pd.read_html(r, index_col=0, header=0)[0]
        df = df.rename(index=lambda x: x.replace('仙西', '仙林'))
        df = df_gxj(df)
        return df

    def trend_gxj(self, by, usg, plate, period, rengou=False):
        """返回一个按时间为行的，以“供、销、价”为列的表格
        :param 
            by: year, month, week
            usg: 物业类型
            plate: 板块
            rengou: 是否包含认购面积
            period: 期数
        :return: df
        """
        # 设置开始时间
        if by == 'week':
            w = Week()
            start = {
                'week_start': f'2017{w.N - period + 1}'
            }

        item = ['上市面积', '销售面积', '销售均价']
        if rengou:
            item.append('认购面积')

        r = self.gongxiao(by=by, plate=plate, usg=usg, item=item, isSum='0', **start)
        df = pd.read_html(r, index_col=0, header=1)[0]
        df = df_reshape(df, -1, list(range(period)), item)
        return df_gxj(df)


def df_reshape(df, row, index, columns):
    """
    :param 
        df: pd.DataFrame()
        row: 保留第几行数据
        index：大概是一个日期组成的列表，转换为每行
        columns：项名称组成的列表，转换为每列
    :return df
    """
    col_len = len(columns)
    index_len = len(index)

    df = df.iloc[row,range(col_len * index_len)]
    matrix = df.as_matrix().reshape(index_len, col_len)
    return pd.DataFrame(matrix, index, columns)

def df_gxj(df):
    """表中面积单位由㎡换算为万㎡，并保留两位小数"""
    # 最后一列为均价，前面2（含认购则为3）列为面积
    for each in df.columns[:-1]:
            df[each].astype('float')
            df[each] = df[each] / 1e4
    df[df.columns[-1]].astype('int')
    df = df.round(2)
    return df