import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64

# ─────────────────────────────────────────────
# CONFIG & CONSTANTS
# ─────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "opportunities.csv")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "Molbio w tagline.PNG.png")

BRAND_RED = "#D32F2F"
BRAND_DARK = "#2D2D2D"
BRAND_LIGHT = "#F5F5F5"
BRAND_RED_LIGHT = "#FFCDD2"
BRAND_RED_DARK = "#B71C1C"
ACCENT_GREEN = "#43A047"
ACCENT_AMBER = "#FFA000"
ACCENT_BLUE = "#1E88E5"

STATUS_OPTIONS = ["Submitted", "Under Review", "Accepted", "Rejected", "Parked"]
SOURCE_OPTIONS = [
    "Customer request",
    "Tender or Government Program",
    "Internal R&D proposal",
    "Technology transfer/Licensing",
    "Customer support escalation",
    "Internal cross-functional idea",
    "Public health or guideline driven",
]
URGENCY_OPTIONS = [
    "Tender deadline",
    "Competitive gap",
    "Regulatory or guideline change",
    "Strategic priority",
    "No urgency",
]
TARGET_SETTING_OPTIONS = [
    "Central Lab",
    "Near-POC/Decentralized",
    "Hospital/Screening Program",
    "Public Health Program",
]
PRIORITY_OPTIONS = ["High", "Medium", "Low"]

STATUS_COLORS = {
    "Submitted": "#1E88E5",
    "Under Review": "#FFA000",
    "Accepted": "#43A047",
    "Rejected": "#E53935",
    "Parked": "#757575",
}

PRIORITY_COLORS = {
    "High": "#E53935",
    "Medium": "#FFA000",
    "Low": "#43A047",
}

st.set_page_config(
    page_title="Molbio Project Management",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Hide default streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Sidebar toggle button — all states */
    [data-testid="stSidebar"] button[kind="headerNoPadding"],
    button[data-testid="stBaseButton-headerNoPadding"],
    [data-testid="collapsedControl"] button,
    button[data-testid="baseButton-headerNoPadding"],
    header button {{
        background: {BRAND_DARK} !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        border: 1px solid #444 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.12) !important;
        transition: background 0.2s ease !important;
        margin: 6px !important;
        font-size: 0 !important;
        overflow: hidden !important;
        color: transparent !important;
    }}
    [data-testid="stSidebar"] button[kind="headerNoPadding"] *,
    button[data-testid="stBaseButton-headerNoPadding"] *,
    [data-testid="collapsedControl"] button *,
    button[data-testid="baseButton-headerNoPadding"] *,
    header button * {{
        display: none !important;
    }}
    [data-testid="stSidebar"] button[kind="headerNoPadding"]:hover,
    button[data-testid="stBaseButton-headerNoPadding"]:hover,
    [data-testid="collapsedControl"] button:hover,
    button[data-testid="baseButton-headerNoPadding"]:hover,
    header button:hover {{
        background: {BRAND_RED} !important;
        border-color: {BRAND_RED} !important;
    }}
    [data-testid="stSidebar"] button[kind="headerNoPadding"]::before,
    button[data-testid="stBaseButton-headerNoPadding"]::before,
    [data-testid="collapsedControl"] button::before,
    button[data-testid="baseButton-headerNoPadding"]::before,
    header button::before {{
        content: "\\2630";
        font-size: 1.3rem;
        color: white !important;
        line-height: 1;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BRAND_DARK} 0%, #1a1a2e 100%);
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label {{
        color: #CCCCCC !important;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Main header gradient bar */
    .main-header {{
        background: linear-gradient(135deg, {BRAND_RED} 0%, {BRAND_RED_DARK} 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(211, 47, 47, 0.3);
    }}
    .main-header h1 {{
        color: white;
        margin: 0;
        font-weight: 700;
        font-size: 1.8rem;
        letter-spacing: -0.02em;
    }}
    .main-header p {{
        color: rgba(255,255,255,0.85);
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
        font-weight: 300;
    }}

    /* KPI Metric Cards */
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 4px solid {BRAND_RED};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }}
    .kpi-card .kpi-value {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {BRAND_DARK};
        line-height: 1;
    }}
    .kpi-card .kpi-label {{
        font-size: 0.8rem;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
    }}

    /* Status badges */
    .status-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }}

    /* Priority badges */
    .priority-high {{ color: #E53935; background: #FFEBEE; }}
    .priority-medium {{ color: #F57F17; background: #FFF8E1; }}
    .priority-low {{ color: #2E7D32; background: #E8F5E9; }}

    /* Detail card */
    .detail-card {{
        background: white;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        border-top: 4px solid {BRAND_RED};
        margin: 1rem 0;
    }}
    .detail-card h3 {{
        color: {BRAND_DARK};
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }}
    .detail-field {{
        margin-bottom: 0.8rem;
    }}
    .detail-field .field-label {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    .detail-field .field-value {{
        font-size: 0.95rem;
        color: {BRAND_DARK};
        margin-top: 0.15rem;
        line-height: 1.5;
    }}

    /* Section headers */
    .section-header {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {BRAND_DARK};
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {BRAND_RED};
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }}

    /* Form styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-radius: 8px !important;
        border: 1.5px solid #E0E0E0 !important;
        transition: border-color 0.2s ease;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {BRAND_RED} !important;
        box-shadow: 0 0 0 1px {BRAND_RED} !important;
    }}

    /* Button styling */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
    }}

    /* Dataframe styling */
    .stDataFrame {{
        border-radius: 12px;
        overflow: hidden;
    }}

    /* Success/info boxes */
    .success-box {{
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-left: 4px solid #43A047;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}

    .info-box {{
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 4px solid #1E88E5;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}

    /* Divider */
    .custom-divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, #E0E0E0, transparent);
        margin: 1.5rem 0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# DATA HELPERS
# ─────────────────────────────────────────────

def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df["submission_date"] = pd.to_datetime(df["submission_date"], errors="coerce")
        return df
    return pd.DataFrame(
        columns=[
            "opportunity_id", "title", "source", "target_setting", "geography",
            "urgency", "priority", "submission_date", "status",
            "submitted_by", "problem_statement", "proposed_product",
            "intended_use", "timeline_comments",
        ]
    )


def save_data(df):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)


def generate_opportunity_id(df):
    year = datetime.now().year
    existing = df["opportunity_id"].dropna().tolist()
    max_num = 0
    for oid in existing:
        try:
            parts = str(oid).split("-")
            if len(parts) == 3 and parts[1] == str(year):
                max_num = max(max_num, int(parts[2]))
        except (ValueError, IndexError):
            continue
    return f"OP-{year}-{max_num + 1:03d}"


def status_badge_html(status):
    color = STATUS_COLORS.get(status, "#757575")
    bg = color + "18"
    return f'<span class="status-badge" style="color:{color}; background:{bg};">{status}</span>'


def priority_badge_html(priority):
    css_class = f"priority-{priority.lower()}" if priority else ""
    return f'<span class="status-badge {css_class}">{priority}</span>'


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        import base64 as b64
        with open(LOGO_PATH, "rb") as f:
            logo_b64 = b64.b64encode(f.read()).decode()
        st.markdown(
            f'<div style="background:white; border-radius:10px; padding:15px; margin-bottom:10px;">'
            f'<img src="data:image/png;base64,{logo_b64}" style="width:100%; display:block;" />'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["📊 Dashboard Overview", "📝 Submit Opportunity", "📋 Manage Opportunities"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.7rem; color:#888; text-align:center;'>"
        "Molbio Project Management<br>Developed by Joyston Jose D'souza • 2026</p>",
        unsafe_allow_html=True,
    )

# Load data
df = load_data()

# ─────────────────────────────────────────────
# PAGE 1: DASHBOARD OVERVIEW
# ─────────────────────────────────────────────
if page == "📊 Dashboard Overview":
    st.markdown(
        '<div class="main-header">'
        "<h1>📊 Dashboard Overview</h1>"
        "<p>Product Opportunity Pipeline — Real-time metrics and insights</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    # KPI Cards
    total = len(df)
    submitted = len(df[df["status"] == "Submitted"])
    under_review = len(df[df["status"] == "Under Review"])
    accepted = len(df[df["status"] == "Accepted"])
    rejected = len(df[df["status"] == "Rejected"])
    parked = len(df[df["status"] == "Parked"])

    cols = st.columns(5)
    kpis = [
        ("Total", total, BRAND_RED),
        ("Submitted", submitted, ACCENT_BLUE),
        ("Under Review", under_review, ACCENT_AMBER),
        ("Accepted", accepted, ACCENT_GREEN),
        ("Rejected / Parked", rejected + parked, "#757575"),
    ]
    for col, (label, value, color) in zip(cols, kpis):
        col.markdown(
            f'<div class="kpi-card" style="border-left-color:{color};">'
            f'<div class="kpi-value" style="color:{color};">{value}</div>'
            f'<div class="kpi-label">{label}</div>'
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Charts Row 1
    if not df.empty:
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown('<div class="section-header">Status Distribution</div>', unsafe_allow_html=True)
            status_counts = df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            color_map = {s: STATUS_COLORS.get(s, "#757575") for s in status_counts["Status"]}
            fig_status = px.donut = px.pie(
                status_counts,
                values="Count",
                names="Status",
                hole=0.55,
                color="Status",
                color_discrete_map=color_map,
            )
            fig_status.update_traces(
                textposition="outside",
                textinfo="label+value",
                textfont_size=12,
                marker=dict(line=dict(color="white", width=2)),
            )
            fig_status.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=320,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter"),
            )
            st.plotly_chart(fig_status, use_container_width=True)

        with chart_col2:
            st.markdown('<div class="section-header">Priority Breakdown</div>', unsafe_allow_html=True)
            priority_counts = df["priority"].value_counts().reindex(PRIORITY_OPTIONS).fillna(0).reset_index()
            priority_counts.columns = ["Priority", "Count"]
            fig_priority = px.bar(
                priority_counts,
                x="Priority",
                y="Count",
                color="Priority",
                color_discrete_map=PRIORITY_COLORS,
                text="Count",
            )
            fig_priority.update_traces(
                textposition="outside",
                marker_line_width=0,
                width=0.5,
            )
            fig_priority.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="",
                margin=dict(t=20, b=40, l=40, r=20),
                height=320,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter"),
                yaxis=dict(gridcolor="#F0F0F0"),
            )
            st.plotly_chart(fig_priority, use_container_width=True)

        # Charts Row 2
        chart_col3, chart_col4 = st.columns(2)

        with chart_col3:
            st.markdown('<div class="section-header">Source Analysis</div>', unsafe_allow_html=True)
            source_counts = df["source"].value_counts().reset_index()
            source_counts.columns = ["Source", "Count"]
            fig_source = px.bar(
                source_counts,
                y="Source",
                x="Count",
                orientation="h",
                text="Count",
                color_discrete_sequence=[BRAND_RED],
            )
            fig_source.update_traces(textposition="outside", marker_line_width=0)
            fig_source.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="",
                margin=dict(t=20, b=20, l=20, r=40),
                height=350,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=11),
                xaxis=dict(gridcolor="#F0F0F0"),
            )
            st.plotly_chart(fig_source, use_container_width=True)

        with chart_col4:
            st.markdown('<div class="section-header">Submissions Over Time</div>', unsafe_allow_html=True)
            time_df = df.dropna(subset=["submission_date"]).copy()
            if not time_df.empty:
                time_df["month"] = time_df["submission_date"].dt.to_period("M").astype(str)
                monthly = time_df.groupby("month").size().reset_index(name="Count")
                fig_time = px.area(
                    monthly,
                    x="month",
                    y="Count",
                    markers=True,
                    color_discrete_sequence=[BRAND_RED],
                )
                fig_time.update_traces(
                    fill="tozeroy",
                    fillcolor="rgba(211,47,47,0.1)",
                    line=dict(width=3),
                    marker=dict(size=8),
                )
                fig_time.update_layout(
                    showlegend=False,
                    xaxis_title="",
                    yaxis_title="",
                    margin=dict(t=20, b=40, l=40, r=20),
                    height=350,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter"),
                    xaxis=dict(gridcolor="#F0F0F0"),
                    yaxis=dict(gridcolor="#F0F0F0"),
                )
                st.plotly_chart(fig_time, use_container_width=True)
            else:
                st.info("No submission dates available to plot.")

        # Geography distribution
        st.markdown('<div class="section-header">Geography Distribution</div>', unsafe_allow_html=True)
        geo_col1, geo_col2 = st.columns([2, 1])
        with geo_col1:
            geo_counts = df["geography"].value_counts().reset_index()
            geo_counts.columns = ["Geography", "Count"]
            fig_geo = px.bar(
                geo_counts,
                x="Geography",
                y="Count",
                color="Count",
                color_continuous_scale=["#FFCDD2", BRAND_RED, BRAND_RED_DARK],
                text="Count",
            )
            fig_geo.update_traces(textposition="outside", marker_line_width=0)
            fig_geo.update_layout(
                showlegend=False,
                coloraxis_showscale=False,
                xaxis_title="",
                yaxis_title="",
                margin=dict(t=20, b=40, l=40, r=20),
                height=280,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter"),
                yaxis=dict(gridcolor="#F0F0F0"),
            )
            st.plotly_chart(fig_geo, use_container_width=True)
        with geo_col2:
            st.markdown("")
            for _, row in geo_counts.iterrows():
                pct = int(row["Count"] / total * 100) if total else 0
                st.markdown(
                    f"**{row['Geography']}** — {row['Count']} ({pct}%)"
                )
    else:
        st.markdown(
            '<div class="info-box">No opportunities in the system yet. '
            "Go to <strong>Submit Opportunity</strong> to add your first one.</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# PAGE 2: SUBMIT OPPORTUNITY
# ─────────────────────────────────────────────
elif page == "📝 Submit Opportunity":
    st.markdown(
        '<div class="main-header">'
        "<h1>📝 Product Opportunity Intake</h1>"
        "<p>Submit a new product opportunity for review by the PM team</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    new_id = generate_opportunity_id(df)

    st.markdown(
        f'<div class="info-box">'
        f"<strong>Opportunity ID:</strong> {new_id} &nbsp;•&nbsp; "
        f"<strong>Submission Date:</strong> {datetime.now().strftime('%B %d, %Y')}"
        f"</div>",
        unsafe_allow_html=True,
    )

    with st.form("intake_form", clear_on_submit=True):
        st.markdown('<div class="section-header">Basic Information</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Product Title *", placeholder="e.g. Truenat MTB Plus v3")
            source = st.selectbox("Source *", SOURCE_OPTIONS)
            target_setting = st.selectbox("Target Setting *", TARGET_SETTING_OPTIONS)
        with col2:
            geography = st.text_input("Geography *", placeholder="e.g. India, Africa, Global")
            urgency = st.selectbox("Urgency *", URGENCY_OPTIONS)
            priority = st.selectbox("Priority *", PRIORITY_OPTIONS)

        st.markdown('<div class="section-header">Detailed Description</div>', unsafe_allow_html=True)

        submitted_by = st.text_input("Submitted By *", placeholder="Your name or department")
        problem_statement = st.text_area(
            "Problem Statement *",
            placeholder="Describe the problem or unmet need this opportunity addresses...",
            height=100,
        )

        col3, col4 = st.columns(2)
        with col3:
            proposed_product = st.text_input(
                "Proposed Product", placeholder="e.g. Truenat XYZ Assay"
            )
        with col4:
            intended_use = st.text_input(
                "Intended Use", placeholder="e.g. Screening at PHC level"
            )

        timeline_comments = st.text_area(
            "Expected Timeline / Comments",
            placeholder="Any deadlines, strategic context, or additional notes...",
            height=80,
        )

        st.markdown("")
        col_btn1, col_btn2, _ = st.columns([1, 1, 3])
        with col_btn1:
            submitted = st.form_submit_button(
                "🚀 Submit Opportunity",
                type="primary",
                use_container_width=True,
            )
        with col_btn2:
            draft = st.form_submit_button(
                "💾 Save as Draft",
                use_container_width=True,
            )

    if submitted or draft:
        if not title or not geography or not submitted_by or not problem_statement:
            st.error("⚠️ Please fill in all required fields marked with *")
        else:
            new_row = {
                "opportunity_id": new_id,
                "title": title,
                "source": source,
                "target_setting": target_setting,
                "geography": geography,
                "urgency": urgency,
                "priority": priority,
                "submission_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "Submitted" if submitted else "Draft",
                "submitted_by": submitted_by,
                "problem_statement": problem_statement,
                "proposed_product": proposed_product,
                "intended_use": intended_use,
                "timeline_comments": timeline_comments,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            if submitted:
                st.markdown(
                    '<div class="success-box">'
                    f"✅ <strong>Opportunity {new_id}</strong> submitted successfully! "
                    "It will appear in the Manage Opportunities section for review."
                    "</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="info-box">'
                    f"💾 <strong>Opportunity {new_id}</strong> saved as draft."
                    "</div>",
                    unsafe_allow_html=True,
                )


# ─────────────────────────────────────────────
# PAGE 3: MANAGE OPPORTUNITIES
# ─────────────────────────────────────────────
elif page == "📋 Manage Opportunities":
    st.markdown(
        '<div class="main-header">'
        "<h1>📋 Manage Opportunities</h1>"
        "<p>Review, filter, and take action on product opportunities</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if df.empty:
        st.markdown(
            '<div class="info-box">No opportunities found. '
            "Submit one from the <strong>Submit Opportunity</strong> page.</div>",
            unsafe_allow_html=True,
        )
    else:
        # Filters
        show_filters = st.checkbox("🔍 Show Filters", value=False)
        if show_filters:
            fcol1, fcol2, fcol3 = st.columns(3)
            with fcol1:
                f_status = st.multiselect("Status", STATUS_OPTIONS, default=STATUS_OPTIONS)
            with fcol2:
                f_priority = st.multiselect("Priority", PRIORITY_OPTIONS, default=PRIORITY_OPTIONS)
            with fcol3:
                f_source = st.multiselect("Source", SOURCE_OPTIONS, default=SOURCE_OPTIONS)
        else:
            f_status = STATUS_OPTIONS
            f_priority = PRIORITY_OPTIONS
            f_source = SOURCE_OPTIONS

        filtered = df[
            (df["status"].isin(f_status))
            & (df["priority"].isin(f_priority))
            & (df["source"].isin(f_source))
        ]

        st.markdown(
            f"<p style='color:#888; font-size:0.85rem;'>"
            f"Showing <strong>{len(filtered)}</strong> of <strong>{len(df)}</strong> opportunities</p>",
            unsafe_allow_html=True,
        )

        # Summary table
        display_df = filtered[
            ["opportunity_id", "title", "source", "geography", "urgency", "priority", "submission_date", "status"]
        ].copy()
        display_df["submission_date"] = pd.to_datetime(display_df["submission_date"], errors="coerce").dt.strftime("%Y-%m-%d")
        display_df.columns = [
            "ID", "Title", "Source", "Geography", "Urgency", "Priority", "Date", "Status"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.TextColumn(width="small"),
                "Title": st.column_config.TextColumn(width="medium"),
                "Source": st.column_config.TextColumn(width="medium"),
                "Geography": st.column_config.TextColumn(width="small"),
                "Urgency": st.column_config.TextColumn(width="medium"),
                "Priority": st.column_config.TextColumn(width="small"),
                "Date": st.column_config.TextColumn(width="small"),
                "Status": st.column_config.TextColumn(width="small"),
            },
        )

        # Drill-down view
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Opportunity Details</div>', unsafe_allow_html=True)

        opp_options = filtered["opportunity_id"].tolist()
        opp_titles = filtered.set_index("opportunity_id")["title"].to_dict()
        opp_display = [f"{oid} — {opp_titles.get(oid, '')}" for oid in opp_options]

        if opp_options:
            selected_display = st.selectbox(
                "Select an opportunity to view details:",
                opp_display,
                label_visibility="visible",
            )
            selected_id = selected_display.split(" — ")[0]
            opp = filtered[filtered["opportunity_id"] == selected_id].iloc[0]

            # Detail card
            status_html = status_badge_html(opp["status"])
            priority_html = priority_badge_html(opp["priority"])

            st.markdown(
                f'<div class="detail-card">'
                f"<h3>{opp['title']} &nbsp;{status_html}&nbsp; {priority_html}</h3>"
                f'<div style="display:grid; grid-template-columns: 1fr 1fr; gap: 0.5rem 2rem;">'
                f'<div class="detail-field"><div class="field-label">Opportunity ID</div><div class="field-value">{opp["opportunity_id"]}</div></div>'
                f'<div class="detail-field"><div class="field-label">Submission Date</div><div class="field-value">{opp["submission_date"]}</div></div>'
                f'<div class="detail-field"><div class="field-label">Source</div><div class="field-value">{opp["source"]}</div></div>'
                f'<div class="detail-field"><div class="field-label">Target Setting</div><div class="field-value">{opp["target_setting"]}</div></div>'
                f'<div class="detail-field"><div class="field-label">Geography</div><div class="field-value">{opp["geography"]}</div></div>'
                f'<div class="detail-field"><div class="field-label">Urgency</div><div class="field-value">{opp["urgency"]}</div></div>'
                f'<div class="detail-field"><div class="field-label">Submitted By</div><div class="field-value">{opp.get("submitted_by", "—")}</div></div>'
                f'<div class="detail-field"><div class="field-label">Proposed Product</div><div class="field-value">{opp.get("proposed_product", "—")}</div></div>'
                f"</div>"
                f'<div class="custom-divider"></div>'
                f'<div class="detail-field"><div class="field-label">Problem Statement</div><div class="field-value">{opp.get("problem_statement", "—")}</div></div>'
                f'<div class="detail-field"><div class="field-label">Intended Use</div><div class="field-value">{opp.get("intended_use", "—")}</div></div>'
                f'<div class="detail-field"><div class="field-label">Timeline / Comments</div><div class="field-value">{opp.get("timeline_comments", "—")}</div></div>'
                f"</div>",
                unsafe_allow_html=True,
            )

            # Action buttons
            st.markdown("")
            current_status = opp["status"]

            if current_status not in ["Accepted", "Rejected"]:
                st.markdown(
                    f"<p style='font-weight:600; color:{BRAND_DARK}; margin-bottom: 0.5rem;'>"
                    "📌 Take Action</p>",
                    unsafe_allow_html=True,
                )

                action_cols = st.columns(4)
                with action_cols[0]:
                    if st.button("✅ Accept", key=f"accept_{selected_id}", type="primary", use_container_width=True):
                        df.loc[df["opportunity_id"] == selected_id, "status"] = "Accepted"
                        save_data(df)
                        st.success(f"✅ {selected_id} — **Accepted**. Eligible for next PLM stage (Feasibility / Evaluation).")
                        st.rerun()
                with action_cols[1]:
                    if st.button("❌ Reject", key=f"reject_{selected_id}", use_container_width=True):
                        df.loc[df["opportunity_id"] == selected_id, "status"] = "Rejected"
                        save_data(df)
                        st.warning(f"❌ {selected_id} — **Rejected**. Status locked and archived.")
                        st.rerun()
                with action_cols[2]:
                    if st.button("⏸️ Park", key=f"park_{selected_id}", use_container_width=True):
                        df.loc[df["opportunity_id"] == selected_id, "status"] = "Parked"
                        save_data(df)
                        st.info(f"⏸️ {selected_id} — **Parked**. Visible but inactive.")
                        st.rerun()
                with action_cols[3]:
                    if current_status != "Under Review":
                        if st.button("🔍 Mark Under Review", key=f"review_{selected_id}", use_container_width=True):
                            df.loc[df["opportunity_id"] == selected_id, "status"] = "Under Review"
                            save_data(df)
                            st.info(f"🔍 {selected_id} — Moved to **Under Review**.")
                            st.rerun()
            else:
                if current_status == "Accepted":
                    st.markdown(
                        '<div class="success-box">'
                        "✅ This opportunity has been <strong>Accepted</strong> and is eligible for the next PLM stage "
                        "(Feasibility / Evaluation)."
                        "</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div style="background:#FFEBEE; border-left:4px solid #E53935; '
                        f'padding:1rem 1.5rem; border-radius:8px; margin:1rem 0;">'
                        "❌ This opportunity has been <strong>Rejected</strong>. Status is locked and archived."
                        "</div>",
                        unsafe_allow_html=True,
                    )

            # Delete button — available for all opportunities
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            del_col1, del_col2, _ = st.columns([1, 1, 3])
            with del_col1:
                confirm_delete = st.checkbox("Confirm delete", key=f"confirm_del_{selected_id}")
            with del_col2:
                if st.button("🗑️ Delete Opportunity", key=f"delete_{selected_id}", use_container_width=True, disabled=not confirm_delete):
                    df = df[df["opportunity_id"] != selected_id]
                    save_data(df)
                    st.warning(f"🗑️ **{selected_id}** has been permanently deleted.")
                    st.rerun()

        # Download section
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download All Opportunities (CSV)",
            data=csv_data,
            file_name=f"molbio_opportunities_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=False,
        )
