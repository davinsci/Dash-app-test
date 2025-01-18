import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import os
import json

# Write the credentials to a temp file
credentials_path = "/tmp/google_credentials.json"
with open(credentials_path, "w") as f:
    f.write(os.getenv("GOOGLE_CREDENTIALS"))

# Use gspread to access Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)

# Open the Google Sheet by its URL or name
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1BAG7bG6ZaQvubJMrakCjawf4DPS-nDJH7TFcjxDpHE8/edit")

# Select a worksheet (e.g., the first sheet)
worksheet = spreadsheet.get_worksheet(0)

# Fetch all data as a list of dictionaries
data = worksheet.get_all_records()

# Convert to a Pandas DataFrame
df = pd.DataFrame(data)

# Initialize the Dash app
app = Dash(__name__)

# External stylesheets (optional, for better aesthetics)
app.css.config.serve_locally = False

app.layout = html.Div([
    html.H1("Google Sheet Data Dashboard"),
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": col, "value": col} for col in df.columns],
        value=df.columns[0],  # Default value
        placeholder="Select a column"
    ),
    dcc.Graph(id="bar-chart"),
])

@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")]
)
def update_chart(selected_column):
    fig = px.bar(df, x=df.index, y=selected_column, title=f"{selected_column} Bar Chart")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
