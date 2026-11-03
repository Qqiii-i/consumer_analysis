import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 消费类别及对应关键词
CATEGORY_KEYWORDS = {
    "收入": [
        "工资", "薪资", "奖金", "收入", "补贴", "报销"
    ],
    "住房": [
        "房租", "物业费", "水电费", "电费", "水费",
        "燃气费", "宽带费", "物业"
    ],
    "医疗": [
        "医院", "药店", "挂号", "看病", "医疗",
        "买药", "药品", "诊疗"
    ],
    "教育": [
        "教材", "学费", "课程", "培训", "学习",
        "考试", "报名费"
    ],
    "交通": [
        "滴滴", "地铁", "公交", "打车", "出行",
        "火车票", "高铁票", "机票", "出租车",
        "停车费", "加油", "充电费"
    ],
    "餐饮": [
        "美团外卖", "饿了么", "麦当劳", "肯德基",
        "星巴克", "瑞幸", "早餐", "午餐", "晚餐",
        "夜宵", "吃饭", "餐饮", "外卖", "奶茶",
        "咖啡", "饭店", "餐厅"
    ],
    "娱乐": [
        "腾讯视频", "爱奇艺", "优酷", "电影票",
        "电影院", "会员", "游戏", "演唱会",
        "旅游", "门票", "KTV"
    ],
    "食品": [
        "食品", "超市", "便利店", "买菜",
        "水果", "蔬菜", "零食", "生鲜"
    ],
    "购物": [
        "京东", "淘宝", "天猫", "拼多多",
        "购买衣服", "衣服", "服装", "运动鞋",
        "鞋子", "耳机", "手机", "数码",
        "商城", "网购", "购物", "购买"
    ]
}


def classify_transaction(description):
    """
    根据交易描述中的关键词自动判断消费类别。
    """

    # 检查输入是否合法
    if not isinstance(description, str) or not description.strip():
        return "未分类"

    description = description.strip()

    # 遍历关键词进行匹配
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description:
                return category

    return "未分类"

def classify_transactions(data):
    """
    对 DataFrame 中的交易描述进行批量分类。
    """
    result = data.copy()

    result["predicted_category"] = result["description"].apply(
        classify_transaction
    )

    return result

def evaluate_classification(data):
    """
    评价自动消费分类效果。
    """
    y_true = data["category"]
    y_pred = data["predicted_category"]

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(
        y_true, y_pred,
        average="weighted",
        zero_division=0
    )
    recall = recall_score(
        y_true, y_pred,
        average="weighted",
        zero_division=0
    )
    f1 = f1_score(
        y_true, y_pred,
        average="weighted",
        zero_division=0
    )

    print("自动分类算法评价结果")
    print(f"准确率：{accuracy:.3f}")
    print(f"精确率：{precision:.3f}")
    print(f"召回率：{recall:.3f}")
    print(f"F1值：{f1:.3f}")