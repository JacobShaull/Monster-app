import altair as alt
from pandas import DataFrame

# Define the properties for the chart
properties = {
    'width': 400,   # Width of the chart
    'height': 300,  # Height of the chart
    'background': 'transparent',  # Background color of the chart
    'padding': 5    # Padding around the chart
}

def chart(df: DataFrame, x: str, y: str, target: str) -> alt.Chart:
    # Create an Altair chart object
    return alt.Chart(df).mark_circle().encode(
        x=x,  # x-axis
        y=y,  # y-axis
        color=target,  # Color encoding
        tooltip=[x, y, target]  # Tooltip information
    ).properties(**properties).interactive()  # Apply properties and make the chart interactive
