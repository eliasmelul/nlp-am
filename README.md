# nlp-am

This repository will hold some of the Word of the Amazon code that I do not mind sharing.
The purpose behind this project is to create a website that analyzes all reviews of a given specific product from Amazon.com. 

**What data will be used?**

The data will be dependent on the specific product the user wants to analyze. The general format the of data will be the scraped reviews for a specific product including the following for each review: name, date, stars, title, review_body. <a href='https://github.com/eliasmelul/nlp-am/blob/master/Functions%20Scraper.ipynb'>Click here</a> to check out the notebook.

**How is the analysis done?**

The analysis will leverage NLP techiniques, including Topic Modeling, Sentiment Analysis, Text Classification and Text Generation.
These methods will be powered by machine learning techniques including LSTMs, LDA, Logistic Regression, etc.

**What will be the output?**

The output will be simple and mostly visual.
What are the main topics that reviewers discussed in their reviews, what is the sentiment of these topics, and how has this sentiment progressed over time. It also includes text generation powered by all the previous reviews and weighted based on helpfulness scores and other metrics that assist detection and exclusion of outliers.
