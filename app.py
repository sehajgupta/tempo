from flask import Flask, jsonify
import logging
import joblib
import parse
import pandas as pd
import random

app = Flask(__name__)

model = joblib.load("./model.pk1", mmap_mode="r")
base_url = "https://jobs.ashbyhq.com"

logging.basicConfig(level=logging.DEBUG)

@app.route('/predict/salary/<string:board_name>/<string:posting_id>', methods=['GET'])
def predict_salary(board_name, posting_id):
    app.logger.info("predicting salary for board: %s, posting ID: %s", board_name, posting_id)

    url = f"{base_url}/{board_name}/{posting_id}"
    parsed_posting = parse.extract_job_details(parse.get_html_content(url))

    df = {
        "Id": random.randint(1, 100000),
        "Title": parsed_posting["title"],
        "FullDescription": parsed_posting["description"],
        "LocationRaw": parsed_posting["job_location"]["address"]["addressLocality"],
        "LocationNormalized": "",
        "ContractType": "",
        "ContractTime": "permanent" if parsed_posting["employment_type"] == "FULL_TIME" else "contract",
        "Company": parsed_posting["hire_organization"]["name"],
        "Category": "Teaching Jobs",
        "SalaryRaw": "",
        "SourceName": "",
    }

    kv_frozen = [(k,v) for k,v in df.items()]
    for label, content in kv_frozen:
      if pd.api.types.is_string_dtype(content):
          df[label] = content.astype("category").cat.as_ordered()
    kv_frozen = [(k,v) for k,v in df.items()]
    for label,content in kv_frozen:
      if not pd.api.types.is_numeric_dtype(content):
          if label == "Id":
             continue
          # Add binary column to indicate whether sample had missing value
          df[label+"is_missing"]=pd.isnull(content)
          # Turn categories into numbers and add+1
          df[label] = pd.Categorical([content]).codes+1

    dataFrame = pd.DataFrame([df])

    prediction = model.predict(dataFrame)

    return jsonify({'Salary': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
