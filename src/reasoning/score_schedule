def score_schedule(solution, event_attendance, venue_capacity):
    #inialising the score
    wasted_seats=0
    #loop through schedule
    for event,allocation in solution.items():
        venue,time=allocation
        unused=venue_capacity[venue]-event_attendance[event]
        wasted_seats+=unused
        #ideally we want a lower score,it means better a better schedule
    return wasted_seats
