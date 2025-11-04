
# Simple Docker image to run the FAIROTrials validators
FROM python:3.11-slim

# Avoid interactive prompts and set UTF-8
ENV DEBIAN_FRONTEND=noninteractive     PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (minimal, here mostly none; keep slim)
RUN apt-get update && apt-get install -y --no-install-recommends     ca-certificates  && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Install in editable mode so entrypoints are available
RUN python -m pip install --upgrade pip && pip install -e .

# Default command prints help for all CLI entry points
CMD ["/bin/sh", "-lc", "echo 'Commands:' &&   echo '  fairo-fair-meta --input samples/sample_fair_trials.json --out_csv fair_metadata_report.csv' &&   echo '  fairo-fdaaa --input samples/sample_fdaaa_trials.json --out_csv fdaaa_timeliness_report.csv' &&   echo '  fairo-accessible --input samples/sample_access_links.json --out_csv accessible_links_report.csv' &&   echo '  fairo-outcomes --input samples/sample_outcomes.json --out_csv outcome_switching_report.csv' &&   echo '  fairo-harms --input samples/sample_harms.json --out_csv consort_harms_report.csv' &&   echo '  fairo-linkage --registry samples/sample_registry_linkage.json --pubs samples/sample_publications.json --out_csv linkage_report.csv' &&   echo '  fairo-data-sharing --pubs samples/sample_data_sharing_pubs.json --out_csv data_sharing_report.csv' &&   echo '---' &&   echo 'Example:' &&   echo '  docker run --rm -v "$PWD:/work" -w /app <image> fairo-fdaaa --input samples/sample_fdaaa_trials.json --out_csv /work/fdaaa.csv'"]
