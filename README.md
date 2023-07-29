# backend
BlaBlaLand backend


# Setup

`pip install -r requirements.txt`

SET ENV VARS: `ELEVEN_API_KEY`, `OPENAI_API_KEY"`, `ASSEMBLYAI_API_KEY`

run PostgreSQL: `docker run --name blablapostgres -e POSTGRES_PASSWORD=postgres -d postgres:15.3-bullseye`
`

# Run

`python main.py`