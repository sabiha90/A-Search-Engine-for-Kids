# A-Search-Engine-for-Kids

A Kid Friendly Search engine which will display results for enhancement of kids' knowledge. The search engine eliminates all kinds of harmful content inappropriate for kids. We are using Neural Network and will rank the results using TF IDF,by tweaking it with our own formula.



The project consists of the following main steps:
<ol>
   <li><a href="#head1"> General instructions to run the project</a>
   <li><a href="#head2"> Scraping data from the web </a>
   <li><a href="#head3"> Assigning labels to the training data using pattern.en</a>
   <li><a href="#head4"> Filtering objectionable content</a>
   <li><a href="#head5"> Identifying topics</a>
   <li><a href="#head6"> Running ElasticSearch</a>
</ol>



<p id="head1"> <h2> General Instructions to run the project </h2></p>
Clone the repository into your local machine by typing the command
<br>


`git clone`

<br>
To run the project, you need to have a running version of Python 3.6(not 3.7) and pip.
<br>
To install the dependencies execute,
<br>

`pip install requirements.txt`

<br>
This command will install all the required dependencies.

<p id="head2"><h2> Scraping the data from the web </h2>
<br>
Scraping the data requires installed version of Selenium and BeautifulSoup. The libraries are present in the requirements.txt file.
<br>
For Data Scraping - 
<ol>
   <li>Run Medium_Scrapper_using_selenium.py
   <li>Run WebScraper.py
   <li>Run Medium_Search_URL_Scrapper.py
   <li>Run WebScraper.py
   <li>Combine the datasets and name them - final_data.csv
</ol>

Or you can download the data from this link: 
https://drive.google.com/file/d/1BrAguUjU6yU4In8iWx4-i37MBcK_gmqi/view
<p id="head3"><h2>Assigning labels to the training data using pattern.en</h2>
<br>
<ol>
<li>Create a new Virtual Environment using the command
   
   ```virtualenv -p python3 venv```
   
<li>A new folder called venv gets created.
<li>To source into the Virtual Environment, type the command
   
   ```source venv/bin/activate```
   
<li>A (venv) will get prepended to the command line. 
<li>Navigate to the Project folder in the path - /A-Search-Engine-for-Kids/helper_scripts/class_labelling_using_pattern.en
<li>Run the command
   
   ```python data_content_labelling.py```
<li>This script was created initially to classify data as Positive, Strongly Positive, Negative, Strongly Negative. The input CSV file taken here is a basic data set with limited records of 1280 rows.
<li>The output of this script is the same input data set with another column for sentiment score appended.
</ol>
   
<p id="head4"><h2>Filtering objectionable content</h2>
<ol>
<li>Once the final_data.csv file is retrieved, the file should be saved in the same directory as the file named, web_content_classification.ipynb file. The file should be executed by entering the command,

```jupyter notebook```
<li> This will open the notebook and all the cells can be executed by using Shift+Enter. Or via Cells> Run All.
</ol>
<br>
Note: Since the data set is huge (149mb), it will take a long period of time to see the results.
<br>
<p id="head5"><h2>Identifying topics</h2>
<ol>
<li> To execute this file, load the classification3.ipynb and topic modelling.ipynb as ipynb files in the jupyter notebook and execute it by using Shift+Enter or Cells> Run All.

<li>This file takes as input the output of the Filtering objectionable content step. The input file is "whole_data.csv" which is found in the same directory as the classification.ipynb file.
</ol>
<p id="head6"><h2>Running ElasticSearch</h2>

<ol>
   <li>Create virtual environment:
      
      `virtualenv -p python3 venv`

<li>Download elastic search (anywhere other than project folder):
   
`brew install elasticsearch`

<li> Set up virtual environment inside the app/ folder

`virtualenv -p python3 venv`
`source venv/bin/activate`
On execution of the last command you will see “venv” in the terminal line
<li> Open a second terminal window and start elastic search process in background 

`brew services start elasticsearch`
<li>Go to this directory, " ./usr/local/bin your elastic search directory and run 

`./elasticsearch` or `.\elasticsearch`
<li> Once elasticsearch is up and running, go to app/index/ and run,
   
   `python elastic_search_helper.py`
   
  This will start the flask app, which can be viewed in the browser using this url: 
  ``http://localhost:5000``
</ol>
## TroubleShooting:
If any error while starting elastic search 
example: failed to obtain node locks, tried [[/usr/local/var/lib/elasticsearch ..

`ps aux | grep 'java'
kill -9 <PID>`

Unable to locate python 3.7 on Pycharm 
locate anaconda if installed
` which anaconda`
Copy the path for the folder into pycharm and locate python 3.7 or similar version

PyCharm run/debug configuration will look like this
![image](https://user-images.githubusercontent.com/25397038/50049102-1f7c2b80-0091-11e9-8369-b13087f1346d.png)
