import streamlit as st
import pandas as pd
from algorithms.anomaly_detection import compare_anomaly_detection

def show_anomaly_detection(data):
    # 异常消费检测
    st.divider()
    st.subheader("异常消费检测")

    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    if not expense_data.empty:

        anomaly_result = compare_anomaly_detection(expense_data)

        abnormal_data = anomaly_result[
            anomaly_result["anomaly_methods"] != "正常"
        ]

        st.write(f"检测到 {len(abnormal_data)} 条统计异常记录")

        if len(abnormal_data) > 0:
            st.dataframe(
                abnormal_data[
                    ["transaction_id", "description", "amount",
                     "category", "anomaly_methods"]
                ],
                width="stretch"
            )
        else:
            st.success("暂未发现统计异常记录")

        st.caption("统计异常仅用于提醒核查，不代表消费错误或欺诈。")

    else:
        abnormal_data = pd.DataFrame()
        st.info("暂无消费支出数据，暂时无法进行异常检测。")

    return abnormal_data