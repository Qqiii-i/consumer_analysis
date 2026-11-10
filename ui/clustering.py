import streamlit as st
import pandas as pd
import plotly.express as px
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

    category_summary = pd.DataFrame(
        columns=[
            "cluster",
            "category",
            "amount",
            "category_ratio"
        ]
    )

    silhouette = None

    if expense_count >= 3:

        clustered_data = cluster_transactions(
            data,
            n_clusters=3
        )

        cluster_summary, category_summary = summarize_clusters(clustered_data)
        silhouette = clustered_data["silhouette_score"].iloc[0]

        if silhouette is not None:
            print(f"K-Means 聚类轮廓系数：{silhouette:.3f}")
        else:
            print("当前数据无法计算轮廓系数。")

        st.write("各聚类组消费统计")
        st.dataframe(cluster_summary, width="stretch")

        st.write("各聚类组交易笔数对比")

        cluster_fig = px.bar(
            cluster_summary,
            x="cluster",
            y="transaction_count",
            title="各聚类组交易笔数对比",
            text="transaction_count",
            labels={
                "cluster": "聚类组",
                "transaction_count": "交易笔数"
            }
        )

        cluster_fig.update_xaxes(tickangle=0)

        st.plotly_chart(cluster_fig, width="stretch")

        st.write("各聚类组平均消费金额对比")

        cluster_fig = px.bar(
            cluster_summary,
            x="cluster",
            y="average_amount",
            title="各聚类组平均消费金额对比",
            text="average_amount",
            labels={
                "cluster": "聚类组",
                "average_amount": "平均消费金额（元）"
            }
        )
        
        cluster_fig.update_xaxes(tickangle=0)

        cluster_fig.update_traces(texttemplate="%{text:.2f}")

        st.plotly_chart(cluster_fig, width="stretch")

        st.write("各聚类组消费类别统计")
        st.dataframe(category_summary, width="stretch")

        st.write("消费群体特征分析")

        overall_average = clustered_data["amount"].mean()

        for cluster_id in sorted(clustered_data["cluster"].unique()):
            group = clustered_data[
                clustered_data["cluster"] == cluster_id
            ]

            group_categories = category_summary[
                category_summary["cluster"] == cluster_id
            ]

            dominant_category = group_categories.loc[
                group_categories["category_ratio"].idxmax()
            ]

            average_amount = group["amount"].mean()
            category_name = dominant_category["category"]
            category_ratio = dominant_category["category_ratio"]

            if average_amount > overall_average:
                spending_level = "平均单笔消费金额较高"
            elif average_amount < overall_average:
                spending_level = "平均单笔消费金额较低"
            else:
                spending_level = "平均单笔消费金额接近整体水平"

            st.markdown(
                f"**Cluster {cluster_id}：** "
                f"{spending_level}，主要消费类别为"
                f" **{category_name}**，占该组消费金额的 "
                f"**{category_ratio:.1f}%**。"
            )

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

    return cluster_summary, category_summary, silhouette