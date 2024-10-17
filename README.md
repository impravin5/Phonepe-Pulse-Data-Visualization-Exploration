# PhonePe Pulse Data Analysis Project

This project provides a comprehensive analysis and visualization of data from the [PhonePe Pulse GitHub repository](https://github.com/PhonePe/pulse). The data is processed and stored in a MySQL database, and the visualizations are displayed through an interactive dashboard built with Streamlit.

## Table of Contents
- [Introduction](#introduction)
- [Uses of This Project](#Uses-of-This-Project)
- [Key Metrics Handled](#Key-Metrics-Handled)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Data Visualization](#data-visualization)
- [ Steps and Usage](#Steps-and-Usage)
- [License](#license)

## Introduction

The `PhonePe Pulse Data Analysis Project` provides a platform to explore digital transaction data from PhonePe. It integrates with the PhonePe Pulse GitHub repository, extracts raw data, stores it in a MySQL database, and visualizes key metrics using an interactive Streamlit dashboard. Users can analyze trends and patterns, helping businesses, governments, and analysts to gain valuable insights into the digital payments ecosystem in India.

## Uses of This Project

- **Real-time data insights** on digital transactions and payment trends.
- Supports **business decision making** based on transaction data.
- Facilitates **market analysis** by understanding user engagement across regions.
- Aids **financial forecasting** by analyzing transaction growth.
- Assists **government policy making** with data on financial inclusion and digital transactions.
- Enables **performance monitoring** for companies offering digital payment services.

## Key Metrics Handled

This project focuses on several key metrics derived from the PhonePe Pulse data:

- **State-wise transaction count**: The number of transactions across different Indian states.
- **Yearly transaction count**: Transaction volume and trends over various years.
- **Quarterly breakdown**: The distribution of transaction volume across different quarters within a year.
- **Category-based analysis**: Transactions categorized by type (e.g., recharge, bill payments, money transfers).
- **Transaction amount**: The total value of transactions for each state, year, and category.
- **Geographical insights**: Displaying transactions across states via choropleth maps to visualize regional performance.

These metrics help users gain actionable insights into digital payment behavior across India.

## Technologies Used

- **Python**: The core programming language for data processing, analysis, and interaction with APIs.
- **GitPython**: For cloning and updating the PhonePe GitHub repository programmatically.
- **Pandas**: For reading, cleaning, and transforming the JSON data.
- **MySQL**: For storing and querying transaction data.
- **Plotly and Matplotlib**: For creating visualizations, including interactive charts and geographical maps.
- **Streamlit**: For building the interactive web dashboard.
- **Git**: For version control and managing updates from the GitHub repository.

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- MySQL Server
- GitHub account for accessing the PhonePe Pulse data repository.

### Installation
## Clone or update the PhonePe Pulse repository:

Run the phonepe.py script to clone the repository or verify if it exists. If the repository exists, it will be updated.
The data will be cloned to the specified directory and stored in the MySQL database for further analysis.

## Launch the Streamlit Dashboard:

The dashboard allows you to interact with the data and visualize trends, patterns, and insights. To run the dashboard:

## Visualize Data:

Use the Streamlit dashboard to visualize the transaction data from the PhonePe Pulse repository. You can explore various transaction metrics across different states, districts, and time periods.

## Data Visualization
This project supports a variety of data visualizations, including:

- Bar Charts: Display aggregated data by categories such as states or districts.
- Line Charts: Analyze trends over time for different regions.
- Scatter Plots: Examine correlations between different metrics.
- Pie Charts: Show proportions of various transaction types.
- Geographical Maps: Explore transaction data across India's states using choropleth maps.
- These visualizations are interactive and help in gaining insights from the PhonePe Pulse data.

### Steps and Usage
* Cloning or Updating the Repository:
    - The script phonepe.py checks if the repository already exists. If not, it clones the PhonePe Pulse repository. If it exists, it pulls the latest updates to ensure the data is current.

* Data Extraction:
    - The script extracts JSON files from the repository, parses them, and converts them into Pandas DataFrames.

* Storing Data in MySQL:
    - Data from the JSON files is stored in tables in a MySQL database. Each table represents a category (state-wise, year-wise, category-wise data).

* Visualization:
    - The Streamlit dashboard uses Plotly and Matplotlib to create visualizations like bar charts, line graphs, scatter plots, and choropleth maps to display the transaction data.

* Key Interactions:
    - The dashboard offers filters for year, category, and state to customize the visualizations and explore specific data segments.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
