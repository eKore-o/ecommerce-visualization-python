import pandas as pd
import numpy as np
import jieba
from PyInstaller.building.build_main import Analysis
from sqlalchemy import create_engine
import sys
import os

# 添加路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class PandasAnalysis:
    def __init__(self):
        self.db_url = f"mysql+pymysql://{Config.User}:{Config.Password}@{Config.Host}:{Config.Port}/{Config.Database}?charset=utf8mb4"
        self.engine = create_engine(self.db_url)
        self.csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clean', 'tb_clean.csv')

    def load_data(self):
        df = pd.read_csv(self.csv_path)

        # 标题, 店铺, 价格, 付款人数, 发货地址, 详情页地址, 图片地址, 特点列表, 卖点, 商品条
        column_mapping = {
            '标题': 'title',
            '店铺': 'shop_name',
            '价格': 'price',
            '付款人数': 'sales_count',
            '发货地址': 'shipping_addr',
            '详情页地址': 'detail_url',
            '图片地址': 'img_url',
            '特点列表': 'feature_list',
            '卖点': 'selling_point',
            '商品': 'product_type'
        }
        df.rename(columns=column_mapping, inplace=True)

        df = df.dropna(subset=['title','shop_name','price','shipping_addr','product_type'])

        def parse_sales(val):
            val = str(val).strip()
            if '万' in val:
                return float(val.replace('万', '').strip()) * 10000
            if val.isdigit():
                return float(val)

            import re
            res = re.findall(r'\d+\.?\d*', val)
            return float(res[0]) if res else 0.0

        df['sales_count'] = df['sales_count'].apply(parse_sales)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] > 0]

        return df

    def save_to_mysql(self, df,table_name):
        df.to_sql(table_name,self.engine,if_exists='replace',index=False)

    def run_analysis(self):
        df = self.load_data()
        print('执行part1商品销量分析....')
        part1 = df.groupby('product_type')['sales_count'].sum().reset_index()
        part1.columns = ['name','value']
        counts = df['product_type'].value_counts()
        valid_types = counts[counts > 10].index
        part1 = part1[part1['name'].isin(valid_types)].sort_values(by='value', ascending=False)
        self.save_to_mysql(part1, 'part1')

        print('执行part2城市销售额分析....')
        part2 = df.groupby('shipping_addr')['sales_count'].sum().reset_index()
        part2.columns = ['name', 'value']
        self.save_to_mysql(part2, 'part2')

        print('执行part3店铺销量排行....')
        part3 = df.groupby('shop_name')['sales_count'].sum().reset_index()
        part3.columns = ['name', 'value']
        part3 = part3.sort_values(by='value', ascending=False).head(10)
        self.save_to_mysql(part3, 'part3')

        print('执行part4价格区间分析....')

        def get_price_range(p):
            if p < 1000:
                return "1000以下"
            if 1000 <= p < 2000:
                return "1000-1999"
            if 2000 <= p < 3000:
                return "2000-2999"
            if 3000 <= p < 4000:
                return "3000-3999"
            if 4000 <= p < 5000:
                return "4000-4999"
            return "5000以上"

        df['price_range'] = df['price'].apply(get_price_range)
        part4 = df['price_range'].value_counts().reset_index()
        part4.columns = ['name', 'value']

        # 按名称排序
        range_order = ["1000以下", "1000-1999", "2000-2999", "3000-3999", "4000-4999", "5000以上"]
        part4['order'] = part4['name'].apply(lambda x: range_order.index(x) if x in range_order else 99)
        part4 = part4.sort_values('order').drop('order', axis=1)
        self.save_to_mysql(part4, 'part4')

        print('执行part5商品特点分布....')
        features_data = []
        for _, row in df.iterrows():
            if pd.isna(row['feature_list']):
                continue
            flist = str(row['feature_list']).split('，')
            for f in flist:
                if f.strip():
                    features_data.append({
                        'product_type': row['product_type'],
                        'feature': f.strip()
                    })

        df_features = pd.DataFrame(features_data)
        part5_raw = df_features.groupby(['product_type', 'feature']).size().reset_index(name='value')
        # 过滤
        part5_raw = part5_raw[part5_raw['value'] > 10]
        part5_raw = part5_raw.sort_values(['product_type', 'value'], ascending=[True, False])
        part5 = part5_raw.groupby('product_type').head(10).reset_index(drop=True)
        part5.columns = ['name', 'name1', 'value']
        self.save_to_mysql(part5, 'part5')

        print('执行part6标题词云分析....')
        #结巴分词
        all_titles = " ".join(df['title'].astype(str))
        words = jieba.lcut(all_titles)
        words_counts = pd.Series([w for w in words if len(w) > 1]).value_counts().reset_index()
        words_counts.columns = ['name', 'value']
        part6 = words_counts.head(50)
        self.save_to_mysql(part6, 'part6')

        print('执行part7商品平均价格分析....')
        part7 = df.groupby('product_type')['price'].mean().reset_index()
        part7.columns = ['name', 'value']
        part7['value'] = part7['value'].round(2)
        # 过滤
        valid_types_p7 = counts[counts > 20].index
        part7 = part7[part7['name'].isin(valid_types_p7)].sort_values(by='value', ascending=False)
        self.save_to_mysql(part7, 'part7')

if __name__ == '__main__':
    analysis = PandasAnalysis()
    analysis.run_analysis()

