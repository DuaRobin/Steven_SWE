<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-1   | Robin Dua |

---

</div>

<div id="part-1" align="center" style="background-color: #3c4b4a;">

| Part | Step | Description | gcloud cli command or console | Results (ScreenPrint) | Notes |
| ---- | ---- | ----------- | ----------------------------- | --------------------- | ----- |
| PreFlight | 1    | Create bq dataset | bq mk --dataset --location=US --description="Week 1 - rdua1" $GOOGLE_CLOUD_PROJECT:rdua1 | ![BQ Datasets](./Images/BigQuery_Dataset.png) | verify the configured project and bq dataset |
| PreFlight | 2.1    | Enable Cloud Build API | gcloud services enable cloudbuild.googleapis.com | N/A | Service needs to be enabled before next command |
| PreFlight | 2.2    | Grant Cloud Build Deployment Permissions | gcloud services enable cloudbuild.googleapis.com | ![BQ Datasets](./Images/CloudBuild_SA_Roles.png) | View From the Console |

---

</div>