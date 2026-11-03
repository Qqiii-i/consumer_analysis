import streamlit as st
import pandas as pd

from algorithms.clustering import (
    cluster_transactions,
    summarize_clusters
)


def show_clustering(data):

    # K-Means消费行为聚类
    st.divider()
    st.subheader("消费行为聚类分析")

    expense_count = (
        data["transaction_type"] == "支出"
    ).sum()

    cluster_summary = pd.DataFrame(
        columns=[
            "cluster",
            "transaction_count",
            "average_amount",
            "total_amount"
        ]
    )

    if expense_count >= 3:

        clustered_data = cluster_transactions(
            data,
            n_clusters=3
        )

        cluster_summary = summarize_clusters(clustered_data)

        silhouette = clustered_data["silhouette_score"].iloc[0]

        if silhouette is not None:
            print(f"K-Means 聚类轮廓系数：{silhouette:.3f}")
        else:
            print("当前数据无法计算轮廓系数。")

        st.write("各聚类组消费统计")
        st.dataframe(cluster_summary, width="stretch")

        st.write("消费记录所属聚类")
        st.dataframe(
            clustered_data[
                ["transaction_id", "description", "amount",
                 "category", "cluster"]
            ],
            width="stretch"
        )

    else:
        st.info("消费记录不足3条，暂时无法进行K-Means聚类分析。")

    return cluster_summary