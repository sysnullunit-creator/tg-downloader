# tg-downloader

A Telegram bot for downloading videos

## Features


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sysnullunit-creator/tg-downloader.git
   cd tg-downloader
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows:

   ```powershell
   .\venv\Scripts\activate
   ```

   Linux/macOS:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:

   ```
   BOT_TOKEN=your_token_from_BotFather
   ```

5. Run the bot:

   ```bash
   python bot.py
   ```

## Docker Deployment

To run the bot in an isolated Docker container with automated restarts:

1. Create and configure `.env`:

   ```bash
   cp .env.example .env
   # Edit .env with your BOT_TOKEN
   chmod 600 .env
   ```

2. Start the container with Docker Compose:

   ```bash
   docker compose up -d --build
   ```

3. View live logs:

   ```bash
   docker compose logs -f
   ```

4. Stop the container:

   ```bash
   docker compose down
   ```

## Getting a Bot Token

1. Open Telegram and find `@BotFather`
2. Send `/newbot`
3. Follow the instructions
4. Copy the token into `.env`

## Status
Under active development


## Development & Contributing

### Git Hooks Setup

To enforce commit message and branch naming conventions locally, enable the included Git hooks:

```bash
git config core.hooksPath .githooks
# or run the setup script
./.githooks/install.sh
```

### Branch Naming Convention

All branches must follow the pattern:
`<type>/<issue-number>-<description>` or `<type>/<description>`

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `hotfix`.

Examples:
- `feat/1-whitelist-middleware`
- `fix/10-audio-extraction`
- `ci/github-actions-setup`

### Commit Message Convention

Commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
`<type>(<scope>): <subject>` or `<type>: <subject>`

Examples:
- `feat(security): implement chat ID whitelist middleware`
- `fix(downloader): handle timeout when fetching metadata`
- `ci: add github actions lint and test workflow`

### Linting & Testing

```bash
# Check code with Ruff
uv run ruff check .

# Format check with Ruff
uv run ruff format --check .

# Run test suite
uv run pytest
```
