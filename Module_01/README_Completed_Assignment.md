<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-1   | Robin Dua |

---
</div>

<div id="pre-flight" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Pre-Flight | 1 | Create BigQuery Dataset | `bq mk --dataset --location=US \`<br>`--description="Week 1 - rdua1" \`<br>`$GOOGLE_CLOUD_PROJECT:rdua1_ml` | ![BQ Datasets](./Images/PreFlight/BigQuery_Dataset.png) | verify the configured project and bq dataset |
| Pre-Flight | 2.1 | Enable Cloud Build API | `gcloud services enable cloudbuild.googleapis.com`| N/A | Service needs to be enabled before adding permissions on SA |
| Pre-Flight | 2.2  | Grant Cloud Build Deployment Permissions | `PROJECT_NUM=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \`<br>`--format="value(projectNumber)")`<br><br>`CB_SA="${PROJECT_NUM}@cloudbuild.gserviceaccount.com"`<br><br>`for ROLE in roles/run.admin roles/iam.serviceAccountUser; do`<br>`gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \`<br>`--member="serviceAccount:${CB_SA}" --role="$ROLE"`<br>`done` | ![CloudBuild Permissions](./Images/PreFlight/CloudBuild_SA_Roles.png)  | Console View |

---

</div>
<br/>
<br/>
<br/>
<div id="part-1" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Part-1 | 1 | Create Model and Train | `Console > BigQuery > Studio > Classic Explorer > Query Editor` | ![Model Training](./Images/Part1/Create_And_Train_Model_v1_vs_v2.png) | Added weight tuning to improve recall to catch more defaulters |
| Part-1 | 2 | Model Evaluation | `Console > BigQuery > Studio > Classic Explorer > Query Editor` | ![Model Evaluation](./Images/Part1/Evaluate_Model_v1_vs_v2_training_data.png)![Model Evaluation](./Images/Part1/Evaluate_Model_v1_vs_v2_full_and_training_data.png) | Difference b/w V1 & V2 Model Evaluate |
| Part-1 | 3  | Model Global Explain | `Console > BigQuery > Studio > Classic Explorer > Query Editor` | ![Model Explain](./Images/Part1/Global_Explain_Model_v1_vs_v2.png)  | Difference b/w V1 & V2 Model Explain |

---

</div>
<br/>
<br/>
<br/>
<div id="part-2" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Part-2 | 1 | Resolve permissions on compute service account before deploying | `PROJECT_NUM=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \`<br>`--format="value(projectNumber)")`<br><br>`COMPUTE_SA="${PROJECT_NUM}-compute@developer.gserviceaccount.com"`<br><br>`for ROLE in roles/artifactregistry.reader roles/artifactregistry.writer roles/logging.logWriter roles/bigquery.jobUser roles/bigquery.dataViewer; do`<br>`gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \`<br>`--member="serviceAccount:${COMPUTE_SA}" --role="$ROLE"`<br>`done` | ![Compute SA Permissions](./Images/Part2/Compute_Service_Account_Permissions.png) | Console View |
| Part-2 | 2 | Cloud Run Deployment<br><br>(using source, via CLI) | `gcloud run deploy rdua1-inference-api \`<br>`--source . \`<br>`--region us-east1 \`<br>`--min-instances 0 \`<br>`--memory 512Mi \`<br>`--timeout 30 \`<br>`--no-allow-unauthenticated \`<br>`--set-env-vars ENVIRONMENT=production` | ![Cloud Run Deployed](./Images/Part2/Cloud_Run_Deployed.png)![API Health Check](./Images/Part2/Inference_API_Health_Check.png) | Deployed Cloud Run Service With Env Vars - Console View |
| Part-2 | 3  | API Code (GitHub) | Inference API With /predict Endpoint | [Please Refer Here](./FastAPI/) |  |
| Part-2 | 4  | Cloud Run API Testing | Postman With Authorization Header<br><br>`gcloud auth print-identity-token` | ![Cloud Run API Testing Sample-1](./Images/Part2/ML_Predict_Payload_Sample_1.png)![Cloud Run API Testing Sample-2](./Images/Part2/ML_Predict_Payload_Sample_2.png)![Cloud Run API Testing Sample-3](./Images/Part2/ML_Predict_Payload_Sample_3.png)![Cloud Run API Testing Sample-4](./Images/Part2/ML_Predict_Payload_Sample_4.png)![Cloud Run API Testing Sample-5](./Images/Part2/ML_Predict_Payload_Sample_5.png)  | Difference b/w V1 & V2 Model Explain |

---

</div>
<br/>
<br/>
<br/>
<div id="part-3" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Part-3 | 1 | Resolve permissions on compute service account before deploying | `PROJECT_NUM=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \`<br>`--format="value(projectNumber)")`<br><br>`COMPUTE_SA="${PROJECT_NUM}-compute@developer.gserviceaccount.com"`<br><br>`for ROLE in roles/run.admin roles/iam.serviceAccountUser roles/cloudbuild.builds.editor roles/artifactregistry.admin roles/storage.admin; do`<br>`gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \`<br>`--member="serviceAccount:${COMPUTE_SA}" --role="$ROLE"`<br>`done` | ![Compute SA Permissions](./Images/Part3/Compute_SA_Permissions_Cloud_Build.png) | Console View |
| Part-3 | 2  | API Code (GitHub) | tests & cloudbuild.yaml | [Please Refer Here](./FastAPI/) |  |
| Part-3 | 3 | Cloud Run Deployment<br><br>(using source, via CI/CD CloudBuild) | `gcloud builds submit --region=us-east1 --config=cloudbuild.yaml .` | ![Successful Tests](./Images/Part3/CI_CD_Build_Logs_Step_0_Tests_Success.png)![Successful Final Build](./Images/Part3/CI_CD_Build_Logs_Step_1_Final_Build_Success.png)![Build History](./Images/Part3/Build_History.png) | Build Logs From Terminal, And Build history From Console View|

---

</div>
<br/>
<br/>
<br/>
<div id="part-4" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Part-4 | 1 | Create Workbench Instance | `gcloud workbench instances create rdua1-eda \`<br>`--location=us-east1-b \`<br>`--machine-type=e2-standard-4 \`<br>`--metadata=idle-timeout-minutes=30` | ![Compute SA Permissions](./Images/Part4/Workbench_Instance_Ready.png) | Console View |
| Part-4 | 2  | Jupyter EDA (GitHub) | Jupyter Notebook with Outputs | [Please Refer Here](./JupyterEDA/credit_default_eda.ipynb) |  |

---

</div>