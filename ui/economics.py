import streamlit as st

from economics.indicators import (
    calculate_engel_coefficient,
    calculate_average_propensity_to_consume,
    calculate_saving_rate,
    calculate_marginal_propensity_to_consume
)


def show_economics(data):

    # 经济学指标分析
    st.divider()
    st.subheader("经济学指标分析")

    engel = calculate_engel_coefficient(data)
    apc = calculate_average_propensity_to_consume(data)
    saving_rate = calculate_saving_rate(data)
    mpc = calculate_marginal_propensity_to_consume(data)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("储蓄率", f"{saving_rate * 100:.2f}%")
    col2.metric("恩格尔系数", f"{engel:.2f}%")
    col3.metric("平均消费倾向（APC）", f"{apc:.2f}")

    if mpc is not None:
        col4.metric("边际消费倾向（MPC）", f"{mpc:.3f}")
    else:
        col4.metric("边际消费倾向（MPC）", "暂无法计算")

    st.caption(
        "恩格尔系数为食品支出占总消费支出的比例；"
        "APC 为总消费支出与总收入之比；"
        "MPC 根据最近两个有数据月份的消费和收入变化计算。"
    )

    with st.expander("查看经济学指标说明"):
        st.markdown("""
        - **储蓄率**：收支结余占总收入的比例，反映收入中用于储蓄的部分。计算公式：储蓄率 =（总收入 - 总支出）/ 总收入 × 100%。
        - **恩格尔系数**：食品支出占总消费支出的比例，可用于观察消费结构。
        - **平均消费倾向（APC）**：总消费支出与总收入的比值，反映收入中用于消费的比例。
        - **边际消费倾向（MPC）**：收入变化量中用于增加消费的比例，根据最近两个有数据月份的收入和消费支出变化计算。

        注意：当前指标基于账单记录计算，结果受数据完整性和分类准确性影响。当总收入不大于0时，储蓄率和APC暂返回0。
        """)

    return engel, apc, saving_rate, mpc