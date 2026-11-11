# FastAPI Calculator

A browser-based calculator built with FastAPI and Python. The application supports addition, subtraction, multiplication, and division.

This project was completed for Module 8, Build and Test Your First Web Application with FastAPI. It demonstrates REST API development, automated testing, logging, Docker, and GitHub Actions.

## Features

- Four arithmetic operations through a browser interface and REST API.
- Input validation using Pydantic.
- Error handling for invalid requests and division by zero.
- Logging for successful calculations and errors.
- Unit, integration, and Playwright browser tests.
- Docker support with a non-root application user and health check.
- GitHub Actions for testing, vulnerability scanning, and publishing images to Docker Hub.

## Test Results

The verified test suite contains 28 passing tests.

| Test file | Tests | Purpose |
|---|---:|---|
| `tests/test_operations.py` | 9 | Check arithmetic functions and division by zero |
| `tests/test_main.py` | 14 | Check endpoints, validation, error handling, and startup |
| `tests/test_e2e.py` | 5 | Check browser calculations and recovery after an error |
| **Total** | **28** | |

The measured application code achieved 100% statement coverage.

| File | Statement coverage |
|---|---:|
| `app/operations/__init__.py` | 100% |
| `main.py` | 100% |
| **Total** | **100%** |

Coverage measures the Python application code. Browser interactions are verified separately through Playwright assertions.

## Technologies

- Python
- FastAPI and Uvicorn
- Pydantic
- Jinja2, HTML, and JavaScript
- pytest and pytest-cov
- Playwright with Chromium
- Docker
- GitHub Actions
- Trivy

## Prerequisites

For the Docker workflow, install Docker and ensure the Docker engine is running.

For local development, install Python and create a virtual environment. The Docker image uses Python 3.10.

## Download the Project

Clone your GitHub repository and open its directory.

```bash
git clone https://github.com/rajaramnpatil/fastapi-calculator
cd fastapi-calculator
```

## Run with Docker

Build the image from the project root.

```bash
docker build -t fastapi-calculator .
```

Start the calculator.

```bash
docker run --rm -d \
  --name fastapi-calculator \
  -p 127.0.0.1:8000:8000 \
  fastapi-calculator
```

Open the calculator at [http://localhost:8000](http://localhost:8000).

Enter two numbers and select an operation. For example, dividing `5` by `2` displays `Calculation Result: 2.5`.

View application logs.

```bash
docker logs fastapi-calculator
```

Stop the container when finished.

```bash
docker stop fastapi-calculator
```

The `--rm` option removes the container when it stops.

The image includes Chromium and its Linux dependencies. The first build downloads these dependencies. Later builds can reuse Docker's cached layers.

## Run Tests in Docker

Keep the calculator container running while executing the tests. Playwright connects to the application at `http://127.0.0.1:8000` inside the container.

Run the complete suite with coverage.

```bash
docker exec fastapi-calculator python -m pytest tests/ -v
```

Run unit and integration tests.

```bash
docker exec fastapi-calculator python -m pytest \
  tests/test_operations.py tests/test_main.py -v
```

Run browser tests separately.

```bash
docker exec fastapi-calculator python -m pytest \
  tests/test_e2e.py -v --no-cov
```

The browser-only command disables coverage because the application runs in a separate Uvicorn process.

Rebuild the image and recreate the container after changing application code, tests, or configuration.

## View the Coverage Report

The test configuration generates a terminal report and an HTML report.

After running the full suite, copy the HTML report from the container.

```bash
docker cp fastapi-calculator:/app/htmlcov ./htmlcov
```

Open `htmlcov/index.html` in a browser. Copy the report before stopping the container.

## Run Locally

Create and activate a virtual environment from the project root.

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies and start the application.

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000). Stop the application with `Ctrl+C`.

Local unit and integration tests can be run with:

```bash
python -m pytest tests/test_operations.py tests/test_main.py -v
```

Use the Docker instructions for Playwright tests. The project's pinned Playwright 1.58.0 failed to install Chromium directly on the Ubuntu 26.04 development host. The Debian-based Docker environment successfully ran all browser tests.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Display the calculator |
| POST | `/add` | Add two numbers |
| POST | `/subtract` | Subtract the second number from the first |
| POST | `/multiply` | Multiply two numbers |
| POST | `/divide` | Divide the first number by the second |

Each arithmetic endpoint accepts a JSON request body.

```json
{
  "a": 5,
  "b": 2
}
```

A successful request to `/divide` returns:

```json
{
  "result": 2.5
}
```

Division by zero returns HTTP 400.

```json
{
  "error": "Cannot divide by zero!"
}
```

Invalid request data also returns HTTP 400 with an `error` message.

Interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Logging

The application logs successful calculations at INFO level and errors at ERROR level.

Logs help identify which operations ran and investigate invalid input, division by zero, and unexpected failures. Container logs are available through `docker logs`.

## pytest Configuration

`pytest.ini` defines test discovery and coverage reporting.

- Tests are discovered under `tests/`.
- Coverage includes the `app` package and `main.py`.
- Terminal reports show uncovered lines.
- HTML reports are written to `htmlcov/`.
- Registered markers can be applied to categorize tests.

## GitHub Actions

The workflow contains three jobs.

1. **Test** builds the Docker image, starts the calculator, waits for it to respond, and runs all tests inside the container.
2. **Security** builds an image and scans it with Trivy. The configured scan fails on fixable HIGH or CRITICAL findings.
3. **Deploy** runs after the security job succeeds on `main` and publishes images to Docker Hub.

The deploy job publishes container images. Running the web application requires starting a container on a host.

Docker Hub publishing uses these repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

### Security Scan Exception

The Trivy configuration excludes pip's embedded inventory file:

```text
**/site-packages/pip/_vendor/bom.cdx.json
```

This addresses a confirmed metadata mismatch. The embedded inventory reported setuptools 70.3.0, while inspection of the scanned image confirmed installed setuptools 84.2.1 and a bundled ensurepip wheel at 79.0.1.

The exclusion applies to all records in that specific inventory file. Installed package metadata continues to be scanned.

## Docker Hub Images

Images are published to:

[rajaramnpatil/601_module8](https://hub.docker.com/r/rajaramnpatil/601_module8)

Each successful publication creates two tags.

| Tag | Purpose |
|---|---|
| `latest` | Most recently published build |
| Git commit SHA | Build associated with that commit |

Run the published image with:

```bash
docker pull rajaramnpatil/601_module8:latest

docker run --rm \
  -p 127.0.0.1:8000:8000 \
  rajaramnpatil/601_module8:latest
```

The publication workflow targets Linux AMD64 and ARM64.



## 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

## 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

## 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)


## Author

Rajaram Patil  
MS in Computer Science  
NJIT, Fall 2026