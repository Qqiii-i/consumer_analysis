import streamlit as st
import pandas as pd
from algorithms.classifier import classify_transactions, evaluate_classification
from pathlib import Path
from datetime import datetime

def save_classification_log(records):
    """
    保存人工修改过的消费分类记录。
    不记录交易单号等敏感信息。
    """

    if records.empty:
        return

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "classification_log.csv"

    log_data = records.copy()
    log_data["修改时间"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_data = log_data.rename(columns={
        "description": "交易描述",
        "predicted_category": "原自动分类",
        "final_category": "人工修改分类"
    })

    log_data = log_data[
        ["修改时间", "交易描述", "原自动分类", "人工修改分类"]
    ]

    log_data.to_csv(
        log_file,
        mode="a",
        header=not log_file.exists(),
        index=False,
        encoding="utf-8-sig"
    )

def reset_classification():
    st.session_state["classification_edits"] = {}

    st.session_state["classification_editor_version"] = (
        st.session_state.get("classification_editor_version", 0) + 1
    )

    st.session_state["classification_reset_triggered"] = True

def show_classification(data):

    st.divider()
    st.subheader("自动消费分类")

    categories = [
        "餐饮", "交通", "购物", "娱乐", "住房",
        "医疗", "教育", "食品", "收入", "未分类"
    ]

    if not data.empty:

        classified_data = classify_transactions(data)

        model_accuracy = classified_data.attrs.get("model_accuracy")

        if model_accuracy is not None:
            st.metric(
                "朴素贝叶斯测试集准确率",
                f"{model_accuracy * 100:.2f}%"
            )
        else:
            st.info("训练数据不足，暂时无法训练朴素贝叶斯模型。")

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
            key=f"classification_editor_{st.session_state.get('classification_editor_version', 0)}"
        )

        st.button(
            "恢复全部自动分类",
            on_click=reset_classification
        )

        # 检测本次新增的人工分类修改
        reset_triggered = st.session_state.pop(
            "classification_reset_triggered", False
        )

        if not reset_triggered:

            changed_mask = (
                edited_data["final_category"].astype(str)
                != classified_data["final_category"].astype(str)
            )

            changed_records = edited_data.loc[
                changed_mask,
                ["description", "predicted_category", "final_category"]
            ].copy()

            if not changed_records.empty:
                save_classification_log(changed_records)
       
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