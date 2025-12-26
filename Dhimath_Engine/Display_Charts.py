import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import altair as alt


def plot_bar_chart(df, colour_picker):
    if len(df.columns) == 1:
        df['Row Number'] = range(1, len(df) + 1)
        bar_chart = st.bar_chart(df, x='Row Number', y=df.columns[0], color=[colour_picker], height=540)
    else:
        bar_chart = st.bar_chart(df, x=df.columns[0], y=df.columns[1], color=[colour_picker], height=540)
    return bar_chart

def plot_altair_bar_chart(df, colour_picker, palette, categorical_cols, numerical_cols, date_cols):
    number_of_columns = len(df.columns)
    number_of_rows = len(df.index)
    if number_of_columns == 1 or number_of_rows == 1:
        # st.warning("Graph cannot be plotted for single column or single row data.")
        c1,c2,c3 = st.columns([30,40,30])
        with c2:
            st.metric(df.columns[0], "{:.3f}".format(df.iloc[0, 0]))
        # # st.write("Only one column")
        # df['Row Number'] = range(1, len(df) + 1)
        # bar_chart = st.bar_chart(df, x='Row Number', y=df.columns[0], color=[colour_picker], height=540)
    
    if number_of_columns == 2:
        # bar_chart = st.bar_chart(df, x=df.columns[0], y=df.columns[1], color=[colour_picker], height=540)
        bar_chart = alt.Chart(df).mark_bar(size=30).encode(
                                                        x=df.columns[0],    
                                                        y=df.columns[1],
                                                        color=alt.value(colour_picker)
                                                        ).properties(height=540)
        st.altair_chart(bar_chart, use_container_width=True)
    
    if number_of_columns == 3:
        custom_palette = palette
        # bar_chart = st.bar_chart(df, x=df.columns[0], y=df.columns[1], color=[colour_picker], height=540)
        bar_chart = alt.Chart(df).mark_bar(size=30).encode(
                                                        x=df.columns[0],    
                                                        y=df.columns[2],
                                                        color=alt.Color(df.columns[1], scale=alt.Scale(range=custom_palette)),
                                                        ).properties(height=540)
        st.altair_chart(bar_chart, use_container_width=True)
    return bar_chart

def plot_altair_grouped_bar_chart(df, palette,  categorical_cols, numerical_cols, date_cols):
    number_of_columns = len(df.columns)
    if number_of_columns == 1:
        st.write("Only one column")
        df['Row Number'] = range(1, len(df) + 1)
        bar_chart = st.bar_chart(df, x='Row Number', y=df.columns[0], color=[palette[1]], height=540)
    
    if number_of_columns == 2:
        # bar_chart = st.bar_chart(df, x=df.columns[0], y=df.columns[1], color=[colour_picker], height=540)
        bar_chart = alt.Chart(df).mark_bar().encode(
                                                        x=df.columns[0],    
                                                        y=df.columns[1],
                                                        color=alt.value(palette[1])
                                                        ).properties(height=540)
        st.altair_chart(bar_chart, use_container_width=True)
    
    if number_of_columns == 3:
        custom_palette = palette
        # bar_chart = st.bar_chart(df, x=df.columns[0], y=df.columns[1], color=[colour_picker], height=540)
        bar_chart = alt.Chart(df).mark_bar().encode(
                                                        x=alt.X(f"{df.columns[0]}:N"),
                                                        xOffset=f"{df.columns[1]}:N",
                                                        y=alt.Y(f"{df.columns[2]}:Q"),
                                                        color=alt.Color(df.columns[1], scale=alt.Scale(range=custom_palette))
                                                        ).properties(height=540)
        st.altair_chart(bar_chart, use_container_width=True)
    return bar_chart

def plot_line_chart(df, colour_picker):
    if len(df.columns) == 1:
        df['Row Number'] = range(1, len(df) + 1)
        line_chart = st.line_chart(df, x='Row Number', y=df.columns[0], color=[colour_picker], height=540)
    else:
        line_chart = st.line_chart(df, x=df.columns[0], y=df.columns[1], color=[colour_picker], height=540)
    return line_chart

def plot_area_chart(df, colour_picker):
    if len(df.columns) == 1:
        df['Row Number'] = range(1, len(df) + 1)
        area_chart = st.area_chart(df, x='Row Number', y=df.columns[0], color=[colour_picker], height=540)
    else:
        area_chart = st.area_chart(df, x=df.columns[0], y=df.columns[1], color=[colour_picker], height=540)
    return area_chart

def plot_scatter_chart(df):
    if df[df.columns[0]].dtype == 'object' or df[df.columns[1]].dtype == 'object':
        st.warning("Scatter chart cannot be plotted for categorical columns.")
        return None
    scatter_chart = st.scatter_chart(df, x=df.columns[0], y=df.columns[1], color=["#F77A52"], height=540)
    return scatter_chart


# def plot_pie_chart(df):
#     category_col = df.columns[0]
#     value_col = df.columns[1]

#     if df[value_col].dtype not in ['int64', 'float64']:
#         st.warning("Numerical values for a pie chart.")
#         return None
#     c1,c2,c3 = st.columns([20,60,20])
#     with c2:
#         st.header("")
#         st.subheader("")
#         fig, ax = plt.subplots()
#         ax.pie(df[value_col], labels=df[category_col], autopct='%1.1f%%', startangle=90, counterclock=False)
#         ax.axis('equal')
#         st.pyplot(fig)

def plot_pie_chart(df, colors=None):
    category_col = df.columns[0]
    value_col = df.columns[1]

    if df[value_col].dtype not in ['int64', 'float64']:
        st.warning("Numerical values required for a pie chart.")
        return None

    if colors is None or len(colors) < len(df):
        st.warning("Insufficient colors provided for the data. Please provide at least as many colors as categories.")
        return None
    c1,c2,c3 = st.columns([20,60,20])
    with c2:
        st.header("")
        # st.subheader("")
        fig, ax = plt.subplots()
        ax.pie(df[value_col], labels=df[category_col], colors=colors[:len(df)], autopct='%1.1f%%', startangle=90,
            counterclock=False)
        ax.axis('equal')
        st.pyplot(fig)


@st.fragment
def display_charts():
    palette_colors = [
                    "#5A6FC0",
                    "#9ECA7E",
                    "#0CA6E9",
                    "#3579BB",
                    "#9B87F5",
                    "#862934",
                    "#b22226",
                    "#a22d59",
                    "#473d88",
                    "#243d80",
                    "#27559a",
                    "#3693bf",
                    "#10a5c8",
                    "#29a160",
                    "#469e50"
                                ]
    # st.write(st.session_state.quiz_data_vars["graph_df"])
    # if len(st.session_state.quiz_data_vars["graph_df"]) == 2:
    #     st.session_state.quiz_data_vars["graph_df"] = st.session_state.quiz_data_vars["graph_df"].set_axis(['Column', 'Count'], axis=1)
    if not st.session_state.quiz_data_vars["graph_df"].empty: 
        number_of_columns = len(st.session_state.quiz_data_vars["graph_df"].columns)
        number_of_rows = len(st.session_state.quiz_data_vars["graph_df"].index)  
        if number_of_columns == 1 or number_of_rows == 1:
            # st.warning("Graph cannot be plotted for single column or single row data.")
            c1,c2,c3 = st.columns([30,40,30])
            with c2:
                # st.write(type(st.session_state.quiz_data_vars["graph_df"].iloc[0, 0]))
                if type(st.session_state.quiz_data_vars["graph_df"].iloc[0, 0]) == 'str':
                    st.write(st.session_state.quiz_data_vars["graph_df"].columns[0])
                    st.write(st.session_state.quiz_data_vars["graph_df"].iloc[0, 0])
                else:
                    st.metric(st.session_state.quiz_data_vars["graph_df"].columns[0], "{:.3f}".format(st.session_state.quiz_data_vars["graph_df"].iloc[0, 0]), border=True)
        else:
            c1, c2, c3, c4, c5 = st.columns([20,5,5,10,60], gap="small", vertical_alignment="bottom")
            with c1:
                chart_type = st.selectbox(":orange[Chart Type:]", 
                                        ["Bar Chart", "Grouped Chart", "Line Chart", "Area Chart", "Scatter Chart", "Pie Chart"], 
                                        index=st.session_state.chart_index, 
                                        placeholder="Chart Types", 
                                        label_visibility="collapsed")
            with c2:
                if chart_type in ["Bar Chart", "Line Chart", "Area Chart"]:
                    colour_picker = st.color_picker(":orange[Colour Picker]", value="#3579BB", label_visibility="collapsed")
            with c3:
                with stylable_container(
                            "data_grid",
                            css_styles="""
                            button {
                                background-color: white ;
                                color: #3E817D;
                            }""",
                        ):
                    if st.session_state.data_clicked:
                        st.session_state.chart_data_icon = ":material/insert_chart:"
                    else:
                        st.session_state.chart_data_icon = ":material/table:"
                    if st.button(f"", icon=st.session_state.chart_data_icon, 
                                            key="data_button", use_container_width=False):
                        st.session_state.data_clicked = not st.session_state.data_clicked
            
            categorical_cols = st.session_state.quiz_data_vars["graph_df"].select_dtypes(include=["object", "category"]).columns.tolist()
            numerical_cols = st.session_state.quiz_data_vars["graph_df"].select_dtypes(include=["int64", "float64"]).columns.tolist()
            date_cols = st.session_state.quiz_data_vars["graph_df"].select_dtypes(include=["datetime"]).columns.tolist()
            
            if st.session_state.data_clicked:
                st.dataframe(st.session_state.quiz_data_vars["graph_df"], hide_index=True, use_container_width=False, height=540)
            else:
                if chart_type in ["Bar Chart"]:
                    bar_chart = plot_altair_bar_chart(st.session_state.quiz_data_vars["graph_df"], 
                                                      colour_picker,
                                                      palette_colors,
                                                      categorical_cols,
                                                      numerical_cols,
                                                      date_cols)
                elif chart_type in ["Grouped Chart"]:
                    bar_chart = plot_altair_grouped_bar_chart(st.session_state.quiz_data_vars["graph_df"], 
                                                              palette_colors,
                                                              categorical_cols,
                                                              numerical_cols,
                                                              date_cols)
                elif chart_type in ["Line Chart"]:  
                    line_chart = plot_line_chart(st.session_state.quiz_data_vars["graph_df"], colour_picker)
                elif chart_type in ["Area Chart"]:
                    line_chart = plot_area_chart(st.session_state.quiz_data_vars["graph_df"], colour_picker)
                elif chart_type in ["Scatter Chart"]:
                    try:
                        scatter_chart = plot_scatter_chart(st.session_state.quiz_data_vars["graph_df"])
                    except Exception as e:
                        st.write("")
                elif chart_type in ["Pie Chart"]:
                    try:
                        pie_chart = plot_pie_chart(st.session_state.quiz_data_vars["graph_df"], palette_colors)
                    except Exception as e:
                        st.write("")
 