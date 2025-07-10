# DocPipe

Documentation generation Pipeline

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
