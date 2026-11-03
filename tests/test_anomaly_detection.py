
import pandas as pd

from algorithms.anomaly_detection import (
    detect_outliers_iqr,
    detect_outliers_zscore,
    compare_anomaly_detection
)

def test_detect_outliers_iqr():
    data = pd.DataFrame({
        "amount": [10, 12, 13, 14, 15, 16, 18, 1000]
    })

    result = detect_outliers_iqr(data)

    assert len(result) == 1
    assert result.iloc[0]["amount"] == 1000

def test_iqr_with_insufficient_data():
    data = pd.DataFrame({
        "amount": [10, 20, 30]
    })

    result = detect_outliers_iqr(data)

    assert result.empty

def test_iqr_with_identical_amounts():
    data = pd.DataFrame({
        "amount": [20, 20, 20, 20, 20]
    })

    result = detect_outliers_iqr(data)

    assert result.empty

def test_detect_outliers_zscore():
    data = pd.DataFrame({
        "amount": [
            10, 12, 13, 14, 15,
            11, 12, 14, 16, 13,
            15, 17, 12, 14, 13,
            16, 11, 15, 14, 12,
            1000
        ]
    })

    result = detect_outliers_zscore(data)

    assert len(result) == 1
    assert result.iloc[0]["amount"] == 1000

def test_zscore_with_identical_amounts():
    data = pd.DataFrame({
        "amount": [20, 20, 20, 20, 20]
    })

    result = detect_outliers_zscore(data)

    assert result.empty

def test_compare_anomaly_detection():
    data = pd.DataFrame({
        "amount": [10, 12, 13, 14, 15, 16, 18, 1000]
    })

    result = compare_anomaly_detection(data)

    assert "iqr_outlier" in result.columns
    assert "zscore_outlier" in result.columns
    assert "anomaly_methods" in result.columns

    assert result.iloc[-1]["iqr_outlier"]
    assert result.iloc[-1]["anomaly_methods"] == "IQR"
