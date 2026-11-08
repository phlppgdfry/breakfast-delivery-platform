> Historical concept requirements. Targets and business numbers are assumptions, not measured results. See README.md for the working demo and delivered scope.

# User Stories — Breakfast Delivery Platform

**Format:** `As a [role], I want to [action], so that [benefit].`  
**Prioritization:** MoSCoW (Must / Should / Could / Won't)  
**Status:** ✅ Ready for Sprint | 🔄 Needs refinement | ❌ Blocked

---

## EPIC 1 — Order Placement (Consumer)

**Epic goal:** A consumer can discover, configure, and confirm a breakfast order in under 2 minutes.

| ID | User Story | Priority | Acceptance Criteria | Status |
|---|---|---|---|---|
| US-01 | As a consumer, I want to browse local suppliers by distance, so I can choose a trusted nearby bakery. | Must | Suppliers shown within 10km radius; sorted by distance by default; rating visible | ✅ |
| US-02 | As a consumer, I want to schedule my order the evening before, so my breakfast is ready when I wake up. | Must | Order cutoff is 22:00; delivery slots shown for next morning only | ✅ |
| US-03 | As a consumer, I want to select individual products and quantities, so I get exactly what I need. | Must | Min 1 item, max configurable per supplier; stock limit respected | ✅ |
| US-04 | As a consumer, I want to pay securely at order placement, so I don't need to handle money at the door. | Must | Stripe payment; Apple Pay / Google Pay supported; receipt via email | ✅ |
| US-05 | As a consumer, I want to modify my order up to 2 hours before cutoff, so I can adjust if plans change. | Should | Full cancel → instant refund; item swap → price difference settled | 🔄 |
| US-06 | As a returning consumer, I want to reorder my last order in one tap, so I save time on repeat purchases. | Should | "Order again" CTA on order history; pre-fills cart; prompts for delivery slot | 🔄 |

---

## EPIC 2 — Delivery & Tracking (Consumer)

**Epic goal:** Consumer is informed and confident about their delivery from dispatch to doorstep.

| ID | User Story | Priority | Acceptance Criteria | Status |
|---|---|---|---|---|
| US-10 | As a consumer, I want to track my delivery on a live map, so I know exactly when it will arrive. | Must | Map view active from pickup; ETA updated every 60 seconds; push notification at 5 min out | ✅ |
| US-11 | As a consumer, I want a push notification when my order is picked up and delivered, so I don't miss it. | Must | 2 notifications: pickup + arrival; opt-out available in settings | ✅ |
| US-12 | As a consumer, I want to rate my delivery and products separately, so the platform can improve quality. | Should | Rating prompt appears 15 min after delivery; 1–5 stars + optional text; skippable | 🔄 |
| US-13 | As a consumer, I want to report a missing or wrong item, so I can receive a refund quickly. | Must | Report available for 2h after delivery; auto-refund trigger for items < €5; manual review above | ✅ |

---

## EPIC 3 — Supplier Management

**Epic goal:** Suppliers can manage their catalog, view orders, and track earnings with minimal effort.

| ID | User Story | Priority | Acceptance Criteria | Status |
|---|---|---|---|---|
| US-20 | As a supplier, I want to add and edit my products via a web portal, so my catalog is always up to date. | Must | Name, price, photo, description, stock limit per day; changes live within 15 min | ✅ |
| US-21 | As a supplier, I want to receive my prep sheet by 04:30 each morning, so I know exactly what to prepare. | Must | Auto-generated PDF + push notification; grouped by product; consumer name + address included | ✅ |
| US-22 | As a supplier, I want to mark individual orders as "ready for pickup", so the delivery partner knows when to collect. | Must | Status toggle in app; triggers delivery partner dispatch notification | ✅ |
| US-23 | As a supplier, I want to see my weekly revenue and order trends, so I can plan production better. | Should | Dashboard: orders/day, revenue/week, top products; exportable as CSV | 🔄 |
| US-24 | As a supplier, I want to set "unavailable" days in advance, so consumers can't order on days I'm closed. | Must | Block dates up to 60 days ahead; affected scheduled orders → consumer notified + refunded | ✅ |

---

## EPIC 4 — AI Personalization

**Epic goal:** The platform learns consumer preferences and reduces ordering friction over time.

| ID | User Story | Priority | Acceptance Criteria | Status |
|---|---|---|---|---|
| US-30 | As a returning consumer, I want to see personalized product suggestions based on my history, so I discover new favorites. | Should | Visible from home screen after 3+ orders; collaborative filtering; "Why this?" tooltip | 🔄 |
| US-31 | As a consumer, I want to set dietary preferences (gluten-free, vegan, etc.), so I only see relevant products. | Should | Filter stored in profile; applied to browse + suggestions; supplier can tag products | 🔄 |
| US-32 | As a consumer, I want to receive a weekly breakfast plan suggestion, so I can subscribe with one tap. | Could | Push notification Sunday evening; proposed plan based on last 4 weeks; subscribe button deeplinks to checkout | ❌ |

---

## EPIC 5 — Subscriptions & Retention

**Epic goal:** Convert one-time buyers into habitual subscribers with predictable recurring revenue.

| ID | User Story | Priority | Acceptance Criteria | Status |
|---|---|---|---|---|
| US-40 | As a consumer, I want to subscribe to a weekly breakfast box, so I never have to think about ordering. | Should | Weekly recurring order; customizable weekly; 10% discount vs à la carte | 🔄 |
| US-41 | As a consumer, I want to pause my subscription for a specific week, so I don't get charged when I'm on holiday. | Should | Pause available until 72h before next delivery; max 4 pauses per year | 🔄 |
| US-42 | As a platform operator, I want to trigger a re-engagement email to consumers inactive for 14+ days, so I recover churned users. | Should | Automated flow via email (Klaviyo); 10% discount voucher; max 1 per user per 30 days | ❌ |

---

## Definition of Done (DoD)

A user story is considered done when:
- [ ] Acceptance criteria met and verified by QA
- [ ] Tested on iOS 16+ (and Android 12+ for cross-platform stories)
- [ ] No critical or high-severity bugs open
- [ ] Stakeholder demo completed and sign-off received
- [ ] Analytics event tracked (Mixpanel) for key actions
- [ ] Documentation updated if flow changes existing behavior

---

*User Stories v1.4 — Breakfast Delivery Platform | Philippe Godfroy*
