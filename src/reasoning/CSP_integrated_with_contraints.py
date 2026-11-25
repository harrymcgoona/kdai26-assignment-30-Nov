from src.knowledge.knowledgebase import load_events, load_venues
from src.knowledge.constraints import build_csp_inputs



class CSP:
    def __init__(self,variables,domains,constraints):
        self.variables=variables
        self.domains=domains
        self.constraints=constraints
        self.attempts=0
        
    def obeys_rules(self,event,allocation,assignment):
        
        for other_event,other_allocation in assignment.items():
            if not self.constraints(
                event,allocation,
                other_event,other_allocation
            ):
                return False
        return True
                
          

        
        
 

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
#calcs total number of unused setas across all assigned venues
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
    #removes vonflicting options from remaining domains and detects deadends
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
#keeps searching for valid schedules and retains ones with lowest score
def backtracking(csp,assignment,domains,event_attendance,venue_capacity,best_solution=None,best_score=float("inf")):
    if len(assignment)==len(csp.variables):
        score = score_schedule(
            assignment,
            event_attendance,
            venue_capacity
        )

        # Is this the best schedule so far, thats the question i need to ask
        if score < best_score:
            return assignment.copy(), score

        return best_solution, best_score

    
    next_event=select_unassigned_variable(csp,assignment,domains)
        
    for allocation in domains[next_event]:
        csp.attempts+=1
        if csp.obeys_rules(next_event,allocation,assignment):
            assignment[next_event]=allocation
            #schedule the remaining events
            new_domains = forward_checking(
                csp, assignment, domains
            )

            # Continue only if no domain became empty
            if new_domains is not None:

                result,result_score = backtracking(
                    csp, assignment, new_domains,event_attendance,venue_capacity,best_solution,best_score
                )

                if result is not None and result_score<best_score:
                    best_solution=result
                    best_score=result_score
                    
            #if its a dead end undo alloaction
            del assignment[next_event]
    return best_solution,best_score

#loads event and venue inof deom project datafiles tgat eric made
real_events=load_events()
real_venues=load_venues()

#converts our data  into CS_ variables ,domains,cinstraints,and scoring inputs
real_variables,real_domains,real_constraint,real_attendance,real_capacity=build_csp_inputs(
    real_events,real_venues
)
#creates csp problem using real project data
real_problem=CSP(
    real_variables,real_domains,real_constraint
)
#runs backtracking solver to find best scehdule
real_solution,real_score=backtracking(
    real_problem,{},
    real_domains,real_attendance,real_capacity
)
#displays final schdule
print("\n final schedule=")
print("Solution:", real_solution)
print("Unused seat score:", real_score)
print("Allocation attempts:", real_problem.attempts)

# Validate the schedule, independently checks that the complted schdeule contains every event
#and satisfies constraints
print("\n schedule validation")
print("Valid schedule:", validate_schedule(real_problem, real_solution))
#confirms evry event allocation belongs to its original domai
for event in real_events:
    assert real_solution[event.id] in real_domains[event.id]
    
print("Domain validation passed")
#displays assigned venue and time for each event
for event in real_events:
    venue_id, slot = real_solution[event.id]

    venue = next(v for v in real_venues if v.id == venue_id)

    print(event.name, "->", venue.name, slot)
    
#confirms each venue has sufficient capacity for its assigned event
for event in real_events:
    venue_id,slot=real_solution[event.id]
    venue = next(v for v in real_venues if v.id==venue_id)
    assert event.attendees<=venue.capacity
    
print("Capacity validation passed")
    #confirms assigned venues contain all requried event features
for event in real_events:
    venue_id,slot=real_solution[event.id]
    venue=next(v for v in real_venues if v.id==venue_id)
    assert event.required_features.issubset(venue.features)
    
print("feature validation passed")
#Confirms that evry event is assigned to an available venue time slot.
for event in real_events:
    venue_id,slot=real_solution[event.id]
    venue=next(v for v in real_venues if v.id==venue_id)
    assert slot in venue.available_slots
print("availabilty validation passed")
#python -m src.reasoning.csp

#we dont want to trust the solver like its a fact

recalculated_score=0

for event in real_events:
    venue_id,slot=real_solution[event.id]
    venue=next(v for v in real_venues if v.id==venue_id)
    
    recalculated_score+=venue.capacity - event.attendees
    
    
assert recalculated_score==real_score

print("Real schdeule score veeifcation passed")
print("recalcuated score",recalculated_score)
#should return 220 again

