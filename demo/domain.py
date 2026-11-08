from demo.contracts import number, text, record, metric


from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import uuid

CLOCK = datetime(2026, 6, 15, 20, 0, tzinfo=ZoneInfo("Europe/Brussels"))
MENU = {
    "Classic": {"cents": 1250, "allergens": "Wheat, milk, egg"},
    "Brunch": {"cents": 1800, "allergens": "Wheat, milk, egg, sesame"},
}
SLOTS = {"06:00–07:00": 4, "07:00–08:00": 4}
STEPS = ["confirmed", "preparing", "out_for_delivery", "delivered"]


CONFIG = {
    "columns": [
        ["name", "Order"],
        ["status", "Fulfilment"],
        ["value", "Total"],
        ["context", "Delivery window"],
    ],
    "title": "Morning Table",
    "heading": "A better morning, planned tonight.",
    "subtitle": "Reserve a breakfast box, choose a delivery window, and follow each order from the bakery to the doorstep.",
    "section": "Breakfast delivery",
    "list_title": "Morning order board",
    "theme": "breakfast",
    "port": 8115,
    "clock": "Simulation clock · 15 June 2026, 20:00 Europe/Brussels",
}


ACTIONS = frozenset(["create", "advance"])


def seed():
    return [
        dict(
            id="ORD-001",
            name="ORD-001 · Alex",
            customer="Alex",
            box="Classic",
            quantity=1,
            total_cents=1250,
            slot="06:00–07:00",
            postal="9000",
            delivery="2026-06-16",
            state="confirmed",
            allergens_ack=True,
        ),
        dict(
            id="ORD-002",
            name="ORD-002 · Sam",
            customer="Sam",
            box="Brunch",
            quantity=2,
            total_cents=3600,
            slot="07:00–08:00",
            postal="9030",
            delivery="2026-06-16",
            state="preparing",
            allergens_ack=True,
        ),
    ]


def occupancy(records, slot, delivery):
    return sum(
        r["quantity"]
        for r in records
        if r["slot"] == slot and r["delivery"] == delivery
    )


def present(records):
    return [
        r
        | {
            "status": r["state"].replace("_", " ").title(),
            "value": f"€{r['total_cents'] / 100:.2f}",
            "context": r["slot"],
        }
        for r in records
    ]


def metrics(records):
    revenue = sum(r["total_cents"] for r in records)
    return [
        metric("Morning orders", len(records), "For the next delivery morning"),
        metric(
            "Reserved boxes",
            sum(r["quantity"] for r in records),
            "Capacity is measured in boxes",
        ),
        metric(
            "Demo order value",
            f"€{revenue / 100:.2f}",
            "Simulated reservation; no money collected",
        ),
        metric(
            "Average order",
            f"€{revenue / len(records) / 100:.2f}" if records else "€0.00",
            "Sum of order totals ÷ order count",
        ),
    ]


def analysis(records):
    return {
        "title": "Freshness starts with a little planning.",
        "headline": "Tonight’s orders. Tomorrow’s breakfast.",
        "description": "Classic €12.50 · Brunch €18.00. Delivery in 9000 and 9030. Reserve before 22:00 for tomorrow. Allergen acknowledgement required. No payment or real dispatch takes place.",
        "bars_title": "Reserved delivery capacity · boxes",
        "bars": [
            {
                "label": slot,
                "value": occupancy(records, slot, "2026-06-16") / capacity * 100,
                "display": f"{occupancy(records, slot, '2026-06-16')}/{capacity}",
            }
            for slot, capacity in SLOTS.items()
        ],
        "menu": MENU,
        "slots": SLOTS,
    }


def execute(records, p, now=None):
    now = now or CLOCK
    if p["action"] == "create":
        if now.astimezone(ZoneInfo("Europe/Brussels")).hour >= 22:
            raise ValueError("Ordering closes at 22:00 Brussels time")
        customer = text(p, "customer", 60)
        box = text(p, "box")
        slot = text(p, "slot")
        postal = text(p, "postal")
        if box not in MENU:
            raise ValueError("Unknown breakfast box")
        if slot not in SLOTS:
            raise ValueError("Unknown delivery window")
        if postal not in ["9000", "9030"]:
            raise ValueError("Delivery is available in 9000 and 9030")
        if p.get("allergens_ack") is not True:
            raise ValueError("Confirm that you reviewed the listed allergens")
        quantity = number(p, "quantity", 1, 4, True)
        delivery = (
            now.astimezone(ZoneInfo("Europe/Brussels")).date() + timedelta(days=1)
        ).isoformat()
        if occupancy(records, slot, delivery) + quantity > SLOTS[slot]:
            raise ValueError(
                "This delivery window has insufficient box capacity; choose another window or quantity"
            )
        identifier = "ORD-" + uuid.uuid4().hex[:10].upper()
        return dict(
            id=identifier,
            name=f"{identifier} · {customer}",
            customer=customer,
            box=box,
            quantity=quantity,
            total_cents=MENU[box]["cents"] * quantity,
            slot=slot,
            postal=postal,
            delivery=delivery,
            state="confirmed",
            allergens_ack=True,
        )
    r = record(records, p)
    if p["action"] != "advance":
        raise ValueError("Unknown action")
    index = STEPS.index(r["state"])
    if index == len(STEPS) - 1:
        raise ValueError("Order already delivered")
    r["state"] = STEPS[index + 1]
    return r
