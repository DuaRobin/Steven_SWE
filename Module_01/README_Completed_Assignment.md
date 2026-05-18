<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-1   | Robin Dua |

---

</div id="pre-flight" align="center" style="color: #23d4c5;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--: | :--: | :---------: | :----------------------------------- | :-------------------: | :---: |
| Pre&#8209;Flight | 1 | Create BigQuery Dataset | `bq mk --dataset --location=US \`<br>`--description="Week 1 - rdua1" \`<br>`$GOOGLE_CLOUD_PROJECT:rdua1_ml` | ![BQ Datasets](./Images/BigQuery_Dataset.png) | verify the configured project and bq dataset                |
| Pre&#8209;Flight | 2.1 | Enable Cloud Build API | `gcloud services enable cloudbuild.googleapis.com`| N/A | Service needs to be enabled before adding permissions on SA |
| Pre&#8209;Flight | 2.2  | Grant Cloud Build Deployment Permissions | `PROJECT_NUM=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \`<br>`--format="value(projectNumber)")`<br><br>`CB_SA="${PROJECT_NUM}@cloudbuild.gserviceaccount.com"`<br><br>`for ROLE in roles/run.admin roles/iam.serviceAccountUser; do`<br>`gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \`<br>`--member="serviceAccount:${CB_SA}" --role="$ROLE"`<br>`done` | ![BQ Datasets](./Images/CloudBuild_SA_Roles.png)  | Console View                                                |

---

</div>
