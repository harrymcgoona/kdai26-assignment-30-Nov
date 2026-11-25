"""Knowledge base: data schemas, data loading, and rules about what events need."""

import json
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@dataclass(frozen=True)
class Venue:
    id: str
    name: str
    capacity: int
    features: frozenset
    available_slots: frozenset


@dataclass(frozen=True)
class Event:
    id: str
    name: str
    event_type: str
    attendees: int
    organiser: str        # lecturer running
    group: str            # the student group attending, e.g. "TU850/3"
    required_features: frozenset


# Each rule is (list_of_required_facts, conclusion).
# Facts look like "type:lab" or "needs:computers".

RULES = [
    (["type:lecture"], "needs:projector"),
    (["type:lab"], "needs:computers"),
    (["type:seminar"], "needs:projector"),
    (["type:guest_talk"], "needs:microphone"),
    (["type:exam"], "needs:exam_desks"),

    # chaining
    (["needs:computers"], "needs:power_sockets"),
    (["needs:microphone"], "needs:sound_system"),
    (["size:large"], "needs:wheelchair_access"),
]


def forward_chaining(facts, rules=RULES):
    """Keep applying rules until no new facts are found."""
    inferred = set(facts)
    while True:
        count_before = len(inferred)
        for conditions, conclusion in rules:
            if set(conditions).issubset(inferred):
                inferred.add(conclusion)
        if len(inferred) == count_before:
            return inferred


def infer_required_features(event_type, attendees, extra_features=()):
    """Work out which venue features an event needs from its type and size."""
    facts = {"type:" + event_type} | {"needs:" + f for f in extra_features}
    if attendees >= 100:
        facts.add("size:large")
    inferred = forward_chaining(facts)
    return frozenset(f[len("needs:"):] for f in inferred if f.startswith("needs:"))


# loading data

def load_venues(path=DATA_DIR / "venues.json"):
    with open(path) as f:
        rows = json.load(f)
    return [
        Venue(r["id"], r["name"], r["capacity"],
              frozenset(r["features"]), frozenset(r["available_slots"]))
        for r in rows
    ]


def load_events(path=DATA_DIR / "events.json"):
    with open(path) as f:
        rows = json.load(f)
    return [
        Event(r["id"], r["name"], r["event_type"], r["attendees"],
              r["organiser"], r["group"],
              infer_required_features(r["event_type"], r["attendees"],
                                      r.get("extra_features", [])))
        for r in rows
    ]
