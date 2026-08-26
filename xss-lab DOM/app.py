from flask import Flask, request, session, redirect, url_for, render_template_string
import os
import secrets

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32)
)

FLAG = os.environ.get(
    "CTF_FLAG",
    "GMIT{dom_xss_mastered}"
)


PAGE = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>DOM XSS Lab</title>

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background:
                radial-gradient(circle at top, #071a36, #020814 50%, #000);
            color: #eaf7ff;
            font-family: "Courier New", monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 25px;
        }

        .container {
            width: 100%;
            max-width: 900px;
        }

        .header {
            text-align: center;
            margin-bottom: 25px;
        }

        .badge {
            display: inline-block;
            padding: 7px 15px;
            border: 1px solid #00d9ff;
            border-radius: 20px;
            color: #00d9ff;
            letter-spacing: 2px;
            font-size: 12px;
        }

        h1 {
            color: white;
            font-size: 48px;
            margin-bottom: 5px;
            text-shadow:
                0 0 10px #008cff,
                0 0 25px #006eff;
        }

        h1 span {
            color: #00d9ff;
        }

        .subtitle {
            color: #739eb8;
        }

        .panel {
            border: 1px solid #0b78a8;
            background: rgba(4, 15, 31, 0.96);
            border-radius: 12px;
            overflow: hidden;

            box-shadow:
                0 0 25px rgba(0, 174, 255, 0.15);
        }

        .panel-header {
            background: #061c30;
            padding: 14px 20px;
            border-bottom: 1px solid #0b78a8;
            color: #00d9ff;
        }

        .content {
            padding: 30px;
        }

        .description {
            color: #bad5e6;
            line-height: 1.7;
        }

        .description strong {
            color: #00e5ff;
        }

        .terminal {
            background: #01060d;
            border: 1px solid #133c59;
            border-radius: 8px;
            padding: 18px;
            margin: 22px 0;
            line-height: 1.8;
            color: #3cff8f;
        }

        .prompt {
            color: #00d9ff;
        }

        input {
            width: 100%;
            padding: 15px;
            background: #020a14;
            border: 1px solid #17658c;
            border-radius: 7px;
            color: white;
            outline: none;
            font-family: inherit;
        }

        input:focus {
            border-color: #00d9ff;
            box-shadow: 0 0 10px rgba(0,217,255,.25);
        }

        button {
            width: 100%;
            margin-top: 10px;
            padding: 14px;

            border: none;
            border-radius: 7px;

            background:
                linear-gradient(
                    135deg,
                    #0077ff,
                    #00c8ff
                );

            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            filter: brightness(1.15);
        }

        .preview {
            margin-top: 25px;
            padding: 20px;

            background: #010811;

            border-left:
                3px solid #00d9ff;

            min-height: 70px;
        }

        .preview-title {
            color: #5f8aa5;
            font-size: 12px;
            margin-bottom: 10px;
        }

        .hint {
            margin-top: 25px;
            font-size: 13px;
            color: #5c8199;
            line-height: 1.7;
        }

        code {
            color: #00d9ff;
        }

        .flag {
            margin-top: 25px;

            background:
                rgba(0, 255, 136, 0.08);

            border:
                1px solid #00ff88;

            border-radius: 8px;

            padding: 20px;

            text-align: center;

            color: #52ffab;
        }

        .flag strong {
            display: block;
            margin-top: 10px;
            color: white;
            font-size: 18px;
        }

        .reset-button {
            display: inline-block;
            margin-top: 18px;
            padding: 12px 20px;

            background:
                linear-gradient(
                    135deg,
                    #ff3b3b,
                    #c62828
                );

            color: white;
            text-decoration: none;
            border-radius: 7px;
            font-weight: bold;

            transition:
                transform 0.2s ease,
                filter 0.2s ease,
                box-shadow 0.2s ease;

            box-shadow:
                0 0 14px
                rgba(255, 59, 59, 0.18);
        }

        .reset-button:hover {
            filter: brightness(1.12);
            transform: translateY(-1px);
            box-shadow:
                0 0 20px
                rgba(255, 59, 59, 0.28);
        }

        .footer {
            text-align: center;
            margin-top: 18px;
            color: #36566c;
            font-size: 12px;
        }

    </style>

</head>


<body>


<div class="container">


    <div class="header">

        <div class="badge">
            WEB SECURITY LAB
        </div>

        <h1>
            DOM <span>XSS</span>
        </h1>

        <div class="subtitle">
            Beginner Capture The Flag Challenge
        </div>

    </div>



    <div class="panel">

        <div class="panel-header">

            root@ctf:~/challenges/dom-xss

        </div>


        <div class="content">


            <div class="description">

                <strong>Challenge:</strong>
                DOM-Based Cross-Site Scripting

                <br><br>

                This page reads information from the URL fragment

                <code>#</code>

                and displays it inside the page.

                <br><br>

                Your job is to determine whether the browser
                handles that data safely.

                <br><br>

                <strong>Objective:</strong>

                Execute JavaScript through the vulnerable DOM
                operation and capture the flag.

            </div>



            <div class="terminal">

                <span class="prompt">$</span>
                challenge --status

                <br>

                [+] Vulnerability: DOM XSS

                <br>

                [+] Difficulty: Beginner

                <br>

                [+] Source: location.hash

                <br>

                [+] Sink: ???

                <br>

                [+] Flag:

                {% if solved %}

                    CAPTURED

                {% else %}

                    LOCKED

                {% endif %}

            </div>



            <input
                id="message"
                type="text"
                placeholder="Enter a message..."
                autocomplete="off"
            >


            <button onclick="updateHash()">

                Preview Message

            </button>



            <div class="preview">

                <div class="preview-title">

                    LIVE MESSAGE PREVIEW

                </div>


                <div id="output">

                    No message supplied.

                </div>

            </div>



            {% if solved %}

                <div class="flag">

                    ✓ DOM XSS CHALLENGE SOLVED

                    <strong>

                        {{ flag }}

                    </strong>

                    <a
                        class="reset-button"
                        href="{{ url_for('reset') }}"
                    >
                        🔄 RESET LAB
                    </a>

                </div>

            {% endif %}



            <div class="hint">

                💡 Hint #1:

                Look at what happens to

                <code>location.hash</code>.

                <br>

                💡 Hint #2:

                Some DOM functions interpret text as HTML.

            </div>


        </div>

    </div>


    <div class="footer">

        Cybersecurity CTF Basic Test •
        Authorized Training Environment

    </div>


</div>



<script>

/*
=================================================
DOM XSS VULNERABILITY
=================================================

SOURCE:
    window.location.hash

SINK:
    element.innerHTML

The browser reads attacker-controlled data from
the URL and inserts it directly into the DOM.

This is intentionally vulnerable for the CTF.
=================================================
*/


function updateHash() {

    const value =
        document.getElementById("message").value;

    window.location.hash =
        encodeURIComponent(value);

}


/*
Read data from the URL fragment.

Example:

    http://localhost:5000/#hello

*/


function loadMessage() {

    if (!window.location.hash) {
        return;
    }


    const message =
        decodeURIComponent(
            window.location.hash.substring(1)
        );


    /*
    =============================================
    INTENTIONALLY VULNERABLE LINE
    =============================================
    */

    document.getElementById("output").innerHTML =
        message;

}


/*
=================================================
CTF SUCCESS DETECTOR
=================================================

When an injected payload executes alert("DOMXSS"),
we mark the challenge solved.
*/


const realAlert = window.alert;


window.alert = function(message) {

    if (String(message) === "DOMXSS") {

        fetch(
            "/dom-solved",
            {
                method: "POST",
                credentials: "same-origin"
            }
        )

        .then(() => {

            realAlert(message);

            window.location.href = "/";

        });

    }

    else {

        realAlert(message);

    }

};


window.addEventListener(
    "hashchange",
    loadMessage
);


window.addEventListener(
    "DOMContentLoaded",
    loadMessage
);


</script>


</body>

</html>
"""


# =========================================================
# ROOT CHALLENGE
# =========================================================

@app.route("/")
def index():

    solved = session.get(
        "dom_xss_solved",
        False
    )

    return render_template_string(
        PAGE,
        solved=solved,
        flag=FLAG
    )


# =========================================================
# SOLVE ENDPOINT
# =========================================================

@app.route(
    "/dom-solved",
    methods=["POST"]
)
def dom_solved():

    session["dom_xss_solved"] = True

    return {
        "status": "solved"
    }, 200


# =========================================================
# RESET
# =========================================================

@app.route("/reset")
def reset():

    session.clear()

    return redirect(
        url_for("index")
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "challenge": "dom-xss"
    }, 200


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print(" DOM XSS CTF LAB")
    print("=" * 55)

    print()
    print("Challenge:")
    print("  http://127.0.0.1:5001/")

    print()
    print("Reset:")
    print("  http://127.0.0.1:5001/reset")

    print()

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )