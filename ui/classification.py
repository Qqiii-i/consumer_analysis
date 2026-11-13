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


def reset_descriptions():
    st.session_state["description_edits"] = {}

    st.session_state["classification_editor_version"] = (
        st.session_state.get("classification_editor_version", 0) + 1
    )

def show_classification(data):

    st.divider()
    st.subheader("自动消费分类")

    categories = [
        "餐饮", "交通", "购物", "娱乐", "住房",
        "医疗", "教育", "食品", "收入", "其他", "未分类"
    ]

    if not data.empty:
        # 初始化人工描述修改记录
        if "description_edits" not in st.session_state:
            st.session_state["description_edits"] = {}

        # 应用已经保存的人工描述
        working_data = data.copy()
        description_edits = st.session_state["description_edits"]

        for index, row in working_data.iterrows():
            transaction_id = row["transaction_id"]

            if transaction_id in description_edits:
                working_data.at[index, "description"] = (
                    description_edits[transaction_id]
                )

        # 使用修改后的描述进行自动分类
        classified_data = classify_transactions(working_data)

        model_accuracy = classified_data.attrs.get("model_accuracy")

        if model_accuracy is not None:
            st.metric(
                "朴素贝叶斯测试集准确率",
                f"{model_accuracy * 100:.2f}%"
            )
        else:
            st.info("训练数据不足，暂时无法训练朴素贝叶斯模型。")

        # 初始化最终类别
        classified_data["final_category"] = (
            classified_data["predicted_category"]
        )

        # 初始化人工分类修改记录
        if "classification_edits" not in st.session_state:
            st.session_state["classification_edits"] = {}

        edits = st.session_state["classification_edits"]

        # 应用人工修改过的分类
        for index, row in classified_data.iterrows():
            transaction_id = row["transaction_id"]

            if transaction_id in edits:
                classified_data.at[index, "final_category"] = (
                    edits[transaction_id]
                )

        st.caption(
            "可以直接编辑交易描述，也可以通过最终类别列的下拉框修改交易类别。"
        )

        # 编辑账单数据
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
                "predicted_category": None,
                "final_category": st.column_config.SelectboxColumn(
                    "Final Category",
                    options=categories,
                    required=True
                )
            },
            disabled=[
                "transaction_id",
                "category",
                "predicted_category"
            ],
            hide_index=True,
            width="stretch",
            key=f"classification_editor_{st.session_state.get('classification_editor_version', 0)}"
        )

        transfer_category_changed = False

        # 微信账单中未分类转账记录的单独展示
        if st.session_state.get("transaction_data_source") == "微信支付账单":


            transfer_mask = (
                edited_data["final_category"].astype(str).eq("未分类")
                & edited_data["description"].astype(str).str.contains(
                    "转账|二维码收款",
                    na=False
                )
            )

            transfer_data = edited_data.loc[transfer_mask].copy()

            st.divider()
            st.subheader(":material/payments: 待处理转账记录")

            if not transfer_data.empty:
                st.caption(
                    "以下记录同时保留在上方原始分类列表中。"
                )

                transfer_edited_data = st.data_editor(
                    transfer_data[
                        [
                            "transaction_id",
                            "description",
                            "predicted_category",
                            "final_category"
                        ]
                    ],
                    column_config={
                        "transaction_id": st.column_config.TextColumn("Transaction ID"),
                        "description": st.column_config.TextColumn("Description"),
                        "predicted_category": st.column_config.TextColumn("Original Category"),
                        "final_category": st.column_config.SelectboxColumn(
                            "Final Category",
                            options=categories,
                            required=True
                        )
                    },
                    disabled=[
                        "transaction_id",
                        "description",
                        "predicted_category"
                    ],
                    hide_index=True,
                    width="stretch",
                    key=f"transfer_editor_{st.session_state.get('classification_editor_version', 0)}"
                )

                st.write(f"共发现 {len(transfer_data)} 条待处理转账记录。")

                # 检查转账区域是否修改了类别
                original_categories = transfer_data.set_index(
                    "transaction_id"
                )["final_category"]

                new_categories = transfer_edited_data.set_index(
                    "transaction_id"
                )["final_category"]

                changed_ids = new_categories[
                    new_categories != original_categories
                ].index

                if len(changed_ids) > 0:

                    new_category_map = new_categories.to_dict()

                    edited_data.loc[
                        edited_data["transaction_id"].isin(changed_ids),
                        "final_category"
                    ] = edited_data.loc[
                        edited_data["transaction_id"].isin(changed_ids),
                        "transaction_id"
                    ].map(new_category_map)

                    transfer_category_changed = True

            else:
                st.success("没有符合条件的待处理转账记录。")

        # 恢复按钮
        col1, col2 = st.columns(2)

        with col1:
            st.button(
                "恢复全部自动分类",
                on_click=reset_classification
            )

        with col2:
            st.button(
                "恢复全部原始描述",
                on_click=reset_descriptions
            )

        # 检测分类修改并保存日志
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

        # 保存人工修改的描述
        original_descriptions = (
            data.set_index("transaction_id")["description"].to_dict()
        )

        description_changed = False

        for _, row in edited_data.iterrows():

            transaction_id = row["transaction_id"]
            new_description = str(row["description"])

            original_description = str(
                original_descriptions.get(transaction_id, "")
            )

            if new_description != original_description:

                if st.session_state["description_edits"].get(
                    transaction_id
                ) != new_description:

                    st.session_state["description_edits"][
                        transaction_id
                    ] = new_description

                    description_changed = True

            else:

                if transaction_id in st.session_state["description_edits"]:
                    del st.session_state["description_edits"][transaction_id]
                    description_changed = True

        # 保存人工修改的分类
        for _, row in edited_data.iterrows():
            st.session_state["classification_edits"][
                row["transaction_id"]
            ] = row["final_category"]

        # 转账区域修改后，刷新两个编辑区域
        if transfer_category_changed:
            st.session_state["classification_editor_version"] = (
                st.session_state.get("classification_editor_version", 0) + 1
            )
            st.rerun()

        classified_data["description"] = edited_data["description"].values

        classified_data["final_category"] = (
            classified_data["transaction_id"].map(
                st.session_state["classification_edits"]
            ).fillna(classified_data["predicted_category"])
        )

        # 描述发生变化时，重新运行分类
        if description_changed:
            st.rerun()

        # 计算原始分类一致率
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