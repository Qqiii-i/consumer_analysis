import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

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
        "买药", "药品", "诊疗", "校医"
    ],
    "教育": [
        "教材", "学费", "课程", "培训", "学习", "书店",
        "考试", "报名费", "打印", "团费", "教育"
    ],
    "交通": [
        "滴滴", "地铁", "公交", "打车", "出行",
        "火车票", "高铁票", "机票", "出租车",
        "停车费", "加油", "充电费", "中铁网络", "哈啰",
        "小马智行", "骑安", "共享单车"
    ],
    "餐饮": [
        "美团外卖", "饿了么", "麦当劳", "肯德基", "火锅", "馄饨",
        "星巴克", "瑞幸", "早餐", "午餐", "晚餐", "饭堂",
        "夜宵", "吃饭", "餐饮", "外卖", "奶茶", "肠粉",
        "咖啡", "饭店", "餐厅", "点餐", "luckin coffee", "古茗",
        "探鱼", "蜜雪冰城", "三号椰", "食堂", "七號糖", "野人先生",
        "喜茶", "茶百道", "奈雪的茶", "烧烤", "烤肉", "烤鱼", "烤串",
        "烧烤店", "火锅店", "自助餐", "酸菜鱼", "牛肉面", "拉面",
        "米线", "炒饭", "炒面", "盖浇饭", "煲仔饭", "焗外人", "潮蹄"
    ],
    "娱乐": [
        "腾讯视频", "爱奇艺", "优酷", "电影票", "SPA",
        "电影院", "会员", "游戏", "演唱会",
        "旅游", "门票", "KTV", "游泳", "免押租借充电宝"
    ],
    "食品": [
        "食品", "超市", "便利店", "买菜", "西亚兴安", "华润万家", "沃尔玛", "家乐福",
        "水果", "蔬菜", "零食", "生鲜",
        "ELEVEN 7", "先购后付", "罗森", "美天惠"
    ],
    "购物": [
        "京东", "淘宝", "天猫", "拼多多", "小红书",
        "购买衣服", "衣服", "服装", "运动鞋",
        "鞋子", "耳机", "手机", "数码",
        "商城", "网购", "购物", "购买",
        "名创优品", "无印良品MUJI",
    ]
}

def train_nb_classifier(data):
    """
    使用 TF-IDF 和朴素贝叶斯训练消费分类模型。
    """
    train_data = data[
        (data["transaction_type"] == "支出")
        & data["description"].notna()
        & data["category"].notna()
        & (~data["category"].isin(["未分类", ""]))
    ].copy()

    train_data["description"] = (
        train_data["description"].astype(str)
    )

    if len(train_data) < 10:
        return None, None, None

    if train_data["category"].nunique() < 2:
        return None, None, None

    X_train, X_test, y_train, y_test = train_test_split(
        train_data["description"],
        train_data["category"],
        test_size=0.2,
        random_state=42,
    )

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(1, 2)
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)

    return model, vectorizer, accuracy

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
    使用 TF-IDF 和朴素贝叶斯进行批量消费分类。
    """
    result = data.copy()

    # 先使用关键词方法进行基础分类
    result["predicted_category"] = (
        result["description"].apply(classify_transaction)
    )

    # 训练朴素贝叶斯模型
    model, vectorizer, accuracy = train_nb_classifier(data)

    if model is not None:
        expense_mask = result["transaction_type"] == "支出"

        descriptions = (
            result.loc[expense_mask, "description"]
            .fillna("")
            .astype(str)
        )

        features = vectorizer.transform(descriptions)

        result.loc[expense_mask, "predicted_category"] = (
            model.predict(features)
        )

    result.attrs["model_accuracy"] = accuracy

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