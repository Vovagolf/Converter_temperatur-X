from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
history = []

@app.route("/", methods=["GET", "POST"])
def convert():
    global history
    result = None

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

    return render_template("index.html", result=result, history=history)

if __name__ == "__main__":
    app.run(debug=True)