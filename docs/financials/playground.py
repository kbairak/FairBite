# Run with: uvx --with plotly --with numpy streamlit run playground.py

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Model ─────────────────────────────────────────────────────────────────────

COURIER_TIME_RATIO = (365 - 22) * 5 / 7 / 365


def compute(p):
    r = {}
    r["gmv"] = p["orders_per_day"] * p["avg_order_value"] * 30

    k = p["orders_per_courier_per_day"]
    r["courier_count"] = p["orders_per_day"] / k / COURIER_TIME_RATIO if k > 0 else 0

    r["variable_costs"] = r["gmv"] * p["variable_cost_over_gmv"]
    r["courier_cost"] = r["courier_count"] * (
        p["courier_wage"] + p["courier_equipment_reimbursement"]
    )
    r["developer_cost"] = p["developer_count"] * p["developer_wage"]
    r["manager_cost"] = p["manager_count"] * p["manager_wage"]
    r["operational_expenses"] = sum(
        p[v]
        for v in (
            "server_cost",
            "twilio_cost",
            "sentry_cost",
            "intercom_cost",
            "mixpanel_cost",
            "postmark_cost",
            "apple_store_cost",
            "docusign_cost",
            "accounting_cost",
            "legal_cost",
            "rent",
            "utilities_cost",
        )
    )
    r["ktlo"] = (
        r["courier_cost"]
        + r["developer_cost"]
        + r["manager_cost"]
        + r["operational_expenses"]
    )
    r["net_surplus"] = r["gmv"] - r["ktlo"] - r["variable_costs"]
    r["minimum_restaurant_reimbursement"] = (1 - p["restaurant_commision_cap"]) * r[
        "gmv"
    ]

    growth_fund_target = max(0, 1 - p["growth_fund_balance_ratio"]) * 3 * r["ktlo"]
    growth_fund_cap_by_rate = r["net_surplus"] * p["growth_fund_contribution_rate"]
    growth_fund_cap_by_surplus = (
        r["net_surplus"] - r["minimum_restaurant_reimbursement"]
    )
    r["growth_fund_contribution"] = max(
        min(growth_fund_target, growth_fund_cap_by_rate, growth_fund_cap_by_surplus),
        0,
    )

    r["restaurant_reimbursement"] = max(
        r["net_surplus"] - r["growth_fund_contribution"],
        r["minimum_restaurant_reimbursement"],
    )
    r["restaurant_commission_pct"] = (
        (r["gmv"] - r["restaurant_reimbursement"]) / r["gmv"] * 100
        if r["gmv"] > 0
        else 0.0
    )
    r["deficit"] = (
        r["ktlo"]
        + r["variable_costs"]
        + r["growth_fund_contribution"]
        + r["restaurant_reimbursement"]
        - r["gmv"]
    )
    return r


# ── Variable metadata: (label, default, min, max, step) ──────────────────────

INPUT_META = {
    "orders_per_day": ("Orders per day", 60, 10, 2000, 10),
    "avg_order_value": ("Avg order value (€)", 18, 10, 35, 1),
    "orders_per_courier_per_day": ("Orders / courier / day", 30, 10, 60, 1),
    "restaurant_commision_cap": ("Commission cap", 0.30, 0.10, 0.45, 0.01),
    "variable_cost_over_gmv": ("Variable costs (% of GMV)", 0.05, 0.01, 0.15, 0.005),
    "growth_fund_contribution_rate": (
        "Growth fund contribution rate",
        0.05,
        0.01,
        0.20,
        0.01,
    ),
    "growth_fund_balance_ratio": (
        "Growth fund fill level (0=empty, 1=full)",
        0.17,
        0.0,
        1.1,
        0.05,
    ),
    "courier_wage": ("Courier wage / month (€)", 2195, 1500, 3500, 50),
    "courier_equipment_reimbursement": ("Courier equipment reimb (€)", 50, 0, 200, 10),
    "developer_count": ("Developer count", 2, 1, 5, 1),
    "developer_wage": ("Developer cost / month (€)", 4281, 3000, 6000, 100),
    "manager_count": ("Manager count", 1, 0, 3, 1),
    "manager_wage": ("Manager cost / month (€)", 3302, 2000, 5000, 100),
    "server_cost": ("Servers (€)", 400, 0, 2000, 50),
    "twilio_cost": ("Twilio (€)", 50, 0, 200, 10),
    "sentry_cost": ("Sentry (€)", 25, 0, 100, 5),
    "intercom_cost": ("Intercom (€)", 75, 0, 300, 25),
    "mixpanel_cost": ("Mixpanel (€)", 30, 0, 200, 10),
    "postmark_cost": ("Postmark (€)", 20, 0, 100, 5),
    "apple_store_cost": ("Apple Developer (€)", 9, 0, 20, 1),
    "docusign_cost": ("DocuSign (€)", 25, 0, 100, 5),
    "accounting_cost": ("Accounting (€)", 350, 100, 800, 50),
    "legal_cost": ("Legal (€)", 200, 0, 1000, 50),
    "rent": ("Rent (€)", 600, 0, 2000, 100),
    "utilities_cost": ("Utilities (€)", 120, 0, 500, 20),
}

OUTPUT_META = {
    "deficit": "Monthly deficit (€)",
    "net_surplus": "Net surplus (€)",
    "restaurant_commission_pct": "Effective commission (%)",
    "gmv": "Monthly GMV (€)",
    "courier_count": "Courier count",
    "ktlo": "KTLO (€)",
    "courier_cost": "Courier cost (€)",
    "variable_costs": "Variable costs (€)",
    "growth_fund_contribution": "Growth fund contribution (€)",
    "restaurant_reimbursement": "Restaurant reimbursement (€)",
    "operational_expenses": "Operational expenses (€)",
}

GROUPS = [
    (
        "Operations",
        [
            "orders_per_day",
            "avg_order_value",
            "orders_per_courier_per_day",
            "restaurant_commision_cap",
            "variable_cost_over_gmv",
            "growth_fund_contribution_rate",
            "growth_fund_balance_ratio",
        ],
    ),
    (
        "Staff costs",
        [
            "courier_wage",
            "courier_equipment_reimbursement",
            "developer_count",
            "developer_wage",
            "manager_count",
            "manager_wage",
        ],
    ),
    (
        "Opex",
        [
            "server_cost",
            "twilio_cost",
            "sentry_cost",
            "intercom_cost",
            "mixpanel_cost",
            "postmark_cost",
            "apple_store_cost",
            "docusign_cost",
            "accounting_cost",
            "legal_cost",
            "rent",
            "utilities_cost",
        ],
    ),
]


# ── App ───────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="OurFood Playground", layout="wide")
st.title("OurFood — Financial Playground")

col_x, col_y = st.columns([1, 2])
with col_x:
    x_key = st.selectbox(
        "X axis (sweep)",
        list(INPUT_META.keys()),
        format_func=lambda k: INPUT_META[k][0],
    )
with col_y:
    y_keys = st.multiselect(
        "Y axis",
        list(OUTPUT_META.keys()),
        default=[
            "gmv",
            "deficit",
            "growth_fund_contribution",
            "restaurant_commission_pct",
        ],
        format_func=lambda k: OUTPUT_META[k],
    )

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.header("Fixed parameters")
params = {}

x_label, x_default, x_vmin, x_vmax, x_step = INPUT_META[x_key]

for group_label, keys in GROUPS:
    visible = [k for k in keys if k != x_key]
    if not visible:
        continue

    ctx = (
        st.sidebar.expander(group_label, expanded=(group_label != "Opex"))
        if group_label == "Opex"
        else None
    )

    def render_sliders(target, visible_keys):
        for key in visible_keys:
            label, default, vmin, vmax, step = INPUT_META[key]
            if isinstance(step, float) or isinstance(default, float):
                params[key] = target.slider(
                    label,
                    float(vmin),
                    float(vmax),
                    float(default),
                    float(step),
                    key=key,
                )
            else:
                params[key] = target.slider(
                    label, int(vmin), int(vmax), int(default), int(step), key=key
                )

    if ctx is not None:
        with ctx:
            render_sliders(st, visible)
    else:
        st.sidebar.subheader(group_label)
        render_sliders(st.sidebar, visible)

# X-axis sweep range
st.sidebar.subheader(f"X range: {x_label}")
x_range = st.sidebar.slider(
    "Sweep range",
    int(x_vmin),
    int(x_vmax),
    (int(x_vmin), int(x_vmax)),
    int(x_step),
    key="_xrange",
)

# ── Compute sweep ─────────────────────────────────────────────────────────────

x_vals = np.linspace(x_range[0], x_range[1], 300)
results = {k: [] for k in y_keys}
for xv in x_vals:
    r = compute({**params, x_key: xv})
    for k in y_keys:
        results[k].append(r[k])

# ── Plot ──────────────────────────────────────────────────────────────────────

if not y_keys:
    st.info("Select at least one Y-axis variable.")
else:
    colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

    fig = make_subplots(
        rows=len(y_keys),
        cols=1,
        shared_xaxes=True,
        subplot_titles=[OUTPUT_META[k] for k in y_keys],
        vertical_spacing=0.08 if len(y_keys) > 1 else 0,
    )

    for i, k in enumerate(y_keys):
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=results[k],
                mode="lines",
                name=OUTPUT_META[k],
                line={"color": colors[i % len(colors)]},
                showlegend=False,
            ),
            row=i + 1,
            col=1,
        )
        fig.add_hline(y=0, line_dash="dot", line_color="lightgray", row=i + 1, col=1)

    fig.update_xaxes(title_text=x_label, row=len(y_keys), col=1)
    fig.update_layout(
        hovermode="x unified",
        height=280 * len(y_keys),
        margin={"t": 40, "b": 40},
    )
    st.plotly_chart(fig, use_container_width=True)
