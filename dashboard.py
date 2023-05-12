import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button("Start Simulation", id="start_simulation"),
    dcc.Graph(id="cost_comparison")
])

@app.callback(
    Output("cost_comparison", "figure"),
    [Input("start_simulation", "n_clicks")])
def update_cost_comparison(n_clicks):
    if n_clicks is None:
        return go.Figure()

    # Run the simulations and get the costs
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map_async(func, [cdn_simulation, frontloaded_simulation])
        cdn_cost, frontloading_cost = results.get()

    # bar chart
    trace = go.Bar(
        x=['CDN', 'Frontloading'],
        y=[cdn_cost, frontloading_cost],
        text=[cdn_cost, frontloading_cost],
        textposition='auto'
    )

    data = [trace]
    layout = go.Layout(title="Cost Comparison: CDN vs. Frontloading")
    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
