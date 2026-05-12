import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
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

    df['price'] = pd.to_numeric(df['价格'], errors='coerce').fillna(0)
    df['pay_count'] = df['付款人数'].apply(clean_pay_count)

    df['title'] = df['标题'].fillna('未知商品')

    df = df[df['price'] > 0]
    if len(df) < 10:
        return

    # 3. 转换和聚类
    df['log_price'] = np.log1p(df['price'])
    df['log_pay'] = np.log1p(df['pay_count'])

    features = ['log_price', 'log_pay']
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # 4. 语义排序
    cluster_means = df.groupby('cluster')['pay_count'].mean().sort_values().index.tolist()
    cluster_mapping = {old_id: new_id for new_id, old_id in enumerate(cluster_means)}
    df['cluster'] = df['cluster'].map(cluster_mapping)

    cluster_names = ["小众潜力款", "大众走量款", "高端溢价款"]
    df['cluster_name'] = df['cluster'].apply(lambda x: cluster_names[x])

    # 5. 保存为 CSV
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)
    save_path = os.path.join(model_dir, 'kmeans_results.csv')

    final_df = df[['title', 'price', 'pay_count', 'cluster', 'cluster_name']]
    final_df.to_csv(save_path, index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    train_rf_model()