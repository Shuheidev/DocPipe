# Salesforce Custom UI Demo

This folder contains a small preview of DocPipe in action. The example assumes a request to generate documentation for a custom Salesforce component used to manage leads more efficiently. The output below was produced using the included agents with dummy data.

## Workflow
1. The React frontend submits a `POST /generate` request with a project name and description.
2. `dispatcher.py` creates a timestamped folder and sequentially executes all agents:
   - **BrdAgent**
   - **SolutionAgent**
   - **FigmaAgent**
   - **StoryAgent**
3. Each agent writes its artefact to the same output directory.
4. The results are returned to the frontend and could be pushed to GitHub or Jira.

## Generated Artefacts
- [`BRD.md`](output/BRD.md)
- [`Solution.md`](output/Solution.md)
- [`figma.json`](output/figma.json)
- [`epics_userstories.yaml`](output/epics_userstories.yaml)

