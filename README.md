# Tempo interview

# Requirements

API:
/predict/salary/<string:board_name>/<string:posting_id> -> [$salary amount]

ML:
Use https://www.kaggle.com/c/job-salary-prediction/data to train a model to predict
salaries from scraped websites.

I'm not focussing too much on the training and validation of the model. I will be using the provided
dataset, train it offline and deploy the model.

Web-scraping:
Use the board name and posting ID to figure out different parameters of the job 
posting and use the model to predict the salary.
