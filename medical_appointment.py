import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Loading the preprocessed data
df = pd.read_csv("Medical_Appointment/preprocessed_data.csv")


app = Dash(__name__)
app.title = "Medical Appointment No-Show Dashboard"


# Layout
app.layout = html.Div(style={'display': 'flex', 'backgroundColor': '#0e1726', 'minHeight': '100vh', 'fontFamily': 'Arial'}, children=[

    # Sidebar
    html.Div(style={
        'width': '300px',
        'backgroundColor': '#1f2c43',
        'padding': '20px',
        'display': 'flex',
        'flexDirection': 'column',
        'gap': '20px',
        'boxShadow': '2px 0px 10px rgba(0,0,0,0.5)'
    }, children=[
        html.H2("Filters", style={'color': 'white',
                'textAlign': 'center', 'marginBottom': '20px'}),

        html.Div(children=[
            html.Label("Select Neighborhood:", style={'color': '#ffffffcc'}),
            dcc.Dropdown(
                id="select_neighborhood",
                options=[{"label": n, "value": n}
                         for n in sorted(df["neighbourhood"].dropna().unique())],
                placeholder="All neighborhoods",
                style={'color': '#000'}
            )
        ]),
        # Select Gender
        html.Div(children=[
            html.Label("Select Gender:", style={'color': '#ffffffcc'}),
            dcc.Dropdown(
                id="gender_filter",
                options=[
                    {"label": "All Genders", "value": "All"},
                    {"label": "Female", "value": "F"},
                    {"label": "Male", "value": "M"}
                ],
                value="All",
                clearable=False,
                style={'color': '#000'}
            )
        ]),
        # Age Slider
        html.Div(children=[
            html.Label("Select Age Range:", style={'color': '#ffffffcc'}),
            dcc.RangeSlider(
                id="age_slider",
                min=int(df["age"].min()),
                max=int(df["age"].max()),
                step=1,
                value=[int(df["age"].min()), int(df["age"].max())],
                marks={
                    int(df["age"].min()): str(int(df["age"].min())),
                    int((df["age"].min() + df["age"].max()) // 2): str(int((df["age"].min() + df["age"].max()) // 2)),
                    int(df["age"].max()): str(int(df["age"].max())),
                },
                tooltip={"always_visible": True}
            )
        ]),

        # Pies below the age slider
        html.Div(style={'display': 'flex', 'flexDirection': 'column', 'gap': '15px', 'height': 'calc(100vh - 200px)'}, children=[

            html.Div(style={
                'backgroundColor': '#1f2c43',
                'padding': '10px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.3)',
                'flex': '1'
            }, children=[
                dcc.Graph(id='scholarship_pie', style={'height': '100%'})
            ]),

            html.Div(style={
                'backgroundColor': '#1f2c43',
                'padding': '10px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.3)',
                'flex': '1'
            }, children=[
                dcc.Graph(id='sms_pie', style={'height': '100%'})
            ]),

            html.Div(style={
                'backgroundColor': '#1f2c43',
                'padding': '10px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.3)',
                'flex': '1'
            }, children=[
                dcc.Graph(id='handcap_pie', style={'height': '100%'})
            ]),
        ])
    ]),

    # Main Content
    html.Div(style={'flex': '1', 'padding': '20px'}, children=[

        html.H1("Medical Appointment Analysis", style={
            'textAlign': 'center', 'color': 'white', 'marginBottom': '20px', 'fontFamily': 'Arial Black'
        }),
        html.Div(id='output_container', style={
                 'marginTop': '10px', 'textAlign': 'center'}),

        # KPI Section
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}, children=[
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '15px', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                html.H3("Total Appointments", style={'color': 'white'}),
                html.H2(id="total_appointments", style={'color': 'white'})
            ]),
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '15px', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                html.H3("No-Show Rate", style={'color': 'white'}),
                html.H2(id="total_no_show_rate", style={'color': 'white'})
            ]),
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '15px', 'borderRadius': '10px', 'textAlign': 'center', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                html.H3("Average Days Until Appointment",
                        style={'color': 'white'}),
                html.H2(id="avg_days_until", style={'color': 'white'})
            ]),
        ]),

        # Bar charts side by side
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}, children=[
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '15px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                dcc.Graph(id='neighborhood_map', style={'height': '400px'})
            ]),
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '15px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                dcc.Graph(id='days_until_appointment',
                          style={'height': '400px'})
            ])
        ]),

        # Three pies below screen
        html.Div(style={'display': 'flex', 'gap': '20px', 'height': 'calc(100vh - 600px)'}, children=[
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                dcc.Graph(id='hipertension_pie', style={'height': '100%'})
            ]),
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                dcc.Graph(id='diabetes_pie', style={'height': '100%'})
            ]),
            html.Div(style={'flex': '1', 'backgroundColor': '#1f2c43', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.3)'}, children=[
                dcc.Graph(id='alcoholism_pie', style={'height': '100%'})
            ])
        ])
    ])
])


# Callback
@app.callback(
    [
        Output('output_container', 'children'),
        Output('total_appointments', 'children'),
        Output('total_no_show_rate', 'children'),
        Output('avg_days_until', 'children'),
        Output('neighborhood_map', 'figure'),
        Output('scholarship_pie', 'figure'),
        Output('sms_pie', 'figure'),
        Output('handcap_pie', 'figure'),
        Output('hipertension_pie', 'figure'),
        Output('diabetes_pie', 'figure'),
        Output('alcoholism_pie', 'figure'),
        Output('days_until_appointment', 'figure'),
    ],
    [
        Input('gender_filter', 'value'),
        Input('select_neighborhood', 'value'),
        Input('age_slider', 'value'),
    ]
)
# updating graphs
def update_graph(selected_gender, selected_neigh, age_range):
    container = html.Span(
        f"Filters >> Neighborhood: {selected_neigh if selected_neigh else 'All'}, "
        f"Age: {age_range[0]} - {age_range[1]}, "
        f"Gender: {selected_gender}",
        style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '18px'}
    )

    dff = df.copy()

    # Input Handle
    if selected_neigh:
        dff = dff[dff["neighbourhood"] == selected_neigh]
    dff = dff[(dff["age"] >= age_range[0]) & (dff["age"] <= age_range[1])]
    if selected_gender != "All":
        dff = dff[dff["gender"] == selected_gender]

    # KPIs
    total_appts = len(dff)
    no_show_rate = f"{(dff['no_show'] == 'Yes').mean()*100:.1f}%"
    avg_days = f"{dff['days_until_appointment'].mean():.1f}"

    # Neighborhood map
    neighborhood_data = dff.groupby('neighbourhood')['no_show'].apply(
        lambda x: (x == "Yes").mean()).reset_index(name='no_show_rate')
    map_fig = px.bar(
        neighborhood_data.sort_values('no_show_rate', ascending=False),
        x='neighbourhood', y='no_show_rate', color='no_show_rate',
        color_continuous_scale='Viridis',
        title='No-show Rates by Neighborhood',
        labels={'no_show_rate': 'No-show Rate',
                'neighbourhood': 'Neighborhood'}
    )
    map_fig.update_yaxes(
        tickformat=".0%"
    )
    map_fig.update_layout(
        template="plotly_dark"
    )

    # Pie for Scholarship
    sch_grouped = dff.groupby(
        ['scholarship', 'no_show']).size().reset_index(name='count')
    scholarship_pie = px.pie(
        sch_grouped, names='no_show',
        values='count',
        title='By Scholarship',
        color='no_show',
        color_discrete_map={'Yes': '#EF553B', 'No': '#00CC96'},
        hole=0.3
    )
    scholarship_pie.update_layout(
        template="plotly_dark",
        margin=dict(t=40, b=20, l=20, r=20),
        title_font_size=18,
        legend_title_font_size=14
    )

    # Pie for SMS Received
    sms_grouped = dff.groupby(
        ['sms_received', 'no_show']).size().reset_index(name='count')
    sms_pie = px.pie(
        sms_grouped, names='no_show',
        values='count',
        title='By SMS Received',
        color='no_show',
        color_discrete_map={'Yes': '#EF553B', 'No': '#00CC96'},
        hole=0.3
    )
    sms_pie.update_layout(
        template="plotly_dark",
        margin=dict(t=40, b=20, l=20, r=20),
        title_font_size=18,
        legend_title_font_size=14)

    # Pie for Handicap
    handcap_grouped = dff.groupby(
        ['handcap', 'no_show']).size().reset_index(name='count')
    handcap_pie = px.pie(
        handcap_grouped,
        names='no_show',
        values='count',
        title='By Disability',
        color='no_show',
        color_discrete_map={'Yes': '#EF553B', 'No': '#00CC96'},
        hole=0.3
    )
    handcap_pie.update_layout(
        template="plotly_dark",
        margin=dict(t=40, b=20, l=20, r=20),
        title_font_size=18,
        legend_title_font_size=14
    )

    # Pie for Hypertension
    hip_grouped = dff.groupby(
        ['hipertension', 'no_show']).size().reset_index(name='count')
    hipertension_pie = px.pie(
        hip_grouped,
        names='no_show',
        values='count',
        title='By Hypertension',
        color='no_show',
        color_discrete_map={'Yes': '#EF553B', 'No': '#00CC96'},
        hole=0.3
    )
    hipertension_pie.update_layout(
        template="plotly_dark",
        margin=dict(t=40, b=20, l=20, r=20),
        title_font_size=18,
        legend_title_font_size=14
    )

    # Pie for Diabetes
    diab_grouped = dff.groupby(
        ['diabetes', 'no_show']).size().reset_index(name='count')
    diabetes_pie = px.pie(
        diab_grouped,
        names='no_show',
        values='count',
        title='By Diabetes',
        color='no_show',
        color_discrete_map={'Yes': '#EF553B', 'No': '#00CC96'},
        hole=0.3
    )
    diabetes_pie.update_layout(
        template="plotly_dark",
        margin=dict(t=40, b=20, l=20, r=20),
        title_font_size=18,
        legend_title_font_size=14
    )

    # Pie for Alcoholism
    alc_grouped = dff.groupby(
        ['alcoholism', 'no_show']).size().reset_index(name='count')
    alcoholism_pie = px.pie(
        alc_grouped,
        names='no_show',
        values='count',
        title='By Alcoholism',
        color='no_show',
        color_discrete_map={'Yes': '#EF553B', 'No': '#00CC96'},
        hole=0.3
    )
    alcoholism_pie.update_layout(
        template="plotly_dark",
        margin=dict(t=40, b=20, l=20, r=20),
        title_font_size=18,
        legend_title_font_size=14
    )

    # Days until appointment histogram
    bins = [0, 3, 7, 14, df['days_until_appointment'].max()+1]
    labels = ['0-3', '4-7', '8-14', '15+']
    dff['days_bin'] = pd.cut(
        dff['days_until_appointment'], bins=bins, labels=labels, right=False)
    hist_data = dff.groupby(['days_bin', 'no_show']
                            ).size().reset_index(name='count')
    hist_pivot = hist_data.pivot(
        index='days_bin',
        columns='no_show',
        values='count').fillna(0)
    hist_pivot_pct = hist_pivot.div(hist_pivot.sum(axis=1), axis=0)*100
    hist_pivot_pct = hist_pivot_pct.reset_index()
    hist_fig = px.bar(hist_pivot_pct,
                      x='days_bin',
                      y=['No', 'Yes'],
                      labels={'value': 'Percentage of Appointments',
                              'days_bin': 'Days Until Appointment', 'variable': 'No Show?'},
                      title='Show vs No-Show by Appointment Delay (%)')
    hist_fig.update_layout(
        template='plotly_dark',
        barmode='stack',
        yaxis=dict(ticksuffix='%'),
        bargap=0.2
    )

    return (
        container,
        total_appts,
        no_show_rate,
        avg_days,
        map_fig,
        scholarship_pie,
        sms_pie,
        handcap_pie,
        hipertension_pie,
        diabetes_pie,
        alcoholism_pie,
        hist_fig
    )


if __name__ == "__main__":
    app.run(debug=True)
