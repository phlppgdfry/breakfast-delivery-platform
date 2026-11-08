> Historical concept requirements. Targets and business numbers are assumptions, not measured results. See README.md for the working demo and delivered scope.

# KPI Definitions — Breakfast Delivery Platform

> This document defines every KPI tracked on the platform: what it measures, how it's calculated, the data source, ownership, and target. A shared KPI taxonomy prevents misalignment between teams.

---

## Operational KPIs

### OPS-01 — On-Time Delivery Rate

| Field | Value |
|---|---|
| **Definition** | % of deliveries that arrive at or before the promised delivery time |
| **Formula** | `(Deliveries where delivered_at ≤ promised_at) / Total deliveries × 100` |
| **Target** | > 92% |
| **Measurement frequency** | Daily |
| **Owner** | Operations Lead |
| **Data source** | `orders` table — `delivered_at` vs `promised_at` |
| **Segmentation** | By supplier, by postal code zone, by delivery time slot |
| **Alert** | Flag if 7-day rolling average drops below 89% |

---

### OPS-02 — Average Delivery Time

| Field | Value |
|---|---|
| **Definition** | Average minutes from order pickup by courier to delivery to consumer |
| **Formula** | `AVG(delivered_at - picked_up_at)` in minutes |
| **Target** | < 35 minutes |
| **Measurement frequency** | Daily |
| **Owner** | Operations Lead |
| **Data source** | `orders` table — `picked_up_at`, `delivered_at` |

---

### OPS-03 — Supplier Prep Compliance Rate

| Field | Value |
|---|---|
| **Definition** | % of orders where supplier marked "ready" before courier arrival |
| **Formula** | `(Orders with ready_at ≤ courier_arrived_at) / Total orders × 100` |
| **Target** | > 95% |
| **Measurement frequency** | Weekly |
| **Owner** | Supplier Relations |
| **Alert** | Flag individual suppliers with < 85% compliance |

---

## Commercial KPIs

### COM-01 — Average Order Value (AOV)

| Field | Value |
|---|---|
| **Definition** | Average gross value per completed order |
| **Formula** | `SUM(order_value) / COUNT(completed_orders)` |
| **Target** | > €16 at launch; > €18 by Month 6 |
| **Measurement frequency** | Weekly |
| **Owner** | Product |
| **Segmentation** | By tier (à la carte vs subscription), by supplier |

---

### COM-02 — Gross Merchandise Value (GMV)

| Field | Value |
|---|---|
| **Definition** | Total consumer spend through the platform (before refunds) |
| **Formula** | `SUM(order_value)` for all completed orders in period |
| **Target** | €50,000/month by Month 6 |
| **Measurement frequency** | Weekly |
| **Owner** | CEO / Finance |

---

### COM-03 — Platform Take Rate

| Field | Value |
|---|---|
| **Definition** | Platform commission as % of GMV |
| **Formula** | `SUM(platform_fee) / SUM(order_value) × 100` |
| **Target** | 18–22% |
| **Measurement frequency** | Monthly |
| **Owner** | Finance |

---

## Retention KPIs

### RET-01 — 30-Day Consumer Retention Rate

| Field | Value |
|---|---|
| **Definition** | % of consumers who place a second order within 30 days of their first |
| **Formula** | `Consumers with 2+ orders in first 30 days / All consumers with first order × 100` |
| **Target** | > 60% |
| **Measurement frequency** | Monthly (by cohort) |
| **Owner** | Product / Growth |
| **Note** | Measure per signup cohort (weekly cohorts) |

---

### RET-02 — Subscription Share

| Field | Value |
|---|---|
| **Definition** | % of total orders fulfilled under a subscription plan |
| **Formula** | `Subscription orders / Total orders × 100` |
| **Target** | > 30% by Month 6 |
| **Measurement frequency** | Weekly |
| **Owner** | Product |

---

### RET-03 — Supplier Churn Rate

| Field | Value |
|---|---|
| **Definition** | % of active suppliers who become inactive within a quarter |
| **Formula** | `Suppliers with 0 orders in quarter / Active suppliers at start of quarter × 100` |
| **Target** | < 5% per quarter |
| **Measurement frequency** | Quarterly |
| **Owner** | Supplier Relations |

---

## Quality KPIs

### QUA-01 — Consumer Rating (Average)

| Field | Value |
|---|---|
| **Definition** | Average consumer rating across all rated deliveries |
| **Formula** | `AVG(consumer_rating)` where rating is not null |
| **Target** | > 4.3 / 5.0 |
| **Measurement frequency** | Weekly |
| **Owner** | Operations |
| **Segmentation** | By supplier, by postal code |

---

### QUA-02 — Refund Rate

| Field | Value |
|---|---|
| **Definition** | % of orders resulting in a full or partial refund |
| **Formula** | `COUNT(orders with refund_amount > 0) / COUNT(total orders) × 100` |
| **Target** | < 2% |
| **Measurement frequency** | Weekly |
| **Owner** | Operations |
| **Alert** | Investigate any week > 3.5% |

---

## Reporting Cadence

| Frequency | KPIs Reviewed | Audience |
|---|---|---|
| Daily | OPS-01, OPS-02 | Operations team |
| Weekly | COM-01, COM-02, RET-02, QUA-01, QUA-02 | Product + Operations leads |
| Monthly | RET-01, COM-03, OPS-03 | Full leadership team |
| Quarterly | RET-03, full cohort analysis | Board / investors |

---

*KPI Definitions v1.0 — Breakfast Delivery Platform | Philippe Godfroy*
