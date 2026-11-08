"""Reproduce baseline evidence without starting a server or writing a database."""

import argparse
import csv
import json
from pathlib import Path
from demo import domain


def baseline():
    records = [r | {"version": 1} for r in domain.seed()]
    return {
        "project": domain.CONFIG["title"],
        "mode": "synthetic baseline",
        "clock": domain.CONFIG["clock"],
        "metrics": domain.metrics(records),
        "analysis": domain.analysis(records),
        "records": domain.present(records),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("reports/baseline"))
    args = parser.parse_args()
    result = baseline()
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "snapshot.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    with (args.output / "records.csv").open(
        "w", newline="", encoding="utf-8"
    ) as output:
        rows = result["records"]
        writer = csv.DictWriter(
            output,
            fieldnames=list(dict.fromkeys(k for r in rows for k in r)),
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    k: json.dumps(v, ensure_ascii=False)
                    if isinstance(v, (dict, list))
                    else v
                    for k, v in row.items()
                }
            )
    print(f"Reproduced {len(result['records'])} synthetic records in {args.output}")


if __name__ == "__main__":
    main()
