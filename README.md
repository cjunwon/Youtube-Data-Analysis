# Youtube-Data-Analysis

To view the main analysis process, click on this Jupyter's [nbviewer link](https://nbviewer.org/github/cjunwon/Youtube-Data-Analysis/blob/main/main.ipynb) to load main.ipynb and its interactive graphs.
 
An end-to-end Youtube Data analysis project currently in progress.

## TABLE OF CONTENTS

* [Background](#background)
* [Objective](#objective)
* [Tools and Packages](#tools)
* [Data Collection](#data-collection)
* [Data Pre-Processing](#data-preprocessing)
* [Data Modeling](#data-modeling)
* [Data Visualization](#data-visualization)
* [Results](#results)
* [Conclusion](#conclusion)
* [Challenges and Future Work](#challenges-and-futurework)

<hr>

## BACKGROUND 
Youtube is the second largest search engine behind Google. It provides a valuable platform for analyzing the general public's attitude toward certain topics and how information is presented to them. This project focuses on user comment interactions and video performances based on various factors. This project also demonstrates automated and scalable data pipelines using APIs and SQL databases.

<hr>

## OBJECTIVE 
* Build data pipeline
  * Retreive raw channel data and comment thread data using the Youtube Data API
  * Upload data to AWS RDS MySQL database
  * Automate/Schedule data updates using ngrok and invictify
  * Pull data from MySQL database back into pandas dataframe for analysis
* Data Analysis (Natural Langauge Processing)

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
    <td>Data Modeling</td>
    <td></td> 
    <td></td>
  </tr>
  <tr>
    <td>Text Analytics</td>
    <td>Natural Language Processing using the VADER (Valence Aware Dictionary and sEntiment Reasoner) analysis tool from the NLTK package.</td> 
    <td>NLP, VADER, NLTK</td>
  </tr>
  <tr>
    <td>Data Visualization</td>
    <td>Plotted view/like counts on average comment sentiment value for each video to analyze patterns.</td> 
    <td>plotly</td>
  </tr>
  <tr>
    <td>Environments & Platforms</td>
    <td></td> 
    <td>Youtube, AWS RDS, Jupyter Notebook</td>
  </tr>
</table><br>

<hr>

## DATA-COLLECTION 

<table style="width:100%">
  <tr>
    <th>Method</th>
    <th>Notes</th> 
  </tr>
  <tr>
    <td>A</td>
    <td>B</td> 
  </tr>
  <tr>
    <td>A</td>
    <td>B</td> 
  </tr>
  <tr>
    <td>A</td>
    <td>B</td> 
  </tr>
  <tr>
    <td><b>A</b></td>
    <td><b>B</b></td> 
  </tr>
  <tr>
    <td>A</td>
    <td>B</td> 
  </tr>
</table>

<h4> Data Collection: Youtube Data API </h4>

<h4> Data Coverage: </h4> A <br>
B <br>
C <br>

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

## DATA-MODELING

<h4> Youtube Data API to AWS</h4>

<hr>

## DATA-VISUALIZATION 

<hr>

## RESULTS 

<hr>

## CONCLUSION 


<hr>


## CHALLENGES-AND-FUTUREWORK 
