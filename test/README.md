# Test Directory

We implemented three tests for the lung cancer risk prediction pipeline. the data contract (schema validation), the live API endpoints, and the raw sample data integrity.

---

## Running the Tests

Prerequisites:

```bash
pip install pytest requests jsonschema pandas
```

The API must be running locally on port 8000 for TestAPI to pass:

```bash
cd misc/api
uvicorn main:app --reload
```

Run all tests

```bash
pytest test/test_pipeline.py -v
```
In total there are 14 tests. An example of succesful execution can be seen in [docs/test_results.jpg](../docs/test_results.jpg)

---

## Test File: `test_pipeline.py`


First of all, this is the reference input used across tests:

```python
VALID_INPUT = {
    'age': 55,
    'country': 'Finland',
    'gender': 'Male',
    'smoker': 'Yes',
    'years_of_smoking': 20,
    'cigarettes_per_day': 15
}
```


### Class 1: `TestDataContract`: JSON Schema Validation (5 tests)

It tests that the data contract in [docs/data_contract.json](../docs/data_contract.json) correctly accepts valid inputs and rejects invalid ones using jsonschema.validate().
We designed 5 test. The first test checks that good data passes without errors. The other four tests each break one rule on purpose (like removing a required field, setting age to 999, or using a gender/smoking value that isn't allowed) and confirm that an error is raised each time.


### Class 2: `TestAPI`: Live API Endpoint Tests (6 tests)

Here there are integration tests that make real HTTP requests to the server (local host) and Validate the FastAPI service defined in [misc/api/main.py](../misc/api/main.py).

One test checks the health endpoint returns a simple "ok" response. The rest all test the /predict endpoint: they check that it returns a 200 status, that the response has the right structure, that the risk score is a number between 0 and 1, that the risk label is one of three valid words, and that bad input returns a 422 error instead of crashing.

---

### Class 3: `TestSampleData`: Data Integrity Tests (3 tests)

Here we validate the sample CSV file at data/sample_lung_cancer.csv that should have the structure and values expected after pipeline processing. These tests run without Databricks and only require pandas.

There are 3 tests. One test checks that all the required columns exist. The other two check the data inside: that no age is negative, and that the cancer diagnosis column only contains "Yes" or "No"

---

## Continuous Integration

Tests run automatically on every push to main via GitHub Actions.

Workflow file: [`.github/workflows/test.yml`](../.github/workflows/test.yml)

CI steps:
1. Check out repository
2. Set up Python 3.11
3. Install the required dependancies like fastapi and uvicorn
4. Start the API server in the background (uvicorn main:app &)
5. Wait 5 seconds for startup
6. Run pytest test/test_pipeline.py -v --tb=short

For an example see [docs/automated_testing_github_actions.jpg](../docs/automated_testing_github_actions.jpg)