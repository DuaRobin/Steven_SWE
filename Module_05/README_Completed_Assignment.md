<div id="header" align="center" style="color: #23d4c5;">

| Assignment | Student   |
| ---------- | --------- |
| Module-5   | Robin Dua |

---
</div>

<div id="phase-0" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Phase-0 | 1 | Single Agent Setup<br><br>[Python Code] | 1: Navigate the Parent Folder Where All the Agents Need To Be Created<br>`cd Module_05/policy_concierge_project`<br><br>2: Setup Policy Concierge Agent (Phase 0)<br>`adk create policy_concierge_phase_0` | [Please Refer Here For Code](./policy_concierge_project/policy_concierge_phase_0/) | Please follow adk documentation |
| Phase-0 | 2 | Initial Setup Chat History Covering All Tools  | Start Dev UI For Testing Via Terminal: <br><br>1: Navigate the Parent Folder Where All the Agents Folders Are Present<br>`cd Module_05/policy_concierge_project`<br><br>2: Start ADK Dev UI<br>`adk web` | ![Initial Setup Chat History](./images/Phase_0/Initial_Setup_Chat_History.png) | Local Testing |
---

</div>
<br/>
<br/>
<br/>
<div id="phase-1" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Phase-1 | 1 | Multiple Agent Setup<br><br>[Python Code] | 1: Navigate the Parent Folder Where All the Agents Need To Be Created<br>`cd Module_05/policy_concierge_project`<br><br>2: Setup Policy Concierge Sequential Agent (Phase 1)<br>`adk create policy_concierge_phase_1` | [Please Refer Here For Code](./policy_concierge_project/policy_concierge_phase_1/) | Please follow adk documentation |
| Phase-2 | 2 | Chat History Covering All Sub Agents  | Start Dev UI For Testing Via Terminal: <br><br>1: Navigate the Parent Folder Where All the Agents Folders Are Present<br>`cd Module_05/policy_concierge_project`<br><br>2: Start ADK Dev UI<br>`adk web` | ![Chat History Showing Invocation of Sub Agents](./images/Phase_1/Phase_1_Chat_History.png)![Chat History Showing Agent Name](./images/Phase_1/Phase_1_Agent.png) | Local Testing |
---

</div>
<br/>
<br/>
<br/>
<div id="phase-2" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Phase-2 | 1 | Deploy To Agent Engine | `adk deploy agent_engine \`<br>`--project $GOOGLE_CLOUD_PROJECT \`<br>`--region us-east1 \`<br>`--display_name "rdua1-policy-concierge" \`<br>`--trace_to_cloud \`<br>`policy_concierge_phase_1` | ![Agent Engine Deployed Successfully](./images/Phase_2/Agent_Engine_Deployed_Successfully.png) | Terminal View<br><br>[Make A Note Of The reasoningEngines Resource ID, will use it to filter Traces later]  |
| Phase-2 | 2 | Agent Engine Testing Via Console/PlayGround | `Console > Agent Platform > Agents > Deployments > rdua1-policy-concierge > Playground` | ![Agent Engine Testing Via Console/Playground](./images/Phase_2/Agent_Engine_SMoke_Test.png) | Console View |
---

</div>
<br/>
<br/>
<br/>
<div id="phase-3" align="center" style="color: #000000; background-color: #479d54;">

| Part | Step | Description | gcloud cli command (bash) or console | Results (ScreenPrint) | Notes |
| :--- | :--- | :---------- | :----------------------------------- | :-------------------- | :---- |
| Phase-3 | 1 | Enable Cloud Trace Service | `gcloud services enable cloudtrace.googleapis.com` | ![Enabled APIs](./images/Phase_3/Enabled_APIs.png) | Console View  |
| Phase-3 | 2 | Agent Engine Testing Via Console/PlayGround For Traces | `Console > Agent Platform > Agents > Deployments > rdua1-policy-concierge > Playground` | ![Agent Engine Testing Via Console/Playground Q1](./images/Phase_3/Agent_Engine_Testing_Q1.png) ![Agent Engine Testing Via Console/Playground Q2](./images/Phase_3/Agent_Engine_Testing_Q2.png) | Console View |
| Phase-3 | 3 | Filtering and Finding Traces in Trace Explorer | `Console > Trace > Trace Explorer` | ![Trace Filter](./images/Phase_3/Trace_Filter.png) ![Trace Span Q1](./images/Phase_3/Trace_Span_Q1.png) ![Trace Span Q2](./images/Phase_3/Trace_Span_Q2.png) | Console View |
---

</div>