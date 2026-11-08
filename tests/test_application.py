import csv
from concurrent.futures import ThreadPoolExecutor
import io
import json
from pathlib import Path
import tempfile
import sqlite3
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
from demo.server import handler_for
from demo.store import Store, Conflict


def valid_action(record):
    return dict(action="advance")


def candidate(records):
    return next(
        r
        for r in records
        if not r.get("hold") and not r.get("cancelled") and r.get("state") != "gate_out"
    )


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "demo.db"
        self.store = Store(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_snapshot_has_reproducible_metrics(self):
        initial = self.store.snapshot()
        self.assertEqual(initial, Store(self.path).snapshot())
        self.assertEqual(len(initial["metrics"]), 4)
        self.assertGreater(len(initial["records"]), 0)
        self.assertEqual(initial["events"], [])

    def test_mutation_persists_and_is_audited(self):
        r = candidate(self.store.snapshot()["records"])
        self.store.act(valid_action(r) | dict(id=r["id"], version=r["version"]))
        snapshot = Store(self.path).snapshot()
        changed = next(x for x in snapshot["records"] if x["id"] == r["id"])
        self.assertEqual(changed["version"], 2)
        self.assertEqual(snapshot["events"][0]["entity"], r["id"])
        self.assertEqual(snapshot["events"][0]["version"], 2)

    def test_stale_write_does_not_create_a_second_audit_event(self):
        r = candidate(self.store.snapshot()["records"])
        action = valid_action(r) | dict(id=r["id"], version=1)
        self.store.act(action)
        with self.assertRaises(Conflict):
            self.store.act(action)
        self.assertEqual(len(self.store.snapshot()["events"]), 1)

    def test_invalid_action_rolls_back_everything(self):
        before = self.store.snapshot()
        r = before["records"][0]
        with self.assertRaises(ValueError):
            self.store.act(dict(action="invalid", id=r["id"], version=1))
        self.assertEqual(before, self.store.snapshot())

    def test_audit_failure_rolls_back_record_update(self):
        class AuditFailure(sqlite3.Connection):
            def execute(self, sql, *args):
                if sql.startswith("INSERT INTO events"):
                    raise sqlite3.OperationalError("Simulated audit write failure")
                return super().execute(sql, *args)

        before = self.store.snapshot()
        r = candidate(before["records"])
        self.store.connect = lambda: sqlite3.connect(self.path, factory=AuditFailure)
        with self.assertRaises(sqlite3.OperationalError):
            self.store.act(valid_action(r) | dict(id=r["id"], version=1))
        self.assertEqual(before, self.store.snapshot())

    def test_two_simultaneous_updates_have_one_winner(self):
        r = candidate(self.store.snapshot()["records"])
        p = valid_action(r) | dict(id=r["id"], version=1)

        def update(_):
            try:
                self.store.act(p)
                return "saved"
            except Conflict:
                return "conflict"

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(update, range(2)))
        self.assertCountEqual(results, ["saved", "conflict"])
        self.assertEqual(len(self.store.snapshot()["events"]), 1)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.store = Store(Path(cls.tmp.name) / "http.db")
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(cls.store))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()
        cls.tmp.cleanup()

    def post(self, body, **headers):
        req = Request(
            self.base + "/api/action",
            data=body,
            headers={"Content-Type": "application/json"} | headers,
        )
        try:
            with urlopen(req) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            try:
                return error.code, json.load(error)
            finally:
                error.close()

    def test_health_assets_and_security_headers(self):
        for path in ["/", "/style.css", "/app.js", "/feature.js", "/api/health"]:
            with urlopen(self.base + path) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
                self.assertIn(
                    "frame-ancestors 'none'",
                    response.headers["Content-Security-Policy"],
                )

    def test_malformed_nonfinite_and_oversize_json(self):
        for body in [b"{", b"[]", b'{"x":NaN}']:
            self.assertEqual(self.post(body)[0], 400)
        self.assertEqual(self.post(b"x" * 16385)[0], 413)

    def test_cross_origin_and_invalid_host_rejected(self):
        self.assertEqual(self.post(b"{}", Origin="https://example.com")[0], 403)
        self.assertEqual(self.post(b"{}", Host="evil.example")[0], 403)

    def test_write_read_export_roundtrip(self):
        r = candidate(self.store.snapshot()["records"])
        status, snapshot = self.post(
            json.dumps(
                valid_action(r) | dict(id=r["id"], version=r["version"])
            ).encode()
        )
        self.assertEqual(status, 200)
        self.assertTrue(snapshot["events"])
        with urlopen(self.base + "/api/export.csv") as response:
            rows = list(csv.DictReader(io.StringIO(response.read().decode())))
        self.assertEqual(len(rows), len(snapshot["records"]))
        self.assertIn(r["id"], {row["id"] for row in rows})

    def test_private_paths_cannot_be_read(self):
        for path in ["/demo/domain.py", "/../README.md", "/var/demo.sqlite3"]:
            with self.assertRaises(HTTPError) as raised:
                urlopen(self.base + path)
            self.assertEqual(raised.exception.code, 404)
            raised.exception.close()


if __name__ == "__main__":
    unittest.main()
