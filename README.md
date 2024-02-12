This is the backedn for Python Lab for Wise2024/24

To run the app, follow the instructions
Python version : 3.8

1. cd into the directory and run
```
pip install -r requirements.txt
```
2. once installation done, run 
```
python main.py
```
3. You are all set.
   
Below are the endpoints in this FLASK application:

1. get_predictions:
   <br/>METHOD TYPE : POST
   <br/>Request information:
      <br/>url : http://localhost:5000/get_predictions
      <br/>body format :
```
{
  "rows" : [
    "Sanofi",
    "Phase 1",
    "2024",
    "3",
    "100",
    "Leukemia"
  ]
 }
```
  Response information:
    <br/>response format: 
 ```
 {
   "predictions_combined": {
     "Failed": 0.88,
     "Success": 0.12
   },
   "predictions_without_combined": {
     "Active, not recruiting": 0.0,
     "Completed": 0.0,
     "Enrolling by invitation": 0.06,
     "Not yet recruiting": 0.15,
     "Recruiting": 0.0,
     "Suspended": 0.0,
     "Terminated": 0.02,
     "Unknown status": 0.01,
     "Withdrawn": 0.76
   }
 }
 ```

2. get_history:
   <br/>METHOD TYPE : GET
   <br/>Request information:
      <br/>url : http://localhost:5000/get_history
      <br/>body format : none
  <br/>Response information:
    <br/>response format:
```
[
   {
       "condition": "Leukemia",
       "datetime": 1705968000000,
       "enrollment": 100,
       "id": 1,
       "phase": "Phase 2",
       "predicted_status": "0",
       "predicted_status_without_combine": "3",
       "sponsor": "Sanofi",
       "start_month": "3",
       "start_year": "2024"
     },
     {
       "condition": "Leukemia",
       "datetime": 1705968000000,
       "enrollment": 100,
  ....
  .....
  }
]
```

3. login:
   <br/>METHOD TYPE : POST
   <br/>Request information:
      <br/>url : http://localhost:5000/login
      <br/>body format :
```
{
   "username" : "faris123",
   "password": "faris@123"
}
```
  <br/>Response information:
    <br/>response format:
```
{
     "authentication": true
}
```

4. register_user:
   <br/>METHOD TYPE : POST
   <br/>Request information:
      <br/>url : http://localhost:5000/register_user
      <br/>body format :
```
{
   "username" : "faris123",
   "password": "faris@123"
}
```
  <br/>Response information:
    <br/>response format: 
```
{
 "message": "User registered successfully"
}
```

4. get_graph_data:
   <br/>METHOD TYPE : GET
   <br/>Request information:
      <br/>url : http://localhost:5000/get_graph_data
      <br/>body format : none
  <br/>Response information:
    <br/>response format: 
```
{
  "line_graph": {
    "Mon": 3,
    "Tue": 4,
    "Wed": 16,
    "Thu": 4,
    "Fri": 5,
    "Sat": 9,
    "Sun": 4
  },
  "bar_graph": {
    "Withdrawn": 45,
    "Suspended": 12,
    "Completed": 2,
    "Enrolling by invitation": 1
  }
}
```
