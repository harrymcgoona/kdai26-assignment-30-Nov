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
