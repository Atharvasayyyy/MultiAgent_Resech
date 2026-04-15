import streamlit as st
import time
import sys
import io
from contextlib import redirect_stdout

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e2e2e8;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #0d0d1a 0%, #111128 50%, #0a0a14 100%);
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(16,185,129,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #a5b4fc 0%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4rem 0;
}
.hero-sub {
    color: #6b7280;
    font-size: 0.95rem;
    font-weight: 300;
    letter-spacing: 0.3px;
}

/* ── Pipeline step cards ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.step-card {
    background: #111120;
    border: 1px solid #1e1e38;
    border-radius: 12px;
    padding: 1.1rem 1rem;
    text-align: center;
    transition: border-color 0.3s, background 0.3s;
    position: relative;
}
.step-card.active {
    border-color: #6366f1;
    background: #13132a;
    box-shadow: 0 0 20px rgba(99,102,241,0.15);
}
.step-card.done {
    border-color: #10b981;
    background: #0d1f1a;
}
.step-icon {
    font-size: 1.5rem;
    margin-bottom: 0.3rem;
}
.step-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.step-name {
    font-size: 0.82rem;
    font-weight: 500;
    color: #c4c4d4;
    margin-top: 0.2rem;
}
.step-card.active .step-label { color: #818cf8; }
.step-card.active .step-name  { color: #e0e0ff; }
.step-card.done  .step-label  { color: #34d399; }
.step-card.done  .step-name   { color: #a7f3d0; }

/* ── Input area ── */
.stTextArea textarea {
    background: #111120 !important;
    border: 1px solid #2a2a4a !important;
    border-radius: 10px !important;
    color: #e2e2e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    resize: vertical;
}
.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* ── Run button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 0.65rem 2.2rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:disabled {
    background: #1e1e38 !important;
    color: #4b4b6b !important;
    cursor: not-allowed !important;
    transform: none !important;
}

/* ── Result tabs / expanders ── */
.result-card {
    background: #0e0e1e;
    border: 1px solid #1e1e38;
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.result-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.8rem;
}
.result-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 700;
}
.badge-search  { background: #1e1b4b; color: #a5b4fc; }
.badge-scrape  { background: #1c1917; color: #fdba74; }
.badge-report  { background: #0f172a; color: #7dd3fc; }
.badge-critic  { background: #1a1f1a; color: #86efac; }
.result-content {
    color: #b0b0c8;
    font-size: 0.88rem;
    line-height: 1.7;
    white-space: pre-wrap;
    max-height: 340px;
    overflow-y: auto;
    padding-right: 4px;
}
.result-content::-webkit-scrollbar { width: 4px; }
.result-content::-webkit-scrollbar-thumb { background: #2a2a4a; border-radius: 4px; }

/* ── Log panel ── */
.log-box {
    background: #070710;
    border: 1px solid #1a1a30;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #4a9e6b;
    max-height: 260px;
    overflow-y: auto;
    white-space: pre-wrap;
    line-height: 1.6;
}
.log-box::-webkit-scrollbar { width: 4px; }
.log-box::-webkit-scrollbar-thumb { background: #1a2a1a; border-radius: 4px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #09090f !important;
    border-right: 1px solid #1a1a2e !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.2rem;
}

/* ── Metrics ── */
.metric-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1.2rem;
}
.metric-pill {
    flex: 1;
    background: #111120;
    border: 1px solid #1e1e38;
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
}
.metric-val {
    font-family: 'Space Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: #a5b4fc;
}
.metric-lbl {
    font-size: 0.68rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 2px;
}

/* Divider */
hr { border-color: #1a1a2e !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper: render pipeline status cards ─────────────────────────────────────
STEPS = [
    ("🔍", "STEP 01", "Search Agent"),
    ("📄", "STEP 02", "Reader Agent"),
    ("✍️",  "STEP 03", "Writer Chain"),
    ("🧠", "STEP 04", "Critic Chain"),
]

def render_pipeline_cards(active: int = -1, done_up_to: int = -1):
    cols = st.columns(4)
    for i, (icon, label, name) in enumerate(STEPS):
        cls = "step-card"
        if i == active:     cls += " active"
        elif i <= done_up_to: cls += " done"
        with cols[i]:
            st.markdown(f"""
            <div class="{cls}">
                <div class="step-icon">{icon}</div>
                <div class="step-label">{label}</div>
                <div class="step-name">{name}</div>
            </div>""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.75rem;
                color:#6366f1; letter-spacing:2px; text-transform:uppercase;
                margin-bottom:1.2rem;">
        ⚙️ &nbsp;Configuration
    </div>""", unsafe_allow_html=True)

    max_retries = st.slider("Max Retries", 1, 10, 5)
    initial_delay = st.slider("Initial Backoff (s)", 5, 60, 15)
    show_raw_logs = st.toggle("Show Live Logs", value=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.7rem;
                color:#4b4b6b; letter-spacing:1px; text-transform:uppercase;
                margin-bottom:0.8rem;">Pipeline Agents</div>""", unsafe_allow_html=True)

    for icon, label, name in STEPS:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:8px; padding:6px 0;
                    border-bottom:1px solid #1a1a2e;">
            <span style="font-size:1rem;">{icon}</span>
            <div>
                <div style="font-size:0.7rem; color:#6b7280;">{label}</div>
                <div style="font-size:0.82rem; color:#c4c4d4;">{name}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.72rem; color:#4b4b6b; line-height:1.6;">
        Multi-Agent Research System<br/>
        <span style="color:#6366f1;">pipeline.py</span> powered
    </div>""", unsafe_allow_html=True)


# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🔬 Multi-Agent Research System</div>
    <div class="hero-sub">Search → Scrape → Write → Critique &nbsp;·&nbsp; Powered by LangGraph agents</div>
</div>
""", unsafe_allow_html=True)

# Pipeline status (default: none active)
pipeline_placeholder = st.empty()
with pipeline_placeholder.container():
    render_pipeline_cards()

st.markdown("<br/>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_area(
        "Research Topic",
        placeholder="e.g.  Latest advances in multimodal AI models (2024–2025)",
        height=80,
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    run_clicked = st.button("▶ RUN", disabled=not topic.strip())

st.markdown("<hr/>", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "logs" not in st.session_state:
    st.session_state.logs = ""


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    st.session_state.results = None
    st.session_state.logs = ""
    log_placeholder = st.empty()
    metrics_placeholder = st.empty()

    t_start = time.time()

    # Capture stdout for live logs
    log_buffer = io.StringIO()

    def update_logs(msg: str):
        st.session_state.logs += msg + "\n"
        if show_raw_logs:
            log_placeholder.markdown(
                f'<div class="log-box">{st.session_state.logs}</div>',
                unsafe_allow_html=True,
            )

    try:
        from pipeline import run_research_pipeline
        import agent  # noqa – ensure importable

        # ── Step 1: Search ────────────────────────────────────────────────────
        with pipeline_placeholder.container():
            render_pipeline_cards(active=0)
        update_logs("▶ [01] Search Agent initialising…")

        from agent import build_search_agent
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        search_content = search_result['messages'][-1].content
        update_logs(f"✔ [01] Search complete — {len(search_content)} chars")

        # ── Step 2: Reader ────────────────────────────────────────────────────
        with pipeline_placeholder.container():
            render_pipeline_cards(active=1, done_up_to=0)
        update_logs("▶ [02] Reader Agent scraping…")

        from agent import build_reader_agent
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{search_content[:800]}"
            )]
        })
        scraped_content = reader_result['messages'][-1].content
        update_logs(f"✔ [02] Scrape complete — {len(scraped_content)} chars")

        # ── Step 3: Writer ────────────────────────────────────────────────────
        with pipeline_placeholder.container():
            render_pipeline_cards(active=2, done_up_to=1)
        update_logs("▶ [03] Writer Chain drafting report…")

        from agent import writer_chain
        research_combined = (
            f"SEARCH RESULTS:\n{search_content}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
        )

        def _write():
            return writer_chain.invoke({"topic": topic, "research": research_combined})

        def retry_with_backoff(func, max_r=max_retries, delay=initial_delay):
            d = delay
            for attempt in range(max_r):
                try:
                    return func()
                except Exception as e:
                    if ("429" in str(e) or "rate_limit" in str(e).lower()) and attempt < max_r - 1:
                        update_logs(f"⏱ Rate limit — waiting {d}s… (attempt {attempt+1}/{max_r})")
                        time.sleep(d); d *= 2
                    else:
                        raise

        report = retry_with_backoff(_write)
        update_logs(f"✔ [03] Report drafted — {len(report)} chars")

        # ── Step 4: Critic ────────────────────────────────────────────────────
        with pipeline_placeholder.container():
            render_pipeline_cards(active=3, done_up_to=2)
        update_logs("▶ [04] Critic Chain reviewing…")

        from agent import critic_chain
        feedback = retry_with_backoff(lambda: critic_chain.invoke({"report": report}))
        update_logs(f"✔ [04] Feedback ready — {len(feedback)} chars")

        # ── Done ──────────────────────────────────────────────────────────────
        with pipeline_placeholder.container():
            render_pipeline_cards(done_up_to=3)

        elapsed = round(time.time() - t_start, 1)
        st.session_state.results = {
            "search_results": search_content,
            "scraped_content": scraped_content,
            "report": report,
            "feedback": feedback,
        }
        st.session_state.elapsed = elapsed
        update_logs(f"\n🎉 Pipeline complete in {elapsed}s")

    except ImportError as e:
        st.error(f"⚠️ Import error: {e}\n\nMake sure `agent.py` and `pipeline.py` are in the same directory as `app.py`.")
    except Exception as e:
        st.error(f"Pipeline error: {e}")
        update_logs(f"✘ Error: {e}")


# ── Results display ───────────────────────────────────────────────────────────
if st.session_state.results:
    res = st.session_state.results

    # Metrics row
    wc = len(res["report"].split())
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-pill">
            <div class="metric-val">{st.session_state.elapsed}s</div>
            <div class="metric-lbl">Total Time</div>
        </div>
        <div class="metric-pill">
            <div class="metric-val">{wc}</div>
            <div class="metric-lbl">Report Words</div>
        </div>
        <div class="metric-pill">
            <div class="metric-val">4</div>
            <div class="metric-lbl">Agents Run</div>
        </div>
        <div class="metric-pill">
            <div class="metric-val">✓</div>
            <div class="metric-lbl">Critic Pass</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Result cards
    cards = [
        ("badge-search",  "🔍 Search Results",   res["search_results"]),
        ("badge-scrape",  "📄 Scraped Content",   res["scraped_content"]),
        ("badge-report",  "✍️  Final Report",      res["report"]),
        ("badge-critic",  "🧠 Critic Feedback",   res["feedback"]),
    ]

    tab_labels = ["🔍 Search", "📄 Scrape", "✍️ Report", "🧠 Critic"]
    tabs = st.tabs(tab_labels)

    for tab, (badge_cls, title, content) in zip(tabs, cards):
        with tab:
            badge_name = title.split()[-1]
            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">
                    <span class="result-badge {badge_cls}">{badge_name.upper()}</span>
                    <span style="font-size:0.82rem; color:#6b7280;">{len(content):,} characters</span>
                </div>
                <div class="result-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)

            # Download button
            st.download_button(
                label=f"⬇ Download {badge_name}",
                data=content,
                file_name=f"{badge_name.lower()}_{topic[:30].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

elif not run_clicked:
    st.markdown("""
    <div style="text-align:center; padding:3rem 0; color:#2a2a4a;">
        <div style="font-size:3rem; margin-bottom:1rem; opacity:0.4;">🔬</div>
        <div style="font-family:'Space Mono',monospace; font-size:0.8rem;
                    letter-spacing:2px; color:#3a3a5a;">
            ENTER A TOPIC ABOVE AND CLICK RUN
        </div>
    </div>
    """, unsafe_allow_html=True)