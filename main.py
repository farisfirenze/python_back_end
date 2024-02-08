from flask import Flask, jsonify, request
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from flask_cors import CORS
import os
import json
import time
import pymysql
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)


model_without_combined_path = "models/random_forest_model_without_combined.joblib"
model_with_combined_path = "models/random_forest_model_with_combined.joblib"

model_without_combined = joblib.load(model_without_combined_path)
model_with_combined = joblib.load(model_with_combined_path)

clinical_data = pd.read_csv("clinical_trials.csv")

#seperating Phase column into two seperate columns ( "primary_phase and secondary_phase")
clinical_data.dropna(inplace=True)
clinical_data["primary_phase"] = clinical_data["Phase"] + "/"
clinical_data["primary_phase"] = clinical_data["primary_phase"].astype(str)
clinical_data["secondary_phase"] = clinical_data["primary_phase"].apply(lambda x: x.split("/")[-2])
clinical_data["primary_phase"] = clinical_data["primary_phase"].apply(lambda x: x.split("/")[0])

clinical_data = clinical_data.drop(columns=['Phase'])
clinical_data.drop(columns=['primary_phase', "index"], inplace=True)

clinical_data.rename(columns={'secondary_phase': 'Phase'}, inplace=True)

clinical_data = clinical_data[clinical_data['Enrollment'] <= 2100]

print(clinical_data.columns)

without_combined = {"0": 'Completed', "1": 'Enrolling by invitation', "2": 'Recruiting', "3": 'Withdrawn', "4": 'Not yet recruiting', "5": 'Terminated', "6": 'Suspended', "7": 'Active, not recruiting', "8": 'Unknown status'}


combined = {
    "1": "Success",
    "0": "Failed"
}

def get_last_7_days_count(data):
    data['datetime'] = pd.to_datetime(data['datetime'], dayfirst=True)
    last_7_days = datetime.now() - timedelta(days=7)
    last_7_days_data = data[data['datetime'] >= last_7_days]
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today_date = datetime.now()
    today_day = today_date.strftime('%a')
    today_index = days_of_week.index(today_day)
    rearranged_days = days_of_week[today_index + 1:] + days_of_week[:today_index + 1]
    last_7_days_count = last_7_days_data['datetime'].dt.strftime('%a').value_counts().reindex(rearranged_days).to_dict()
    print(last_7_days_count)
    return last_7_days_count

def get_predicted_status_count(data):
    predicted_status_count = data['predicted_status_without_combine'].value_counts().to_dict()
    return predicted_status_count

@app.route('/get_predictions', methods=['POST'])
def get_predictions():
    
    connection = pymysql.connect(
        host='sql11.freesqldatabase.com',
        user='sql11679154',
        password='MtH7ILFSeH',
        database='sql11679154',
        port=3306
    )

    cursor = connection.cursor()

    predictions_combined = {}
    predictions_without_combined = {}
    manual_input = request.get_json()

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")

    row = manual_input.get("rows")
    
    new_row_df = pd.DataFrame([row], columns=['Sponsor', 'Phase', 'Start_Year', 'Start_Month', 'Enrollment', 'Condition'])

    df_new = clinical_data.copy()
    df_new = pd.concat([df_new, new_row_df], ignore_index=True)

    label_encoder = LabelEncoder()

    df_new['Status'] = label_encoder.fit_transform(df_new['Status'])
    df_new['Phase'] = label_encoder.fit_transform(df_new['Phase'])
    df_new['Sponsor'] = label_encoder.fit_transform(df_new['Sponsor'])
    df_new['Condition'] = label_encoder.fit_transform(df_new['Condition'])

    # print(dict(zip(list(set(df_new["Status"].tolist())), list(set(clinical_data["Status"].tolist())))))

    df_new = df_new[['Sponsor', 'Phase', 'Start_Year', 'Start_Month', 'Enrollment', 'Condition']]
    manual_input_reshaped = df_new.values.tolist()[-1]
    manual_input_reshaped = [str(element) for element in manual_input_reshaped]

    predicted_probabilities_without_combined = model_without_combined.predict_proba([manual_input_reshaped])
    predicted_probabilities_with_combined = model_with_combined.predict_proba([manual_input_reshaped])

    for class_index, class_name in enumerate(model_without_combined.classes_):
        predictions_without_combined[without_combined[str(class_name)]] = predicted_probabilities_without_combined[0, class_index]
    
    for class_index, class_name in enumerate(model_with_combined.classes_):
        predictions_combined[combined[str(class_name)]] = predicted_probabilities_with_combined[0, class_index]
    
    predictions = {"predictions_combined": predictions_combined, "predictions_without_combined": predictions_without_combined}
    max_key_combined = max(predictions_combined, key=lambda k: predictions_combined[k])

    # Find the key with the maximum value in predictions_without_combined
    max_key_without_combined = max(predictions_without_combined, key=lambda k: predictions_without_combined[k])

    
    insert_query = f"INSERT INTO predictions(datetime, sponsor, phase, start_year, start_month, enrollment, `condition`, predicted_status, predicted_status_without_combine) VALUES('{formatted_date}', '{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', {int(row[4])}, '{row[5]}', '{max_key_combined}', '{max_key_without_combined}');"
    print(insert_query)
    cursor.execute(insert_query)
    connection.commit()
    cursor.close()
    connection.close()
    print(predictions)
    return predictions

# Endpoint for getting user history
@app.route('/get_history', methods=['GET'])
def get_history():
    connection = pymysql.connect(
        host='sql11.freesqldatabase.com',
        user='sql11679154',
        password='MtH7ILFSeH',
        database='sql11679154',
        port=3306
    )
    # Retrieve user ID from request (you may use authentication for this)
    sql_query = "SELECT * FROM predictions"
    df = pd.read_sql(sql_query, connection)
    predictions = json.loads(df.to_json(orient='records'))
    return predictions

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    authentication = False
    data = request.get_json()

    # Retrieve username and password from request
    username = data.get('username')
    password = data.get('password')

    connection = pymysql.connect(
        host='sql11.freesqldatabase.com',
        user='sql11679154',
        password='MtH7ILFSeH',
        database='sql11679154',
        port=3306
    )

    # Retrieve user ID from request (you may use authentication for this)
    sql_query = "SELECT * FROM users"
    users = pd.read_sql(sql_query, connection)

    if username in users["username"].tolist():
        if users[users["username"] == username]["password"].tolist()[0] == password:
            authentication = True
    
    return jsonify({'authentication': authentication}), 200

# Endpoint for user registration
@app.route('/register_user', methods=['POST'])
def register_user():

    connection = pymysql.connect(
        host='sql11.freesqldatabase.com',
        user='sql11679154',
        password='MtH7ILFSeH',
        database='sql11679154',
        port=3306
    )
    cursor = connection.cursor()

    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")

    data = request.get_json()

    sql_query = "SELECT * FROM users"
    users = pd.read_sql(sql_query, connection)["username"].tolist()

    # Retrieve username and password from request
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400

    # Register the user (you may want to hash the password for security)
    insert_query = f"INSERT INTO users(created_time, username, password) VALUES('{formatted_date}', '{username}', '{password}');"

    cursor.execute(insert_query)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User registered successfully'})

# Endpoint for getting user history
@app.route('/get_graph_data', methods=['GET'])
def get_graph_data():
    connection = pymysql.connect(
        host='sql11.freesqldatabase.com',
        user='sql11679154',
        password='MtH7ILFSeH',
        database='sql11679154',
        port=3306
    )
    # Retrieve user ID from request (you may use authentication for this)
    sql_query = "SELECT * FROM predictions"
    df = pd.read_sql(sql_query, connection)
    line_graph = get_last_7_days_count(df)
    bar_graph = get_predicted_status_count(df)
    print(line_graph)
    response = json.dumps({
        "line_graph": line_graph,
        "bar_graph": bar_graph
    })


    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
