# Morning Table — delivery case study

## Problem and intended user

Scheduled breakfast delivery needs a reservation model that prevents oversold delivery windows and gives operators a clear fulfilment sequence.

## Delivered vertical slice

A breakfast reservation and fulfilment demo with server-side prices, atomic delivery capacity and an end-to-end order board.

1. Reserve three Classic boxes for a fictional customer in 9000, in the 06:00–07:00 window. Acknowledge the displayed allergens.
2. The total is €37.50. Advance the order through preparation, delivery handover and delivered.
3. Try another box in the same window: the seeded one plus your three have exhausted the four-box capacity. Reload to verify the order persists.

## Acceptance criteria mapped to evidence

| Criterion | Verification |
| --- | --- |
| A reviewer can run the product without external credentials | `python3 -m demo.server`; standard-library runtime |
| Domain constraints are enforced on the server | `tests/test_demo_domain.py`; invalid transitions and boundary cases |
| Successful actions survive a new connection | `PersistenceTests.test_mutation_persists_and_is_audited` |
| A stale edit cannot overwrite newer state | Version conflict and simultaneous update tests |
| An audit write failure leaves the record unchanged | Fault-injected SQLite audit failure test |
| The main task works through the rendered interface | Domain workflow in `tests/browser/workspace.spec.cjs` |
| The interface works at mobile and desktop widths | 390, 768 and 1440 px browser tests; screenshots in `docs/` |
| Reported numbers can be reproduced | `python3 -m demo.report`; committed baseline JSON and CSV |

Domain-specific evidence: 22:00 cutoff and timezone conversion, integer-cent price, zones, allergen acknowledgement, quantity validation, concurrent capacity and full fulfilment.

## What this demonstrates

Requirements are reduced to a coherent executable workflow, rather than a catalogue of disconnected features. Input contracts, state ownership, failure states, persistence and explanations are part of the product. Design choices and operational limits are recorded so another engineer can inspect the implementation and reproduce its behaviour.

## What it does not prove

Reservations and deliveries are simulated. No payment, real bakery order, routing optimisation, AI recommendation, real courier tracking, supplier integration or food-safety process is performed.

No user study, commercial result, uptime, production scale, legal compliance or measured improvement is claimed. The historical concept is context, not evidence.
