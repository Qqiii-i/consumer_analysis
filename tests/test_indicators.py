import pandas as pd
from economics.indicators import (
    calculate_basic_indicators,
    calculate_category_statistics,
    calculate_monthly_expenses,
    calculate_engel_coefficient,
    calculate_average_propensity_to_consume,
    calculate_saving_rate,
    calculate_marginal_propensity_to_consume
)

def test_basic_indicators():
    data = pd.DataFrame({
        "transaction_type": ["收入", "支出", "支出"],
        "amount": [5000, 1000, 500]
    })

    result = calculate_basic_indicators(data)

    assert result["total_income"] == 5000
    assert result["total_expense"] == 1500
    assert result["balance"] == 3500

def test_category_statistics():
    data = pd.DataFrame({
        "transaction_type": ["支出", "支出", "支出", "收入"],
        "category": ["餐饮", "交通", "餐饮", "收入"],
        "amount": [100, 50, 200, 5000]
    })

    result = calculate_category_statistics(data)

    assert result.iloc[0]["category"] == "餐饮"
    assert result.iloc[0]["amount"] == 300
    assert result.iloc[1]["category"] == "交通"

def test_category_statistics_without_expenses():
    data = pd.DataFrame({
        "transaction_type": ["收入"],
        "category": ["收入"],
        "amount": [5000]
    })

    result = calculate_category_statistics(data)

    assert result.empty

def test_monthly_expenses():
    data = pd.DataFrame({
        "transaction_date": [
            "2026-01-03",
            "2026-01-15",
            "2026-02-05"
        ],
        "transaction_type": ["支出", "支出", "支出"],
        "amount": [100, 200, 300]
    })

    result = calculate_monthly_expenses(data)

    assert result["month"].tolist() == [
        "2026-01", "2026-02"
    ]

    assert result["total_expense"].tolist() == [
        300, 300
    ]

def test_engel_coefficient():
    data = pd.DataFrame({
        "transaction_type": ["支出", "支出", "支出", "收入"],
        "category": ["食品", "餐饮", "购物", "收入"],
        "amount": [100, 200, 700, 5000]
    })

    result = calculate_engel_coefficient(data)

    assert result == 10.0

def test_average_propensity_to_consume():
    data = pd.DataFrame({
        "transaction_type": ["收入", "支出", "支出"],
        "amount": [5000, 1000, 1500]
    })

    result = calculate_average_propensity_to_consume(data)

    assert result == 0.5

def test_marginal_propensity_to_consume():
    data = pd.DataFrame({
        "transaction_date": [
            "2026-01-10",
            "2026-01-20",
            "2026-02-10",
            "2026-02-20"
        ],
        "transaction_type": [
            "收入", "支出", "收入", "支出"
        ],
        "amount": [5000, 2657, 5500, 2330]
    })

    result = calculate_marginal_propensity_to_consume(data)

    assert result == -0.654

def test_saving_rate():
    data = pd.DataFrame({
        "transaction_type": ["收入", "支出", "支出"],
        "amount": [5000, 1000, 1500]
    })

    result = calculate_saving_rate(data)

    assert result == 0.5

def test_saving_rate_without_income():
    data = pd.DataFrame({
        "transaction_type": ["支出", "支出"],
        "amount": [1000, 500]
    })

    result = calculate_saving_rate(data)

    assert result == 0.0

def test_saving_rate_when_expense_exceeds_income():
    data = pd.DataFrame({
        "transaction_type": ["收入", "支出"],
        "amount": [3000, 4000]
    })

    result = calculate_saving_rate(data)

    assert result == -1 / 3