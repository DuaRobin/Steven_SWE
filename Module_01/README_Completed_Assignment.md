<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-1   | Robin Dua |

---

</div id="pre-flight" align="center" style="color: #23d4c5;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--: | :--: | :---------: | :----------------------------------- | :-------------------: | :---: |
| Pre&#8209;Flight | 1 | Create BigQuery Dataset | `bq mk --dataset --location=US \`<br>`--description="Week 1 - rdua1" \`<br>`$GOOGLE_CLOUD_PROJECT:rdua1_ml` | ![BQ Datasets](./Images/BigQuery_Dataset.png) | verify the configured project and bq dataset |
| Pre&#8209;Flight | 2.1 | Enable Cloud Build API | `gcloud services enable cloudbuild.googleapis.com`| N/A | Service needs to be enabled before adding permissions on SA |
| Pre&#8209;Flight | 2.2  | Grant Cloud Build Deployment Permissions | `PROJECT_NUM=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT \`<br>`--format="value(projectNumber)")`<br><br>`CB_SA="${PROJECT_NUM}@cloudbuild.gserviceaccount.com"`<br><br>`for ROLE in roles/run.admin roles/iam.serviceAccountUser; do`<br>`gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \`<br>`--member="serviceAccount:${CB_SA}" --role="$ROLE"`<br>`done` | ![BQ Datasets](./Images/CloudBuild_SA_Roles.png)  | Console View |

---

</div>
<br/>
<br/>
<br/>
</div id="part-1" align="center" style="color: #23d4c5;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--: | :--: | :---------: | :----------------------------------: | :-------------------: | :---: |
| Part&#8209;1 | 1 | Create Model and Train | `Console > BigQuery > Studio > Classic Explorer > Query Editor` | ![Model Training](./Images/Create_And_Train_Model_v1_vs_v2.png) | Added weight tuning to improve recall to catch more defaulters |
| Part&#8209;1 | 2 | Model Evaluation | `Console > BigQuery > Studio > Classic Explorer > Query Editor` | ![Model Explain](./Images/Evaluate_Model_v1_vs_v2_training_data.png)![Model Explain](./Images/Evaluate_Model_v1_vs_v2_full_and_training_data.png) | Difference b/w V1 & V2 Model Evaluate |
| Part&#8209;1 | 3  | Model Global Explain | `Console > BigQuery > Studio > Classic Explorer > Query Editor` | ![Model Explain](./Images/Global_Explain_Model_v1_vs_v2.png)  | Difference b/w V1 & V2 Model Explain |

---

</div>
