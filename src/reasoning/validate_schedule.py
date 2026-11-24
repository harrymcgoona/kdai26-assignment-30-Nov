def validate_schedule(csp,solution):
    #detects if no solution
    if solution is None:
        return False
    #checks if correct number of events
    if len(solution )!=len(csp.variables):
        return False
    #extract scheduled events
    events=list(solution.keys())
    #compare every pair of events
    for i in range(len(events)):
        for j in range(i+1,len(events)):
            #retrieve events and allocations
            event1=events[i]
            event2=events[j]
            
            allocation1=solution[event1]
            allocation2=solution[event2]
            #check constraint
            if not csp.constraints(
                event1,allocation1,
                event2,allocation2
            ):
                return False
    #all g then return true
    return True
