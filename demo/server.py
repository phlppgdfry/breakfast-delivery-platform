"""Loopback-only portfolio server. No external services or runtime dependencies."""

import argparse
import csv
import io
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from demo import domain
from demo.store import Store, Conflict

PUBLIC = Path(__file__).parent / "web"
ASSETS = {
    "/": ("index.html", "text/html"),
    "/app.js": ("app.js", "text/javascript"),
    "/style.css": ("style.css", "text/css"),
    "/feature.js": ("feature.js", "text/javascript"),
}
ASSETS.update(
    {
        "/favicon.svg": ("favicon.svg", "image/svg+xml"),
        "/logo.svg": ("logo.svg", "image/svg+xml"),
        "/site.webmanifest": ("site.webmanifest", "application/manifest+json"),
        "/apple-touch-icon.png": ("apple-touch-icon.png", "image/png"),
        "/social-preview.png": ("social-preview.png", "image/png"),
    }
)


def handler_for(store):
    class Handler(BaseHTTPRequestHandler):
        def send(self, status, body, kind="application/json"):
            if kind == "application/json":
                body = json.dumps(body, allow_nan=False).encode()
            elif isinstance(body, str):
                body = body.encode()
            self.send_response(status)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
            )
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/favicon.ico":
                return self.send(204, b"", "image/x-icon")
            if path == "/api/health":
                return self.send(200, {"status": "ok", "mode": "local-demo"})
            if path == "/api/snapshot":
                return self.send(200, store.snapshot())
            if path == "/api/export.csv":
                rows = store.snapshot()["records"]
                output = io.StringIO(newline="")
                writer = csv.DictWriter(
                    output,
                    fieldnames=list(dict.fromkeys(key for row in rows for key in row))
                    if rows
                    else ["id"],
                )
                writer.writeheader()
                for row in rows:
                    # Prevent spreadsheet formula execution in exported user-controlled fields.
                    writer.writerow(
                        {
                            key: (
                                "'" + str(value)
                                if str(value).startswith(
                                    ("=", "+", "-", "@", "\t", "\r")
                                )
                                else value
                            )
                            for key, value in row.items()
                        }
                    )
                return self.send(200, output.getvalue(), "text/csv")
            if path in ASSETS:
                filename, kind = ASSETS[path]
                return self.send(200, (PUBLIC / filename).read_bytes(), kind)
            return self.send(404, {"error": "Not found"})

        def do_POST(self):
            # Browser writes must originate from this loopback server. Also check Host
            # to reject DNS rebinding. Non-browser local CLI calls may omit Origin.
            allowed = {
                f"127.0.0.1:{self.server.server_port}",
                f"localhost:{self.server.server_port}",
            }
            host = self.headers.get("Host", "")
            origin = self.headers.get("Origin")
            if host not in allowed or (origin and origin != "http://" + host):
                return self.send(403, {"error": "Same-origin local requests only"})
            if urlsplit(self.path).path != "/api/action":
                return self.send(404, {"error": "Not found"})
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 16384:
                    return self.send(
                        413, {"error": "Request must contain 1–16384 bytes"}
                    )
                if self.headers.get_content_type() != "application/json":
                    return self.send(415, {"error": "Use application/json"})
                payload = json.loads(
                    self.rfile.read(size),
                    parse_constant=lambda _: (_ for _ in ()).throw(
                        ValueError("Non-finite JSON number")
                    ),
                )
                if not isinstance(payload, dict):
                    raise ValueError("Expected a JSON object")
                store.act(payload)
                return self.send(200, store.snapshot())
            except Conflict as exc:
                return self.send(409, {"error": str(exc)})
            except (ValueError, KeyError, TypeError, UnicodeDecodeError) as exc:
                return self.send(400, {"error": str(exc) or "Invalid request"})
            except Exception:
                self.log_error("Unexpected action failure")
                return self.send(
                    500, {"error": "Action failed; no partial changes were saved"}
                )

    return Handler


def main():
    parser = argparse.ArgumentParser(description=domain.CONFIG["title"] + " local demo")
    parser.add_argument("--port", type=int, default=domain.CONFIG["port"])
    parser.add_argument(
        "--db", type=Path, default=Path(os.environ.get("DEMO_DB", "var/demo.sqlite3"))
    )
    args = parser.parse_args()
    store = Store(args.db)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(store))
    print(
        f"{domain.CONFIG['title']}: http://127.0.0.1:{server.server_port}", flush=True
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
