import streamlit as st
import pandas as pd
from algorithms.classifier import (
    classify_transactions,
    evaluate_classification
)

def show_classification(data):

    st.divider()
    st.subheader("自动消费分类")

    categories = [
        "餐饮", "交通", "购物", "娱乐", "住房",
        "医疗", "教育", "食品", "收入", "未分类"
    ]

    if not data.empty:

        classified_data = classify_transactions(data)
        evaluate_classification(classified_data)

        # 初始化最终类别
        if "final_category" not in classified_data.columns:
            classified_data["final_category"] = (
                classified_data["predicted_category"]
            )

        # 保存人工修改结果，避免页面刷新后丢失
        if "classification_edits" not in st.session_state:
            st.session_state["classification_edits"] = {}

        edits = st.session_state["classification_edits"]

        for index, row in classified_data.iterrows():
            transaction_id = row["transaction_id"]

            if transaction_id in edits:
                classified_data.at[index, "final_category"] = (
                    edits[transaction_id]
                )

        st.caption("可以通过最终类别列的下拉框修改交易类别。")

        edited_data = st.data_editor(
            classified_data[
                [
                    "transaction_id",
                    "description",
                    "category",
                    "predicted_category",
                    "final_category"
                ]
            ],
            column_config={
                "transaction_id": st.column_config.TextColumn("Transaction ID"),
                "description": st.column_config.TextColumn("Description"),
                "category": st.column_config.TextColumn("Original Category"),
                "predicted_category": st.column_config.TextColumn("Predicted Category"),
                "final_category": st.column_config.SelectboxColumn(
                    "Final Category",
                    options=categories,
                    required=True
                )
            },
            disabled=[
                "transaction_id",
                "description",
                "category",
                "predicted_category"
            ],
            hide_index=True,
            width="stretch",
            key="classification_editor"
        )
        if st.button("恢复全部自动分类"):
            st.session_state["classification_edits"] = {}
            st.rerun()
            
        # 保存人工修改结果
        for _, row in edited_data.iterrows():
            st.session_state["classification_edits"][
                row["transaction_id"]
            ] = row["final_category"]

        classified_data["final_category"] = (
            classified_data["transaction_id"].map(
                st.session_state["classification_edits"]
            ).fillna(classified_data["predicted_category"])
        )

        # 计算原始分类一致率，不受人工修改影响
        matched_count = (
            classified_data["category"]
            == classified_data["predicted_category"]
        ).sum()

        accuracy = matched_count / len(classified_data) * 100

        st.metric(
            "分类与原始标签一致率",
            f"{accuracy:.2f}%"
        )

    else:
        classified_data = pd.DataFrame(
            columns=[
                "transaction_id",
                "description",
                "category",
                "predicted_category",
                "final_category"
            ]
        )

        st.info("暂无交易记录，暂时无法进行自动分类。")

    return classified_data