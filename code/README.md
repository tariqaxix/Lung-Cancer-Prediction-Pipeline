# Code Directory

All pipeline logic is implemented as Databricks notebooks. Run them **in the order listed below**. Each notebook depends on the output of the previous one.

---

## Execution Order

| # | Notebook | Input | Output
|---|---|---|---|
| 1 | [Setup.ipynb](Setup.ipynb) | — | Databricks databases + volume |
| 2 | [Bronze_Ingestion.ipynb](Bronze_Ingestion.ipynb) | Raw files + live API | 6 Bronze Delta tables |
| 3 | [Silver_ETL.ipynb](Silver_ETL.ipynb) | Bronze tables | 4 Silver Delta tables | 
| 4 | [Gold_Aggregations.ipynb](Gold_Aggregations.ipynb) | Silver tables | 6 Gold Delta tables + ZORDER 
| 5 | [ML_Models.ipynb](ML_Models.ipynb) | `gold.ml_features` | MLflow experiment + model registry + `gold.risk_predictions` | 
| 6 | [Pipeline_Dashboard.ipynb](Pipeline_Dashboard.ipynb) | Gold tables + pipeline logs | Interactive Databricks charts |

---

## Notebook Details

---

### 1. `Setup.ipynb`: Database & Volume Initialization

**Purpose:** Initialization of the Databricks environment before the pipeline runs.

Here we just created three databases (bronze, silver, and gold) and one volume under the bronze database for the raw data files.

---

### 2. `Bronze_Ingestion.ipynb`: Raw Data Ingestion

**Purpose:** Just ingest all four data sources into the Bronze layer with zero transformation

**Prerequisites:** Upload the following files to the volume before running Bronze_Ingestion:
- `lung_cancer_dataset.csv`
- `WHO_pollution.csv`
- `abstract-lungcancer.txt`

#### Section 1: Structured Data

Here we read both the lung cancer dataset (`data/lung_cancer_dataset.csv`) and the WHO pollution (`data/WHO_pollution.csv`) using spark.read.csv

The first one is written in `bronze.raw_lung_cancer` delta table with 220,632 rows. The second one is written in `bronze.raw_who_pollution` delta table with 13,177 rows. `_ingest_timestamp` (current timestamp) and `_source_file` (file path) are added to both.

#### Section 2: Unstructured Data (PubMed Abstracts)

From `abstract-lungcancer.txt` we create two bronze tables:

`bronze.raw_pubmed_abstracts` where we read the txt file line by line via spark.read.text(). Then we try to split the whole text so that each paper becomes one record in the output table. First we did it with simple regex looking for the number+dot+space pattern (because in the txt file, the papers were indicated with 1. and 2. and 3. and so on) and then improved it by adding the contraint that the numbers should be sequential.   

`bronze.raw_pubmed_keywords` where a Spark UDF scans each abstract's raw_text for 18 lung-cancer risk terms: smoking, tobacco, cigarette, radon, asbestos, pm2.5, pm10, particulate, pollution, carcinogen, exposure, occupational, genetic, mutation, adenocarcinoma, squamous, small cell, non-small cell
We add these two columns: risk_keywords array and keyword_count

#### Section 3: Real-Time Air Quality Data

Source: [Open-Meteo Air Quality API](https://air-quality-api.open-meteo.com/)

14 countries were fetched with their capital's coordinates. For each country we got the hourly data of past 4 days + tomorrow's prediction (near 120 hours). The API provides different air quality measurements but we just request pm10 amd pm2.5.

#### Structured Logging

Every ingestion event is logged to bronze.pipeline_logs as a Delta table entry with:

| Field | Description |
|---|---|
| timestamp | UTC ISO-8601 timestamp of the event |
| pipeline_stage | Always 'bronze' for this notebook |
| table | Target table name |
| records | Number of rows written |
| source | Source file path or API URL |
| status | 'success' or 'failed' |
| error | Error message if failed, else None |

The logger uses structlog for structured JSON-format output to the Databricks driver logs.

#### Output Tables

| Table | Rows | Description |
|---|---|---|
| bronze.raw_lung_cancer | 220,632 | lung cancer record for each patient |
| bronze.raw_who_pollution | 13,177 | WHO pollution mortality data |
| bronze.raw_pubmed_abstracts | 10000 | PubMed articles about lung cancer with their abstracts |
| bronze.raw_pubmed_keywords | 10000 | Same records with risk keyword arrays |
| bronze.raw_air_quality | 1,680 | Hourly PM10/PM2.5 by country |
| bronze.pipeline_logs | growing | Structured ingestion audit log |

---

### 3. `Silver_ETL.ipynb`: Cleaning, Transformation & Validation

**Purpose:** Apply ETL and cleaning on the bronze layer

A log_step() helper tracks records_before and records_after for every transformation step which prints a diff for each stage.

#### Lung Cancer Data -> `silver.lung_cancer`

1. Column rename: all column names lowercased and spaces replaced with underscores
2. Whitespace trim: applied to all StringType columns
3. Type casting:
   - age -> IntegerType
   - cancer_stage -> extract numeric part via regex -> IntegerType
   - survival_years → DoubleType
   - cigarettes_per_day → IntegerType
4. Null drop: rows with null age, country, or gender dropped
5. Deduplication: using dropDuplicates()
6. Metadata added: _silver_timestamp, _silver_version = '1.0'

#### WHO Pollution Data → `silver.who_pollution`

1. Deduplication
2. Whitespace trim
3. Type casting: Year -> IntegerType, ValueNumeric/Low/High -> FloatType
4. Gender normalization:  BOTH SEXES -> Both
5. Range validation: Year nulled if outside 1900–2100; ValueNumeric/Low/High nulled if negative
6. Column drop: raw Value string column removed

#### Air Quality Data → `silver.air_quality`

1. Deduplication
2. AQI calculation:
   - pm25_aqi(pm): PM2.5 AQI via linear interpolation across 5 breakpoints
   - pm10_aqi(pm): PM10 AQI via linear interpolation across 5 breakpoints
   - Final AQI = max(pm25_aqi, pm10_aqi)
3. Aggregation by country
4. AQI category assigned based on avg_aqi: ≤ 50: Good | ≤ 100: Moderate | ≤ 150: Unhealthy for Sensitive Groups ≤ 200: Unhealthy | ≤ 300: Very Unhealthy | > 300: Hazardous


#### PubMed Abstracts → `silver.abstracts`

1. Deduplication
2. Structured extraction via UDFs:
   - get_year(raw): extracts 4-digit year from citation line
   - get_journal(raw): extracts journal name from citation
   - get_title(raw): second paragraph block
   - get_authors(raw): third paragraph, strips affiliation numbers
   - get_abstract(raw): text between Author information: and DOI:/PMID: markers
   - get_doi(raw): extracts DOI string
   - get_pmid(raw): extracts PubMed ID number
   - get_pmcid(raw): extracts PubMed Central ID


#### Advanced Metadata Validation: Great Expectations

It runs on a 10,000 row sample of silver.lung_cancer. And we check for 5 things:
1. age column exists
2. cancer_stage column exists
3. country column is not null
4. age is between 0 and 120
5. gender is either 'Male' or 'Female'

Results printed as: Validation passed: True/False | Passed: X / 5

#### Output Tables

| Table | Description |
|---|---|
| silver.lung_cancer | ~220k rows, cleaned and typed |
| silver.who_pollution  | ~13k rows, normalized |
| silver.air_quality | 14 rows (one per country), aggregated AQI |
| silver.abstracts | Structured PubMed metadata |

---

### 4. `Gold_Aggregations.ipynb`: Final Tables for Analytics

**Purpose:** This is actually the best version of the data which is aggregated from Silver data

#### `gold.risk_by_country`

Aggregated from silver.lung_cancer and is grouped by country. So for each country we'll have:

| Column | Calculation |
|---|---|
| total_patients | COUNT(*) |
| cancer_cases | SUM(WHEN lung_cancer_diagnosis = 'Yes') |
| avg_age | AVG(age) |
| smokers | SUM(WHEN smoker = 'Yes') |
| avg_cigarettes_per_day | AVG(cigarettes_per_day) |
| avg_mortality_rate | AVG(mortality_rate) |
| cancer_rate | ROUND(cancer_cases / total_patients, 4) |
| smoker_rate | ROUND(smokers / total_patients, 4) |

Optimized: OPTIMIZE ... ZORDER BY (country) + VACUUM RETAIN 168 HOURS
#### `gold.ml_features`

These features were selected for training the ML model: age, gender, country, smoker, years_of_smoking, cigarettes_per_day, passive_smoker, family_history, air_pollution_exposure, occupational_exposure, indoor_pollution, lung_cancer_diagnosis

lung_cancer_diagnosis is the target label.

Optimized: ZORDER BY (country, age)

#### `gold.who_country_summary`

We agregated from silver.who_pollution (grduped by Country). These are the final features for each country: avg_deaths, max_deaths, earliest_year, latest_year.

Optimized: ZORDER BY (country)

#### `gold.pubmed_keyword_summary`

From silver.abstracts we did these:
- Group by risk_keywords array -> abstract_count
- Explode keyword array -> one row per keyword
- Re-aggregate to get total_mentions per keyword
- Ordered by total_mentions (descending)

Optimized: ZORDER BY (keyword)

#### `gold.air_quality_summary`

From silver.air_quality we selected these columns: country, avg_pm2_5, avg_pm10, avg_aqi, max_aqi, aqi_category

Optimized: ZORDER BY (country)

#### Performance Tuning Applied

All Gold tables receive:
- **OPTIMIZE ... ZORDER BY (...)**: It makes the queries efficient by minimizing the data scanned per query
- **VACUUM RETAIN 168 HOURS**: It removes Delta Lake version files older than 7 days for more space
- **DESCRIBE HISTORY**: It inspects Delta table version history to confirm optimization ran

---

### 5. `ML_Models.ipynb`: XGBoost Training + MLflow

**Purpose:** Train a binary classification model to predict lung cancer diagnosis, track the experiment with MLflow, register the model, and write predictions to the Gold layer.

#### Data Preparation

We first load gold.ml_features and convert it to a Pandas DataFrame. As it was mentioned earlier, the target variable is "lung_cancer_diagnosis" which can be Yes/No. Also we know that there's an imbalance between two calsses (cancer is only 3%). We addressed this issue with scale_pos_weight.

Label encoding applied to categorical columns like gender and country.

Feature correlation analysis: All encoded features correlated against target to identify top predictors.

Train/test split: 80% train / 20% test, stratified by the target class

#### Final Features Used

After correlation analysis, four features selected for the final model: smoker_enc, cigarettes_per_day, years_of_smoking, gender_enc

#### XGBoost Training

**Hyperparameters:**
n_estimators -> 300
max_depth -> 5
learning_rate -> 0.05
subsample -> 0.8
colsample_bytree -> 0.8
scale_pos_weight -> neg/pos ratio

**MLflow tracking** (`/lung_cancer_risk_prediction` experiment):
- All hyperparameters logged via mlflow.log_params()
- Metrics logged: auc (ROC-AUC), accuracy, f1
- Model artifact logged via mlflow.xgboost.log_model()
- Model signature inferred from training data and saved
- Input example (5 rows) saved with the model

**Model registry:** Registered as LungCancerRiskModel (versioned). Each run creates a new version.

#### Predictions

We put the decision threshold as 0.3. It's lower than default (0.5) because we wanted it to intentionally be sensitive for cancer screening. You can see it in gold.risk_predictions. There, in addition to 4 training features we have these three columns:


- actual-> True label (0 or 1)
- predicted_prob -> Model output probability (0.0–1.0)
- predicted_label -> Binary prediction at threshold 0.3

---

### 6. `Pipeline_Dashboard.ipynb`: SQL Visualizations

**Purpose:** Interactive dashboard for exploring results and monitoring pipeline health.

All cells use %sql magic. Each query is displayed as a Databricks native visualization (bar chart, scatter plot, or table).

#### Query 1: Cancer Rate by Country

```sql
SELECT country, cancer_cases, total_patients,
       ROUND(cancer_rate * 100, 2) AS cancer_rate_pct,
       ROUND(smoker_rate * 100, 2) AS smoker_rate_pct,
       ROUND(avg_mortality_rate, 2) AS avg_mortality_rate
FROM gold.risk_by_country
ORDER BY cancer_rate_pct DESC
```
**Visualization:** Bar chart - countries ranked by lung cancer rate percentage

#### Query 2: Cancer Rate vs. Air Quality

```sql
SELECT r.country,
       ROUND(r.cancer_rate * 100, 2) AS cancer_rate_pct,
       a.avg_aqi, a.aqi_category, r.total_patients
FROM gold.risk_by_country r
JOIN gold.air_quality_summary a ON r.country = a.country
```
**Visualization:** Scatter plot - AQI vs. cancer rate per country

#### Query 3: PubMed Risk Factor Keywords

```sql
SELECT keyword, total_mentions
FROM gold.pubmed_keyword_summary
ORDER BY total_mentions DESC
```
**Visualization:** Bar chart - most mentioned lung cancer risk terms in scientific literature

#### Query 4: Smoking Rate by Country

```sql
SELECT country,
       ROUND(smoker_rate * 100, 2) AS smoker_rate_pct,
       ROUND(cancer_rate * 100, 2) AS cancer_rate_pct,
       total_patients, cancer_cases
FROM gold.risk_by_country
ORDER BY smoker_rate_pct DESC
```
**Visualization:** Bar chart - countries ranked by smoking rate

#### Query 5: Air Quality Category Distribution

```sql
SELECT aqi_category, COUNT(*) AS country_count,
       ROUND(AVG(avg_aqi), 1) AS avg_aqi
FROM gold.air_quality_summary
GROUP BY aqi_category
ORDER BY avg_aqi
```
**Visualization:** Table or bar chart - number of countries per AQI category

#### Query 6: Pipeline Statistics (Ingestion Audit)

```sql
SELECT stage, `table`,
       SUM(records_after) AS total_records,
       COUNT(*) AS runs,
       MAX(timestamp)     AS last_run,
       SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failures
FROM bronze.pipeline_logs
GROUP BY stage, `table`
ORDER BY last_run DESC
```
**Visualization:** Table - per table ingestion counts, run timestamps, and failure counts