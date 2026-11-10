import pandas as pd

def detect_outliers_iqr(data, column="amount"):
    # 使用 IQR 四分位距法检测异常消费记录。
    values = pd.to_numeric(data[column], errors="coerce")

    if values.notna().sum() < 4:
        return pd.DataFrame()

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    mask = ((values < lower_bound) | (values > upper_bound))

    return data.loc[mask].copy()


def detect_outliers_zscore(data, column="amount", threshold=3):
    # 使用 Z-score 标准分数法检测异常消费记录。
    values = pd.to_numeric(data[column], errors="coerce")

    valid_values = values.dropna()

    if len(valid_values) < 2:
        return pd.DataFrame()

    mean = valid_values.mean()
    std = valid_values.std()

    if std == 0:
        return pd.DataFrame()

    z_scores = (values - mean) / std

    return data.loc[z_scores.abs() > threshold].copy()

def compare_anomaly_detection(data, column="amount"):
    # 整合 IQR 和 Z-score 的异常检测结果。
    result = data.copy()

    iqr_outliers = detect_outliers_iqr(data, column)
    zscore_outliers = detect_outliers_zscore(data, column)

    result["iqr_outlier"] = result.index.isin(iqr_outliers.index)
    result["zscore_outlier"] = result.index.isin(zscore_outliers.index)

    result["anomaly_methods"] = result.apply(
        lambda row: ", ".join(
            method
            for method, detected in [
                ("IQR", row["iqr_outlier"]),
                ("Z-score", row["zscore_outlier"])
            ]
            if detected
        ) or "Normal",
        axis=1
    )

    return result