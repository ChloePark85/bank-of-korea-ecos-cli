# Bank of Korea ECOS CLI

Minimal command-line client for the Bank of Korea Economic Statistics System (ECOS) Open API.

- List available statistic tables
- Fetch time series by statistic code and frequency (A,S,Q,M,D)
- JSON output, suitable for piping to jq or saving to files

## Installation

This project is a simple Python package. You can run it directly via `pipx` or `uv` once published to PyPI. For now, clone and run:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Usage

Environment variables:
- `BOK_API_KEY` (required): Your ECOS API key
- `BOK_LANG` (optional): `kr` or `en` (default: `kr`)

Commands:

```bash
# Help
ecos-cli -h

# List statistic tables (first 1000)
ecos-cli table-list | jq '.[] | .[]? // .'

# Example: Fetch a monthly time series for a statistic code between start/end dates
# Cycle: A (Annual), S (Semiannual), Q (Quarterly), M (Monthly), D (Daily)
ecos-cli series 722Y001 M 202001 202412 | jq .
```

Notes:
- Date formats depend on the cycle: `YYYY` for A/S, `YYYYQQ` for Q (ECOS accepts `YYYYQ#` in some cases), `YYYYMM` for M, `YYYYMMDD` for D.
- Output structure is a direct passthrough of the ECOS JSON response.

## API References
- ECOS API: https://ecos.bok.or.kr/api/
- StatisticTableList: `/StatisticTableList/{API_KEY}/json/{lang}/{start}/{end}/`
- StatisticSearch: `/StatisticSearch/{API_KEY}/json/{lang}/{start}/{end}/{STAT_CODE}/{CYCLE}/{START}/{END}/`

## License
MIT
