import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

def cluster_transactions(data, n_clusters=3):
    """
    使用 K-Means 对消费记录进行聚类。
    根据消费金额和消费类别划分相似的交易。
    """

    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    if len(expense_data) < n_clusters:
        raise ValueError("消费记录数量不能少于聚类数量")

    features = pd.get_dummies(
        expense_data[["amount", "category"]],
        columns=["category"],
        dtype=float
    )

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(scaled_features)
    expense_data["cluster"] = labels

    if 1 < len(set(labels)) < len(labels):
        score = silhouette_score(scaled_features, labels)
    else:
        score = None

    expense_data["silhouette_score"] = score

    return expense_data


def summarize_clusters(data):
    # 统计各聚类组的消费金额和类别特征。
    summary = (
        data.groupby("cluster")
        .agg(
            transaction_count=("amount", "count"),
            average_amount=("amount", "mean"),
            total_amount=("amount", "sum")
        )
        .reset_index()
    )

    category_summary = (
        data.groupby(["cluster", "category"])["amount"]
        .sum()
        .reset_index()
    )

    category_summary["category_ratio"] = (
        category_summary["amount"]
        / category_summary.groupby("cluster")["amount"].transform("sum")
        * 100
    )

    return summary, category_summary