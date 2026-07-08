from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# =========================
# Загрузка датасета
# =========================
df = pd.read_csv("dataset.csv")
print(df.columns)

df.columns = df.columns.str.strip()
# признаки и цель
X = df.drop("target", axis=1)
y = df["target"]

# обучение модели
model = DecisionTreeClassifier()
model.fit(X, y)

# =========================
# Главная страница
# =========================
@app.route("/")
def start():
    return render_template("start.html")

@app.route("/test")
def test():
    return render_template("index_py.html")
# Предсказание

@app.route("/predict", methods=["POST"])
def predict():

    try:
        fatigue = int(request.form["fatigue"])
        interest = int(request.form["interest"])
        anxiety = int(request.form["anxiety"])
        clarity = int(request.form["clarity"])
        distractions = int(request.form["distractions"])
        resistance = int(request.form["resistance"])
        sleep = int(request.form["sleep"])
        stress = int(request.form["stress"])
        confidence = int(request.form["confidence"])
        perfectionism = int(request.form["perfectionism"])
        meaning = int(request.form["meaning"])
        deadline = int(request.form["deadline"])
    except:
        return "Ошибка ввода данных"
    print("ПРИШЕЛ ЗАПРОС")

    translations = {
        "fatigue": ("Усталость", "Вы перегружены и нуждаетесь в отдыхе."),
        "boredom": ("Скука", "Задача не вызывает интереса."),
        "fear": ("Страх", "Есть тревога перед началом задачи."),
        "distraction": ("Отвлечения", "Вас постоянно отвлекают."),
        "perfectionism": ("Перфекционизм", "Вы боитесь сделать неидеально."),
        "overload": ("Перегрузка", "Слишком много задач сразу."),
        "low_confidence": ("Неуверенность", "Вы сомневаетесь в себе."),
        "no_meaning": ("Нет смысла", "Задача кажется бессмысленной.")
    }

    data = [[
        fatigue, interest, anxiety, clarity, distractions, resistance,
        sleep, stress, confidence, perfectionism, meaning, deadline
    ]]
    print(request.form)


    result = model.predict(data)[0].strip().lower()
    print("MODEL RESULT:", result)

    rus_name, description = translations.get(result, ("Неизвестно", ""))

    return render_template("result.html",
                           result=rus_name,
                           description=description)

# =========================
# Запуск
# =========================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)