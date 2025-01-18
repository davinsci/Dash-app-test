from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    "Category": ["A", "B", "C"],
    "Values": [10, 20, 30]
})

app = Dash(__name__)
# server = app.server  # Expose the Flask server

app.layout = html.Div([
    html.H1("Simple Dash App"),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": col, "value": col} for col in df.columns],
        value="Values"
    ),
    dcc.Graph(id="bar-chart")
])

@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")]
)
def update_chart(selected_column):
    fig = px.bar(df, x="Category", y=selected_column, title=f"{selected_column} Bar Chart")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
