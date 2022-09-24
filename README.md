# Youtube-Data-Analysis
 
An end-to-end Youtube Data analysis project.

## TABLE OF CONTENTS

* [Background](#background)
* [Objective](#objective)
* [Tools and Packages](#tools)
* [Data Pre-Processing](#data-preprocessing)
* [Data Modeling (Pipeline)](#data-modeling-pipeline)
* [Data Visualization](#data-visualization)
* [Conclusion](#conclusion)
* [Challenges and Future Work](#challenges-and-futurework)

<hr>

## BACKGROUND 
Youtube is the second largest search engine behind Google. It provides a valuable platform for analyzing the general public's attitude toward certain topics and how information is presented to them. This project focuses on user comment interactions and video performances based on various factors - in particular, it explores ***whether polar/extreme video titles attract more views and interactions***. This project also demonstrates automated and scalable data pipelines using APIs and SQL databases.

<hr>

## OBJECTIVE 
* Build data pipeline
  * Retreive raw channel data and comment thread data using the Youtube Data API
  * Upload data to AWS RDS MySQL database
  * Automate/Schedule data updates using ngrok and invictify
  * Pull data from MySQL database back into pandas dataframe for analysis
* Data Analysis (Natural Langauge Processing)
  * Main question to answer: *Do videos with stronger sentiment values show high view counts?*

<hr> 

## TOOLS
**Languages Used:** Python, SQL (MySQL), Shell
<table style="width:100%">
  <tr>
    <th>Task</th>
    <th>Technique</th> 
    <th>Tools/Packages Used</th>
  </tr>
  <tr>
    <td>Data Collection</td>
    <td>Channel and comment data extraction through Youtube Data API</td> 
    <td>Youtube API, pandas, AWS RDS, mysql.connector</td>
  </tr>
  <tr>
    <td>Data Pre-processing</td>
    <td>Converted string/object values to appropriate quantitative data types, extracted published day of the week from given date values, converted ISO formatted video duration values to seconds, added tag counts, removed unsused columns</td> 
    <td>pandas, numpy, datetime, isodate</td>
  </tr>
  <tr>
    <td>Data Modeling (Pipeline)</td>
    <td>Autmation/scheduling scripts to pull & push data to and from MySQL database</td> 
    <td>Flask, ngrok, Invictify</td>
  </tr>
  <tr>
    <td>Text Analytics</td>
    <td>Natural Language Processing using the VADER (Valence Aware Dictionary and sEntiment Reasoner) analysis tool from the NLTK package.</td> 
    <td>NLP, VADER, NLTK</td>
  </tr>
  <tr>
    <td>Data Visualization</td>
    <td>Exploratory Data Analysis. Plotted view/like counts on average comment sentiment value for each video to analyze patterns.</td> 
    <td>Matplotlib, seaborn, plotly</td>
  </tr>
  <tr>
    <td>Environments & Platforms</td>
    <td>Main functions stored and organized in python scripts, analysis and comment extractions hosted on Jupyter notebook</td> 
    <td>Youtube, AWS RDS, Jupyter Notebook</td>
  </tr>
</table><br>

<hr>

## DATA-PREPROCESSING

There were two stages to the data cleaning process, the first for video information collected through the Youtube Data API, and the second for preparing the comments for natural language processing.
* Video Information:
  * The code for this process can be found in [youtube_api_functions.py](https://github.com/cjunwon/Youtube-Data-Analysis/blob/main/youtube_api_functions.py) under the 'clean_video_df' function.
  * The Youtube API returns all video information as object values. Columns containing numeric information were converted to numeric data types.
  * Added column showing published day of the week through python datetime values
  * Converted duration (originally in ISO format) to seconds using the 'isodate' library
  * Removed unused columns
* Comment Texts:
  * The code for this process can be found in [main.ipynb](https://github.com/cjunwon/Youtube-Data-Analysis/blob/main/main.ipynb) under the 'preprocess' function.
  * Since the VADER model was used for NLP analysis, the comment texts did not require heavy cleaning - the model comfortably handles emojis, stopwords, etc. The "\n" for new line was removed for all comments.

<hr>

## DATA-MODELING-PIPELINE

<h3>Youtube Video Data</h3>
(Channel playlist data extracted using Youtube API - stored and cleaned in pandas dataframe) <br>
↓
<h3>AWS MySQL RDS</h3>
(Processed dataframe uploaded to MySQL RDS hosted through AWS - function checks to see repeating videos through unique ids and updates with current statistics) <br>
↓
<h3>Automation using Flask, ngrok, Invictify</h3>
(Schedule the above MySQL database push by hosting API collection and SQL upload functions on Flask server and schedule scripts using ngrok and invictify) <br>
↓
<h3>Data pulled from MySQL database back into pandas dataframe for analysis</h3>
(Video IDs and other relevant columns can be selected for further analysis) <br>
↓
<h3>Youtube Comment data </h3>
(Top level comments for selected video ids from above extracted through Youtube API for analysis)

<hr>

## DATA-VISUALIZATION 

Exploratory data analysis was completed using the Matplotlib and Seaborn library.

The [final interactive plot](https://cjunwon.github.io/Youtube-Data-Analysis/) was created using the plotly library.

<hr>

## CONCLUSION 

The Youtube Data API provides a rich set of data for selected channels and videos for various types of analysis. The tools and methods used in this project could be applied to managing your personal Youtube channel and keep a personalized and up-to-date feedback on your channel's performance.

<hr>


## CHALLENGES-AND-FUTUREWORK 

* Comment extraction process through the Youtube Data API can be added along with the video information and updated onto the MySQL database, stored in a separate table/schema.
* An interactive dashboard can be generated to capture and display data for multiple Youtube channels in a more efficient and accecible manner.
