import re
import pandas as pd
import ast

def tb_clean():
    df = pd.read_csv('../data/tb.csv')
    df['标题'] = df['标题'].str.replace(r'<span.*?>|</span>', '', regex=True)
    df['标题'] = df['标题'].str.strip()

    # 清洗价格列
    df['价格'] = df['价格'].astype(str).str.replace(',', '')
    df['价格'] = pd.to_numeric(df['价格'], errors='coerce')

    # 清洗付款人数列
    def clean_payment(x):
        if pd.isna(x):
            return 0
        x = str(x)
        if '万+人付款' in x:
            x = int(x.replace('万+人付款', '')) * 10000
            return x
        elif '+人付款' in x:
            return x.replace('+人付款', '')
        elif '人付款' in x:
            return x.replace('人付款', '')
        else:
            return 0  # 其他情况也替换为0

    df['付款人数'] = df['付款人数'].apply(clean_payment)
    df['付款人数'] = df['付款人数'].fillna(0).astype(int)

    # 清洗发货地址列
    df['发货地址'] = df['发货地址'].str.strip()
    df['发货地址'] = df['发货地址'].str.split(' ').str[0]

    # 清洗特点列表列 - 提取文字内容并按空格拼接
    def extract_features(x):
        if isinstance(x, str):
            try:
                # 安全地解析列表
                features_list = ast.literal_eval(x)
                if isinstance(features_list, list):
                    # 提取列表中的文字内容并用空格拼接
                    return ' '.join([str(item) for item in features_list])
                else:
                    return str(x)
            except:
                return str(x)
        elif isinstance(x, list):
            # 如果已经是列表，直接拼接
            return ' '.join([str(item) for item in x])
        else:
            return str(x) if pd.notna(x) else ''

    df['特点列表'] = df['特点列表'].apply(extract_features)

    # 清洗卖点列 - 提取['']中的文字内容
    def extract_selling_points(x):
        if pd.isna(x):
            return ''
        x_str = str(x)
        # 使用正则表达式提取中括号内的内容
        matches = re.findall(r"\['\"](.*?)['\"]\]", x_str)
        if matches:
            # 如果有多个匹配，用空格拼接
            return ' '.join(matches)
        else:
            # 如果没有中括号格式，返回原内容
            return x_str

    df['卖点'] = df['卖点'].apply(extract_selling_points)

    df = df[df['标题'] != '0']
    df = df.drop_duplicates(subset='标题')

    # 保存清洗后的数据
    df.to_csv('tb_clean.csv', index=False, encoding='utf-8-sig')


tb_clean()