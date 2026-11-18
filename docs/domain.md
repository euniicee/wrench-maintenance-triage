# Domain Notes: Residence Maintenance Triage

These notes describe how residence maintenance requests work in practice. They are based on my first-hand experience as a Facilities Assistant and Service Centre Assistant in Student Housing. They are the source of truth for `data/taxonomy.json`, the synthetic dataset, and the evaluation rubric.

> No real resident requests are used anywhere in this project. All test data is synthetic, generated from these notes and hand-labelled.

## How a request flows

```
Resident message ──► Triage (AI) ──► Ticket(s) ──► Route
                                                    ├─ Facilities (repairs, missing items, requests)
                                                    │     └─ Caretaking (cleaning, assigned by Facilities)
                                                    └─ Service Centre(lockouts / temporary keys)
```

- **Facilities** handles most work.
- **Caretaking** does cleaning, but jobs are *assigned through Facilities*.
- **Lockouts are not maintenance.** The resident goes to the Service Centre for a temporary key. If the *lock itself* is faulty ("my key doesn't turn"), that is a Facilities repair.

## Two labels per ticket

Every ticket gets a **category** (what it's about) and a **type** (what kind of work it is).

| Type | Meaning | Example |
|---|---|---|
| Repair | Exists but broken | Toilet not flushing |
| Missing item | Should be there, isn't | No desk chair |
| Request | A change the resident wants, not a fault | Raise bed height |
| Cleaning | Needs cleaning, not fixing | Writing on the fridge |

**Why both labels matter:** "Mattress" could be a repair (torn), cleaning (dirty) or a request (preference). Type decides the route and often the urgency.

## Urgency

There were no formal response-time targets in practice, so these tiers are **project-defined**:

| Level | Target | Examples |
|---|---|---|
| Emergency | Same day | Lockout, room can't be locked, no heat in winter, only toilet broken, sparks or gas smell |
| High | 24–48h | Dead outlet, mold, fridge down, shared bathroom locked from the other side, clogged sink |
| Normal | ~1 week | Bulb out, blinds, cabinet handle, broken bin |
| Low | Scheduled | Wall patch, torn carpet, chair change, bed height (preference) |

### Context changes urgency

The same issue can land in a different tier depending on what the resident says. **This is why a keyword matcher isn't enough.**

- **Season:** a broken heater is an emergency in January and less urgent in September.
- **Alternatives:** a broken toilet is high priority, or an emergency if it's the only one available.
- **Safety signals:** "outlet not working" is high priority, and "outlet sparked" is an emergency.
- **Ambiguity:** "the room smells" could be minor, sewage (high) or gas (emergency). The system should ask a follow-up question when it can't tell.

### Accessibility

Bed height and chair changes are sometimes preferences and sometimes accessibility accommodations. Accommodations get a higher priority (Low → Normal).

**Privacy rule:** the system sets `accessibility_flag` *only* when the resident explicitly says it's an accommodation or a medical or accessibility need. It never infers this, and it stores the flag, not the details.

## Real-world messiness the AI must handle

- Several issues in one message ("light's out and the blinds are broken too") → split into separate tickets.
- Vague descriptions ("the thing in the bathroom won't stop").
- Typos, slang, missing room numbers.
- Duplicates: many residents reporting the same shared-space issue (laundry, kitchen, bins).

## Labelling guidelines
 
These rules keep the hand-labelled test set consistent. They were agreed after reviewing the first 15 labels.
 
1. **Label only what the message says.** The AI sees only the message and its timestamp, so the label must too. It doesn't use outside knowledge ("it's probably the only toilet") and doesn't add tickets for problems the resident didn't mention.
2. **Use taxonomy IDs exactly.** `category` and `issue` must match `data/taxonomy.json`. If nothing fits, don't invent an ID. Set `needs_review: true`, explain in `notes`, and propose a taxonomy change.
3. **`needs_review` means triage can't be completed confidently.** That covers a missing location, an unclear issue, nothing in the taxonomy fitting, or a message that isn't a maintenance request. It does *not* mean "a technician should inspect it", because most repairs need inspection.
4. **`needs_review` is always `true` or `false`, never `null`.**
5. **Location format:** `room` is a string (`"108"`), because rooms can look like `"108B"`. `building` is the capitalized name (`"Maple"`), and comparisons ignore case. Fill in whatever the message gives and use `null` for the rest.
6. **Same situation, same label.** If two messages describe the same thing, they get the same urgency.


## Open questions / assumptions

- Heating season assumed to be Oct–Apr.
- Urgency tiers are a first draft and will be refined against the hand-labelled set.
- Building and room-type structure (suites vs. traditional, shared bathrooms) still to be modelled.
