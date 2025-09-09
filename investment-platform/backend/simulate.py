from flask import Blueprint, render_template, request, flash
import numpy as np

simulate_bp = Blueprint("simulate", __name__)

@simulate_bp.route("/", methods=["GET", "POST"])
def simulate():
    result = None
    labels, dist = [], []

    if request.method == "POST":
        try:
            initial = int(request.form.get("initial", 100000))  # 本金
            years = int(request.form.get("years", 10))          # 年限
            stock = int(request.form.get("stock", 0))
            bond = int(request.form.get("bond", 0))
            etf = int(request.form.get("etf", 0))

            if stock + bond + etf != 100:
                flash("⚠️ 股票、債券、ETF 的比例總和必須等於 100%")
            else:
                # 各資產的期望報酬與風險
                returns = {
                    "stock": (0.08, 0.15),
                    "bond": (0.03, 0.05),
                    "etf": (0.06, 0.10)
                }

                # 加權期望報酬與風險
                expected_return = (
                    stock/100 * returns["stock"][0] +
                    bond/100 * returns["bond"][0] +
                    etf/100 * returns["etf"][0]
                )
                risk = (
                    stock/100 * returns["stock"][1] +
                    bond/100 * returns["bond"][1] +
                    etf/100 * returns["etf"][1]
                )

                # Monte Carlo 模擬
                sims = 5000
                results = []
                for _ in range(sims):
                    growth = 1
                    for _ in range(years):
                        annual = np.random.normal(expected_return, risk)
                        growth *= (1 + annual)
                    results.append(initial * growth)

                results = np.array(results)

                # 統計值
                mean_value = np.mean(results)
                percentile_10 = np.percentile(results, 10)
                percentile_90 = np.percentile(results, 90)

                # 直方圖資料
                hist, bin_edges = np.histogram(results, bins=30)
                labels = [f"新台幣 {int(edge):,}" for edge in bin_edges[:-1]]
                dist = hist.tolist()

                # 傳到前端的字典
                result = {
                    "initial": initial,
                    "years": years,
                    "stock": stock,
                    "bond": bond,
                    "etf": etf,
                    "expected_return": round(expected_return * 100, 2),
                    "risk": round(risk * 100, 2),
                    "mean_value": round(mean_value, 2),
                    "percentile_10": round(percentile_10, 2),
                    "percentile_90": round(percentile_90, 2)
                }

        except ValueError:
            flash("⚠️ 請輸入正確的數值！")

    return render_template("simulate.html", result=result, labels=labels, values=dist)
