<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-6   | Robin Dua |

---
</div>

<div id="pre-task" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Pre-Task | 1 | Create Bucket | Create Cloud Storage Bucket<br><br>`gcloud storage buckets create gs://rdua1-stevens-swe-20049317 \`<br>`--location=us-east1 \`<br>`--default-storage-class=standard` |  | I already had this bucket from previous modules, so used it instead of creating another bucket |
| Pre-Task | 2 | Train model from a public, claims-flavored dataset.  | [Please Refer Here For Code (GitHub)](./pre_task/make_starter.py) | ![Make Starter Output](./evidence/pre_task/Starters_Created_And_Uploaded_To_Bucket.png)<br>It also produces output files, please refer them [here](./pre_task/starter_outputs/). | Local Testing |
---

</div>
<br/>
<br/>
<br/>
<div id="task-1" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-1 | 1 | Evaluate Model | [Please Refer the Code (GitHub) Here](./task_01/evaluate.py) | ![Model Evaluation Result](./evidence/task_01/Model_Evaluation.png) | Local Testing |
| Task-1 | 2 | Model Registry | [Please Refer the Code (GitHub) Here](./task_01/register.py) | ![Model Registery Terminal View](./evidence/task_01/Model_Registry_Terminal_Output.png)![Model Registry Console](./evidence/task_01/Model_Registry_Console_View.png) | Local Testing |
| Task-1 | 3 | Model Card | | [Please Refer Model Card Here](./task_01/model_card.md) | |
---

</div>
<br/>
<br/>
<br/>
<div id="task-2" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-2 | 1 | Deploy Model To Agent Platform (Vertex AI) | [Please Refer Here For Code (GitHub)](./task_02/deploy.py) | ![Model Deployed Terminal](./evidence/task_02/Endpoint_Deployed_Successfully.png)![Model Deployed Console](./evidence/task_02/Endpoint_Deployed_Console.png) | Terminal & Console View |
| Task-2 | 2 | Smoke Test Deployed Model On Agent Platform (Vertex AI) | [Please Refer Here For Code (GitHub)](./task_02/endpoint_smoke_test.py) | ![Smoke Testing](./evidence/task_02/Endpoint_Smoke_Tested.png) | Terminal View |
---

</div>
<br/>
<br/>
<br/>
<div id="task-3" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-3 | 1 | Register Model V1.1 | [Please Refer Here For Code (GitHub)](./task_03/register_v1_1.py) | ![Model Registery V1.1](./evidence/task_03/Model_1.1_Registry.png)![Model Registery V1.1](./evidence/task_03/Model_1.1_Registry_Console.png) | Terminal & Console View  |
| Task-3 | 2 | Deploy Model V1.1 & Test 90, 10 Traffic Split | [Please Refer Here For Code (GitHub)](./task_03/deploy_v1_1.py) | ![Canary Testing 90/10 Split](./evidence/task_03/Logs_Canary_Rollout_90_10_Split.png) You can also refer the logs [here](./evidence/task_03/downloaded-logs-20260617-093826.csv) | Logs Console View |
| Task-3 | 3 | Roll Up & Move Production Aliases | 1: [Please Refer Here For Code (GitHub)](./task_03/canary_rollout.py) | ![Roll Out + Aliases](./evidence/task_03/Ramp_Up_V1_1_Full_Traffic.png) ![Roll Out + Aliases](./evidence/task_03/V1_1_Labels_And_Production_Aliases.png) | Console View |
| Task-3 | 4 | Roll Back | 1: [Please Refer Here For Code (GitHub)](./task_03/canary_rollout.py) | ![Roll BAck](./evidence/task_03/Rollback_To_V1_0_Full_Traffic.png) | Console View |
---

</div>
<br/>
<br/>
<br/>
<div id="task-4" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-4 | 1 | Enable Model Monitoring On Endpoint | | ![Model Monitoring Config 1](./evidence/task_04/Model_Monitoring_Config_1.png)![Model Monitoring Config 2](./evidence/task_04/Model_Monitoring_Config_2.png) | Console View  |
| Task-4 | 2 | Send Some Valid Traffic For Monitoring Job To Learn Schema So its State Changes from PENDING to RUNNING | 1: [Please Refer Here For Code (GitHub)](./task_03/canary_rollout_testing.py) <br><br>2: List the monitoring jobs:<br>`gcloud ai model-monitoring-jobs list \`<br>`--region=us-east1`<br><br>3: Get The State of your configured job:<br><br>`gcloud ai model-monitoring-jobs describe 1870567590095486976 \`<br>`--region=us-east1 \`<br>`--format="value(state)"`| ![Monitoring Job Running](./evidence/task_04/Model_Monitoring_Job_Running.png) | Terminal View |
| Task-4 | 3 | Inject Skew (Skew Testing) | [Please Refer Here For Code (GitHub)](./task_04/inject_skew.py) | | |
| Task-4 | 4 | Set Budget Alert @ Project (Environemnt) Level | | ![Budget Alert](./evidence/task_04/Monthly_Budget_Alert.png) | Console View<br><br> At Hartford, Each Environment gets its own Project, hence budget is set project level |
| Task-4 | 5 | Runbook | | [Please Refer Here](./runbook.md) | |
---

</div>
<br/>
<br/>
<br/>
<div id="task-5" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-5 | 1 | Reflection | | [Please Refer Here](./reflection.md) | |
---

</div>