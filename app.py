import os
import html
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app

st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide"
)

# ══════════════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM  —  "Airmail"
#  Ink navy · airmail red · airmail blue · stamp yellow · cool paper
#  Headlines: Bricolage Grotesque   Body: Hanken Grotesk
#  Signature: postage-stamp photos, airmail border, boarding-pass result card
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Hanken+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --ink: #14213d;
    --paper: #f3f6fa;
    --card: #ffffff;
    --red: #d62839;
    --red-dark: #a31d2b;
    --blue: #2c5fc4;
    --sun: #f6b73c;
    --muted: #5b6b82;
    --line: #d3dce8;
    --display: 'Bricolage Grotesque', 'Segoe UI', sans-serif;
    --body: 'Hanken Grotesk', 'Segoe UI', sans-serif;
    --airmail: repeating-linear-gradient(-45deg,
        #d62839 0 12px, #ffffff 12px 24px, #2c5fc4 24px 36px, #ffffff 36px 48px);
}

/* ── Base ─────────────────────────────────────────────────────────────── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: var(--body);
    background: var(--paper) !important;
    color: var(--ink) !important;
}
.stApp::before {                       /* airmail band along the top edge */
    content: "";
    position: fixed; top: 0; left: 0; right: 0; height: 8px;
    background: var(--airmail);
    z-index: 999;
}
.block-container { max-width: 1120px; padding-top: 2.2rem; padding-bottom: 4rem; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }

h1, h2, h3 { font-family: var(--display) !important; color: var(--ink) !important; letter-spacing: -0.02em; }
.stMarkdown p, .stMarkdown li { line-height: 1.7; }
.stMarkdown a { color: var(--blue) !important; }
.stMarkdown code {
    background: #e9eef6 !important; color: var(--ink) !important;
    padding: 0.12em 0.4em; border-radius: 4px;
}

/* ── Hero envelope ────────────────────────────────────────────────────── */
.envelope {
    position: relative;
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    gap: 2rem;
    align-items: center;
    background: #ffffff;
    padding: 2.2rem 2.4rem;
    margin: 0.4rem 0 2.4rem;
    border: 12px solid transparent;
    border-image: repeating-linear-gradient(-45deg,
        #d62839 0 12px, #ffffff 12px 24px, #2c5fc4 24px 36px, #ffffff 36px 48px) 12;
    box-shadow: 0 14px 30px rgba(20,33,61,0.10);
}
.par-avion {
    display: inline-block;
    border: 2px solid var(--blue);
    color: var(--blue);
    font-style: italic;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    padding: 0.2rem 0.7rem;
    border-radius: 3px;
    transform: rotate(-2deg);
    margin-bottom: 1.1rem;
}
.env-title {
    font-family: var(--display);
    font-weight: 800;
    font-size: clamp(2.8rem, 6vw, 4.6rem);
    line-height: 0.95;
    letter-spacing: -0.035em;
    color: var(--ink);
    margin: 0 0 1rem;
}
.env-sub { color: var(--muted); font-size: 1.05rem; line-height: 1.6; max-width: 30rem; margin: 0; }
.env-stamps { position: relative; height: 270px; }
.env-stamps .s-big   { position: absolute; right: 18px; top: 0;    width: 200px; }
.env-stamps .s-small { position: absolute; left: 8px;  bottom: 0;  width: 142px; }

/* ── Postage stamps (the memorable element) ───────────────────────────── */
.stamp-wrap {
    --rot: 0deg;
    transform: rotate(var(--rot));
    filter: drop-shadow(0 2px 0 rgba(20,33,61,0.16)) drop-shadow(0 10px 14px rgba(20,33,61,0.16));
}
.stamp {
    background: #ffffff;
    padding: 10px;
    -webkit-mask: linear-gradient(#000 0 0) content-box,
                  radial-gradient(circle at center, transparent 3px, #000 3.6px) 0 0 / 10px 10px round;
            mask: linear-gradient(#000 0 0) content-box,
                  radial-gradient(circle at center, transparent 3px, #000 3.6px) 0 0 / 10px 10px round;
}
.stamp-img {
    width: 100%;
    background-color: var(--ink);
    background-size: cover;
    background-position: center;
}
.stamp-cap {
    display: flex; justify-content: space-between; align-items: baseline;
    padding: 0.45rem 0.1rem 0.1rem;
}
.stamp-cap b { font-family: var(--display); font-weight: 700; font-size: 1rem; color: var(--ink); }
.stamp-cap i { font-style: normal; font-weight: 700; font-size: 0.78rem; color: var(--red); }

.postmark {
    position: absolute; right: -4px; bottom: 14px;
    width: 104px; height: 104px;
    border: 3px solid rgba(20,33,61,0.6);
    border-radius: 50%;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    color: rgba(20,33,61,0.7);
    font-family: var(--display);
    transform: rotate(-14deg);
    background: repeating-linear-gradient(0deg, transparent 0 9px, rgba(20,33,61,0.0) 9px 10px);
}
.postmark::after {
    content: ""; position: absolute; inset: 7px;
    border: 1.5px solid rgba(20,33,61,0.45); border-radius: 50%;
}
.postmark b  { font-size: 1.7rem; line-height: 1; font-weight: 800; }
.postmark small { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.06em; }

/* one-time entrance: stamps land on the envelope */
@keyframes stampIn {
    from { opacity: 0; transform: scale(1.3) rotate(var(--rot)); }
    to   { opacity: 1; transform: scale(1)   rotate(var(--rot)); }
}
.envelope .stamp-wrap { animation: stampIn 0.45s cubic-bezier(.2,.9,.3,1.2) both; }
.envelope .s-small    { animation-delay: 0.18s; }
@media (prefers-reduced-motion: reduce) { .envelope .stamp-wrap { animation: none; } }

@media (max-width: 760px) {
    .envelope { grid-template-columns: 1fr; padding: 1.5rem 1.3rem; }
    .env-stamps { height: 230px; }
}

/* ── Section headings ─────────────────────────────────────────────────── */
.sec-head { margin: 2.2rem 0 1rem; }
.sec-head h2 { font-size: 1.7rem; font-weight: 800; margin: 0; padding: 0; }
.sec-head p  { color: var(--muted); margin: 0.2rem 0 0; font-size: 0.97rem; }

/* ── Buttons ──────────────────────────────────────────────────────────── */
div[data-testid="stButton"] > button,
div[data-testid="stDownloadButton"] > button {
    font-family: var(--body) !important;
    font-weight: 600 !important;
    background: #ffffff !important;
    color: var(--ink) !important;
    border: 1.5px solid var(--ink) !important;
    border-radius: 999px !important;
    padding: 0.35rem 0.9rem !important;
    transition: background 0.15s ease, transform 0.15s ease !important;
}
div[data-testid="stButton"] > button *,
div[data-testid="stDownloadButton"] > button * { color: inherit !important; }
div[data-testid="stButton"] > button:hover {
    background: var(--sun) !important;
    border-color: var(--ink) !important;
}
div[data-testid="stButton"] > button:focus-visible,
div[data-testid="stDownloadButton"] > button:focus-visible {
    outline: 3px solid var(--blue) !important; outline-offset: 2px !important;
}

/* primary action: stamped-red with a hard press shadow */
div[data-testid="stButton"] > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: var(--red) !important;
    color: #ffffff !important;
    border: 2px solid var(--ink) !important;
    border-radius: 12px !important;
    padding: 0.8rem 2rem !important;
    font-family: var(--display) !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    box-shadow: 0 5px 0 var(--ink) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background: #e23547 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 0 var(--ink) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:active,
button[data-testid="stBaseButton-primary"]:active {
    transform: translateY(4px);
    box-shadow: 0 1px 0 var(--ink) !important;
}

div[data-testid="stDownloadButton"] > button {
    background: var(--ink) !important; color: #ffffff !important;
    border-radius: 10px !important; padding: 0.6rem 1rem !important;
}

/* ── Request field: ruled postcard paper ──────────────────────────────── */
.stTextArea [data-baseweb="textarea"],
.stTextArea [data-baseweb="textarea"] > div,
.stTextArea [data-baseweb="base-input"],
.stTextArea [data-testid="stTextAreaRootElement"] {
    background: #fffdf8 !important;
    background-color: #fffdf8 !important;
    border-radius: 10px !important;
}
.stTextArea [data-baseweb="textarea"] {
    border: 2px solid var(--ink) !important;
}
.stTextArea [data-baseweb="textarea"] > div,
.stTextArea [data-baseweb="base-input"] { border: none !important; }
.stTextArea textarea {
    font-family: var(--body) !important;
    font-size: 1.08rem !important;
    line-height: 2rem !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    padding: 0.5rem 1.1rem !important;
    background-color: #fffdf8 !important;
    caret-color: var(--red) !important;
    background-image: repeating-linear-gradient(
        transparent 0, transparent calc(2rem - 1px), #d6deea calc(2rem - 1px), #d6deea 2rem) !important;
    background-attachment: local !important;
    background-position: 0 0.5rem !important;
    resize: none !important;
}
.stTextArea textarea::placeholder { color: #8a99ae !important; -webkit-text-fill-color: #8a99ae !important; }
.stTextArea [data-baseweb="textarea"]:focus-within { border-color: var(--blue) !important; box-shadow: 0 0 0 3px rgba(44,95,196,0.2) !important; }

/* ── Agent reports (st.status) → dashed coupon cards ──────────────────── */
[data-testid="stExpander"], [data-testid="stStatus"] {
    background: #ffffff !important;
    border: 1.5px dashed #8fa1ba !important;
    border-radius: 12px !important;
    margin-bottom: 0.7rem;
}
[data-testid="stExpander"] details, [data-testid="stStatus"] details { background: transparent !important; border: none !important; }
[data-testid="stExpander"] summary, [data-testid="stStatus"] summary {
    font-family: var(--display); font-weight: 700; font-size: 1.05rem; color: var(--ink) !important;
}
[data-testid="stExpander"] summary *, [data-testid="stStatus"] summary * { color: var(--ink) !important; }
[data-testid="stExpander"] p, [data-testid="stExpander"] li,
[data-testid="stStatus"] p, [data-testid="stStatus"] li { color: #26344f !important; }

/* ── Run summary: ticket strip ────────────────────────────────────────── */
.ticket {
    display: flex;
    background: #ffffff;
    border: 2px solid var(--ink);
    border-radius: 12px;
    margin: 1.6rem 0 0.4rem;
}
.t-cell { flex: 1; padding: 1rem 1.3rem; }
.t-cell + .t-cell { border-left: 2px dashed var(--line); }
.t-val { display: block; font-family: var(--display); font-weight: 800; font-size: 2.1rem; line-height: 1.05; color: var(--ink); }
.t-val.ok { color: var(--blue); }
.t-lbl { color: var(--muted); font-size: 0.9rem; }

/* ── Final plan: boarding pass ────────────────────────────────────────── */
.st-key-final_pass,
div[data-testid="stVerticalBlockBorderWrapper"] {
    position: relative;
    background: #ffffff;
    border: 2px solid var(--ink) !important;
    border-radius: 16px !important;
    padding: 1.5rem 1.8rem 1.4rem;
    box-shadow: 0 14px 30px rgba(20,33,61,0.10);
}
.st-key-final_pass::before, .st-key-final_pass::after {
    content: ""; position: absolute; top: 3.5rem;
    width: 24px; height: 24px; border-radius: 50%;
    background: var(--paper); border: 2px solid var(--ink);
}
.st-key-final_pass::before { left: -12px;  clip-path: inset(0 0 0 50%); }
.st-key-final_pass::after  { right: -12px; clip-path: inset(0 50% 0 0); }
.pass-head {
    display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; flex-wrap: wrap;
    padding-bottom: 0.9rem; margin-bottom: 1rem;
    border-bottom: 2px dashed var(--line);
}
.pass-head b { font-family: var(--display); font-weight: 800; font-size: 1.4rem; color: var(--ink); }
.pass-head span { color: var(--muted); font-size: 0.9rem; }

/* ── Save bar ─────────────────────────────────────────────────────────── */
.save-bar {
    background: #ffffff;
    border: 1.5px dashed #8fa1ba;
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    color: var(--muted);
    font-size: 0.92rem;
    margin-top: 0.3rem;
}
.save-bar code { background: #e9eef6 !important; color: var(--ink) !important; }

/* ── Alerts ───────────────────────────────────────────────────────────── */
[data-testid="stAlert"] { background: #fff4d6 !important; border: 1.5px solid var(--sun) !important; border-radius: 10px !important; }
[data-testid="stAlert"] * { color: var(--ink) !important; }

/* ── Sidebar: the route board ─────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * { color: #dbe5f3; }
section[data-testid="stSidebar"] button svg { color: #ffffff !important; fill: #ffffff !important; }
.brand { font-family: var(--display); font-weight: 800; font-size: 1.45rem; letter-spacing: -0.02em; color: #ffffff !important; line-height: 1.1; margin-top: 0.5rem; }
.brand-sub { color: #9db2d0 !important; font-size: 0.88rem; margin: 0.3rem 0 1.4rem; }
.side-title { font-family: var(--display); font-weight: 700; font-size: 1.05rem; color: var(--sun) !important; margin: 1.8rem 0 0.9rem; }

.route { position: relative; padding-left: 26px; }
.route::before {
    content: ""; position: absolute; left: 6px; top: 8px; bottom: 14px;
    border-left: 2px dashed rgba(255,255,255,0.4);
}
.stop { position: relative; margin-bottom: 1rem; }
.stop::before {
    content: ""; position: absolute; left: -26px; top: 4px;
    width: 14px; height: 14px; border-radius: 50%;
    background: var(--ink); border: 2px solid var(--sun);
}
.stop.last::before { background: var(--sun); }
.stop b     { display: block; color: #ffffff !important; font-weight: 700; font-size: 0.97rem; }
.stop small { display: block; color: #9db2d0 !important; font-size: 0.84rem; line-height: 1.4; }
.tech { color: #9db2d0 !important; font-size: 0.88rem; line-height: 1.9; }

section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }
section[data-testid="stSidebar"] input {
    background: #1d2d52 !important; color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1.5px solid #3a4d78 !important; border-radius: 8px !important;
}
section[data-testid="stSidebar"] input:focus { border-color: var(--sun) !important; }
section[data-testid="stSidebar"] label p { color: #dbe5f3 !important; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def stamp(img_url, name, code, rot, img_h, extra=""):
    """A perforated postage stamp with a photo, a name and a country code."""
    return (
        f'<div class="stamp-wrap {extra}" style="--rot:{rot}deg">'
        f'<div class="stamp">'
        f'<div class="stamp-img" style="height:{img_h}px;background-image:url(\'{img_url}\')"></div>'
        f'<div class="stamp-cap"><b>{name}</b><i>{code}</i></div>'
        f'</div></div>'
    )


def set_query(text):
    st.session_state["query"] = text


if "query" not in st.session_state:
    st.session_state["query"] = ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div class='brand'>AI Travel<br>Booking System</div>"
        "<div class='brand-sub'>Flights, hotels and a day-by-day plan from one request.</div>",
        unsafe_allow_html=True,
    )

    thread_id = st.text_input("User ID", value="aarohi_user",
                              help="Your session ID — keeps travel history across queries")

    st.markdown("<div class='side-title'>How your plan is built</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='route'>"
        "<div class='stop'><b>Flight agent</b><small>Finds routes and fares</small></div>"
        "<div class='stop'><b>Hotel agent</b><small>Shortlists places to stay</small></div>"
        "<div class='stop'><b>Itinerary agent</b><small>Lays out each day</small></div>"
        "<div class='stop last'><b>Final agent</b><small>Combines it into one plan</small></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='side-title'>Powered by</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='tech'>LangGraph<br>Groq · LLaMA 3.3 70B<br>PostgreSQL<br>"
        "Tavily Search<br>AviationStack</div>".replace(" · ", " / "),
        unsafe_allow_html=True,
    )

# ── Hero ──────────────────────────────────────────────────────────────────────
HERO_PLANE = "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&q=80"
HERO_TOKYO = "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=500&q=75"

st.markdown(
    '<div class="envelope">'
    '<div class="env-copy">'
    '<div class="par-avion">Par avion · by air mail</div>'
    '<h1 class="env-title">Where to next?</h1>'
    '<p class="env-sub">Describe the trip you have in mind. Four agents check flights, hotels '
    'and things to do, then hand back one plan you can book from.</p>'
    '</div>'
    '<div class="env-stamps">'
    + stamp(HERO_PLANE, "Window seat", "AIR", 4, 150, "s-big")
    + stamp(HERO_TOKYO, "Tokyo", "JP", -6, 90, "s-small")
    + '<div class="postmark"><small>4 AGENTS</small><b>1</b><small>PLAN</small></div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Destination stamps (tap to fill the request) ──────────────────────────────
DESTINATIONS = [
    ("Tokyo",   "JP", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=500&q=75", "7-day Japan trip under ₹2L"),
    ("Paris",   "FR", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=500&q=75", "Paris trip for 5 days"),
    ("Bangkok", "TH", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=500&q=75", "Bangkok 4-day food and temples trip"),
    ("Rome",    "IT", "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=500&q=75", "Rome 6-day history trip"),
    ("Dubai",   "AE", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=500&q=75", "Dubai weekend trip"),
    ("Bali",    "ID", "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=500&q=75", "Bali backpacking 10 days"),
]
TILTS = [-2, 1.5, -1, 2, -1.5, 1]

st.markdown(
    "<div class='sec-head'><h2>Start from a stamp</h2>"
    "<p>Pick a destination to fill in a starter request, then edit it however you like.</p></div>",
    unsafe_allow_html=True,
)

dcols = st.columns(len(DESTINATIONS))
for col, (name, code, img, prompt), tilt in zip(dcols, DESTINATIONS, TILTS):
    with col:
        st.markdown(stamp(img, name, code, tilt, 104), unsafe_allow_html=True)
        st.button(f"Plan {name}", key=f"dest_{name}", on_click=set_query,
                  args=(prompt,), use_container_width=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='sec-head'><h2>Describe your trip</h2>"
    "<p>Say where, how long and your budget. The more you tell us, the better the plan.</p></div>",
    unsafe_allow_html=True,
)

user_query = st.text_area(
    "Describe your trip",
    key="query",
    placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs",
    height=120,
    label_visibility="collapsed",
)

generate = st.button("Generate my travel plan", type="primary", use_container_width=True)

# ── Agent pipeline ────────────────────────────────────────────────────────────
AGENT_META = {
    "flight_agent":    ("✈️", "Flight Agent"),
    "hotel_agent":     ("🏨", "Hotel Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "final_agent":     ("🧠", "Final Agent"),
}

if generate:
    if not user_query.strip():
        st.warning("Describe your trip first, then generate the plan.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        collected = {"flight_results": "", "hotel_results": "",
                     "itinerary": "", "final_response": "", "llm_calls": 0}

        st.markdown(
            "<div class='sec-head'><h2>Live from your agents</h2>"
            "<p>Each agent reports in as soon as it finishes.</p></div>",
            unsafe_allow_html=True,
        )

        for chunk in app.stream(
            {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                icon, label = AGENT_META.get(node_name, ("🔧", node_name))

                with st.status(f"{icon}  {label}", state="complete", expanded=True):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")

                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")

                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")

                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")

                    collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        # Run summary
        st.markdown(f"""
<div class="ticket">
<div class="t-cell"><span class="t-val">4</span><span class="t-lbl">Agents run</span></div>
<div class="t-cell"><span class="t-val">{collected['llm_calls']}</span><span class="t-lbl">LLM calls</span></div>
<div class="t-cell"><span class="t-val ok">Complete</span><span class="t-lbl">Status</span></div>
</div>
""", unsafe_allow_html=True)

        # Final plan — rendered as real markdown inside the boarding-pass card
        if collected["final_response"]:
            st.markdown("<div class='sec-head'><h2>Your travel plan</h2></div>",
                        unsafe_allow_html=True)
            try:
                pass_box = st.container(border=True, key="final_pass")
            except TypeError:               # older Streamlit without `key`
                pass_box = st.container(border=True)
            with pass_box:
                st.markdown(
                    f"<div class='pass-head'><b>Ready to book</b>"
                    f"<span>Traveller: {html.escape(str(thread_id))}</span></div>",
                    unsafe_allow_html=True,
                )
                st.markdown(collected["final_response"])

        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User ID:** {thread_id}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*LLM Calls: {collected['llm_calls']}*
"""
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        st.markdown("<br>", unsafe_allow_html=True)
        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button("Download plan", data=file_content,
                               file_name=filename, mime="text/markdown",
                               use_container_width=True)
        with info_col:
            st.markdown(f"<div class='save-bar'>Saved automatically to <code>travel_plans/{filename}</code></div>",
                        unsafe_allow_html=True)