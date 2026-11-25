# knowledge base - the venues, events and the rules for what each event needs

import json
from dataclasses import dataclass
from pathlib import Path

# where the json files are (the data folder at the top of the project)
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


# ---- what a venue and an event look like ----

@dataclass(frozen=True)
class Venue:
    id: str
    name: str
    capacity: int
    features: frozenset         # stuff the room has, like projector
    available_slots: frozenset  # times the room is free


@dataclass(frozen=True)
class Event:
    id: str
    name: str
    event_type: str
    attendees: int
    organiser: str        # lecturer running it
    group: str            # class going to it eg TU850/3
    required_features: frozenset


# ---- rules ----
# each rule is (what you need to know, what you then know)
# like lab 7, if the left side is true you add the right side

RULES = [
    # what each kind of event needs
    (["type:lecture"], "needs:projector"),
    (["type:lab"], "needs:computers"),
    (["type:seminar"], "needs:projector"),
    (["type:guest_talk"], "needs:microphone"),
    (["type:exam"], "needs:exam_desks"),

    # these ones come off other rules
    (["needs:computers"], "needs:power_sockets"),
    (["needs:microphone"], "needs:sound_system"),
    (["size:large"], "needs:wheelchair_access"),
]


def forward_chaining(facts, rules=RULES):
    # keep going through the rules adding new stuff
    # stop when nothing new gets added
    inferred = set(facts)
    while True:
        count_before = len(inferred)
        for conditions, conclusion in rules:
            if set(conditions).issubset(inferred):
                inferred.add(conclusion)
        if len(inferred) == count_before:
            return inferred


def infer_required_features(event_type, attendees, extra_features=()):
    # figure out what the room needs from the type of event
    facts = {"type:" + event_type} | {"needs:" + f for f in extra_features}
    # 100 or more people counts as a big event
    if attendees >= 100:
        facts.add("size:large")
    inferred = forward_chaining(facts)
    # only keep the needs: ones and cut off the "needs:" bit
    return frozenset(f[len("needs:"):] for f in inferred if f.startswith("needs:"))


# ---- loading the data from the json files ----

def load_venues(path=DATA_DIR / "venues.json"):
    with open(path) as f:
        rows = json.load(f)
    # turn each row into a Venue
    return [
        Venue(r["id"], r["name"], r["capacity"],
              frozenset(r["features"]), frozenset(r["available_slots"]))
        for r in rows
    ]


def load_events(path=DATA_DIR / "events.json"):
    with open(path) as f:
        rows = json.load(f)
    # turn each row into an Event and work out what it needs
    return [
        Event(r["id"], r["name"], r["event_type"], r["attendees"],
              r["organiser"], r["group"],
              infer_required_features(r["event_type"], r["attendees"],
                                      r.get("extra_features", [])))
        for r in rows
    ]
