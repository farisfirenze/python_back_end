This is the backedn for Python Lab for Wise2024/24

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

3. get_history:
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

5. login:
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

6. register_user:
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
