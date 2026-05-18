# Misc Directory

It contains supplementary scripts that support the pipeline and validate the working of our project. 



**api/** - FastAPI Prediction Service

File: [`api/main.py`](api/main.py)

Framework: FastAPI 0.100+

Language: Python 3.9+

The REST API offers a health endpoint, a prediction endpoint, and a data-sharing endpoint. These endpoints can be use to show the working of our pipeline. 



#### How to Start

Run the mentioned command on your local system. 

1. Go the root folder od the project and open command prompt. 
2. Install the necessary libararies including fastapi uvicorn pandas. 
3. Run the given command `uvicorn misc.api.main:app --reload --port 8000'

Since, the main.py is in misc folder, it is important to write `uvicorn misc.api.main:app --reload --port 8000'. 

The API will then be available at 
- `http://localhost:8000` - root message
- `http://localhost:8000/docs` - interactive Swagger UI
- `http://localhost:8000/redoc` - ReDoc documentation

The snapshot for `http://localhost:8000/docs` - interactive Swagger UI, can be found at `misc/Prediction API.png`.

![Prediction API](Prediction%20API.png)


--
#### Endpoints

**POST /predict** - Lung Cancer Risk Prediction

We use FAST API to accept the patient data and then provide a risk score accordingly. The following is the request model. 


| Field | Type | Constraints | Example |
|---|---|---|---|
| age | int | 0 ≤ age ≤ 120 (Pydantic ge/le) | 55 |
| country | str | required | "Japan" |
| gender | Literal["Male","Female"] | enum enforced by Pydantic | "Male" |
| smoker | Literal["Yes","No"] | enum enforced by Pydantic | "Yes" |
| years_of_smoking | int | ≥ 0 | 20 |
| cigarettes_per_day | int | ≥ 0 | 15 |

For instance, we can have such kind of request 


curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age":55,"country":"Finland","gender":"Male","smoker":"Yes","years_of_smoking":20,"cigarettes_per_day":15}'



The JSON response would be something like 

{
  "risk_score": 0.71,
  "risk_label": "High",
  "model_version": "1.0"
}

In case of wrong inputs such as wrong types, out-of-range values, missing fields, it would return HTTP 422 Unprocessable Entity



--

**GET /data/risk_by_country** - Risk Data Feed

It would read `data/risk_by_country.csv` (the Gold-layer export) and will return the JSON array of records. 

`curl http://localhost:8000/data/risk_by_country`

It will return something similar to the below example. 
[
  {"country":"Mexico","total_patients":8812,"cancer_cases":392,"avg_age":52.1,
   "smokers":3521,"avg_cigarettes_per_day":7.2,"avg_mortality_rate":1.8,
   "cancer_rate":0.0445,"smoker_rate":0.3995},
  ...
]

The sample snapshot for risk by countries can be found at `misc/API Risk by country.png`.

![API Risk by country](API%20Risk%20by%20country.png)

--




