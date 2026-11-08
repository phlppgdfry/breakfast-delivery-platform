> Historical concept requirements. Targets and business numbers are assumptions, not measured results. See README.md for the working demo and delivered scope.

# Business Requirements Document (BRD)
## AI-Powered Breakfast Delivery Platform

| Field | Value |
|---|---|
| Document version | 1.2 |
| Status | Approved |
| Author | Philippe Godfroy |
| Last updated | 2025-Q1 |
| Stakeholders | Product Owner, Operations Lead, Tech Lead, Supplier Relations |

---

## 1. Executive Summary

This document defines the business requirements for a hyperlocal breakfast delivery platform. The platform connects consumers with local food suppliers (bakeries, dairy farmers, specialty vendors) via a mobile app, enabling pre-scheduled, fresh breakfast delivery between 06:00 and 09:00.

The primary business driver is the **untapped morning revenue opportunity** for local food suppliers and the **consumer convenience gap** not addressed by existing general-purpose delivery platforms.

---

## 2. Business Objectives

| ID | Objective | KPI | Target |
|---|---|---|---|
| BO-01 | Enable local suppliers to reach new consumer segment | New supplier-driven orders per month | > 500 by Month 6 |
| BO-02 | Provide consumers with reliable pre-scheduled delivery | On-time delivery rate | > 92% |
| BO-03 | Build a sustainable recurring revenue model | Subscription share of orders | > 30% by Month 12 |
| BO-04 | Achieve unit economics viability | Contribution margin per order | > €2.50 by Month 9 |

---

## 3. Scope

### 3.1 In Scope
- Consumer-facing mobile application (iOS first, Android Phase 2)
- Supplier onboarding portal (web-based)
- Order scheduling, routing, and dispatch system
- Payment processing (Stripe integration)
- Basic recommendation engine (collaborative filtering)
- KPI reporting dashboard (internal)

### 3.2 Out of Scope
- Own delivery fleet management (3PL integration only in Phase 1)
- Lunch or dinner delivery
- B2B / catering orders
- Hardware (label printers, tablets for suppliers — evaluated for Phase 2)

---

## 4. Business Requirements

### 4.1 Order Management

| ID | Requirement | Priority | Notes |
|---|---|---|---|
| BR-01 | System shall allow consumers to schedule orders up to 7 days in advance | Must | Cutoff for next-day delivery: 22:00 |
| BR-02 | System shall send supplier prep sheets automatically by 04:30 | Must | Via app notification + email fallback |
| BR-03 | System shall support flexible delivery windows (06:00, 07:00, 07:30, 08:00) | Must | Per postal code zone |
| BR-04 | System shall allow order modification up to 2 hours before cutoff | Should | Full cancel or item swap |
| BR-05 | System shall handle partial delivery scenarios with automated refund trigger | Should | If supplier item unavailable |

### 4.2 Supplier Management

| ID | Requirement | Priority | Notes |
|---|---|---|---|
| BR-10 | Suppliers shall be able to manage their catalog via web portal | Must | Product name, price, availability, photo |
| BR-11 | Suppliers shall set daily production limits per product | Must | Prevents oversell |
| BR-12 | Suppliers shall receive weekly performance reports | Should | Automated email, PDF format |
| BR-13 | Platform shall flag suppliers with > 3 late deliveries in 30 days | Must | Automatic alert to Supplier Relations team |

### 4.3 Consumer Experience

| ID | Requirement | Priority | Notes |
|---|---|---|---|
| BR-20 | Consumer onboarding shall be completable in < 3 minutes | Must | Max 4 screens to first order |
| BR-21 | Consumer shall receive live delivery tracking from pickup | Must | Map view in app |
| BR-22 | Platform shall suggest repeat orders based on history | Should | Visible from order screen |
| BR-23 | Consumer shall be able to rate delivery + product separately | Should | 1–5 stars + optional comment |

### 4.4 Payments & Financials

| ID | Requirement | Priority | Notes |
|---|---|---|---|
| BR-30 | Payment shall be captured at order placement, not delivery | Must | Reduces no-show risk |
| BR-31 | Platform shall support subscription billing (weekly, monthly) | Should | Via Stripe Billing |
| BR-32 | Supplier payouts shall be processed weekly via bank transfer | Must | Net 7 days |
| BR-33 | System shall generate VAT-compliant invoices for suppliers | Must | Belgian VAT requirements |

---

## 5. Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | App launch to browsable catalog | < 2 seconds |
| NFR-02 | Order placement end-to-end | < 60 seconds |
| NFR-03 | System uptime | > 99.5% (excl. planned maintenance) |
| NFR-04 | GDPR compliance | Full — data processing agreement with all suppliers |
| NFR-05 | Payment security | PCI DSS Level 2 via Stripe |

---

## 6. Assumptions & Constraints

**Assumptions:**
- Suppliers have a smartphone capable of running the supplier app (iOS 14+ or Android 10+)
- Delivery is handled by a third-party logistics partner (not owned fleet)
- Initial launch is limited to 3 postal code zones for market validation

**Constraints:**
- Budget for Phase 1 development: €80,000
- Timeline to MVP launch: 6 months
- Team: 1 PM, 2 developers, 1 designer, 1 supplier relations manager

---

## 7. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Low supplier adoption | Medium | High | Guarantee first 30 orders per supplier in launch zone |
| Delivery partner unreliability | Medium | High | Multi-partner contract; SLA with penalties |
| Regulatory issue (FAVV food safety) | Low | High | Legal review pre-launch; supplier compliance checklist |
| Consumer retention below target | Medium | Medium | Weekly NPS monitoring; onboarding A/B test |

---

## 8. Sign-off

| Role | Name | Status |
|---|---|---|
| Business Owner | Philippe Godfroy | ✅ Approved |
| Tech Lead | TBD | Pending |
| Legal / Compliance | TBD | Pending |

---

*Business Requirements Document — Breakfast Delivery Platform v1.2*
