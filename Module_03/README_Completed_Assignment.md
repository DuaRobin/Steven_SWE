<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-3   | Robin Dua |

---
</div>

<div id="pre-flight-1" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Pre-Flight-1 | 1 | Enable Required API's | `gcloud services enable aiplatform.googleapis.com \`<br>`sqladmin.googleapis.com run.googleapis.com` | ![Enabled APIs](./images/PreFlight01/Enabled_APIs_Console_View.png) | Console View |
| Pre-Flight-1 | 2 | Create Cloud SQL Instance For Postgres Database | 1: Create Cloud SQL Instance For Postgres Database: <br><br>`gcloud sql instances create rdua1-rag-db \`<br>`--edition=ENTERPRISE \`<br>`--database-version=POSTGRES_18 \`<br>`--tier=db-f1-micro \`<br>`--region=us-east1`<br><br>2: Create Database on the instance<br><br>`gcloud sql databases create rdua1_ragdb \`<br>`--instance=rdua1-rag-db`<br><br>3: Set password for default user 'postgres' on the instance<br><br>`gcloud sql users set-password postgres \`<br>`--instance=rdua1-rag-db \`<br>`--prompt-for-password` | | Note: This provisioning may take some time |
---

</div>
<br/>
<br/>
<br/>
<div id="pre-flight-2" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Pre-Flight-2 | 1 | Download CMS Manuals | 1: Download CMS Policy Manuals [Internet Only Manuals, Pub 100-02 (Medicare Benefit Policy Manual), 16 Chapters]:<br><br>`mkdir -p cms_manual && cd cms_manual`<br><br>`for i in $(seq -w 1 16); do`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/\`<br>`Guidance/Manuals/Downloads/bp102c${i}.pdf"`<br>`done`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/bp102c03pdf.pdf"`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/bp102c08pdf.pdf"`<br><br>2: Download CMS Claim Manuals [Internet Only Manuals, Pub 100-04 (Medicare Claims Processing Manual), 39 Chapters]<br><br>`for i in $(seq -w 1 38); do`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/\`<br>`Guidance/Manuals/Downloads/clm104c${i}.pdf"`<br>`done`<br>`curl -fsSL -O "https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/chapter-39-opioid-treatment-programs-otps.pdf"` | ![All Manuals Downloaded](./images/PreFligh02/all_manuals_downloaded.png)<br><br> [Please Refer Here For Downloaded Manuals](./corpus/) | Terminal View & GitHub Path |
---

</div>
<br/>
<br/>
<br/>
<div id="pre-flight-3" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Pre-Flight-3 | 1 | Setup Cloud SQL Auth Proxy | 1: Download Cloud SQL Auth Proxy<br><br>`curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.22.0/cloud-sql-proxy.linux.amd64`<br><br>2: Make the Cloud SQL Auth Proxy executable<br><br>`chmod +x cloud-sql-proxy` |  | will use it later in the module |
---

</div>
<br/>
<br/>
<br/>
<div id="task-01" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-01 | 1 | Read the PDF's (load.py) | [Python Code (GitHub)](./rag-assignment/ingest/1.load.py) | [Output Data File](./output_data/all_pdfs_data.json)<br><br>[Output Log File](./logs/ingest.log) | Python Code For Task01 Step-1 With Output & Logs |
| Task-01 | 2 | Split into chunks (chunk.py) | [Python Code (GitHub)](./rag-assignment/ingest/2.chunk.py) | [Output Data File](./output_data/all_pdfs_chunks.json)<br><br>[Output Log File](./logs/chunk.log) | Python Code For Task01 Step-2 With Output & Logs |
| Task-01 | 3 | Create embeddings (embed.py) | [Python Code (GitHub)](./rag-assignment/ingest/3.embed.py) | [Output Data File](./output_data/all_pdfs_embeddings.json)<br><br>[Output Log File](./logs/embed.log) | Python Code For Task01 Step-3 With Output & Logs |
| Task-01 | 4.1 | Enable vector Extension on Cloud SQL | 1: Get Instance Connection Name:<br><br>`gcloud sql instances describe rdua1-rag-db --format="value(connectionName)"`<br><br>2: Start Proxy On the Connection:<br><br>`cloud-sql-proxy --address 0.0.0.0 project-1737319559746:us-east1:rdua1-rag-db`<br><br>3: Use a separate Terminal abd Connect To Database via PSQL:<br><br>`psql -h 127.0.0.1 -U postgres` | ![Extension vector Enabled](./images/Task02/PGvector_Enabled_Via_PSQL.png) | Terminal View |
| Task-01 | 4.2 | Save to the database (store.py) | [Python Code (GitHub)](./rag-assignment/ingest/4.store.py) | [Output Log File](./logs/store.log)<br><br> ![PSQL Count From Stored Chunks](./images/Task01/CloudSQL_Stored_Chunks.png) ![Query_With_100_Rows](./images/Task01/Query_100_Rows.png) | Python Code For Task01 Step-4 With Output & Logs |
---

</div>
<br/>
<br/>
<br/>
<div id="task-02" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-02 | 1 | SQL Scripts (GitHub) |  | [Please Refer Here For All SQL Scripts](./rag-assignment/ingest/sql/) | SQL Scripts For Task02 |
| Task-02 | 2 | Query With Metadata Filter | | ![Query With Metadata Filter](./images/Task02/Query_With_Metadata_Filter.png) | Metadata Query |
---

</div>
<br/>
<br/>
<br/>
<div id="task-03" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-03 | 1 | API Code (GitHub) | `Chat API With Grounding` | [Please Refer Here](./FastAPI_Task03/) | API Code For Task03 |
| Task-03 | 2 | Cloud Run Deployment<br><br>(using source, via CLI) | `gcloud run deploy rdua1-medicare-policy-chat-api \`<br>`--source . \`<br>`--region us-east1 \`<br>`--min-instances 0 \`<br>`--max-instances 1 \`<br>`--memory 512Mi \`<br>`--timeout 30 \`<br>`--no-allow-unauthenticated \`<br>`--set-env-vars ENVIRONMENT=production` | ![Cloud Run Deployed](./Images/Task03/Deployed_Cloud_Run_Ver_3.0.0.png)![API Health Check](./Images/Task03/API_Health_Check_Ver_3.0.0.png) | Deployed Cloud Run Service With Env Vars - Console View |
| Task-03 | 3 | Chat API Testing With Authorization<br><br>(using Postman) | `1: Golden Question-15, Chapter 9`<br><br>`2: Golden Question-3, Chapter 9`<br><br>`3: Golden Question-7, Chapter 7` | ![Sample-Test-1.1](./Images/Task03/Smoke_Test_1_Part_1.png) ![Sample-Test-1.2](./Images/Task03/Smoke_Test_1_Part_2.png) ![Sample-Test-2](./Images/Task03/Smoke_Test_2.png) ![Sample-Test-3](./Images/Task03/Smoke_Test_3.png)| Postman Testing Using Golden Set Questions|
---

</div>
<br/>
<br/>
<br/>
<div id="task-04" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-04 | 1 | API Code (GitHub) | `Chat API With Grounding`<br>`(Same From Task03)` | [Please Refer Here](./FastAPI_Task04/) | API Code For Task04 |
| Task-04 | 2 | Evaluation Script (GitHub) | | [Please Refer Here](./FastAPI_Task04/eval.py) | Python Script to Invoke Chat API For Every Question in Golden Set For Evaluation |
| Task-04 | 3 | Evaluation Reports | | [Please Refer Here For Pass-1](./FastAPI_Task04/eval_results_pass_1.json) [Please Refer Here For Pass-2](./FastAPI_Task04/eval_results_pass_2.json) [Please Refer Here For Pass-3](./FastAPI_Task04/eval_results_pass_3.json) | Result of Executing eval.py |
---

</div>
<br/>
<br/>
<br/>
<div id="task-05" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-05 | 1 | API Code (GitHub) | `Chat API With Grounding` | [Please Refer Here](./FastAPI_Task05/) | API Code For Task05 |
| Task-05 | 2 | REACT UI SPA Code (GitHub) | | [Please Refer Here](./React_UI_Task05/) | React UI Supporting 'Streaming Server Events' and with Abort Controller |
| Task-05 | 3 | Chat History | | ![Please Refer Here For Chat History Screenshot](./Images/Task05/Agent_Chat_History.png) | Screenshot of the Chat |
| Task-05 | 4 | Live Chat Recording | [Download The Live Chat Recording](./Images/Task05/Agent_Chat_Recording.webm)| [▶️ Watch the Live Chat Recording](https://github.com/user-attachments/assets/ccdfabbd-da9e-4311-9d38-f50d97f5bce1) | Live Chat Recording<br><br>Note Streaming & Abort Action |
---

</div>
