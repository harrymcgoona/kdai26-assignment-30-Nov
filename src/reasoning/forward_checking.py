def forward_checking(csp, assignment, domains):
     #copy the domains
    new_domains = {
        event: list(allocations)
        for event, allocations in domains.items()
    }

    for event in csp.variables:
            #looking at each unscdheuled event
        if event not in assignment:
           #removed invalid allocations
            new_domains[event] = [
                allocation
                for allocation in new_domains[event]
                if csp.obeys_rules(event, allocation, assignment)
            ]
            #detect the dead ends early
            if len(new_domains[event]) == 0:
                return None

    return new_domains
