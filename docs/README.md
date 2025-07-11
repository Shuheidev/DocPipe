# DocPipe Documentation

DocPipe is an automated documentation pipeline. It generates a set of artefacts from a project name and short description. The pipeline is composed of asynchronous agents that write files and a small React interface for interacting with the API.

## Overview

The backend exposes a `/generate` endpoint using **FastAPI**. When the endpoint receives a payload it sequentially runs a series of agents:

- **BrdAgent** – produces a Business Requirement Document (BRD).
- **SolutionAgent** – writes a brief solution proposal.
- **FigmaAgent** – creates a placeholder Figma project and stores the resulting URLs.
- **StoryAgent** – generates epics and user stories and optionally pushes them to Jira.

Each agent writes its artefact to the same output directory and returns an `AgentResult` describing the artefact type and location. The caller receives a list of these results.

A simple React application under `frontend/` allows submitting a project description and displays the generated artefacts.

## Architecture

```
Client (React) ---> /generate (FastAPI) ---> Agents ---> Output files
```

1. **API** (`api/dispatcher.py`)
   - Defines the `/generate` route.
   - Creates a timestamped output directory for each request.
   - Instantiates and executes all agents concurrently.
   - Stubbed `GitHubClient` demonstrates how results might be pushed to a pull request.
2. **Agents** (`agents/`)
   - All agents inherit from `BaseAgent` which provides a retry wrapper and a common `execute` method.
   - Jinja2 templates under `prompts/` are used to render text files.
   - Agents may depend on external services (e.g. Jira or Figma); dummy clients are provided for tests.
3. **Frontend** (`frontend/`)
   - Built with Vite and React.
   - Offers a small form that POSTs to the API and lists the artefacts returned.

## Getting Started

1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the API server:

   ```bash
   uvicorn api.dispatcher:app --reload
   ```

3. (Optional) Start the React frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The API will listen on `localhost:8000` by default. The frontend expects the API on the same origin unless `VITE_API_URL` is set.
When the React app is hosted separately (e.g. on GitHub Pages) you must deploy the FastAPI service elsewhere and expose it over HTTPS. Set `VITE_API_URL` to this public endpoint so the POST request to `/generate` succeeds. The API includes CORS middleware allowing requests from any origin by default.

### Docker Compose

The repository includes a simple `docker-compose.yml` which starts the API and a Redis service:

```bash
docker-compose up --build
```

### Tests

Run the automated test suite with **pytest**:

```bash
pytest
```

### Type Checking

Static type checking is configured via `mypy`:

```bash
mypy
```

## Example Output
A set of mocked artefacts generated for a Salesforce UI component can be found in [docs/salesforce_demo](salesforce_demo/README.md). The same demo is presented in the frontend under the "Example" tab so visitors know what to expect.


## Directory Layout

- `agents/` – asynchronous worker classes responsible for artefact creation.
- `api/` – FastAPI application and routing logic.
- `frontend/` – React application for user interaction.
- `prompts/` – Jinja2 templates used by the agents.
- `scripts/` – helper scripts (e.g. `bootstrap_repo.py`).
- `tests/` – pytest based unit tests.

## Contributing

Contributions should keep the documentation up to date. Any new module, endpoint or behaviour must be described here or in a new file inside `docs/`.

For detailed guidelines aimed at AI powered tools see [AI guidelines](AI_GUIDELINES.md).
