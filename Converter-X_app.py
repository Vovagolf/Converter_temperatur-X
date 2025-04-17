from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)
history = []

html_template = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Конвертер температури</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            width: 350px;
        }

        h2 {
            text-align: center;
            color: #333;
        }

        label {
            font-weight: bold;
        }

        input, select, button {
            width: 100%;
            padding: 10px;
            margin-top: 8px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
        }

        button {
            background-color: #3498db;
            color: white;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background-color: #2980b9;
        }

        .history {
            margin-top: 20px;
            background: #f9f9f9;
            padding: 10px;
            border-radius: 6px;
            max-height: 150px;
            overflow-y: auto;
        }

        .result {
            font-size: 1.1em;
            text-align: center;
            margin-top: 10px;
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Конвертер температури</h2>
        <form method="POST">
            <label>Значення / Value:</label>
            <input type="number" step="any" name="value">

            <label>Тип конвертації / Conversion type:</label>
            <select name="type">
                <option value="C">Цельсій → Фаренгейт</option>
                <option value="F">Фаренгейт → Цельсій</option>
            </select>

            <button type="submit" name="action" value="convert">Конвертувати</button>
            <button type="submit" name="action" value="clear">Очистити історію</button>
        </form>

        {% if result %}
            <div class="result">{{ result }}</div>
        {% endif %}

        {% if history %}
            <div class="history">
                <strong>Історія:</strong>
                <ul>
                {% for entry in history %}
                    <li>{{ entry }}</li>
                {% endfor %}
                </ul>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def convert():
    result = None
    global history

    if request.method == "POST":
        if request.form["action"] == "clear":
            history = []
            return redirect(url_for('convert'))

        if request.form["action"] == "convert":
            try:
                value_raw = request.form.get("value", "").strip()
                temp_type = request.form.get("type", "")

                if not value_raw:
                    raise ValueError("Значення не введено.")

                value = float(value_raw)

                if temp_type not in ["C", "F"]:
                    raise ValueError("Невідомий тип температури.")

                if temp_type == "C":
                    converted = value * 9 / 5 + 32
                    result = f"{value}°C = {converted:.2f}°F"
                else:
                    converted = (value - 32) * 5 / 9
                    result = f"{value}°F = {converted:.2f}°C"

                history.append(result)

            except ValueError as e:
                result = f"Помилка: {e}"

    return render_template_string(html_template, result=result, history=history)

if __name__ == "__main__":
    app.run(debug=True)