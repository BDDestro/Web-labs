from flask import Flask, request, session, redirect, url_for, render_template_string
import os
import secrets

app = Flask(__name__)

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

app.secret_key = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32)
)

FLAG = os.environ.get(
    "CTF_FLAG",
    "GMIT{reflected_xss_basic}"
)


# ---------------------------------------------------------
# HTML / CSS / JAVASCRIPT
# ---------------------------------------------------------

PAGE = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Cybersecurity CTF - XSS Basic Test</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }


        body {

            min-height: 100vh;

            background:
                radial-gradient(
                    circle at top,
                    #071a36 0%,
                    #020814 45%,
                    #000000 100%
                );

            color: #eaf7ff;

            font-family:
                "Courier New",
                monospace;

            display: flex;

            align-items: center;

            justify-content: center;

            padding: 30px;
        }


        .container {

            width: 100%;

            max-width: 900px;
        }


        /* -----------------------------
           HEADER
        ----------------------------- */

        .header {

            text-align: center;

            margin-bottom: 30px;
        }


        .badge {

            display: inline-block;

            padding: 7px 16px;

            border: 1px solid #00d9ff;

            color: #00d9ff;

            border-radius: 20px;

            margin-bottom: 15px;

            font-size: 13px;

            letter-spacing: 2px;

            box-shadow:
                0 0 12px
                rgba(0, 217, 255, 0.15);
        }


        h1 {

            font-size:
                clamp(
                    32px,
                    6vw,
                    62px
                );

            color: white;

            text-shadow:
                0 0 10px #008cff,
                0 0 30px #006eff;
        }


        h1 span {

            color: #00d9ff;
        }


        .subtitle {

            color: #78a9c7;

            margin-top: 12px;
        }


        /* -----------------------------
           PANEL
        ----------------------------- */

        .panel {

            background:
                rgba(
                    4,
                    15,
                    31,
                    0.93
                );

            border:
                1px solid
                #0b78a8;

            box-shadow:
                0 0 25px
                rgba(
                    0,
                    174,
                    255,
                    0.15
                ),
                inset
                0 0 30px
                rgba(
                    0,
                    174,
                    255,
                    0.03
                );

            border-radius: 14px;

            overflow: hidden;
        }


        .panel-title {

            background: #061c30;

            border-bottom:
                1px solid
                #0b78a8;

            padding:
                14px 20px;

            color: #00d9ff;
        }


        .content {

            padding: 30px;
        }


        /* -----------------------------
           CHALLENGE DESCRIPTION
        ----------------------------- */

        .challenge-info {

            margin-bottom: 25px;

            line-height: 1.7;

            color: #b9d3e5;
        }


        .challenge-info strong {

            color: #00e5ff;
        }


        /* -----------------------------
           TERMINAL
        ----------------------------- */

        .terminal {

            background: #01060d;

            border:
                1px solid
                #133c59;

            border-radius: 8px;

            padding: 18px;

            margin:
                20px 0;

            color: #3cff8f;

            font-size: 14px;

            line-height: 1.8;
        }


        .terminal .prompt {

            color: #00d9ff;
        }


        /* -----------------------------
           FORM
        ----------------------------- */

        form {

            display: flex;

            gap: 10px;

            margin-top: 20px;
        }


        input {

            flex: 1;

            background: #020a14;

            border:
                1px solid
                #17658c;

            border-radius: 7px;

            padding: 14px;

            color: white;

            outline: none;

            font-family: inherit;
        }


        input:focus {

            border-color: #00d9ff;

            box-shadow:
                0 0 10px
                rgba(
                    0,
                    217,
                    255,
                    0.25
                );
        }


        button {

            background:
                linear-gradient(
                    135deg,
                    #0077ff,
                    #00c8ff
                );

            color: white;

            border: none;

            border-radius: 7px;

            padding:
                13px 22px;

            font-weight: bold;

            cursor: pointer;
        }


        button:hover {

            filter:
                brightness(1.15);
        }


        /* -----------------------------
           SERVER RESPONSE
        ----------------------------- */

        .output {

            margin-top: 25px;

            background: #010811;

            border-left:
                3px solid
                #00d9ff;

            padding: 18px;

            min-height: 60px;
        }


        .output-title {

            color: #6e96ad;

            font-size: 12px;

            margin-bottom: 8px;
        }


        /* -----------------------------
           FLAG
        ----------------------------- */

        .flag {

            margin-top: 25px;

            padding: 20px;

            background:
                rgba(
                    0,
                    255,
                    135,
                    0.08
                );

            border:
                1px solid
                #00ff88;

            border-radius: 8px;

            color: #52ffab;

            text-align: center;

            box-shadow:
                0 0 20px
                rgba(
                    0,
                    255,
                    136,
                    0.08
                );
        }


        .flag strong {

            display: block;

            margin-top: 10px;

            color: white;

            font-size: 19px;
        }


        .reset-button {

            display: inline-block;

            margin-top: 18px;

            padding: 11px 18px;

            background:
                linear-gradient(
                    135deg,
                    #ff3b5c,
                    #ff6b35
                );

            color: white;

            text-decoration: none;

            border:
                1px solid
                #ff7a7a;

            border-radius: 7px;

            font-family: inherit;

            font-weight: bold;

            letter-spacing: 0.5px;

            box-shadow:
                0 0 16px
                rgba(
                    255,
                    70,
                    90,
                    0.22
                );

            transition:
                transform 0.2s ease,
                filter 0.2s ease,
                box-shadow 0.2s ease;
        }


        .reset-button:hover {

            filter: brightness(1.15);

            transform: translateY(-1px);

            box-shadow:
                0 0 22px
                rgba(
                    255,
                    70,
                    90,
                    0.35
                );
        }


        /* -----------------------------
           HINT
        ----------------------------- */

        .hint {

            margin-top: 25px;

            color: #60869c;

            font-size: 13px;

            line-height: 1.7;
        }


        code {

            color: #00d9ff;
        }


        /* -----------------------------
           FOOTER
        ----------------------------- */

        .footer {

            text-align: center;

            margin-top: 20px;

            color: #35536a;

            font-size: 12px;
        }


        /* -----------------------------
           MOBILE
        ----------------------------- */

        @media(max-width: 600px) {

            body {
                padding: 15px;
            }

            .content {
                padding: 20px;
            }

            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }

    </style>


    <script>

        /*
        -------------------------------------------------------
        CTF SOLVE DETECTOR

        For this beginner lab, successful use of alert()
        records the challenge as solved.

        The player's injected JavaScript runs inside this page,
        and overriding alert allows us to tell Flask that the
        XSS payload executed.
        -------------------------------------------------------
        */

        const originalAlert = window.alert;


        window.alert = function(message) {

            fetch(
                "/xss-solved",
                {
                    method: "POST",
                    credentials: "same-origin"
                }
            )

            .then(() => {

                originalAlert(message);

                setTimeout(() => {

                    window.location.href = "/";

                }, 300);

            })

            .catch(() => {

                originalAlert(message);

            });

        };

    </script>

</head>


<body>


<div class="container">


    <!-- HEADER -->

    <div class="header">

        <div class="badge">

            BEGINNER SECURITY LAB

        </div>


        <h1>

            &lt;

            <span>
                CTF
            </span>

            /&gt;

        </h1>


        <p class="subtitle">

            Cybersecurity CTF • XSS Basic Test

        </p>

    </div>



    <!-- MAIN PANEL -->

    <div class="panel">


        <div class="panel-title">

            root@ctf:~/challenges/xss-basic

        </div>


        <div class="content">


            <!-- DESCRIPTION -->

            <div class="challenge-info">

                <strong>
                    Challenge:
                </strong>

                Reflected Cross-Site Scripting

                <br><br>


                This application prints your supplied username
                directly back onto the page.

                <br><br>


                Your objective is to discover whether the input
                is properly sanitized and make the browser execute
                JavaScript.

                <br><br>


                <strong>
                    Goal:
                </strong>

                Execute JavaScript and capture the flag.

            </div>



            <!-- TERMINAL STATUS -->

            <div class="terminal">

                <span class="prompt">
                    $
                </span>

                challenge --status

                <br>


                [+] Target:
                Reflected XSS

                <br>


                [+] Difficulty:
                Easy

                <br>


                [+] Input sanitization:
                ???

                <br>


                [+] Flag status:

                {% if solved %}

                    CAPTURED

                {% else %}

                    LOCKED

                {% endif %}

            </div>



            <!-- INPUT -->

            <form
                method="GET"
                action="/"
            >

                <input
                    type="text"
                    name="name"
                    placeholder="Enter your username..."
                    autocomplete="off"
                >


                <button
                    type="submit"
                >

                    Submit

                </button>

            </form>



            <!-- VULNERABLE OUTPUT -->

            {% if name %}

                <div class="output">

                    <div class="output-title">

                        SERVER RESPONSE

                    </div>


                    Welcome,


                    <!--

                    ----------------------------------------
                    INTENTIONALLY VULNERABLE CTF CODE
                    ----------------------------------------

                    Normally Jinja escapes HTML automatically.

                    Using:

                        {{ name|safe }}

                    disables escaping.

                    This allows HTML/JavaScript supplied by
                    the user to be interpreted by the browser.

                    DO NOT use this pattern in real apps.

                    -->


                    {{ name|safe }}

                </div>

            {% endif %}



            <!-- FLAG -->

            {% if solved %}

                <div class="flag">

                    ✓ FLAG CAPTURED


                    <strong>

                        {{ flag }}

                    </strong>


                    <a
                        href="/reset"
                        class="reset-button"
                    >

                        🔄 RESET LAB

                    </a>

                </div>

            {% endif %}



            <!-- HINT -->

            <div class="hint">

                💡 Hint:

                The application reflects your input directly
                into the HTML response.

                Check whether characters such as

                <code>
                    &lt;
                </code>

                and

                <code>
                    &gt;
                </code>

                are escaped.

            </div>


        </div>

    </div>



    <div class="footer">

        Cybersecurity CTF Basic Test •
        Authorized Training Environment

    </div>


</div>


</body>

</html>
"""


# ---------------------------------------------------------
# ROOT PATH
# ---------------------------------------------------------

@app.route("/", methods=["GET"])
def index():

    name = request.args.get(
        "name",
        ""
    )

    solved = session.get(
        "xss_solved",
        False
    )

    return render_template_string(
        PAGE,
        name=name,
        solved=solved,
        flag=FLAG
    )


# ---------------------------------------------------------
# XSS SUCCESS ENDPOINT
# ---------------------------------------------------------

@app.route(
    "/xss-solved",
    methods=["POST"]
)
def xss_solved():

    session["xss_solved"] = True

    return {
        "status": "success",
        "message": "XSS challenge solved"
    }, 200


# ---------------------------------------------------------
# RESET CHALLENGE
# ---------------------------------------------------------

@app.route("/reset")
def reset():

    session.clear()

    return redirect(
        url_for("index")
    )


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.route("/health")
def health():

    return {

        "status": "ok",

        "service":
            "ctf-xss-basic"

    }, 200


# ---------------------------------------------------------
# 404
# ---------------------------------------------------------

@app.errorhandler(404)
def not_found(error):

    return {

        "error": "Not Found",

        "root_path": "/",

        "challenge":
            "Cybersecurity CTF - XSS Basic"

    }, 404


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 60)
    print(" CYBERSECURITY CTF - XSS BASIC TEST")
    print("=" * 60)

    print()
    print("Root path:")
    print("  /")

    print()
    print("Routes:")
    print("  /             -> XSS Challenge")
    print("  /reset        -> Reset Challenge")
    print("  /health       -> Health Check")
    print("  /xss-solved   -> Solve Endpoint")

    print()
    print("Listening:")
    print("  0.0.0.0:5000")

    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )