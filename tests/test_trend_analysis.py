import pandas as pd
import pytest
from algorithms.trend_analysis import (
    calculate_monthly_trend,
    calculate_moving_average,
    calculate_expense_by_period,
    calculate_expense_frequency
)

def test_calculate_monthly_trend():
    data = pd.DataFrame({
        "transaction_date": [
            "2026-01-05",
            "2026-01-10",
            "2026-02-05",
            "2026-02-10"
        ],
        "transaction_type": [
            "支出", "支出", "支出", "收入"
        ],
        "amount": [100, 200, 300, 500]
    })

    result = calculate_monthly_trend(data)

    assert len(result) == 2
    assert result.loc[0, "month"] == "2026-01"
    assert result.loc[0, "total_expense"] == 300
    assert result.loc[1, "month"] == "2026-02"
    assert result.loc[1, "total_expense"] == 300

def test_calculate_moving_average():
    data = pd.DataFrame({
        "month": ["2026-01", "2026-02", "2026-03"],
        "total_expense": [100, 200, 300]
    })

    result = calculate_moving_average(data, window=2)

    assert pd.isna(result.loc[0, "moving_average"])
    assert result.loc[1, "moving_average"] == 150
    assert result.loc[2, "moving_average"] == 250

def test_moving_average_invalid_window():
    data = pd.DataFrame({
        "total_expense": [100, 200]
    })

    with pytest.raises(ValueError):
        calculate_moving_average(data, window=0)

def test_calculate_expense_by_period():
    data = pd.DataFrame({
        "transaction_date": [
            "2026-01-05",
            "2026-01-05",
            "2026-01-10",
            "2026-02-05",
            "2027-01-05",
            "2027-01-10"
        ],
        "transaction_type": [
            "支出", "支出", "支出", "支出", "收入","支出"
        ],
        "amount": [100, 200, 300, 400, 500, 1000]
    })

    # 日统计
    daily = calculate_expense_by_period(data, "D")
    assert daily.loc[0, "total_expense"] == 300

    # 周统计
    weekly = calculate_expense_by_period(data, "W")
    assert weekly["total_expense"].sum() == 2000

    # 月统计
    monthly = calculate_expense_by_period(data, "M")
    assert monthly.loc[0, "period"] == "2026-01"
    assert monthly.loc[0, "total_expense"] == 600

    # 年统计
    yearly = calculate_expense_by_period(data, "Y")
    assert len(yearly) == 2
    assert yearly.loc[0, "period"] == "2026"
    assert yearly.loc[0, "total_expense"] == 1000
    assert yearly.loc[1, "period"] == "2027"
    assert yearly.loc[1, "total_expense"] == 1000

def test_calculate_expense_frequency():
    data = pd.DataFrame({
        "transaction_date": [
            "2026-01-05",
            "2026-01-05",
            "2026-01-10",
            "2026-02-05",
            "2027-01-05"
        ],
        "transaction_type": [
            "支出", "支出", "支出", "支出", "收入"
        ],
        "amount": [100, 200, 300, 400, 500]
    })

    # 月度消费频率
    result = calculate_expense_frequency(data, "M")

    assert len(result) == 2
    assert result.loc[0, "period"] == "2026-01"
    assert result.loc[0, "transaction_count"] == 3
    assert result.loc[1, "period"] == "2026-02"
    assert result.loc[1, "transaction_count"] == 1

def test_calculate_expense_distribution():
    import pandas as pd
    from algorithms.trend_analysis import calculate_expense_distribution

    data = pd.DataFrame({
        "transaction_type": ["支出", "支出", "支出", "支出", "收入"],
        "transaction_date": [
            "2026-01-05",
            "2026-01-10",
            "2026-01-15",
            "2026-01-20",
            "2026-01-25"
        ],
        "amount": [30, 80, 300, 600, 1000]
    })

    result = calculate_expense_distribution(data)

    assert result["transaction_count"].tolist() == [1, 1, 1, 1]
    assert result["amount_range"].astype(str).tolist() == [
        "0-50元", "50-100元", "100-500元", "500元以上"
    ]
    assert result["period"].tolist() == ["2026-01"] * 4