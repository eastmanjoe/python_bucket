import plotly.offline as py
import plotly.graph_objs as go
import numpy as np

voltage_a_angle = 0.0
voltage_b_angle = 239.0
voltage_c_angle = 131.0
voltage_an = 206.23
voltage_bn = 221.30
voltage_cn = 217.09
current_a_angle = -10.23
current_b_angle = -7.20
current_c_angle = -7.00
current_a = 915.35
current_b = 892.41
current_c = 892.69

current_vector = go.Scatter(
    r = [current_a, current_b, current_c],
    t = [voltage_a_angle - current_a_angle, voltage_b_angle - current_b_angle, voltage_c_angle - current_c_angle],
    mode='markers',
    name='Current',
    # symbol="diamond",
    line=dict(
        color='rgb(27,158,119)',
        ),
    marker=dict(
        color='rgb(27,158,119)',
        size=110,
        line=dict(
            color='white'
        ),
        opacity=0.7
    )
)
voltage_vector = go.Scatter(
    r=[voltage_an, voltage_bn, voltage_cn],
    t=[voltage_a_angle, voltage_b_angle, voltage_c_angle],
    mode='markers',
    name='Voltage',
    # symbol="diamond",
    line=dict(
        color='rgb(217,95,2)',
        ),
    marker=dict(
        color='rgb(217,95,2)',
        size=110,
        line=dict(
            color='white'
        ),
        opacity=0.7
    )
)

data = [current_vector, voltage_vector]
layout = go.Layout(
    title='Phasor Diagram',
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(223, 223, 223)',
    angularaxis=dict(
        tickcolor='rgb(253,253,253)'
    )
)
fig = go.Figure(data=data, layout=layout)
py.plot(fig)
