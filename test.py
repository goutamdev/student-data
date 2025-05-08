import pandas as pd
import plotly.graph_objects as go
import json


# Calculate the average total cost per city for each country
average_costs = df.groupby(['Country', 'City'])['Total'].mean().reset_index()

# Get the list of unique countries
countries = average_costs['Country'].unique()

# Define background and grid colors
plot_bgcolor = '#f9f9f9'
gridcolor = '#d3d3d3'

# Create a dictionary to store the chart configurations (JSON strings)
chart_configs = {}

# Iterate through each country and create the chart configuration
for country in countries:
    country_data = average_costs[average_costs['Country'] == country]

    fig = go.Figure(data=[go.Bar(x=country_data['City'], y=country_data['Total'])])

    fig.update_layout(
        title=f"Average Total Cost in {country} by City",
        xaxis_title="City",
        yaxis_title="Average Total Cost (USD)",
        plot_bgcolor=plot_bgcolor,
        xaxis=dict(gridcolor=gridcolor),
        yaxis=dict(gridcolor=gridcolor)
    )

    # Convert the Plotly figure to a JSON string
    chart_configs[country] = fig.to_json()

# Save the chart configurations to a JSON file (optional)
with open("chart_configs.json", "w") as f:
    json.dump(chart_configs, f, indent=4)

# Construct the HTML content using string concatenation
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Average Study Abroad Costs</title>
    <style>
        body { font-family: sans-serif; margin: 0; padding: 20px; background-color: """ + plot_bgcolor + """; }
        h1 { text-align: center; color: #333; }
        .chart-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .chart {
            margin-bottom: 20px;
            box-sizing: border-box;
            width: calc(100%); /* Two charts per row for wider screens */
            height: 50%; /* Ensure charts have a minimum height */
        }
        /* Media query for mobile devices (max-width: 600px) */
        @media (max-width: 600px) {
            .chart {
                width: 100%; /* One chart per row for smaller screens */
            }
        }
    </style>
    <script src="https://cdn.plot.ly/plotly-2.27.1.min.js"></script>
</head>
<body>
    <h1>Average Total Study Abroad Costs by Country</h1>
    <div class="chart-container" id="chartContainer">
    </div>
    <script>
    const chartContainer = document.getElementById('chartContainer');
    const chartConfigs = """ + json.dumps(chart_configs) + """;

    const config = {
        displayModeBar: false,   // Hides mode bar
        displaylogo: false       // Optional: hides the Plotly logo
    };

    for (const country in chartConfigs) {
        if (chartConfigs.hasOwnProperty(country)) {
            const chartDiv = document.createElement('div');
            chartDiv.classList.add('chart');
            chartContainer.appendChild(chartDiv);

            const chartData = JSON.parse(chartConfigs[country]);
            const data = chartData.data || [];
            const layout = chartData.layout || {};

            Plotly.newPlot(chartDiv, data, layout, config);
        }
    }
</script>


</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)

print("HTML file (index.html) created to display charts using Plotly.js.")
