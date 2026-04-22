import argparse
import os
import sys

from .core import EcosClient, print_json


def main(argv=None):
    parser = argparse.ArgumentParser(prog="ecos-cli", description="Bank of Korea ECOS Open API CLI")
    parser.add_argument("--api-key", dest="api_key", default=os.environ.get("BOK_API_KEY"), help="API key (or set BOK_API_KEY)")
    parser.add_argument("--lang", dest="lang", default=os.environ.get("BOK_LANG", "kr"), help="Language code: kr or en (default: kr)")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("table-list", help="List available statistic tables")
    p_list.add_argument("--start", type=int, default=1)
    p_list.add_argument("--end", type=int, default=1000)

    p_series = sub.add_parser("series", help="Fetch a time series by stat code")
    p_series.add_argument("stat_code", help="Statistic table code (e.g., 722Y001)")
    p_series.add_argument("cycle", help="A,S,Q,M,D")
    p_series.add_argument("start_date", help="Start date (YYYY, YYYYMM, or YYYYMMDD per cycle)")
    p_series.add_argument("end_date", help="End date (YYYY, YYYYMM, or YYYYMMDD per cycle)")
    p_series.add_argument("--start", type=int, default=1)
    p_series.add_argument("--end", type=int, default=1000)

    args = parser.parse_args(argv)

    client = EcosClient(api_key=args.api_key, lang=args.lang)

    if args.cmd == "table-list":
        data = client.table_list(start=args.start, end=args.end)
        print_json(data)
        return 0
    elif args.cmd == "series":
        data = client.series(
            stat_code=args.stat_code,
            cycle=args.cycle,
            start_date=args.start_date,
            end_date=args.end_date,
            start=args.start,
            end=args.end,
        )
        print_json(data)
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
