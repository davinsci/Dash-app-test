from dash import Dash
import dash_html_components as html

app = Dash(__name__)
app.layout = html.Div("Hello, Dash!")

if __name__ == "__main__":
    app.run_server(debug=True)
