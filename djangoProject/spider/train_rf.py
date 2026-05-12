import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import re

def train_rf_model():

    #1.路径处理
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'data/tb.csv')

    # 2. 数据加载与清洗
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"读取 CSV 失败: {e}")
        return

    def clean_pay_count(x):
        if pd.isna(x) or str(x).strip() == '':
            return 0
        s = str(x).replace('人付款', '').replace('+', '').strip()
        if '万' in s:
            try:
                return int(float(s.replace('万', '')) * 10000)
            except:
                return 0
        nums = re.findall(r'\d+', s)
        return int(nums[0]) if nums else 0

    df['pay_count'] = df['付款人数'].apply(clean_pay_count)
    df['price'] = pd.to_numeric(df['价格'], errors='coerce').fillna(0)
    df['title_len'] = df['标题'].str.len().fillna(0)

    def count_features(x):
        if pd.isna(x) or x == '[]':
            return 0
        return str(x).count(',') + 1

    df['features_count'] = df['特点列表'].apply(count_features)

    # 3. 编码处理
    encoders = {}
    category_map = {
        'shop_code': '店铺',
        'brand_code': '商品',
        'address_code': '发货地址',
    }

    for code_col, orig_col in category_map.items():
        le = LabelEncoder()
        df[orig_col] = df[orig_col].fillna('未知')
        df[code_col] = le.fit_transform(df[orig_col].astype(str))
        encoders[code_col] = le

    # 4. 训练
    feature_cols = ['price', 'title_len', 'features_count', 'shop_code', 'brand_code', 'address_code']
    X = df[feature_cols]
    y = df['pay_count']
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=1)
    model.fit(X, y)

    # 5. 保存
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)

    bundle_path = os.path.join(model_dir, 'rf_model_bundle.joblib')
    joblib.dump({
        'model': model,
        'model_encoders': encoders,
        'feature_cols': feature_cols,
    }, bundle_path)
if __name__ == '__main__':
    train_rf_model()