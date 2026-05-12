import pymysql
import pandas as pd
import csv
from typing import List,Optional
import re

from pymysql.cursors import DictCursor


class CSVToMysql:
    def __init__(self,host:str = 'localhost',user:str='root',
                 password:str='123456',database:str='db_cp_tb_commodity_project',):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):

        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败{e}")
            raise
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("数据库连接关闭")

    def create_table(self):
        """创建数据表"""
        create_table_sql = """
    CREATE TABLE IF NOT EXISTS data (
        id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
        title VARCHAR(500) COMMENT '商品标题',
        shop VARCHAR(100) COMMENT '店铺名称',
        price DECIMAL(10,2) COMMENT '商品价格',
        pay_count INT COMMENT '付款人数',
        ship_address VARCHAR(100) COMMENT '发货地址',
        detail_url TEXT COMMENT '详情页地址',
        image_url TEXT COMMENT '图片地址',
        features TEXT COMMENT '特点列表',
        selling_points TEXT COMMENT '卖点',
        product_brand VARCHAR(100) COMMENT '商品品牌'
    ) COMMENT '淘宝商品项目数据表'
    """
        try:
            self.cursor.execute(create_table_sql)
            self.connection.commit()
            print("数据表创建成功")
        except Exception as e:
            print(f"数据表创建失败: {e}")
            raise

    def clean_data(self, value: str) -> Optional[str]:
        """清洗数据"""
        if not value or value.strip() == '' or value == 'NaN' or value == 'None' or value == 'Null':
            return None
        return value.strip()



    def parse_pay_count(self, value: str) -> Optional[int]:
        """解析付款人数"""
        if not value:
            return None

        value = str(value).strip()

        # 处理"200000"这样的数字字符串
        if value.isdigit():
            return int(value)

        # 处理包含"万"的情况
        if '万' in value:
            try:
                num = float(value.replace('万', '').strip())
                return int(num * 10000)
            except:
                return None

        # 处理0值
        if value == '0':
            return 0

        return None

    def parse_price(self, value: str) -> Optional[float]:
        """解析价格"""
        if not value:
            return None

        try:
            # 移除可能的货币符号和空格
            value = str(value).replace('¥', '').replace('￥', '').strip()
            # 处理空字符串或None
            if value == '' or value == 'None' or value == 'NaN':
                return None
            return float(value)
        except:
            return None

    def read_csv(self, file_path: str) -> List[dict]:
        """读取CSV文件"""
        data = []
        try:
            # 使用utf-8-sig编码读取，自动处理BOM
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                dict_reader = csv.DictReader(file)

                for i, row in enumerate(dict_reader):
                    if i < 3:  # 打印前3行数据用于调试
                        print(f"第{i + 1}行数据: {dict(row)}")
                    data.append(row)

            print(f"成功读取 {len(data)} 行数据")
            return data
        except Exception as e:
            print(f"读取CSV文件失败: {e}")
            raise

    def get_column_value(self, row: dict, possible_keys: list) -> Optional[str]:
        """获取列值，支持多个可能的列名"""
        for key in possible_keys:
            if key in row and row[key] is not None:
                return self.clean_data(row[key])
        return None

    def insert_data(self, data: List[dict]):
        """插入数据到数据库"""
        insert_sql = """
        INSERT INTO data 
        (title, shop, price, pay_count, ship_address, detail_url, image_url, features, selling_points, product_brand)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        success_count = 0
        error_count = 0

        for i, row in enumerate(data):
            try:
                # 处理BOM问题，尝试多种可能的标题列名
                title = self.get_column_value(row, ['\ufeff标题', '标题', 'title', '商品标题'])

                # 其他列
                shop = self.get_column_value(row, ['店铺', 'shop'])
                price = self.parse_price(self.get_column_value(row, ['价格', 'price']))
                pay_count = self.parse_pay_count(self.get_column_value(row, ['付款人数', 'pay_count']))
                ship_address = self.get_column_value(row, ['发货地址', 'ship_address'])
                detail_url = self.get_column_value(row, ['详情页地址', 'detail_url'])
                image_url = self.get_column_value(row, ['图片地址', 'image_url'])
                features = self.get_column_value(row, ['特点列表', 'features'])
                selling_points = self.get_column_value(row, ['卖点', 'selling_points'])
                product_brand = self.get_column_value(row, ['商品', 'product_brand', 'brand'])

                if i < 5:  # 打印前5行处理结果
                    print(f"处理第{i + 1}行 - 标题: {title}")

                # 执行插入
                self.cursor.execute(insert_sql, (
                    title, shop, price, pay_count, ship_address,
                    detail_url, image_url, features, selling_points, product_brand
                ))
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"插入数据失败（第{i + 1}行）: {e}")
                print(f"失败行的数据: {row}")
                continue

        self.connection.commit()
        print(f"数据插入完成：成功 {success_count} 条，失败 {error_count} 条")

    def import_from_csv(self, csv_file_path: str):
        """主方法：从CSV导入数据到MySQL"""
        try:
            # 连接数据库
            self.connect()

            # 创建表
            self.create_table()

            # 读取CSV数据
            data = self.read_csv(csv_file_path)

            # 插入数据
            self.insert_data(data)

        except Exception as e:
            print(f"导入过程出错: {e}")
        finally:
            # 关闭连接
            self.disconnect()

if __name__ == '__main__':
    # 初始化导入器
    importer = CSVToMysql(
        host='localhost',
        user='root',
        password='123456',
        database='db_cp_tb_commodity_project'
    )
    # 执行导入
    importer.import_from_csv('clean/tb_clean.csv')