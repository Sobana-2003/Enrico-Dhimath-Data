import streamlit as st
import streamlit.components.v1 as components  
import json
import pandas as pd

    
st.set_page_config(layout="wide")

def line_graph(
            df: pd.DataFrame,
            title: str,
            legend: list[str],
            x_label: str,
            y_label: str,
            series_names: list[str],
            colours: list[str],
            height: str = "600px",  
            width: str = "45%"       
        ):
    """
    Renders a line graph using streamlit-echarts.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing the data to be plotted.
        title (str): Title of the graph.
        legend (list[str]): List of legend labels for each series.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        series_names (list[str]): List of y-axis series names for each line.
        colours (list[str]): List of colours for each line in the chart.
        height (str, optional): Height of the chart. Defaults to "500px".
        width (str, optional): Width of the chart. Defaults to "100%".

    Returns:
        Apache eCharts Graph rendered in streamlit.
    """
    latest_values = df.iloc[-1, 1:]
    y_min = float(latest_values.min())
    y_max = float(latest_values.max())

    options = {
        "title": {"text": title,
                  "textStyle": {
                      "color": "black",
                      "fontSize": 18,
                      "fontWeight": "bold",
                  }},
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": list(df.iloc[:, 0]),
            "name": x_label,
            "nameLocation": 'middle',
            "nameGap": 55,
            "nameTextStyle": {
                "color": "black",
                "fontSize": 14,
                "fontWeight": "bold"
            },
            "splitLine": {
                "lineStyle": {
                    "color": "#899499"
                }
            },
            "axisLabel": {
                "color": "black",
                "fontSize": 12,
            },
        },
        "yAxis": {
            "type": "value",
            "name": y_label,
            "scale": True,
            "min": "dataMin",
            "max": "dataMax",
            "nameLocation": 'middle',
            "nameGap": 55,
            "nameTextStyle": {
                "color": "black",
                "fontSize": 14,
                "fontWeight": "bold"
            },
            "splitLine": {
                "lineStyle": {
                    "color": "#899499"
                }
            },
            "axisLabel": {
                "color": "black",
                "fontSize": 12,
            },
        },
        "legend": {"data": legend,
                   "textStyle": {
                       "color": "black",
                       "fontSize": 12,
                       "fontWeight": "bold",
                   }},
          "dataZoom": [
            {
                "type": "inside",      
                "xAxisIndex": 0,       
                "start": 0,            
                "end": 100,            
                "zoomOnMouseWheel": True  
                },
            ],
            "stateAnimation": {
                "animation": 'auto',
                "animationDuration": 1000,
                "animationDurationUpdate": 500,
                "animationEasing": 'cubicInOut',
                "animationEasingUpdate": 'cubicInOut',
                "animationThreshold": 2000,
                "progressiveThreshold": 3000,
                "progressive": 400,
                "hoverLayerThreshold": 3000,
                "useUTC": False
            },
            "series": [
                {
                    "name": series_names[i-1],
                    "type": "line",
                    "data": [round(val, 2) for val in df.iloc[:, i]],
                    "color": colours[i-1],
                    "smooth": True
                }
                for i in range(1, len(df.columns))
            ],
    }
    render_chart(options, height, width, "line-chart")
    return

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    dept_col = None
    for col in df.columns:
        if col.strip().lower() == "department":
            dept_col = col
            break
    if dept_col is None:
        st.error("No 'Department' column found in the uploaded Excel.")
        return df
    if dept_col != "Department":
        df = df.rename(columns={dept_col: "Department"})
    
    df['Department'] = df['Department'].ffill()
    pivot_df = df.pivot_table(index='Department', columns='Gender', values='Count', aggfunc='sum', fill_value=0).reset_index()
    if 'Male' not in pivot_df.columns:
        pivot_df['Male'] = 0
    if 'Female' not in pivot_df.columns:
        pivot_df['Female'] = 0
    return pivot_df

def render_chart(options: dict, chart_id: str):
    json_options = json.dumps(options)

    html = f"""
    <html>
      <head>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
      </head>
      <body>
        <div id="{chart_id}" style="width:500px; height:500px;"></div>
        <script>
          var chart = echarts.init(document.getElementById('{chart_id}'), null, {{ width: 500, height: 500 }});
          var option = {json_options};
          chart.setOption(option);
        </script>
      </body>
    </html>
    """
    components.html(html, height=500, width=500)

def display_charts(df: pd.DataFrame):
    departments = df['Department'].tolist()
    male_counts = df['Male'].tolist()
    female_counts = df['Female'].tolist()

    stacked_option = {
        "title": {"text": "Stacked Chart", "left": "center"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": ["Male", "Female"], "bottom": 0},
        "xAxis": {"type": "category", "data": departments},
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Female",
                "type": "bar",
                "stack": "total",
                "data": female_counts,
                "barWidth": 60,
                "color": "#abcdef",
                "label": {
                    "show": True,
                    "position": "inside"
                }
            },
            {
                "name": "Male",
                "type": "bar",
                "stack": "total",
                "data": male_counts,
                "barCategoryGap": "40%",
                "barWidth": 60,
                "color": "#36A2EB",
                "label": {
                    "show": True,
                    "position": "inside"
                }
            }
        ]
    }
    
    grouped_option = {
        "title": {"text": "Grouped Chart", "left": "center"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "legend": {"data": ["Male", "Female"], "bottom": 0},
        "xAxis": {"type": "category", "data": departments},
        "yAxis": {"type": "value"},
        "series": [
            {
                "name": "Male",
                "type": "bar",
                "data": male_counts,
                "color": "#36A2EB",
                "barCategoryGap": "40%",
                "barGap": "0%",
                "label": {
                    "show": True,
                    "position": "inside"
                }
            },
            {
                "name": "Female",
                "type": "bar",
                "data": female_counts,
                "color": "#abcdef",
                "barCategoryGap": "40%",
                "barGap": "0%",
                "label": {
                    "show": True,
                    "position": "inside"
                }
            }
        ]
    }

    st.markdown("<div style='display: flex; justify-content: space-around;'>", unsafe_allow_html=True)
    left, right = st.columns([50,50])
    with left:
        render_chart(stacked_option, "stacked-chart")
    with right:     
        render_chart(grouped_option, "grouped_option")

    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    st.title("Excel Data Visualization")        
    
    uploaded_file = f"G:\\XLS Data\\e_charts_data.xlsx"
    df = pd.read_excel(uploaded_file)
    c1, c2 = st.columns([50,50])
    with c1:    
        st.write("Raw Data from Excel:", df)
    
    df_processed = process_data(df)
    with c2:
        st.write("Processed Data:", df_processed)
    
    display_charts(df_processed)

if __name__ == "__main__":
    main()