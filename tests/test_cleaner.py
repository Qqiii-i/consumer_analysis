
import pandas as pd

from processors.cleaner import (
    clean_transactions,
    check_data_quality,
    remove_invalid_transactions
)


def sample_data():
    return pd.DataFrame({
        "transaction_id": ["001", "002", "002", "004"],
        "transaction_date": [
            "2026-01-01", "2026-01-02",
            "2026-01-02", "invalid"
        ],
        "amount": ["100", "200", "200", "abc"],
        "description": ["早餐", None, "重复记录", "购物"],
        "category": ["餐饮", None, "餐饮", "购物"],
        "payment_method": ["微信", None, "支付宝", "银行卡"]
    })


def test_clean_transactions():
    data = sample_data()
    result = clean_transactions(data)

    assert pd.api.types.is_datetime64_any_dtype(
        result["transaction_date"]
    )
    assert pd.api.types.is_numeric_dtype(result["amount"])
    assert pd.isna(result.loc[3, "transaction_date"])
    assert pd.isna(result.loc[3, "amount"])


def test_check_data_quality():
    data = clean_transactions(sample_data())
    report = check_data_quality(data)

    assert report["duplicate_ids"] == 1
    assert report["invalid_dates"] == 1
    assert report["invalid_amounts"] == 1


def test_remove_invalid_transactions():
    data = clean_transactions(sample_data())
    result = remove_invalid_transactions(data)

    assert len(result) == 2
    assert result["transaction_id"].is_unique
    assert result["description"].notna().all()
    assert result["category"].notna().all()
    assert result["payment_method"].notna().all()


def test_remove_invalid_transactions_fills_missing_values():
    data = clean_transactions(sample_data())
    result = remove_invalid_transactions(data)

    row = result[result["transaction_id"] == "002"].iloc[0]

    assert row["description"] == "未填写"
    assert row["category"] == "未填写"
    assert row["payment_method"] == "未填写"


def test_clean_transactions_does_not_modify_original_data():
    data = sample_data()
    original = data.copy(deep=True)

    clean_transactions(data)

    pd.testing.assert_frame_equal(data, original)
