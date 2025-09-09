from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, User, bcrypt
from simulate import simulate_bp  # 投資模擬工具 blueprint

# ========== 開關設定 ==========
USE_LOGIN = False

if USE_LOGIN:
    from flask_login import (
        LoginManager, login_user, login_required,
        logout_user, current_user
    )

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化
db.init_app(app)
bcrypt.init_app(app)

# 登入初始化
if USE_LOGIN:
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

# ========== 註冊 Blueprint ==========
app.register_blueprint(simulate_bp, url_prefix="/simulate")

# ========== 基本路由 ==========
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    if USE_LOGIN:
        return render_template("home.html", user=current_user)
    return render_template("home.html")

@app.route("/map")
def map():
    if USE_LOGIN:
        return render_template("map.html", user=current_user)
    return render_template("map.html")

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    topics = {
        1: "金融市場全貌",
        2: "股票基礎入門",
        3: "股票分析與策略",
        4: "債券基礎入門",
        5: "債券風險與評級",
        6: "ETF 入門",
        7: "資產配置基礎",
        8: "動態資產配置與市場變化",
        9: "期末成果驗收"
    }
    title = topics.get(topic_id, "未知主題")

    # 🚩 Week6 改成直接跳 week6.html
    if topic_id == 6:
        return render_template("week6.html", title=title)

    return render_template("topic.html", topic_id=topic_id, title=title)

# ========== 第九週心理測驗 ==========
@app.route("/topic/9/test", methods=["GET", "POST"])
def topic9_test():
    if request.method == "GET":
        return render_template("week9.html")

    # ✅ 只取數字答案 (q1~q10)，避免 ValueError
    answers = {k: v for k, v in request.form.items() if k.startswith("q")}
    scores = [int(v) for v in answers.values()]
    score = sum(scores)

    # ✅ 文字答案 (a1~a10) 用來顯示回顧
    review_answers = {k: v for k, v in request.form.items() if k.startswith("a")}

    # 題目字典
    questions = {
        1: "🌩️ 暴風雨來襲！市場暴跌 20%，你會怎麼辦？",
        2: "🎯 這趟冒險，你的首要目標是？",
        3: "🗡️ 好友遞給你『高風險神器』，你會？",
        4: "🏴‍☠️ 你遇到海盜要求合作，你會？",
        5: "🤝 你要挑選一位航海伙伴，他是？",
        6: "💰 海上漂浮金幣，你會？",
        7: "⚓ 你的航海經驗像是？",
        8: "🗺️ 海圖上出現未知島嶼，你會？",
        9: "⚖️ 船上資源有限，你會？",
        10: "🔥 旅程最後，你能承受的最大損失是？"
    }

    # 判斷角色與配置
    if score <= 15:
        result = ("🐢 保守型探險者", "偏向安全，適合定存、債券、保守型ETF", "你謹慎小心，重視資產安全。")
        allocation = {"定存/債券": 70, "ETF": 20, "股票": 10}
    elif score <= 30:
        result = ("🦊 平衡型探險者", "股票+債券+ETF均衡配置", "你懂得觀察環境，追求風險與收益平衡。")
        allocation = {"定存/債券": 40, "ETF": 30, "股票": 30}
    elif score <= 45:
        result = ("🦁 積極型探險者", "股票為主，追求長期成長", "你勇於承擔風險，期待高報酬。")
        allocation = {"股票": 70, "ETF": 20, "債券": 10}
    else:
        result = ("🦅 冒險型探險者", "高風險資產為主", "你像老鷹一樣追求高空獵物，承擔巨大風險。")
        allocation = {"股票": 90, "ETF": 10}

    return render_template("week9.html",
                           result=result,
                           allocation=allocation,
                           review_answers=review_answers,
                           questions=questions)

# ========== 主程式 ==========
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
