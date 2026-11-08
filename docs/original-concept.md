# Original concept — historical, unverified

This is preserved design history. Statements about customers, outcomes, integrations and files below are original hypotheses, not verified implementation or measured results. See the current README for delivered scope.

# 🥐 AI-Powered Breakfast Delivery Platform — Business Analysis Case

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Type](https://img.shields.io/badge/Type-Business%20Analysis-blue)
![Domain](https://img.shields.io/badge/Domain-E--commerce%20%7C%20Logistics-orange)

> **Problem statement:** Local bakeries lose up to 40% of their potential morning revenue because consumers don't plan breakfast in advance. Existing delivery platforms aren't optimized for pre-scheduled, freshness-critical, early-morning delivery windows.
> **This case analyzes the full business architecture for a hyperlocal breakfast delivery platform** — from supplier onboarding to AI-powered personalization and last-mile logistics.

---

## 📌 Business Problem

**Context:**
The breakfast moment is underserved by existing food delivery platforms. Deliveroo and Uber Eats are optimized for on-demand lunch/dinner — not for 06:00 pre-scheduled deliveries requiring fresh croissants and dairy products.

**Stakeholder Pain Points:**

| Stakeholder | Pain Point |
|---|---|
| Consumer | No reliable way to pre-order fresh breakfast the evening before |
| Local bakery | Overproduction waste + missed revenue from walk-in only model |
| Dairy supplier | No direct-to-consumer channel; dependent on supermarkets |
| Delivery platform | No specialized infrastructure for early-morning time slots |

**Opportunity:**
Build a platform connecting consumers with local food suppliers, optimized specifically for the breakfast window (06:00–09:00), with AI-powered order suggestions and route optimization.

---

## 🎯 Project Scope & Objectives

**In Scope:**
- Consumer mobile app (iOS/Android)
- Supplier onboarding and management portal
- Order scheduling and routing engine
- Payment and subscription flows
- KPI reporting dashboard

**Out of Scope:**
- Own delivery fleet (third-party logistics integration only — Phase 1)
- Grocery / lunch / dinner delivery
- B2B catering

**Success Criteria:**

| Metric | Target | Timeframe |
|---|---|---|
| On-time delivery rate | > 92% | From launch |
| Average order value (AOV) | > €16 | Month 3 |
| 30-day customer retention | > 60% | Month 6 |
| Supplier churn rate | < 5% per quarter | Ongoing |
| App Store rating | > 4.3 ⭐ | Month 3 |

---

## 👥 Stakeholder Map

```
PRIMARY STAKEHOLDERS
├── Consumer (end user)          → Wants reliable, fresh, on-time breakfast delivery
├── Local bakery / supplier      → Wants predictable demand + new revenue channel
└── Platform operator            → Wants GMV growth, margin, and retention

SECONDARY STAKEHOLDERS
├── Delivery partner (3PL)       → Wants optimized routing and clear SLAs
├── Payment provider (Stripe)    → Minimal friction; PSD2 compliant
└── Regulatory (FASFC / FAVV)   → Food safety compliance for perishables

INFLUENCERS
├── Local press / community      → Key for hyperlocal brand launch
└── Bakery associations          → Gatekeepers for supplier network
```

---

## 📁 Repository Structure

```
breakfast-delivery-platform/
│
├── README.md                        ← You are here
├── BRD.md                           ← Business Requirements Document
├── UserStories.md                   ← Full epic + story breakdown (MoSCoW)
├── StakeholderMap.md                ← Detailed stakeholder analysis
├── KPI_Definitions.md               ← KPI taxonomy + measurement plan
│
├── process-flows/
│   ├── AS-IS_order_flow.md          ← Current consumer breakfast journey
│   └── TO-BE_order_flow.md          ← Future state with platform
│
├── sql/
│   ├── delivery_performance.sql     ← On-time rate per supplier + zone
│   └── supplier_analysis.sql        ← Supplier revenue + retention query
│
└── dashboards/
    └── kpi_dashboard_mockup.md      ← Dashboard layout + data sources
```

---

## 📋 Key Requirements (Summary)

Full detail in [`BRD.md`](./BRD.md) and [`UserStories.md`](./UserStories.md).

### Functional Requirements (MoSCoW)

**Must Have:**
- Consumer can pre-order breakfast the evening before (cutoff: 22:00)
- Supplier receives order confirmation + prep sheet by 04:30
- Consumer receives live delivery tracking from 06:00
- Payment processed at order placement (not on delivery)
- Admin can configure time slots per postal code zone

**Should Have:**
- AI-based order suggestions based on history (collaborative filtering)
- Subscription model ("Weekly Breakfast Box")
- Supplier rating + review system

**Could Have:**
- Carbon footprint display per order
- Group order functionality (family / office)
- Integration with smart home devices (order via voice)

**Won't Have (Phase 1):**
- Own delivery fleet
- Real-time inventory sync with POS systems

---

## 🔄 Process Flow (Summary)

### AS-IS (No Platform)
```
Consumer wakes up → Decides on breakfast → Drives to bakery →
Limited stock → Overpays for convenience → No digital history
```

### TO-BE (With Platform)
```
Consumer orders night before (app, 2 min) →
Supplier receives automated prep sheet (04:30) →
Delivery partner picks up (05:45) →
Consumer receives fresh breakfast (06:00–07:30) →
Rating + AI learns preferences
```

**Key Improvement:** Consumer effort reduced from ~25 minutes (drive, queue, drive back) to 2 minutes (app order). Supplier gets predictable demand 8 hours in advance.

---

## 📊 SQL Queries

### Delivery Performance Analysis
```sql
-- Average delivery time per supplier and postal code zone
-- Used to identify underperforming routes and supplier SLA compliance

SELECT
    s.name                                                      AS supplier,
    o.delivery_postal_code,
    AVG(DATEDIFF(minute, o.placed_at, o.delivered_at))          AS avg_delivery_minutes,
    COUNT(o.id)                                                 AS total_orders,
    SUM(CASE WHEN o.delivered_at <= o.promised_at THEN 1 ELSE 0 END) * 100.0
        / COUNT(*)                                              AS on_time_pct,
    AVG(o.order_value)                                          AS avg_order_value
FROM orders o
JOIN suppliers s ON o.supplier_id = s.id
WHERE
    o.placed_at >= DATEADD(month, -3, GETDATE())
    AND o.status = 'delivered'
GROUP BY
    s.name,
    o.delivery_postal_code
HAVING
    COUNT(o.id) > 10
ORDER BY
    on_time_pct ASC;
```

### Supplier Retention Risk Query
```sql
-- Flag suppliers with declining order volume (churn risk signal)

WITH monthly_volume AS (
    SELECT
        supplier_id,
        DATEFROMPARTS(YEAR(placed_at), MONTH(placed_at), 1) AS month,
        COUNT(*)                                              AS orders,
        SUM(platform_fee)                                     AS platform_revenue
    FROM orders
    WHERE placed_at >= DATEADD(month, -6, GETDATE())
    GROUP BY supplier_id, DATEFROMPARTS(YEAR(placed_at), MONTH(placed_at), 1)
),
ranked AS (
    SELECT *,
        LAG(orders) OVER (PARTITION BY supplier_id ORDER BY month) AS prev_month_orders
    FROM monthly_volume
)
SELECT
    s.name,
    r.month,
    r.orders,
    r.prev_month_orders,
    ROUND((r.orders - r.prev_month_orders) * 100.0 / NULLIF(r.prev_month_orders, 0), 1) AS mom_change_pct
FROM ranked r
JOIN suppliers s ON r.supplier_id = s.id
WHERE r.prev_month_orders IS NOT NULL
  AND r.orders < r.prev_month_orders * 0.75   -- flag >25% drop
ORDER BY mom_change_pct ASC;
```

---

## 📈 KPI Dashboard (Mockup)

**Row 1 — Operational Health**

| Metric | Value | Trend | Owner |
|---|---|---|---|
| On-time delivery rate | 94.2% | ✅ +1.3% | Operations |
| Orders per day (avg) | 312 | ✅ +8% WoW | Growth |
| Active suppliers | 47 | ➡️ stable | Partnerships |

**Row 2 — Commercial**

| Metric | Value | Trend | Owner |
|---|---|---|---|
| AOV | €18.40 | ✅ +€1.20 vs target | Product |
| 30-day retention | 58% | ⚠️ below 60% target | Product |
| Subscription share | 31% | ✅ growing | Marketing |

---

## 💡 Key Insights & Recommendations

1. **Retention is the bottleneck.** 30-day retention at 58% (vs 60% target) driven by delivery timing variance in outer postal codes. Fix: add postal code–level time slot restrictions where on-time rate < 88%.

2. **Subscription model drives LTV.** Subscribers order 3.2x more per month than pay-per-order customers. Priority: push subscription upsell at order confirmation screen.

3. **Supplier concentration risk.** Top 3 suppliers handle 61% of volume. Diversification plan needed — target 2 new suppliers per active zone per quarter.

---

## 🔗 Related Documents

- [`BRD.md`](./BRD.md) — Full Business Requirements Document
- [`UserStories.md`](./UserStories.md) — 28 user stories across 5 epics
- [`KPI_Definitions.md`](./KPI_Definitions.md) — Measurement framework
- [`sql/delivery_performance.sql`](./sql/delivery_performance.sql)

---

*Case study by Philippe Godfroy — Business Analyst Portfolio*
