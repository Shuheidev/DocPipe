# DocPipe

Documentation generation Pipeline

## Documentation

Full usage and architecture details are provided in [docs/README.md](docs/README.md). Any contributor, human or AI, should ensure the documentation stays in sync with the codebase. See [docs/AI_GUIDELINES.md](docs/AI_GUIDELINES.md) for agent specific guidance.
A demo output is available under [docs/salesforce_demo](docs/salesforce_demo/README.md) and is also viewable from the "Example" tab of the deployed frontend.

## Frontend

A small React application lives in the `frontend` directory. It provides a form to submit a project name and description to the `/generate` API endpoint and shows the generated artefacts. The app is built with [Vite](https://vitejs.dev/) and is automatically deployed to GitHub Pages via a workflow.

### Local Development

```
cd frontend
npm install
npm run dev
```

By default the app expects the API to be available at the same origin. You can override the API base URL by setting `VITE_API_URL` in a `.env` file inside the `frontend` directory.

### Production Build

```
npm run build
```

The static files will be output to `frontend/dist`. The workflow in `.github/workflows/pages.yml` publishes this directory to GitHub Pages whenever changes are pushed to `main`.

### GitHub Pages

Before publishing the site you should replace the placeholder value in `frontend/package.json` with your GitHub username:

```json
"homepage": "https://<your-username>.github.io/DocPipe/"
```

The Vite configuration already sets `base: '/DocPipe/'` so the app loads correctly from the Pages URL. Remember that GitHub Pages is **static hosting only**. You must run the FastAPI backend elsewhere (for example on a cloud VM or PaaS) and expose it over HTTPS. Set `VITE_API_URL` in `frontend/.env` to point at this backend so the React app can POST to `/generate`.

### Type Checking

Run mypy to check the Python modules:

```
mypy
```

