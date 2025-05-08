## Refrence documents 
# https://docs.streamlit.io/develop/concepts/design/custom-classes

import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns


class Graph:
    def __init__(self, data):
        self.data = data
    
    def show_graph(self):
        if "show_graph" not in st.session_state:
            st.session_state.show_graph = False
        if st.button("Click to View Rating Distribution", key="view_graph_button"):
            st.session_state.show_graph = not st.session_state.show_graph
        if st.session_state.show_graph:
            st.subheader("Movie Ratings Distribution (Histogram)")
            plt.figure(figsize=(10, 6))
            sns.histplot(self.data["IMDb Rating"], bins=10, kde=True, color="blue")
            plt.title("Ratings Distribution", fontsize=14, fontweight="bold")
            plt.xlabel("Rating", fontsize=12)
            plt.ylabel("Frequency", fontsize=12)
            plt.xticks(rotation=80, fontsize=10)
            plt.grid(axis="y", linestyle="--", alpha=0.7)
            st.pyplot(plt)

class Style:
    def __init__(self, data):
        self.data = data
    def button_style(self):
        button_style = """
        <style>
            .styled-button {
                background-color: #4CAF50; /* Green background */
                border: none; /* Remove borders */
                color: white; /* White text */
                padding: 15px 32px; /* Some padding */
                text-align: center; /* Centered text */
                text-decoration: none; /* Remove underline */
                display: inline-block; /* Get the element to line up correctly */
                font-size: 16px; /* Increase font size */
                margin: 4px 2px; /* Some margin */
                cursor: pointer; /* Pointer/hand icon */
                border-radius: 8px; /* Rounded corners */
            }
            .styled-button:hover {
                background-color: #45a049; /* Darker green on hover */
            }
            </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)

        