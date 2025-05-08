-------------------------------------------------------------------------------
	--------------------------- README ---------------------------
-------------------------------------------------------------------------------

IMDB Data Scraping and Visualizations Project Description
A detailed project description can be found here: https://docs.google.com/document/d/1gk-OZUyMo0VsMV-OyKsOME7PIVtLDzL_4rsrNdTsY0M/edit?tab=t.0

Summary
This project focuses on scraping, cleaning, visualizing, and interactively filtering movie data from IMDb’s 2024 feature films page (https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31). 
The workflow is divided into several stages, each utilizing Python, Selenium, MySQL, and Streamlit.

Data Extraction
- Method:
- Utilized Python-based Selenium with XPath selectors to scrape data.
- Extracted the first 200 movies per genre by clicking the "50 more" button multiple times.

- Output:
- Stored the scraped data for each genre in individual CSV files.
- Example Code:
Action_df["Genre"] = "Action"
Action_df.to_csv(r"action_movies.csv", index=False)  # 'index=False' prevents writing the index column to the CSV.


Data Cleaning & Storage
- Process:
- Merged all the genre-wise CSV files into one consolidated DataFrame.
- Cleaned the data by handling null values, removing duplicates, and converting data into meaningful formats.

- Database Integration:
- Stored the cleaned dataset into an SQL database for easier querying and future analysis.
- Example Code:
insert_query = "INSERT INTO imdb_movies(title, rating, votes, duration, genre) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(insert_query, data_to_insert)
conn.commit()


Data Visualization
- Approach:
- Conducted Exploratory Data Analysis (EDA) to clean and transform the dataset.
- Generated graphs and visual representations to meet the requirements outlined in the project description.

Interactive Filtering
- Technologies Used:
- MySQL, Python, and Streamlit.

- Functionality:
- Developed a dynamic filtering interface allowing users to filter the dataset based on various criteria.

- Deployment:
- To run, execute the app.py and class.py files located in the Scripts folder under the Streamlit directory. (Ensure your environment is activated.)

References
- Streamlit API Reference - https://docs.streamlit.io/develop/api-reference
- Web Scraping with Selenium and Python - https://scrapfly.io/blog/web-scraping-with-selenium-and-python/


Attached Files and Folders
- Jupyter Notebooks:
- selwebscrap_data.ipynb – Data Extraction
- df_collected_genre.ipynb – Data Cleaning and Storage
- data_visulaziation_python.ipynb – Data Manipulation and Visualization
- Streamlit Application:
- app.py and class.py – Interactive Filtering scripts (to be run from the Scripts folder)
- Data Storage:
- IMDB_Project1_CollectedCsvData – Folder containing collected CSV files
- SQLDB – Folder containing the stored SQL database
- Documentation:
- Results.pdf – Screenshots of output as specified in the project description
