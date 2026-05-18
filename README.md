# Lung Cancer Risk Prediction - Data Pipeline

**Data-Driven Computing Architectures | Final Project**


## Project Overview

This project builds an end-to-end data pipeline for lung cancer risk prediction using Databricks. It ingests data from four different sources, processes it through a medallion architecture (Bronze -> Silver -> Gold), trains a machine learning model for cancer risk prediction, and exposes the model via a REST API with a formal data contract. Its goal is to predict the probability of an individual developing lung cancer based on features like smoking history, location, and the air quality data.

![Data Lineage](./example/data_lineage.jpg)
## Data Sources

Please find the detailed descrption and schema of our data sources from [data/README.md](data/README.md). This is an overview:

| Type | Source | Description | Size |
|---|---|---|---|
| Structured | [Kaggle: Lung Cancer Risk & Trends Across 25 Countries](https://www.kaggle.com/datasets/ankushpanday1/lung-cancer-risk-and-trends-across-25-countries) | 220,632 individuals with age, gender, smoking history, cancer diagnosis, environmental exposure, survival rates across 25 countries | 220k rows |
| Structured | [WHO: Ambient Air Pollution Attributable Deaths](https://datasource.kapsarc.org/explore/dataset/ambientairpollution_attributabledeaths/information/?disjunctive.indicator&disjunctive.parentlocation&disjunctive.location&disjunctive.dim1&disjunctive.dim2&sort=period&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJsaW5lIiwiZnVuYyI6IkFWRyIsInlBeGlzIjoiZmFjdHZhbHVlbnVtZXJpY2hpZ2giLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiJyYW5nZS1BY2NlbnQifV0sInhBeGlzIjoiaW5kaWNhdG9yIiwibWF4cG9pbnRzIjpudWxsLCJ0aW1lc2NhbGUiOiIiLCJzb3J0IjoiIiwic2VyaWVzQnJlYWtkb3duIjoiZGltMSIsImNvbmZpZyI6eyJkYXRhc2V0IjoiYW1iaWVudGFpcnBvbGx1dGlvbl9hdHRyaWJ1dGFibGVkZWF0aHMiLCJvcHRpb25zIjp7ImRpc2p1bmN0aXZlLmluZGljYXRvciI6dHJ1ZSwiZGlzanVuY3RpdmUucGFyZW50bG9jYXRpb24iOnRydWUsImRpc2p1bmN0aXZlLmxvY2F0aW9uIjp0cnVlLCJkaXNqdW5jdGl2ZS5kaW0xIjp0cnVlLCJkaXNqdW5jdGl2ZS5kaW0yIjp0cnVlLCJzb3J0IjoicGVyaW9kIn19fV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWUsInRpbWVzY2FsZSI6IiJ9) | Annual estimates of deaths caused by ambient air pollution (2016–2019) by country, gender, and cause of death | 13k rows |
| Unstructured | [PubMed: Lung Cancer Abstracts](https://pubmed.ncbi.nlm.nih.gov/?term=lung+cancer) | Scientific publication metadata and abstracts about lung cancer, used for keyword analysis and literature statistics | ~487k lines (10k papers) |
| Real-time | [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/) | Hourly PM2.5, PM10 air quality readings for 14 countries (past 4 days + tomorrow forecast) | Live API |


## Completed Tasks

**Data Ingestion**
- Structured data (batch/manual)
- Unstructured data (batch/manual)
- Real-time or automated batch ingestion

**Data Processing & Cleaning**
- Implement ETL to clean, transform, and standardize data
- Apply data deduplication & type validation, basic metadata
- Advanced/automated metadata (e.g., profiling, schema evolution)

**Architecture & Advanced Features**
- Implement medallion architecture (Bronze-Silver-Gold)
- Data lineage
- Implement an AI/ML model as part of the data pipeline
- Performance tuning (e.g., partitioning, z-ordering, etc.)

**Visualization & Dashboard**
- Basic visualization (plots, dashboard, ...)
- Record and present pipeline statistics (e.g., number of ingested records, ingestion timing)

**Data Sharing**
- External visualization or other type of data usage via API/sharing protocols

**Data Product**
- Simple data contract
- Access the data product through an API
- Automated testing of schema/data

**Logging**
- Structured logging & error handling





## Pipeline Description

The pipeline actually runs as a sequence of Databricks notebooks. See [code/README.md](code/README.md) for the execution order and notebook details.

**Raw Data / API → Bronze → Silver → Gold → API / Dashboard / Looker Studio**

A full end-to-end data lineage diagram is in [docs/data_lineage.jpg](docs/data_lineage.jpg).



## Tasks


**Solution description with schema and pipeline description**

The pipeline, data schema, and each stage are documented in this README and in the sub-folder READMEs. Data source schemas are in [data/README.md](data/README.md). The pipeline notebook details are in [code/README.md](code/README.md). Supporting diagrams and screenshots are in [docs/](docs/).

**Repository organization**

The repository follows the required folder structure: `code/`, `data/`, `docs/`, `misc/`, `test/`, `example/`. Each folder has its own README explaining its contents.

**Scope & originality**

The project combines four data sources (structured patient data, WHO pollution stats, unstructured PubMed abstracts, and a live air quality API) into a single pipeline that ends with a lung cancer risk prediction model and a REST API.

---


### Data Ingestion

**Structured data (batch/manual)**

Two CSV files are ingested in [code/Bronze_Ingestion.ipynb](code/Bronze_Ingestion.ipynb) (Section 1):
- lung_cancer_dataset.csv -> bronze.raw_lung_cancer
- WHO_pollution.csv -> bronze.raw_who_pollution 

Both are read with spark.read.csv and written as Delta tables with an added ingestion timestamp and source file path. Raw files uploaded to the Databricks volume are shown in [example/Raw files inside catalog.png](example/Raw%20files%20inside%20catalog.png) and ingested row counts in [example/LungsData, WHO, PubMed Data.png](example/LungsData%2C%20WHO%2C%20PubMed%20Data.png).

**Unstructured data (batch/manual)**

PubMed abstracts text file (abstract-lungcancer.txt) is ingested in [code/Bronze_Ingestion.ipynb](code/Bronze_Ingestion.ipynb) (Section 2). We downloaded this txt file from the official website where you can search and filter publications related to a subject. The raw text is split into individual paper records but all in one file that made us use regex to separate each record. We save it as one bronze table and then Spark UDF scans each abstract for 18 lung cancer risk keywords and adds "risk_keywords" and "keyword_count" columns.

Output tables: bronze.raw_pubmed_abstracts and bronze.raw_pubmed_keywords.

**Real-time / automated batch ingestion**

[code/Bronze_Ingestion.ipynb](code/Bronze_Ingestion.ipynb) (Section 3) fetches live hourly data from the Open-Meteo Air Quality API for 14 countries and writes the result to bronze.raw_air_quality. The ingestion is scheduled as a recurring Databricks job (see [docs/Job Schedule Air Quality.png](docs/Job%20Schedule%20Air%20Quality.png)). An example of a successful API fetch is in [example/API Air quality Ingestion.png](example/API%20Air%20quality%20Ingestion.png).


---


### Data Processing & Cleaning

**ETL: clean, transform, standardize**

[code/Silver_ETL.ipynb](code/Silver_ETL.ipynb) processes all four bronze tables.

- For silver.lung_cancer: column names are lowercased, types are cast (age -> int, cancer_stage -> int, survival_years -> double), and nulls in key columns are dropped. ([example/Silver Lung cancer data clean.png](example/Silver%20Lung%20cancer%20data%20clean.png))
- For silver.who_pollution: gender values are normalized, year and value ranges are validated. ([example/WHO silver clean data.png](example/WHO%20silver%20clean%20data.png))
- For silver.air_quality: AQI is calculated by interpolating PM2.5 and PM10 across standard breakpoints, then countries are assigned an AQI category. ([example/Air Quality Silver Clean.png](example/Air%20Quality%20Silver%20Clean.png))
- For silver.abstracts: UDFs extract year, journal, title, authors, abstract text, DOI, PMID, and PMCID from the raw text. ([example/PubMed Clean Silver.png](example/PubMed%20Clean%20Silver.png))

**Deduplication, type validation, basic metadata**

dropDuplicates() is applied to every Silver table. All type casts are explicit (IntegerType, DoubleType, FloatType). Metadata columns "_silver_timestamp" and "_silver_version" are added to silver.lung_cancer. We also print the number of recored before and after the transformations with log_step()

**Advanced/automated metadata and Great Expectations**

[code/Silver_ETL.ipynb](code/Silver_ETL.ipynb) runs a Great Expectations on a 10,000-row sample of silver.lung_cancer. It checks column existence, non-null constraints, and value ranges (age 0–120, gender Male/Female). There is a total of 5 tests.


---


### Architecture & Advanced Features

**Medallion architecture (Bronze → Silver → Gold)**

- **Bronze** ([code/Bronze_Ingestion.ipynb](code/Bronze_Ingestion.ipynb)): raw data only, no changes.
- **Silver** ([code/Silver_ETL.ipynb](code/Silver_ETL.ipynb)): cleaned and validated.
- **Gold** ([code/Gold_Aggregations.ipynb](code/Gold_Aggregations.ipynb)): aggregated tables ready for analytics and ML. ([example/gold_risk_by_country_aggregated.jpg](example/gold_risk_by_country_aggregated.jpg))

**Data lineage**

The full lineage diagram is in [docs/data_lineage.jpg](docs/data_lineage.jpg). It shows how a gold table is built from previous layers. You can also track each column in this graph.

**AI/ML model**

[code/ML_Models.ipynb](code/ML_Models.ipynb) trains an XGBoost binary classifier on gold.ml_features to predict lung cancer diagnosis. Class imbalance (3% positive) is handled with scale_pos_weight. The decision threshold is set to 0.3 for higher sensitivity. The model is tracked with MLflow (hyperparameters, AUC, accuracy, F1), registered as LungCancerRiskModel, and predictions are written to gold.risk_predictions. See [example/Train Test Split for ML model.png](example/Train%20Test%20Split%20for%20ML%20model.png) and [example/Performance of XGBoost model.png](example/Performance%20of%20XGBoost%20model.png).

**Performance tuning**

All Gold tables in [code/Gold_Aggregations.ipynb](code/Gold_Aggregations.ipynb) are optimized with
- OPTIMIZE ... ZORDER BY (...) on their most-queried columns (country, age, keyword).
- VACUUM RETAIN 168 HOURS removes old Delta version files. 
- DESCRIBE HISTORY is used to confirm the optimization ran. (see [example/gold optimization.jpg](example/gold%20optimization.jpg))


---


### Visualization & Dashboard

**Basic visualization**

[code/Pipeline_Dashboard.ipynb](code/Pipeline_Dashboard.ipynb) contains six SQL queries displayed as native Databricks charts: cancer rate by country ([example/Cancer Rate percentage Graph.png](example/Cancer%20Rate%20percentage%20Graph.png)), cancer rate vs. AQI ([example/Air Quality and Cancer rate percentage graph.png](example/Air%20Quality%20and%20Cancer%20rate%20percentage%20graph.png)), PubMed keyword frequency ([example/Wordcloud for keywords used in abstracts graph.png](example/Wordcloud%20for%20keywords%20used%20in%20abstracts%20graph.png)), smoking rate by country ([example/Country and smoker percentage graph.png](example/Country%20and%20smoker%20percentage%20graph.png)). An external Google Looker Studio dashboard is shown in [docs/external_visualization_google_looker_studio.jpg](docs/external_visualization_google_looker_studio.jpg).

![Smoker Rate Map](./example/Country%20and%20smoker%20percentage%20graph.png)

**Pipeline statistics**

Query 6 in [code/Pipeline_Dashboard.ipynb](code/Pipeline_Dashboard.ipynb) reads "bronze.pipeline_logs" and shows record counts, run timestamps, and failure counts for each table. Every ingestion event (bronze stage) is logged to this table with timestamp, stage, table name, record count, source, status, and error message.


---


### Data Sharing

**External visualization / data usage via API**

The "GET /data/risk_by_country" endpoint in [misc/api/main.py](misc/api/main.py) serves the Gold-layer export as JSON. This data is also loaded into Google Looker Studio for external visualization (see [docs/external_visualization_google_looker_studio.jpg](docs/external_visualization_google_looker_studio.jpg) and [docs/data_sharing_via_api.jpg](docs/data_sharing_via_api.jpg)). See [misc/README.md](misc/README.md) for how to start the API.


---


### Data Product

**Simple data contract**

The JSON Schema contract for the prediction API is at [docs/data_contract.json](docs/data_contract.json). It defines required fields, types, and value constraints for both request and response.

**Access the data product through an API**

[misc/api/main.py](misc/api/main.py) is a FastAPI service with three endpoints:
- GET /health: service health check
- POST /predict: returns these things -> risk_score (0–1), risk_label (Low/Medium/High), model_version
- GET /data/risk_by_country: returns the Gold-layer country risk table as JSON

See [misc/README.md](misc/README.md) for startup instructions and [docs/Lung Cancer Risk prediction API.png](docs/Lung%20Cancer%20Risk%20prediction%20API.png) for a Swagger UI screenshot.

**Automated testing of schema/data**

[test/test_pipeline.py](test/test_pipeline.py) has 14 tests in three classes:
- TestDataContract (5 tests): validates the JSON Schema contract accepts valid input and rejects invalid inputs.
- TestAPI (6 tests): integration tests against the live FastAPI server.
- TestSampleData (3 tests): validates data/sample_lung_cancer.csv for required columns, non-negative age, and valid diagnosis values.

Tests run automatically with every push to main via GitHub Actions ([.github/workflows/test.yml](.github/workflows/test.yml)). See [test/README.md](test/README.md) for details and [docs/automated_testing_github_actions.jpg](docs/automated_testing_github_actions.jpg) for CI evidence.


---


### Logging

**Structured logging & error handling**

Every ingestion event in [code/Bronze_Ingestion.ipynb](code/Bronze_Ingestion.ipynb) is written to the bronze.pipeline_logs Delta table and also emitted as structured JSON via structlog to the Databricks driver logs. Each log entry contains: timestamp, pipeline_stage, table, records, source, status (success/failed), and error message. We don't let the errors crash our pipeline. Instead they are caught with try/except blocks and logged with status failed.
