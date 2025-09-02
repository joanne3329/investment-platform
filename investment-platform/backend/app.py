from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # ⚠️ 正式環境請換成隨機生成的金鑰
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 沒登入會自動導向 login 頁

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 首頁
@app.route("/")
def index():
    return render_template("index.html")

# 主頁 (需要登入)
@app.route("/home")
@login_required
def home():
    return render_template("home.html", user=current_user)

# 學習地圖 (需要登入)
@app.route("/map")
@login_required
def map():
    return render_template("map.html")

# 單一主題頁面
@app.route("/topic/<int:topic_id>")
@login_required
def topic(topic_id):
    # 可以根據 topic_id 來決定要顯示的內容
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
    return render_template("topic.html", topic_id=topic_id, title=title)

# 註冊
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 檢查帳號是否存在
        if User.query.filter_by(username=username).first():
            flash("❌ 帳號已存在！")
            return redirect(url_for('register'))

        # 建立新使用者
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # 註冊後自動登入
        login_user(new_user)
        flash("✅ 註冊成功，已自動登入！")
        return redirect(url_for('home'))

    return render_template("register.html")

# 登入
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"👋 歡迎回來，{username}！")
            return redirect(url_for('home'))
        else:
            flash("❌ 帳號或密碼錯誤！")

    return render_template("login.html")

# 登出
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("🚪 已成功登出！")
    return redirect(url_for('index'))

# 使用者清單 (開發用，正式上線要移除或加權限保護)
@app.route("/users")
@login_required
def users():
    # 這裡只顯示 ID, 帳號, Email
    user_list = User.query.all()
    return render_template("users.html", users=user_list)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
