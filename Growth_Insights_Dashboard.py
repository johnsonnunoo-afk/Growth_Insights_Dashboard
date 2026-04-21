"""
Growth Insights Dashboard — Startup.OS Performance Console
A living view of revenue, profit, burn, and unit economics in one console.

Run:
    pip install dash plotly pandas numpy
    python growth_insights_dashboard.py

Then open http://localhost:8053
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ── Theme ──────────────────────────────────────────────────────────────────────
BG       = "#080B12"
SURFACE  = "#0E1420"
CARD     = "#111827"
BORDER   = "#1C2537"
BORDER2  = "#243048"
TEXT     = "#E4EAF4"
MUTED    = "#5B6B8A"
DIM      = "#1E2D45"
ACCENT   = "#3B82F6"    # electric blue
GREEN    = "#10D98A"
RED      = "#F05252"
YELLOW   = "#F5C518"
CYAN     = "#06B6D4"
PURPLE   = "#A78BFA"

FONT_DISPLAY = "'Orbitron', monospace"
FONT_MONO    = "'JetBrains Mono', monospace"
FONT_BODY    = "'Outfit', sans-serif"

# ── Data ──────────────────────────────────────────────────────────────────────
months = ["May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]

revenue_data  = [72400, 81200, 88600, 94100, 91800, 103400, 124600, 148200, 112400, 128600, 142800, 178400]
expense_data  = [58200, 61400, 63800, 67200, 69100, 71800,  76400,  89200,  72100,  74800,  80200,  89600]
profit_data   = [r - e for r, e in zip(revenue_data, expense_data)]
cac_data      = [198, 188, 181, 174, 179, 168, 159, 147, 162, 158, 152, 156]

products = {
    "Filly Suite":      {"revenue": 78400,  "pct": 44, "color": ACCENT},
    "Aegis Security":   {"revenue": 52100,  "pct": 29, "color": GREEN},
    "Filly API":        {"revenue": 31200,  "pct": 17, "color": CYAN},
    "Other":            {"revenue": 16700,  "pct": 10, "color": MUTED},
}

transactions = [
    {"id": "TX-9241", "customer": "Northwind Labs",  "product": "Aegis Enterprise",  "amount": "$4,800", "status": "paid"},
    {"id": "TX-9240", "customer": "Helio Studio",    "product": "Filly Suite Pro",   "amount": "$1,290", "status": "paid"},
    {"id": "TX-9239", "customer": "Vector Capital",  "product": "Filly API",         "amount": "$890",   "status": "pending"},
    {"id": "TX-9238", "customer": "Quantum Forge",   "product": "Aegis Standard",    "amount": "$2,400", "status": "paid"},
    {"id": "TX-9237", "customer": "Lumen Works",     "product": "Filly Suite",       "amount": "$690",   "status": "failed"},
    {"id": "TX-9236", "customer": "Ridge & Co.",     "product": "Aegis Enterprise",  "amount": "$4,800", "status": "paid"},
]

# ── Chart layout base ─────────────────────────────────────────────────────────
def base_layout(height=210, b=24):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_MONO, color=TEXT, size=10),
        margin=dict(l=8, r=8, t=8, b=b),
        height=height,
        xaxis=dict(showgrid=False, tickfont=dict(color=MUTED, size=9), zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#151E2E", tickfont=dict(color=MUTED, size=9),
                   zeroline=False),
        hovermode="x unified",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED, size=9)),
    )

# Revenue vs Expenses
rev_exp_fig = go.Figure()
rev_exp_fig.add_trace(go.Scatter(
    x=months, y=expense_data, name="Expenses",
    mode="lines", line=dict(color=RED, width=1.5, dash="dot"),
    hovertemplate="$%{y:,.0f}<extra>Expenses</extra>",
))
rev_exp_fig.add_trace(go.Scatter(
    x=months, y=revenue_data, name="Revenue",
    mode="lines+markers",
    line=dict(color=ACCENT, width=2),
    marker=dict(color=ACCENT, size=4),
    fill="tozeroy", fillcolor="rgba(59,130,246,0.06)",
    hovertemplate="$%{y:,.0f}<extra>Revenue</extra>",
))
rev_exp_fig.update_layout(**base_layout(height=200))

# Net Profit
profit_colors = [GREEN if v >= 0 else RED for v in profit_data]
profit_fig = go.Figure()
profit_fig.add_trace(go.Bar(
    x=months, y=profit_data,
    marker_color=profit_colors,
    marker_opacity=0.85,
    hovertemplate="$%{y:,.0f}<extra>Net Profit</extra>",
))
profit_fig.add_trace(go.Scatter(
    x=months, y=profit_data,
    mode="lines",
    line=dict(color=GREEN, width=1.5),
    showlegend=False,
    hoverinfo="skip",
))
profit_fig.update_layout(**base_layout(height=200))

# CAC trend
cac_fig = go.Figure()
cac_fig.add_trace(go.Scatter(
    x=months, y=cac_data,
    mode="lines+markers",
    line=dict(color=YELLOW, width=2),
    marker=dict(color=YELLOW, size=5,
                line=dict(color=BG, width=1.5)),
    fill="tozeroy",
    fillcolor="rgba(245,197,24,0.05)",
    hovertemplate="$%{y}<extra>CAC</extra>",
))
cac_fig.add_hline(y=180, line_color=f"{RED}60", line_width=1, line_dash="dot",
                  annotation_text="target", annotation_font_color=MUTED,
                  annotation_font_size=9)
cac_fig.update_layout(**base_layout(height=200))

# Product donut
prod_fig = go.Figure(go.Pie(
    labels=list(products.keys()),
    values=[products[p]["revenue"] for p in products],
    hole=0.68,
    marker=dict(
        colors=[products[p]["color"] for p in products],
        line=dict(color=CARD, width=3),
    ),
    textinfo="none",
    hovertemplate="%{label}: $%{value:,.0f}<extra></extra>",
    direction="clockwise",
    sort=False,
))
prod_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=0, b=0),
    height=180,
    showlegend=False,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def kpi_card(label, value, delta, sub, delta_dir="up"):
    dcolor = GREEN if delta_dir == "up" else RED
    arrow  = "↑" if delta_dir == "up" else "↓"
    return html.Div([
        html.Div([
            html.Span(label, style={
                "color": MUTED, "fontSize": "9px",
                "letterSpacing": "0.14em", "textTransform": "uppercase",
                "fontFamily": FONT_MONO,
            }),
            html.Span(f"{arrow} {delta}", style={
                "color": dcolor, "fontSize": "9px", "fontFamily": FONT_MONO,
                "background": f"{dcolor}18", "padding": "1px 6px",
                "borderRadius": "3px", "marginLeft": "8px",
            }),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
        html.H2(value, style={
            "color": TEXT, "fontSize": "26px", "fontWeight": "700",
            "fontFamily": FONT_DISPLAY, "margin": "0 0 6px",
            "letterSpacing": "-0.02em",
        }),
        html.Div(sub, style={"color": MUTED, "fontSize": "10px", "fontFamily": FONT_MONO}),
    ], style={
        "background": CARD,
        "border": f"1px solid {BORDER}",
        "borderRadius": "10px",
        "padding": "18px 20px",
        "flex": "1",
        "minWidth": "180px",
        "position": "relative",
        "overflow": "hidden",
    })


def panel_header(eyebrow, title, sub=None):
    return html.Div([
        html.Span(eyebrow, style={
            "color": MUTED, "fontSize": "9px", "letterSpacing": "0.14em",
            "textTransform": "uppercase", "fontFamily": FONT_MONO,
            "display": "block", "marginBottom": "4px",
        }),
        html.Div([
            html.H3(title, style={
                "color": TEXT, "fontSize": "13px", "fontWeight": "600",
                "fontFamily": FONT_BODY, "margin": "0",
            }),
            html.Span(sub, style={"color": MUTED, "fontSize": "9px",
                                   "fontFamily": FONT_MONO}) if sub else None,
        ], style={"display": "flex", "justifyContent": "space-between",
                   "alignItems": "center", "marginBottom": "14px"}),
    ])


def card(children, flex="1", min_w="260px", extra_style=None):
    style = {
        "background": CARD,
        "border": f"1px solid {BORDER}",
        "borderRadius": "10px",
        "padding": "18px 20px",
        "flex": flex,
        "minWidth": min_w,
    }
    if extra_style:
        style.update(extra_style)
    return html.Div(children, style=style)


def status_pill(status):
    cfg = {
        "paid":    (GREEN,  f"rgba(16,217,138,0.12)"),
        "pending": (YELLOW, f"rgba(245,197,24,0.12)"),
        "failed":  (RED,    f"rgba(240,82,82,0.12)"),
    }
    fg, bg = cfg.get(status, (MUTED, DIM))
    return html.Span(status, style={
        "color": fg, "background": bg, "fontSize": "9px",
        "fontWeight": "600", "fontFamily": FONT_MONO,
        "padding": "3px 10px", "borderRadius": "20px",
        "textTransform": "uppercase", "letterSpacing": "0.08em",
    })


def nav_tab(label, active=False):
    return html.Span(label, style={
        "padding": "6px 14px",
        "borderRadius": "6px",
        "fontSize": "11px",
        "cursor": "pointer",
        "marginRight": "4px",
        "fontFamily": FONT_MONO,
        "background": ACCENT if active else "transparent",
        "color": BG if active else MUTED,
        "fontWeight": "600" if active else "400",
        "letterSpacing": "0.05em",
    })


def time_tab(label, active=False):
    return html.Span(label, style={
        "padding": "4px 12px",
        "borderRadius": "5px",
        "fontSize": "10px",
        "cursor": "pointer",
        "marginRight": "2px",
        "fontFamily": FONT_MONO,
        "background": BORDER2 if active else "transparent",
        "color": TEXT if active else MUTED,
    })


# ── App ───────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="Growth Insights Dashboard — Startup.OS")

app.index_string = """<!DOCTYPE html>
<html>
<head>
  {%metas%}<title>{%title%}</title>{%favicon%}{%css%}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;900&family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:#080B12;color:#E4EAF4;font-family:'Outfit',sans-serif}
    ::-webkit-scrollbar{width:4px}
    ::-webkit-scrollbar-thumb{background:#1C2537;border-radius:2px}
    .glow{box-shadow:0 0 24px rgba(59,130,246,0.08)}
  </style>
</head>
<body>{%app_entry%}{%config%}{%scripts%}{%renderer%}</body>
</html>"""

app.layout = html.Div([

    # ── Header ──
    html.Div([
        # Left — branding
        html.Div([
            html.Div([
                html.Span("STARTUP", style={
                    "fontFamily": FONT_DISPLAY, "fontSize": "15px", "fontWeight": "900",
                    "color": TEXT, "letterSpacing": "0.08em",
                }),
                html.Span(".OS", style={
                    "fontFamily": FONT_DISPLAY, "fontSize": "15px", "fontWeight": "900",
                    "color": ACCENT, "letterSpacing": "0.08em",
                }),
            ]),
            html.Div("Performance Console", style={
                "color": MUTED, "fontSize": "10px", "fontFamily": FONT_MONO,
                "letterSpacing": "0.1em", "textTransform": "uppercase", "marginTop": "2px",
            }),
        ]),

        # Centre — nav tabs
        html.Div([
            nav_tab("Overview", active=True),
            nav_tab("Revenue"),
            nav_tab("Customers"),
            nav_tab("Burn"),
            nav_tab("Reports"),
        ], style={"display": "flex", "alignItems": "center"}),

        # Right — live indicator + date
        html.Div([
            html.Div([
                html.Span("●", style={"color": GREEN, "fontSize": "8px", "marginRight": "5px",
                                       "animation": "pulse 2s infinite"}),
                html.Span("Apr 21, 22:23 UTC", style={
                    "color": MUTED, "fontSize": "10px", "fontFamily": FONT_MONO,
                }),
            ], style={"display": "flex", "alignItems": "center", "marginBottom": "4px"}),
            html.Div("FY · Fiscal Year 2025", style={
                "color": DIM, "fontSize": "9px", "fontFamily": FONT_MONO,
                "textAlign": "right",
            }),
        ]),

    ], style={
        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
        "padding": "20px 36px",
        "borderBottom": f"1px solid {BORDER}",
        "background": SURFACE,
        "position": "sticky", "top": "0", "zIndex": "100",
    }),

    # ── Body ──
    html.Div([

        # Page title
        html.Div([
            html.Div([
                html.H1("Performance overview", style={
                    "fontFamily": FONT_DISPLAY, "fontSize": "22px", "fontWeight": "700",
                    "color": TEXT, "letterSpacing": "0.04em", "margin": "0 0 4px",
                }),
                html.P("A living view of how the business is operating — revenue, profit, burn and unit economics in one console.",
                       style={"color": MUTED, "fontSize": "12px", "fontFamily": FONT_BODY,
                              "lineHeight": "1.5"}),
            ], style={"flex": "1"}),
            html.Div([
                time_tab("7D"), time_tab("30D"), time_tab("QTD"),
                time_tab("YTD", active=True), time_tab("ALL"),
            ], style={"display": "flex", "alignItems": "center",
                       "background": CARD, "padding": "4px",
                       "borderRadius": "8px", "border": f"1px solid {BORDER}"}),
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "alignItems": "flex-end", "marginBottom": "20px",
        }),

        # ── KPI row ──
        html.Div([
            kpi_card("Revenue (YTD)",  "$1,160,500", "18.4%", "178.4K this month",     "up"),
            kpi_card("Net Profit (YTD)","$638,800",  "32.1%", "55.0% margin",          "up"),
            kpi_card("Expenses (YTD)", "$521,700",   "6.2%",  "Burn under control",    "down"),
            kpi_card("CAC (current)",  "$156",        "9.3%",  "13.8% MoM growth",     "down"),
        ], style={"display": "flex", "gap": "10px", "marginBottom": "16px", "flexWrap": "wrap"}),

        # ── Row 2: Revenue vs Expenses + Product breakdown ──
        html.Div([
            card([
                panel_header("P&L · Last 12 months · USD", "Revenue vs Expenses"),
                dcc.Graph(figure=rev_exp_fig, config={"displayModeBar": False}),
            ], flex="1.4"),

            card([
                panel_header("Current quarter", "Revenue by Product"),
                html.Div([
                    # Donut
                    html.Div([
                        dcc.Graph(figure=prod_fig, config={"displayModeBar": False}),
                        html.Div([
                            html.Div("$178.4K", style={
                                "color": TEXT, "fontSize": "16px", "fontWeight": "700",
                                "fontFamily": FONT_DISPLAY, "textAlign": "center",
                                "letterSpacing": "0.02em",
                            }),
                            html.Div("this quarter", style={
                                "color": MUTED, "fontSize": "9px", "textAlign": "center",
                                "fontFamily": FONT_MONO,
                            }),
                        ], style={
                            "position": "absolute", "top": "50%", "left": "50%",
                            "transform": "translate(-50%, -50%)",
                        }),
                    ], style={"position": "relative", "width": "180px", "flexShrink": "0"}),

                    # Legend
                    html.Div([
                        *[html.Div([
                            html.Div(style={
                                "width": "8px", "height": "8px", "borderRadius": "2px",
                                "background": products[p]["color"], "flexShrink": "0",
                            }),
                            html.Div([
                                html.Div(p, style={"color": TEXT, "fontSize": "11px",
                                                    "fontFamily": FONT_BODY}),
                                html.Div([
                                    html.Span(f"${products[p]['revenue']:,}",
                                              style={"color": MUTED, "fontSize": "10px",
                                                     "fontFamily": FONT_MONO}),
                                    html.Span(f" · {products[p]['pct']}%",
                                              style={"color": products[p]["color"],
                                                     "fontSize": "10px", "fontFamily": FONT_MONO}),
                                ]),
                            ]),
                        ], style={"display": "flex", "gap": "10px", "alignItems": "flex-start",
                                   "marginBottom": "12px"}) for p in products],
                    ], style={"flex": "1"}),
                ], style={"display": "flex", "alignItems": "center", "gap": "16px"}),
            ]),
        ], style={"display": "flex", "gap": "10px", "marginBottom": "16px", "flexWrap": "wrap"}),

        # ── Row 3: Net Profit + CAC ──
        html.Div([
            card([
                panel_header("Monthly contribution · USD", "Net Profit"),
                dcc.Graph(figure=profit_fig, config={"displayModeBar": False}),
            ]),
            card([
                panel_header("USD per new customer", "Customer Acquisition Cost"),
                dcc.Graph(figure=cac_fig, config={"displayModeBar": False}),
            ]),
        ], style={"display": "flex", "gap": "10px", "marginBottom": "16px", "flexWrap": "wrap"}),

        # ── Recent Transactions ──
        card([
            html.Div([
                panel_header("Live feed · last 24h", "Recent Transactions"),
                html.Div([
                    html.Span("●", style={"color": GREEN, "fontSize": "8px", "marginRight": "5px"}),
                    html.Span("live", style={"color": GREEN, "fontSize": "9px",
                                              "fontFamily": FONT_MONO, "fontWeight": "600",
                                              "letterSpacing": "0.1em"}),
                ], style={"display": "flex", "alignItems": "center",
                           "background": "rgba(16,217,138,0.08)",
                           "border": "1px solid rgba(16,217,138,0.2)",
                           "padding": "3px 10px", "borderRadius": "20px",
                           "marginBottom": "14px"}),
            ], style={"display": "flex", "justifyContent": "space-between",
                       "alignItems": "flex-start"}),

            # Table header
            html.Div([
                html.Div("ID",       style={"color": MUTED, "fontSize": "9px", "flex": "0.7",
                                             "fontFamily": FONT_MONO, "letterSpacing": "0.1em",
                                             "textTransform": "uppercase"}),
                html.Div("Customer", style={"color": MUTED, "fontSize": "9px", "flex": "1.2",
                                             "fontFamily": FONT_MONO, "letterSpacing": "0.1em",
                                             "textTransform": "uppercase"}),
                html.Div("Product",  style={"color": MUTED, "fontSize": "9px", "flex": "1.2",
                                             "fontFamily": FONT_MONO, "letterSpacing": "0.1em",
                                             "textTransform": "uppercase"}),
                html.Div("Amount",   style={"color": MUTED, "fontSize": "9px", "flex": "0.6",
                                             "fontFamily": FONT_MONO, "letterSpacing": "0.1em",
                                             "textTransform": "uppercase", "textAlign": "right"}),
                html.Div("Status",   style={"color": MUTED, "fontSize": "9px", "flex": "0.6",
                                             "fontFamily": FONT_MONO, "letterSpacing": "0.1em",
                                             "textTransform": "uppercase", "textAlign": "right"}),
            ], style={
                "display": "flex", "padding": "0 0 8px",
                "borderBottom": f"1px solid {BORDER}",
            }),

            # Rows
            *[html.Div([
                html.Div(tx["id"], style={
                    "color": MUTED, "fontSize": "10px", "flex": "0.7",
                    "fontFamily": FONT_MONO,
                }),
                html.Div(tx["customer"], style={
                    "color": TEXT, "fontSize": "11px", "flex": "1.2",
                    "fontFamily": FONT_BODY, "fontWeight": "500",
                }),
                html.Div(tx["product"], style={
                    "color": MUTED, "fontSize": "11px", "flex": "1.2",
                    "fontFamily": FONT_BODY,
                }),
                html.Div(tx["amount"], style={
                    "color": TEXT, "fontSize": "11px", "flex": "0.6",
                    "fontFamily": FONT_MONO, "fontWeight": "600",
                    "textAlign": "right",
                }),
                html.Div(status_pill(tx["status"]), style={
                    "flex": "0.6", "textAlign": "right",
                }),
            ], style={
                "display": "flex", "alignItems": "center",
                "padding": "12px 0",
                "borderBottom": f"1px solid {BORDER}22",
            }) for tx in transactions],

        ], min_w="100%"),

        # Footer
        html.Div([
            html.Span("STARTUP.OS · v1.0", style={
                "color": DIM, "fontSize": "9px", "fontFamily": FONT_DISPLAY,
                "letterSpacing": "0.14em",
            }),
            html.Span("All figures simulated for demo purposes", style={
                "color": DIM, "fontSize": "9px", "fontFamily": FONT_MONO,
            }),
        ], style={
            "display": "flex", "justifyContent": "space-between",
            "padding": "20px 0 4px",
        }),

    ], style={"padding": "28px 36px", "maxWidth": "1400px", "margin": "0 auto"}),

], style={"minHeight": "100vh", "background": BG, "fontFamily": FONT_BODY})


if __name__ == "__main__":
    app.run(debug=True, port=8053)
