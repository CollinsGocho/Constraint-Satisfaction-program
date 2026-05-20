
class AustraliaMapcoloring:
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors

    def is_consistent(self, var, color, assignment):
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment and assignment[neighbor] == color:
                return False
        return True

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]
        var = min(unassigned, key=lambda v: len(self.domains[v]))

        for color in self.domains[var][:]:
            if self.is_consistent(var, color, assignment):
                assignment[var] = color
                
                removed = self.forward_check(var, color, assignment)
                if removed is not None:
                    result = self.backtrack(assignment)
                    if result:
                        return result
                    self.restore_domains(removed)
                
                del assignment[var]
        return None

    def forward_check(self, var, color, assignment):
        removed = {}
        for neighbor in self.neighbors.get(var, []):
            if neighbor not in assignment and color in self.domains[neighbor]:
                self.domains[neighbor].remove(color)
                removed[neighbor] = color
                if not self.domains[neighbor]:
                    return None
        return removed

    def restore_domains(self, removed):
        for var, color in removed.items():
            self.domains[var].append(color)


states = ["WA", "NT", "Qld", "SA", "NSW", "Vic", "Tas", "ACT"]
colors = ["Red", "Green", "Blue"]

domains = {s: colors[:] for s in states}

adj = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "SA", "Qld"],
    "SA": ["WA", "NT", "Qld", "NSW", "Vic"],
    "Qld": ["NT", "SA", "NSW"],
    "NSW": ["Qld", "SA", "Vic", "ACT"],
    "Vic": ["SA", "NSW"],
    "Tas": [],
    "ACT": ["NSW"]
}

csp = MapColoringCSP(states, domains, adj)
solution = csp.backtrack({})

if solution:
    for state in sorted(solution.keys()):
        print(f"{state}: {solution[state]}")
    
    # check constraints
    ok = True
    for s, neighbors in adj.items():
        for n in neighbors:
            if solution[s] == solution[n]:
                print(f"Error: {s} and {n} share {solution[s]}")
                ok = False
    if ok:
        print("All constraints satisfied")
else:
    print("No solution found")
