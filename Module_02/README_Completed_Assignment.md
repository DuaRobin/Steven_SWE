<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-2   | Robin Dua |

---
</div>

<div id="pre-flight-setup" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Pre-Flight | 1 | Enable Required API's | `gcloud services enable aiplatform.googleapis.com \`<br>`discoveryengine.googleapis.com \`<br>`run.googleapis.com` | ![Enabled APIs](./Images/PreFlight/Enabled_APIs.png) | Console View |
| Pre-Flight | 2 | Bucket + Data Store For Manuals | 1: Download CMS Manuals [Internet Only Manuals, Pub 100-02 (Medicare Benefit Policy Manual), 16 Chapters]: <br><br>`mkdir -p cms_manual && cd cms_manual`<br><br>`for i in $(seq -w 1 16); do`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/\`<br>`Guidance/Manuals/Downloads/bp102c${i}.pdf"`<br>`done`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/bp102c03pdf.pdf"`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/bp102c08pdf.pdf"`<br><br>2: Create Cloud Storage Bucket<br><br>`gcloud storage buckets create gs://rdua1-stevens-swe-20049317 \`<br>`--location=us-east1 \`<br>`--default-storage-class=standard`<br><br>3: Create AI Applications - Data Store (Via Console)<br><br>`AI Applications > Data Stores > Create Data Store > Choose 'Cloud Storage' for Source > Choose 'Documents' under 'Unstructured Data Import' > Choose Bucket & Folder > Continue` | ![Cloud Storage Bucket](./Images/PreFlight/CloudStorage_Bucket_For_Manuals.png) ![Datastore](./Images/PreFlight/Datastore_with_loaded_manuals.png) | Console View |
---

</div>
<br/>
<br/>
<br/>
<div id="task-01" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-01 | 1 | Resolve permissions on compute service account before deploying | `PROJECT_NUM=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \`<br>`--format="value(projectNumber)")`<br><br>`COMPUTE_SA="${PROJECT_NUM}-compute@developer.gserviceaccount.com"`<br><br>`for ROLE in roles/aiplatform.user; do`<br>`gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \`<br>`--member="serviceAccount:${COMPUTE_SA}" --role="$ROLE"`<br>`done` | ![Compute SA Permissions](./Images/Task01/Compute_Service_Account_Permissions.png) | Console View |
| Task-01 | 2 | API Code (GitHub) | `Chat API Without Grounding First` | [Please Refer Here](./FastAPI_Task01/) | API Code For Task01 |
| Task-01 | 3 | Cloud Run Deployment<br><br>(using source, via CLI) | `gcloud run deploy rdua1-medicare-policy-chat-api \`<br>`--source . \`<br>`--region us-east1 \`<br>`--min-instances 0 \`<br>`--max-instances 1 \`<br>`--memory 512Mi \`<br>`--timeout 30 \`<br>`--no-allow-unauthenticated \`<br>`--set-env-vars ENVIRONMENT=production` | ![Cloud Run Deployed](./Images/Task01/Cloud_Run_Deployed.png)![API Health Check](./Images/Task01/Chat_API_Health_Check.png) | Deployed Cloud Run Service With Env Vars - Console View |
| Task-01 | 4 | Chat API Testing With Authorization<br><br>(using Curl/Postman) | 1: Health Check:<br><br>`curl -N -X GET https://rdua1-medicare-policy-chat-api-744841270406.us-east1.run.app/health \`<br>`-H "Authorization: Bearer $(gcloud auth print-identity-token)"`<br><br>2: Chat Request-1:<br><br>`curl -N -X POST https://rdua1-medicare-policy-chat-api-744841270406.us-east1.run.app/chat \`<br>`-H "Content-Type: application/json" \`<br>`-H "Authorization: Bearer $(gcloud auth print-identity-token)" \`<br>`-d '{"message": "What is the Capital of France?"}'`<br><br>3: Chat Request-2:<br><br>`curl -N -X POST https://rdua1-medicare-policy-chat-api-744841270406.us-east1.run.app/chat \`<br>`-H "Content-Type: application/json" \`<br>`-H "Authorization: Bearer $(gcloud auth print-identity-token)" \`<br>`-d '{"message": "What is medicare?"}'` | ![Curl Commands & Outputs](./Images/Task01/Curl_Outputs.png) ![Postman Positive Testing](./Images/Task01/Positive_Testing.png) ![Postman Negative Testing](./Images/Task01/Negative_Testing.png)| Curl & Postman Testing |
---

</div>
<br/>
<br/>
<br/>
<div id="task-02" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-02 | 1 | Resolve permissions on compute service account before deploying | `PROJECT_NUM=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \`<br>`--format="value(projectNumber)")`<br><br>`COMPUTE_SA="${PROJECT_NUM}-compute@developer.gserviceaccount.com"`<br><br>`for ROLE in roles/discoveryengine.viewer; do`<br>`gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \`<br>`--member="serviceAccount:${COMPUTE_SA}" --role="$ROLE"`<br>`done` | ![Compute SA Permissions](./Images/Task02/Compute_Service_Account_Permissions.png) | Console View |
| Task-02 | 2 | API Code (GitHub) | `Chat API Without Grounding First` | [Please Refer Here](./FastAPI_Task02/) | API Code For Task02 |
| Task-02 | 3 | Cloud Run Deployment<br><br>(using source, via CLI) | `gcloud run deploy rdua1-medicare-policy-chat-api \`<br>`--source . \`<br>`--region us-east1 \`<br>`--min-instances 0 \`<br>`--max-instances 1 \`<br>`--memory 512Mi \`<br>`--timeout 30 \`<br>`--no-allow-unauthenticated \`<br>`--set-env-vars ENVIRONMENT=production` | ![Cloud Run Deployed](./Images/Task02/Cloud_Run_Deployed_All_Traffic.png)![API Health Check](./Images/Task02/API_Health_Check_Ver-2.0.0.png) | Deployed Cloud Run Service With Env Vars - Console View |
| Task-02 | 4 | Chat API Testing With Authorization<br><br>(using Postman) | `1: Golden Question-1, Chapter 8`<br><br>`2: Golden Question-9, Chapter 1`<br><br>`3: Golden Question-15, Chapter 9` | ![Sample-Test-1](./Images/Task02/Smoke_Test_1.png) ![Sample-Test-2](./Images/Task02/Smoke_Test_2.png) ![Sample-Test-3](./Images/Task02/Smoke_Test_3.png)| Postman Testing Using Golden Set Questions|
---

</div>