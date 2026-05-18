<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-1   | Robin Dua |

---

</div>

<div id="part-1" align="center" style="background-color: #3c4b4a;">
<table>
  <thead>
    <tr>
      <th style="text-align: left;">Part</th>
      <th style="text-align: left;">Step</th>
      <th style="text-align: left;">Description</th>
      <th style="text-align: left;">gcloud cli command (bash) or console</th>
      <th style="text-align: left;">Results (ScreenPrint)</th>
      <th style="text-align: left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="white-space: nowrap;">Pre-Flight</td>
      <td>1</td>
      <td>Create BigQuery Dataset</td>
      <td><pre><code>bq mk --dataset --location=US \
--description="Week 1 - rdua1" \
&#36;GOOGLE_CLOUD_PROJECT:rdua1_ml</code></pre></td>
      <td><img src="./Images/BigQuery_Dataset.png" alt="BigQuery Dataset"></td>
      <td>verify the configured project and bq dataset</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;">Pre-Flight</td>
      <td>2.1</td>
      <td>Enable Cloud Build API</td>
      <td><pre><code>gcloud services enable cloudbuild.googleapis.com</code></pre></td>
      <td>N/A</td>
      <td>Service needs to be enabled before adding permissions on SA</td>
    </tr>
    <tr>
      <td style="white-space: nowrap;">Pre-Flight</td>
      <td>2.2</td>
      <td>Grant Cloud Build Deployment Permissions</td>
      <td><pre><code>PROJECT_NUM=&#36;(gcloud projects describe &#36;GOOGLE_CLOUD_PROJECT \
--format="value(projectNumber)")</code></pre>
      <pre><code>CB_SA="&#36;{PROJECT_NUM}@cloudbuild.gserviceaccount.com"</code></pre>
      <pre><code>for ROLE in roles/run.admin roles/iam.serviceAccountUser; do
gcloud projects add-iam-policy-binding &#36;GOOGLE_CLOUD_PROJECT \
--member="serviceAccount:${CB_SA}" --role="$ROLE"
done</code></pre></td>
      <td><img src="./Images/CloudBuild_SA_Roles.png" alt="BigQuery Dataset"></td>
      <td>Console View</td>
    </tr>
  </tbody>
</table>
</div>
