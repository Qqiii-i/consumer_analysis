import pandas as pd
from algorithms.classifier import classify_transactions
from algorithms.classifier import classify_transaction


def test_food_classification():
    assert classify_transaction("美团外卖") == "餐饮"


def test_transport_classification():
    assert classify_transaction("滴滴出行") == "交通"


def test_shopping_classification():
    assert classify_transaction("京东商城") == "购物"


def test_entertainment_classification():
    assert classify_transaction("腾讯视频会员") == "娱乐"


def test_empty_description():
    assert classify_transaction("") == "未分类"


def test_unknown_description():
    assert classify_transaction("未知交易内容") == "未分类"


def test_non_string_description():
    assert classify_transaction(None) == "未分类"

def test_description_with_spaces():
    assert classify_transaction("  美团外卖  ") == "餐饮"


def test_keyword_inside_description():
    assert classify_transaction("在京东商城购买耳机") == "购物"

def test_batch_classification():
    data = pd.DataFrame({
        "description": ["美团外卖", "滴滴出行", "工资收入"]
    })

    result = classify_transactions(data)

    assert result["predicted_category"].tolist() == [
        "餐饮", "交通", "收入"
    ]

    # 确认原始数据没有被修改
    assert "predicted_category" not in data.columns