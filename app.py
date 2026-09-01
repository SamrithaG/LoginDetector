from flask import Flask, render_template, request

app = Flask(__name__)

failed_attempts = 0
blocked = False
login_history = []


@app.route("/", methods=["GET", "POST"])
def login():

    global failed_attempts, blocked

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if blocked:
            message = "🚨 Suspicious Activity Detected! Account Blocked."
            login_history.append(f"{username} → 🚨 Suspicious")

        elif username == "admin" and password == "1234":
            message = "✅ Login Successful!"
            login_history.append(f"{username} → ✅ Successful")
            failed_attempts = 0

        else:
            failed_attempts += 1
            login_history.append(f"{username} → ❌ Failed")

            if failed_attempts >= 3:
                blocked = True
                message = "🚨 Suspicious Activity Detected! Account Blocked."
                login_history.append(f"{username} → 🚨 Suspicious")
            else:
                message = f"❌ Invalid Login! Failed Attempts: {failed_attempts}"

    return render_template(
        "login.html",
        message=message,
        history=login_history
    )


@app.route("/reset")
def reset():

    global failed_attempts, blocked, login_history

    failed_attempts = 0
    blocked = False
    login_history = []

    return "Login Detector has been reset. Go back to the login page."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)