"""Paleta e tema Plotly comuns (paleta categórica validada para daltonismo, ordem fixa)."""
import plotly.graph_objects as go
import plotly.io as pio

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
DIV = [[0.0, "#e34948"], [0.5, "#f0efec"], [1.0, "#2a78d6"]]  # negativo → neutro → positivo
STATUS = {"good": "#0ca30c", "warning": "#fab219", "serious": "#ec835a", "critical": "#d03b3b"}
TEXT, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"

pio.templates["estudio"] = go.layout.Template(
    layout=dict(
        font=dict(family="Inter, Segoe UI, Arial, sans-serif", size=13, color=TEXT),
        colorway=SERIES,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=SURFACE,
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID, tickfont=dict(color=MUTED)),
        legend=dict(orientation="h", y=-0.18, x=0, font=dict(color=MUTED)),
        margin=dict(l=40, r=20, t=50, b=40),
        hoverlabel=dict(bgcolor="white", font_size=12),
        title=dict(font=dict(size=15)),
        bargap=0.25,
    )
)
pio.templates.default = "plotly_white+estudio"


def quad_shapes(fig, xmid, ymid, xr, yr, labels, colors=None):
    """Desenha linhas de quadrante e rótulos nos cantos (labels: TL, TR, BL, BR)."""
    fig.add_vline(x=xmid, line_dash="dot", line_color=MUTED, line_width=1)
    fig.add_hline(y=ymid, line_dash="dot", line_color=MUTED, line_width=1)
    pos = {"TL": (xr[0], yr[1], "left", "top"), "TR": (xr[1], yr[1], "right", "top"),
           "BL": (xr[0], yr[0], "left", "bottom"), "BR": (xr[1], yr[0], "right", "bottom")}
    for k, txt in labels.items():
        x, y, xa, ya = pos[k]
        fig.add_annotation(x=x, y=y, text=f"<b>{txt}</b>", showarrow=False, xanchor=xa, yanchor=ya,
                           font=dict(size=11, color=MUTED), bgcolor="rgba(255,255,255,0.7)")
    fig.update_xaxes(range=xr)
    fig.update_yaxes(range=yr)
    return fig
