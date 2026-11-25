# constraints for the scheduling csp
# each event is a variable
# a value is (venue id, time slot)
# the schedule is a dict like {event id: (venue id, slot)}


# ---- rules for one event on its own ----

def fits_capacity(event, venue):
    # room has to be big enough
    return event.attendees <= venue.capacity


def has_features(event, venue):
    # room has to have everything the event needs
    return event.required_features.issubset(venue.features)


# ---- rules for two events together ----

def no_double_booked_venue(allocation1, allocation2):
    # cant have two events in the same room at the same time
    return allocation1 != allocation2


def no_person_clash(event1, allocation1, event2, allocation2):
    # same lecturer or same class cant be in two places at once
    same_slot = allocation1[1] == allocation2[1]          # [1] is the time slot
    shares_organiser = event1.organiser == event2.organiser
    # ALL means everyone goes so it clashes with every class
    shares_group = (event1.group == event2.group
                    or "ALL" in (event1.group, event2.group))
    return not (same_slot and (shares_organiser or shares_group))


# ---- domains ----

def build_domains(events, venues):
    # for each event get every room and time that works
    # takes out rooms that are too small or missing stuff before the search starts
    domains = {}
    for event in events:
        options = []
        for venue in venues:
            if fits_capacity(event, venue) and has_features(event, venue):
                for slot in venue.available_slots:
                    options.append((venue.id, slot))
        domains[event.id] = sorted(options)
    return domains


# ---- stuff to pass into henrys CSP class ----

def make_scheduling_constraint(events):
    # makes the function henrys csp uses to check two events
    by_id = {e.id: e for e in events}

    def scheduling_constraint(event1, allocation1, event2, allocation2):
        e1, e2 = by_id[event1], by_id[event2]
        if not no_double_booked_venue(allocation1, allocation2):
            return False
        if not no_person_clash(e1, allocation1, e2, allocation2):
            return False
        return True

    return scheduling_constraint


def build_csp_inputs(events, venues):
    # gives the solver everything it needs in one go
    variables = [e.id for e in events]
    domains = build_domains(events, venues)
    constraint = make_scheduling_constraint(events)
    event_attendance = {e.id: e.attendees for e in events}
    venue_capacity = {v.id: v.capacity for v in venues}
    return variables, domains, constraint, event_attendance, venue_capacity
