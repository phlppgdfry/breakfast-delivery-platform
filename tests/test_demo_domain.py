from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zoneinfo import ZoneInfo
from demo import domain
from demo.store import Store


def order(**changes):
    return (
        dict(
            action="create",
            customer="Taylor",
            box="Classic",
            quantity=1,
            postal="9000",
            slot="06:00–07:00",
            allergens_ack=True,
        )
        | changes
    )


class OrderingTests(unittest.TestCase):
    def test_money_calculated_on_server_in_integer_cents(self):
        r = domain.execute([], order(quantity=3, total_cents=1))
        self.assertEqual(r["total_cents"], 3750)
        self.assertEqual(r["delivery"], "2026-06-16")

    def test_cutoff_in_brussels_timezone(self):
        for minute, allowed in [(59, True), (0, False)]:
            now = datetime(
                2026,
                6,
                15,
                21 if allowed else 22,
                minute,
                tzinfo=ZoneInfo("Europe/Brussels"),
            )
            if allowed:
                self.assertEqual(domain.execute([], order(), now)["state"], "confirmed")
            else:
                with self.assertRaises(ValueError):
                    domain.execute([], order(), now)
        now = datetime(2026, 6, 15, 20, 0, tzinfo=ZoneInfo("UTC"))
        with self.assertRaises(ValueError):
            domain.execute([], order(), now)

    def test_invalid_zone_quantity_menu_allergens_and_capacity(self):
        for change in [
            dict(postal="1000"),
            dict(quantity=0),
            dict(quantity=1.5),
            dict(box="Unknown"),
            dict(allergens_ack=False),
            dict(allergens_ack="true"),
            dict(quantity=4),
        ]:
            with self.assertRaises(ValueError):
                domain.execute(domain.seed(), order(**change))

    def test_concurrent_orders_cannot_overbook_last_capacity(self):
        with TemporaryDirectory() as tmp:
            store = Store(Path(tmp) / "demo.db")
            store.act(order(quantity=2))  # seeded 1 + 2 -> one box remains

            def reserve(_):
                try:
                    store.act(order())
                    return "saved"
                except ValueError:
                    return "full"

            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(reserve, range(2)))
            self.assertCountEqual(results, ["saved", "full"])
            rows = store.snapshot()["records"]
            self.assertEqual(domain.occupancy(rows, "06:00–07:00", "2026-06-16"), 4)
            self.assertEqual(len(store.snapshot()["events"]), 2)

    def test_complete_fulfilment_lifecycle(self):
        r = domain.seed()[0]
        p = dict(id=r["id"], action="advance")
        for state in domain.STEPS[1:]:
            r = domain.execute([r], p)
            self.assertEqual(r["state"], state)
        with self.assertRaises(ValueError):
            domain.execute([r], p)
