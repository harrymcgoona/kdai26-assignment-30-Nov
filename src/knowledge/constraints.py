"""CSP formulation and constraint rules (AIMA style).

Variables : one per event
Values    : (venue_id, slot) pairs
State     : assignment dict {event_id: (venue_id, slot)}
Goal      : every event assigned and no hard constraint broken
Path cost : soft constraints (wasted seats)
"""


def fits_capacity(event, venue):
    """The venue must hold everyone attending."""
    return event.attendees <= venue.capacity

def has_features(event, venue):
    """The venue must have every feature the event needs."""
    return event.required_features.issubset(venue.features)

def no_double_booked_venue(value1, value2):
    """Two events can't be in the same venue at the same time."""
    return value1 != value2

def no_person_clash(event1, value1, event2, value2):
    """The same lecturer or student group can't be in two places at once."""
    same_slot = value1[1] == value2[1]          # [1] is the slot
    shares_organiser = event1.organiser == event2.organiser
    shares_group = (event1.group == event2.group
                    or "ALL" in (event1.group, event2.group))
    return not (same_slot and (shares_organiser or shares_group))

def build_domains(events, venues):
    """For each event, list every (venue, slot) that passes the unary constraints."""
    domains = {}
    for event in events:
        options = []
        for venue in venues:
            if fits_capacity(event, venue) and has_features(event, venue):
                for slot in venue.available_slots:
                    options.append((venue.id, slot))
        domains[event.id] = sorted(options)
    return domains


def is_consistent(assignment, events):
    """Check a full or partial assignment against the binary constraints."""
    by_id = {e.id: e for e in events}
    ids = list(assignment)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            e1, e2 = by_id[ids[i]], by_id[ids[j]]
            v1, v2 = assignment[ids[i]], assignment[ids[j]]
            if not no_double_booked_venue(v1, v2):
                return False
            if not no_person_clash(e1, v1, e2, v2):
                return False
    return True


def is_goal(assignment, events):
    """Goal test: every event is scheduled and nothing clashes."""
    return len(assignment) == len(events) and is_consistent(assignment, events)

def wasted_seats(assignment, events, venues):
    """Lower is better: total empty seats across the schedule."""
    event_by_id = {e.id: e for e in events}
    venue_by_id = {v.id: v for v in venues}
    total = 0
    for event_id, (venue_id, _slot) in assignment.items():
        total += venue_by_id[venue_id].capacity - event_by_id[event_id].attendees
    return total
