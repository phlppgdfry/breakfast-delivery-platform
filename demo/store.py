"""Durable records with atomic audit writes and optimistic concurrency checks."""

from contextlib import closing
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from demo import domain


class Conflict(ValueError):
    pass


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.connect()) as db, db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, at TEXT NOT NULL, entity TEXT NOT NULL, action TEXT NOT NULL, version INTEGER NOT NULL)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            if not db.execute("SELECT 1 FROM meta WHERE key='seed_version'").fetchone():
                for record in domain.seed():
                    record["version"] = 1
                    db.execute(
                        "INSERT INTO records VALUES (?, ?)",
                        (record["id"], json.dumps(record)),
                    )
                db.execute("INSERT INTO meta VALUES ('seed_version', '1')")

    def connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def snapshot(self):
        with closing(self.connect()) as db:
            db.execute("BEGIN")
            records = [
                json.loads(row[0])
                for row in db.execute("SELECT payload FROM records ORDER BY id")
            ]
            events = [
                dict(zip(("seq", "at", "entity", "action", "version"), row))
                for row in db.execute("SELECT * FROM events ORDER BY seq DESC LIMIT 12")
            ]
        return {
            "config": domain.CONFIG,
            "records": domain.present(records),
            "metrics": domain.metrics(records),
            "analysis": domain.analysis(records),
            "events": events,
        }

    def act(self, payload):
        if not isinstance(payload.get("action"), str):
            raise ValueError("Action is required")
        if payload["action"] not in domain.ACTIONS:
            raise ValueError("Unknown action")
        with closing(self.connect()) as db, db:
            # Serialise validation + mutation, including capacity checks across entities.
            db.execute("BEGIN IMMEDIATE")
            records = [
                json.loads(row[0])
                for row in db.execute("SELECT payload FROM records ORDER BY id")
            ]
            creating = payload["action"] == "create"
            if not creating:
                current = next(
                    (r for r in records if r["id"] == payload.get("id")), None
                )
                if current is None:
                    raise ValueError("Record not found")
                if (
                    type(payload.get("version")) is not int
                    or current["version"] != payload["version"]
                ):
                    raise Conflict("This record changed. Refresh and try again.")
            updated = domain.execute(records, payload)
            if creating and any(r["id"] == updated["id"] for r in records):
                raise Conflict("Record already exists")
            updated["version"] = 1 if creating else current["version"] + 1
            db.execute(
                "INSERT INTO records VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload",
                (updated["id"], json.dumps(updated, allow_nan=False)),
            )
            db.execute(
                "INSERT INTO events(at,entity,action,version) VALUES (?,?,?,?)",
                (
                    datetime.now(timezone.utc).isoformat(),
                    updated["id"],
                    payload["action"],
                    updated["version"],
                ),
            )
