from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Correct login credentials
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "1234"

# Track failed login attempts
failed_attempts = 0

# Maximum allowed failed attempts
MAX_ATTEMPTS = 3


@app.route("/", methods=["GET", "POST"])
def login():

    global failed_attempts

    message = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Check whether account is already blocked
        if failed_attempts >= MAX_ATTEMPTS:
            message = "Suspicious activity detected! Account is temporarily blocked."
            return render_template("login.html", message=message)

        # Check login credentials
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:

            # Reset failed attempts after successful login
            failed_attempts = 0

            # Redirect user to dashboard
            return redirect(url_for("dashboard"))

        else:

            # Increase failed attempt counter
            failed_attempts += 1

            if failed_attempts >= MAX_ATTEMPTS:

                message = "Suspicious activity detected! Account is blocked."

            else:

                remaining = MAX_ATTEMPTS - failed_attempts

                message = (
                    f"Invalid username or password. "
                    f"{remaining} attempt(s) remaining."
                )

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


@app.route("/logout")
def logout():

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)