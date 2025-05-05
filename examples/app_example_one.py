# Import packages
from dash import Dash, html, dash_table
import pandas as pd

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
#df = pd.read_csv('RED SOX - Mustang 9 Winter 2024-2025 Stats.csv')

# If using a csv on the same pc, save it in the same folder as app.py and update this line to: df = pd.read_csv('NameOfYourFile.csv')
# If you are using an Excel sheet: 'pip install openpyxl' then use: df = pd.read_excel('NameOfYourFile.xlsx', sheet_name='Sheet1')

# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)