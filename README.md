# Selenium-PyTest-BDD-Automation Framework

A scalable, BDD-driven UI test automation framework built with Python, pytest-bdd, and Selenium WebDriver.
Tests cover the [SauceDemo](https://www.saucedemo.com/) web application across login, checkout, and end-to-end purchase flows.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Programming language |
| pytest-bdd | BDD framework (Gherkin feature files + step definitions) |
| Selenium WebDriver | Browser automation |
| Page Object Model (POM) | Separation of page logic from test logic |
| pytest-html | HTML test reports with screenshots on failure |
| Allure | Advanced test reporting |
| Docker + Selenium Grid | Distributed cross-browser execution |
| BrowserStack | Cloud-based real browser testing |
| pytest-xdist | Parallel test execution |
| python-dotenv | Environment variable management |

---

## Project Structure

```
PyTest-BDD-Automation/
├── features/
│   ├── login.feature          # Login scenarios in Gherkin
│   ├── checkout.feature       # Checkout scenarios in Gherkin
│   └── e2e.feature            # End-to-end purchase flow
├── pages/
│   ├── login.py               # Login page POM
│   ├── inventory.py           # Inventory/products page POM
│   ├── cart.py                # Cart page POM
│   ├── checkout_step1_page.py       # Checkout step one POM
│   ├── checkout_step2_page.py       # Checkout step two POM
│   └── checkoutcomplete.py    # Order confirmation POM
├── steps/
│   ├── test_login.py          # Login step definitions
│   ├── test_checkout.py       # Checkout step definitions
│   └── test_e2e.py            # E2E step definitions
├── reports/                   # Generated reports (git ignored)
├── conftest.py                # pytest fixtures and browser configuration
├── docker-compose.yml         # Selenium Grid with Chrome and Firefox nodes
├── pytest.ini                 # pytest configuration
├── requirements.txt           # Python dependencies
└── .gitignore
```

---

## Test Coverage

### Login (5 scenarios)
- Username only shows password required error
- Password only shows username required error
- Invalid credentials shows mismatch error
- Locked out user sees locked out error
- Valid credentials navigates to inventory *(smoke test)*

### Checkout (7 scenarios)
- Missing first name shows validation error
- Missing last name shows validation error
- Missing postal code shows validation error
- Cancel on step one returns to cart
- Overview page totals are correct (item price + tax = total)
- Cancel on overview returns to inventory
- Successful order completion *(smoke test)*

### End-to-End (1 scenario)
- Full purchase journey: login → add item → remove item → add item → cart → checkout → confirm *(smoke test)*

---

## Prerequisites

- Python 3.11+
- Google Chrome installed
- Firefox installed (optional)
- Docker Desktop (for Grid execution)
- BrowserStack account (for cloud execution)

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/Suriyarashmis/pytest_bdd_selenium_framework.git 
cd PyTest-BDD-Automation

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running Tests

### Local - Chrome (default)
```bash
pytest steps/
```

### Local - Firefox
```bash
pytest steps/ --browser_name=firefox
```

### Headless mode
```bash
pytest steps/ --headless
```

### Smoke tests only
```bash
pytest steps/ -m smoke
```

### Parallel execution
```bash
pytest steps/ -n 4
```

### With HTML report
```bash
pytest steps/ --html=reports/result.html --self-contained-html
```

### With Allure report
```bash
pytest steps/ --alluredir=reports/allure
allure serve reports/allure
```

---

## Docker Selenium Grid

```bash
# Start the Grid (Hub + Chrome + Firefox nodes)
docker-compose up -d

# Run steps against the Grid
pytest steps/ --env=grid --browser_name=chrome

# Run with Firefox on Grid
pytest steps/ --env=grid --browser_name=firefox

# Stop the Grid
docker-compose down
```

Grid UI available at: `http://localhost:4444`

---

## BrowserStack

```bash
# Set credentials (Windows)
set BS_USERNAME=your_username
set BS_ACCESS_KEY=your_access_key

# Set credentials (Mac/Linux)
export BS_USERNAME=your_username
export BS_ACCESS_KEY=your_access_key

# Run on BrowserStack
pytest steps/ --env=browserstack --browser_name=chrome
pytest steps/ --env=browserstack --browser_name=firefox
```

Or pass it in environment variables:
```
BS_USERNAME=your_username
BS_ACCESS_KEY=your_access_key
```

---

## CI/CD

This project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:
- Triggers automatically on push and pull requests
- Runs tests in a headless Chrome container using Selenium
- Installs dependencies and executes tests with pytest
- Generates HTML reports and saves them as downloadable artifacts

View workflow results:
```
GitHub → Actions → Run UI Tests → Run
```

---

## Key Design Decisions

**Page Object Model** — All page interactions are encapsulated in `pageObjects/`. If a locator changes, it's updated in one place only, not across every test.

**BDD with pytest-bdd** — Gherkin feature files serve as living documentation readable by non-technical stakeholders. pytest-bdd was chosen over Behave to leverage the full pytest ecosystem (fixtures, plugins, parallel execution).

**JS click over `.click()`** — Several elements on SauceDemo are intercepted by overlapping elements. `execute_script("arguments[0].click()")` bypasses this reliably.

**`context` dictionary** — A shared state dictionary is passed between BDD steps via a pytest fixture, avoiding global variables while keeping step definitions clean.

---


