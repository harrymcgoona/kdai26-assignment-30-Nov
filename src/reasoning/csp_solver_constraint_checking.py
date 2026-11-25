#creating the class for the csp
class CSP:
    def __init__(self,variables,domains,constraints):
        self.variables=variables
        self.domains=domains
        self.constraints=constraints
        self.attempts=0
        #obey rules function ensures our scheduling constraints are applied
    def obeys_rules(self,event,allocation,assignment):
        
        for other_event,other_allocation in assignment.items():
            if not self.constraints(
                event,allocation,
                other_event,other_allocation
            ):
                return False
        return True
      #the actual scheduling constraint rules function
    def scheduling_constraint(event1,allocation1,event2,allocation2):
      venue1,time1=allocation1
      #(room a,09:00)=allocation
      venue2,time2=allocation2
      #checking for clash
      if venue1==venue2 and time1==time2:
        return False  #clash so returns invalid
      return True  
