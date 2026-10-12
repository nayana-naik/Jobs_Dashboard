# Global AI Jobs 2026 Dashboard

An interactive Streamlit dashboard for exploring the Global AI Jobs 2026 dataset — compensation, in-demand skills, and geographic distribution across AI job postings worldwide.

## Project structure

```
Week_1_Project_Vis/
├── README.md
├── pyproject.toml
├── data/
│   └── global_ai_jobs_2026_cleaned.csv
└── src/
    ├── app.py            # Entry point: page setup, filters, tabs
    ├── theme.py           # Color palette, chart styling, and AI summary rendering
    ├── data_loader.py     # CSV loading and caching
    ├── filters.py         # Sidebar filter widgets
    ├── ai_client.py       # AI chart summary client (Ollama)
    └── tabs/
        ├── overview.py    # Overview & Trends tab
        ├── roles.py       # Roles & Compensation tab
        ├── skills.py      # Skills & Demand tab
        └── geography.py   # Geography & Work Style tab
```

## Setup & run

This project uses [uv](https://docs.astral.sh/uv/) to manage dependencies.

```bash
git clone <repo-url>
uv run streamlit run src/app.py
```

`uv` automatically creates a virtual environment and installs the dependencies listed in `pyproject.toml` on first run — no manual `pip install` step needed. Don't have `uv`? Install it from the [uv docs](https://docs.astral.sh/uv/getting-started/installation/), or fall back to a standard venv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install streamlit pandas plotly requests python-dotenv
streamlit run src/app.py
```

The app reads its data from `data/global_ai_jobs_2026_cleaned.csv` relative to the project root — keep the `data/` folder alongside `src/`.

## AI-generated chart summaries

Each chart has a one-line AI-generated takeaway that updates automatically when filters change. It's powered by a local [Ollama](https://ollama.com) server, configured via a `.env` file at the project root (loaded automatically, kept out of git).

### Install Ollama

Pick the option for your OS:

```bash
# macOS (Homebrew)
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download and run the installer from https://ollama.com/download
```

Alternatively, download the app directly from the [Ollama downloads page](https://ollama.com/download).

Start the Ollama server (skip this if it's already running, e.g. as a background service after install):

```bash
ollama serve
```

Pull the model used by this project:

```bash
ollama pull qwen3.6
```

### Configure the app

Copy the template and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `AI_BASE_URL` | Yes | Base URL of the Ollama server, e.g. `http://localhost:11434`. Summaries are skipped with a fallback message if unset. |
| `AI_MODEL` | No | Model name (defaults to `qwen3.6`). |

## Dashboard tabs

- **Overview & Trends** — top job titles, top industries, and jobs by continent
- **Roles & Compensation** — salary heatmap by industry × specialization, experience level mix, and salary distribution by experience level
- **Skills & Demand** — top required skills and a Skill Premium Analyzer to compare median salary with vs. without a selected skill
- **Geography & Work Style** — top countries by job count, and average remote work % by industry

All charts respond to the global sidebar filters (job title, continent, industry, specialization, experience level, company size, skills, salary range), which persist across every tab.
