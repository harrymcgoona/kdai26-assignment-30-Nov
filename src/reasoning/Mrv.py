#deciding which event to assign next,fewest legal allocations remaining
def select_unassigned_variable(csp,assignment,domains):
    unassigned=[
        event for event in csp.variables
        if event not in assignment
        #mrv will pick the lowest allocations if event1 venue/time slot left=2 vs event2=4, scheduler will pick event1
    ]
    return min(
        unassigned,
        key=lambda event: sum(
            1 for alloaction in domains[event]
            if csp.obeys_rules(event,alloaction,assignment)
        )
    )
