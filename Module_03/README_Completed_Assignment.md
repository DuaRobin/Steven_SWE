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

## Architecture & Design Choices

* **Chunk Size and Overlap:** We implemented a **fixed-size chunking strategy with a maximum of 1,200 characters per chunk and a 200-character overlap**. This character limit ensures we stay safely within the 2,048-token input limit of the `gemini-embedding-001` embedding model. The 200-character overlap prevents the fragmentation of meaning at the boundaries, ensuring that context isn't lost if a sentence is split.

* **Vector Index Architecture (HNSW):** We utilize an **HNSW (Hierarchical Navigable Small World) index via PostgreSQL/pgvector**. HNSW was selected because it delivers very low-latency approximate nearest-neighbor search for medium-scale corpora (under 50 million vectors) and **supports incremental updates**, meaning we can continuously ingest new policy documents without having to rebuild the entire index. Additionally, using `pgvector` allows us to combine our vector similarity searches with structured SQL data filters (like document metadata) in a single query.

* **Top-K Retrieval:** Our retrieval step targets a Top-5 optimized to balance recall and precision (often evaluated as **recall@10** in our testing). We constrain the number of returned chunks to ensure the language model has enough contextual data to answer the prompt accurately, without retrieving so many chunks that the semantic signal is diluted by irrelevant noise.

* **Vector Dimension Size:** We configured our `gemini-embedding-001` model to output **768-dimensional vectors** instead of the default 3,072. By leveraging Matryoshka Representation Learning (MRL), truncating to 768 dimensions allows us to retain approximately 95–97% of full recall while achieving a 4x reduction in storage costs and faster nearest-neighbor search latency. This 768-dimension target serves as a practical, optimal baseline for balancing retrieval performance and memory constraints.
<br/>
<br/>
<br/>
<div id="task-01" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-01 | 1 | Read the PDF's (load.py) | [Python Code (GitHub)](./rag-assignment/ingest/1.load.py) | [Output Data File](./output_data/all_pdfs_data.json)<br><br>[Output Log File](./logs/ingest.log) | Python Code For Task01 Step-1 With Output & Logs |
| Task-01 | 2 | Split into chunks (chunk.py) | [Python Code (GitHub)](./rag-assignment/ingest/2.chunk.py) | [Output Data File](./output_data/all_pdfs_chunks.json)<br><br>[Output Log File](./logs/chunk.log) | Python Code For Task01 Step-2 With Output & Logs |
| Task-01 | 3 | Create embeddings (embed.py) | [Python Code (GitHub)](./rag-assignment/ingest/3.embed.py) | [Output Data File](./output_data/split_embeddings/)<br><br>[Output Log File](./logs/embed.log) | Python Code For Task01 Step-3 With Output & Logs |
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
| Task-03 | 1 | API Code (GitHub) With Retrieve (Top-5) & Generate | | [Please Refer Here For retrieve, generate & api code](./rag-assignment/serve/) | Retrieve (Top-5), Generate & API Code For Task03 |
| Task-03 | 2 | API Testing With Full Response | | ![Example-1](./images/Task03/API_Testing_Example_1.png)<br>![Example-2](./images/Task03/API_Testing_Example_2.png)<br>![Example-3](./images/Task03/API_Testing_Example_3.png) | Testing via Postman using questions from the golden set |
---

</div>
<br/>
<br/>
<br/>
To ensure the reliability of our CMS Policy Assistant, we evaluated the system against a golden set of **25 questions** using our `eval/run_eval.py` script. The evaluation results (documented in `eval_results.json`) measure two primary rubrics:

* **Factual Accuracy (Mean Score: 3.68):** This rubric evaluates how accurately and comprehensively the generated answer addresses the user's question. It measures whether the pipeline successfully retrieved the right information and formulated the correct response.
* **Faithfulness (Mean Score: 4.12):** This rubric evaluates how strictly the generated answer is grounded in the retrieved context. A high score here indicates that the model is successfully adhering to our strict system prompt to only use the provided policy documents, effectively minimizing hallucinations.
<div id="task-04" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Task-04 | 1 | Evaluation Script (GitHub) | | [Please Refer Here For Evaluation Script](./rag-assignment/eval/run_eval.py) | Python Script to Invoke Query API For Every Question (25) in Golden Set For Evaluation |
| Task-04 | 2 | Evaluation Report | | [Please Refer Here For Evaluation Results](./rag-assignment/eval/eval_results.json) | Result of Executing eval.py |
---

</div>