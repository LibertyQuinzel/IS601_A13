  # Module 13 — JWT Authentication and CI/CD Pipeline

  This repository contains a small FastAPI application that provides simple calculator operations and user management (registration, login, and JWT-based authentication). It includes unit, integration, and end-to-end tests (Playwright), a CI workflow that runs tests and publishes a Docker image, and example front-end pages for manual verification.

  ---

  ## What this project includes

  - FastAPI application (`main.py` & `app/`)
    - `app/routers/users.py` — register and login endpoints and a protected `GET /users/me`
    - `app/routers/calculations.py` — calculator endpoints
    - `app/security.py` — password hashing and JWT helpers
    - `app/crud.py`, `app/models.py`, `app/db.py` — DB access and models
  - Front-end templates in `templates/`:
    - `register.html` and `login.html` with client-side validation and token storage in `localStorage`
  - Tests in `tests/`:
    - Unit, integration, and Playwright E2E tests (Playwright-driven browser tests in `tests/e2e/`)
  - CI workflow at `.github/workflows/ci.yml` that runs tests and pushes a Docker image to Docker Hub
  - `generate_secret.py` — helper script to securely generate a `SECRET_KEY` value

  ---

  ## Prerequisites

  - Python 3.10+ (the project uses modern typing and Pydantic v2 patterns)
  - pip
  - Optional: Docker (to build/push images locally), and `gh` CLI if you want to manage secrets from the command line

  ---

  ## Quick local setup

  1. Create and activate a virtual environment (recommended):

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  ```

  2. Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

  3. (Optional) Install Playwright browsers for E2E tests:

  ```bash
  python -m playwright install --with-deps
  ```

  4. Generate and set a strong SECRET_KEY for JWT signing (recommended):

  ```bash
  # generate a URL-safe secret and copy it
  python3 generate_secret.py --bytes 32 --format urlsafe

  # export into your shell session (replace with the actual generated value)
  export SECRET_KEY='paste-generated-value-here'
  ```

  The application falls back to a default insecure secret if `SECRET_KEY` is not set — do not rely on that for production or public CI.

  ---

  ## Run the application (development)

  Start the app with Uvicorn from the project root:

  ```bash
  uvicorn main:app --reload
  ```

  Open these URLs in your browser:

  - `http://127.0.0.1:8000/` — index page
  - `http://127.0.0.1:8000/register` — registration page (front-end)
  - `http://127.0.0.1:8000/login` — login page (front-end)
  - `http://127.0.0.1:8000/docs` — OpenAPI (Swagger) UI

  Manual verification flow:
  - Register a user in `/register` using an email and a password of at least 8 characters. The frontend stores the returned JWT in `localStorage`.
  - Login using `/login` with the same credentials; the JWT is stored again.
  - From your browser DevTools console, you can call the protected endpoint `/users/me` and pass the stored token in the `Authorization: Bearer <TOKEN>` header to confirm the current user is returned.

  Example JS (browser console):

  ```js
  const token = localStorage.getItem('access_token');
  fetch('/users/me', { headers: { Authorization: 'Bearer ' + token } }).then(r => r.json()).then(console.log);
  ```

  Or using curl (replace `<TOKEN>`):

  ```bash
  curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:8000/users/me | jq
  ```

  ---

  ## API endpoints (high-level)

  - POST `/users/register` — register a new user. Request body (JSON): `{ "email": "you@example.com", "password": "password123" }`.
  - POST `/users/login` — log in and receive `{ "access_token": "...", "token_type": "bearer" }`.
  - GET `/users/me` — protected; returns the current user (requires `Authorization: Bearer <token>` header).
  - Calculation endpoints are available under `/calculations`.

  Server enforces basic Pydantic validation for email and password (server-side password minimum length validator is present). Client-side forms also validate email format and password length.

  ---

  ## Testing

  Run the test suite locally from the project root (with your venv active):

  ```bash
  pytest -q
  ```

  - To run only e2e tests (Playwright tests are marked `@pytest.mark.e2e`):

  ```bash
  pytest -q -m e2e
  ```

  - To run a single test file:

  ```bash
  pytest -q tests/test_user_integration.py
  ```

  Notes:
  - Playwright E2E tests require browser binaries (`python -m playwright install --with-deps`).
  - `tests/conftest.py` starts the FastAPI server for E2E tests and creates DB tables before tests run.
  - The repository includes coverage reporting; the default `pytest` addopts produces an HTML report in `htmlcov/`.

  ---

  ## CI / GitHub Actions

  The workflow in `.github/workflows/ci.yml` performs the following (main job `test`):

  - Starts a Postgres service container (Postgres 15) for the job
  - Installs Python and project dependencies
  - Installs Playwright browsers
  - Waits for Postgres to be ready, then runs `pytest` (unit, integration, and e2e tests)

  If the tests pass, a `docker` job builds a Docker image and pushes it to Docker Hub. To allow the docker job to push, add the following secrets to your GitHub repository:

  - `SECRET_KEY` — a secure key for JWT signing (use the `generate_secret.py` helper to generate one)
  - `DOCKERHUB_USERNAME` — your Docker Hub username
  - `DOCKERHUB_TOKEN` — a Docker Hub access token

  Example: add a `TEST_DATABASE_URL` secret instead of embedding DB credentials directly, and set `DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}` in the workflow environment for safety.

  ---

  ## Docker

  A `Dockerfile` is included for building the application image. The CI workflow already builds and pushes an image as `${{ secrets.DOCKERHUB_USERNAME }}/is601_app:latest` when `DOCKERHUB` secrets are configured.

  To build and run locally:

  ```bash
  # build
  docker build -t yourusername/is601_app:local .

  # run (example using SQLite default DB in the container)
  docker run -e SECRET_KEY="$SECRET_KEY" -p 8000:8000 yourusername/is601_app:local
  ```

  ---

  ## Submission checklist (Module 13 grading requirements)

  Ensure your repository contains the following before submission:

  - Source code for the app (`app/`), templates (`templates/`), tests (`tests/`), and CI workflow (`.github/workflows/ci.yml`) — present in this repo.
  - A working `generate_secret.py` helper (present) and documentation on setting `SECRET_KEY` in the README (added here).
  - Playwright E2E tests covering positive and negative flows (present in `tests/e2e/`).
  - GitHub Actions run showing tests pass and Docker image push (capture this screenshot from your repository after pushing changes and setting secrets).
  - Screenshots saved in the repo under `docs/screenshots/` (recommended):
    - `ci_success.png` — GitHub Actions successful run
    - `playwright_e2e.png` — Playwright E2E passing output or a screenshot of a successful test
    - `ui_register_login.png` — Browser showing registration/login success
  - `REFLECTION.md` — a short reflection document with your development & testing notes (create this file describing what you found, challenges, and improvements).

  Add these files and reference them in the README to make it easy for graders.

  ---

  ## Security notes & best practices

  - Do NOT commit secrets (do not commit `.env` or secret values). Use GitHub repository secrets for CI and local environment variables for development.
  - Rotate the `SECRET_KEY` if it is accidentally exposed. Rotation invalidates previously issued tokens.
  - For production, consider more robust token revocation, short access token lifetimes, and refresh tokens.

  ---

  ## Troubleshooting

  - If Playwright E2E tests fail in CI but pass locally, confirm that the Playwright browsers are installed in the CI job and environment variables (like `DATABASE_URL` and `SECRET_KEY`) are set.
  - If the Docker push step fails, confirm `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets exist and are correct.
  - Check the CI logs in GitHub Actions for detailed error traces.

  ---


