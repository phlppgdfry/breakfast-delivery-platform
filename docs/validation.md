# Validation evidence

Validation date: 8 November 2026. Fixtures represent June 2026 and are intentionally frozen. No historical business outcomes are inferred from this validation.

## Recorded local result

Python 3.14.10: **17 tests passed**. Chromium: **6 tests passed**. JavaScript syntax checks and Python compilation passed. The report command reproduced the committed synthetic baseline.

## Automated checks

- `make check`: Python unit/integration tests, HTTP round trips, invalid input, read/export round trip, durable state, stale-write rejection, simultaneous updates and audit-failure rollback; Python compilation; JavaScript syntax checks.
- `npm run test:e2e`: six Chromium tests covering served brand assets, filters/empty state, responsive layouts at 390/768/1440 px and the domain workflow with reload persistence.
- `make report`: baseline JSON and CSV generated from the same domain calculations used by the browser.

Domain coverage: 22:00 cutoff and timezone conversion, integer-cent price, zones, allergen acknowledgement, quantity validation, concurrent capacity and full fulfilment.

## Browser review

The native browser entry point reported no browser available, so review used the shared Playwright browser. The core flow was exercised through real forms and buttons against the local Python server. Reload persistence, visible success and rejection messages, record selection and mobile document width were checked. Screenshots are actual rendered pages, not design mockups.

1. Reserve three Classic boxes for a fictional customer in 9000, in the 06:00–07:00 window. Acknowledge the displayed allergens.
2. The total is €37.50. Advance the order through preparation, delivery handover and delivered.
3. Try another box in the same window: the seeded one plus your three have exhausted the four-box capacity. Reload to verify the order persists.

See [desktop screenshot](preview.png), [mobile screenshot](mobile.png), and the current [GitHub Actions run](https://github.com/phlppgdfry/breakfast-delivery-platform/actions/workflows/demo.yml). The badge reports the remote result; this document describes the checks, not an invented production certification.

## Limits of the evidence

The suite tests a local single-workspace product with synthetic records. It does not establish external integration reliability, real user outcomes, scale, production security, legal compliance or clinical validity. Reservations and deliveries are simulated. No payment, real bakery order, routing optimisation, AI recommendation, real courier tracking, supplier integration or food-safety process is performed.
