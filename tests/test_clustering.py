
import pandas as pd

from algorithms.clustering import (
    cluster_transactions,
    summarize_clusters
)

def test_cluster_transactions():
    data = pd.DataFrame({
        "transaction_type": [
            "支出", "支出", "支出", "支出",
            "支出", "支出", "收入"
        ],
        "amount": [10, 20, 30, 200, 300, 400, 5000],
        "category": [
            "餐饮", "餐饮", "交通",
            "购物", "购物", "娱乐", "收入"
        ]
    })

    result = cluster_transactions(data, n_clusters=3)

    assert len(result) == 6
    assert "cluster" in result.columns
    assert result["cluster"].nunique() == 3

import pytest


def test_cluster_with_insufficient_data():
    data = pd.DataFrame({
        "transaction_type": ["支出", "支出"],
        "amount": [20, 30],
        "category": ["餐饮", "交通"]
    })

    with pytest.raises(ValueError):
        cluster_transactions(data, n_clusters=3)

def test_summarize_clusters():
    data = pd.DataFrame({
        "cluster": [0, 0, 1, 1],
        "amount": [10, 20, 100, 200]
    })

    result = summarize_clusters(data)

    assert len(result) == 2
    assert result.loc[0, "transaction_count"] == 2
    assert result.loc[0, "average_amount"] == 15
    assert result.loc[0, "total_amount"] == 30