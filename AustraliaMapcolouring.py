class MapColoringCSP:
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.assignments = {}

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

        for color in list(self.domains[var]):
            if self.is_consistent(var, color, assignment):
                assignment[var] = color
                
                
                saved_domains = {}
                for n in self.neighbors.get(var, []):
                    saved_domains[n] = list(self.domains[n])
                
                if self.forward_check(var, color):
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                
                self.restore_domains(saved_domains)
                del assignment[var]

        return None

    def forward_check(self, var, color):
        for neighbor in self.neighbors.get(var, []):
            if neighbor not in self.assignments:
                if color in self.domains[neighbor]:
                    self.domains[neighbor].remove(color)
                    if not self.domains[neighbor]:
                        return False
        return True

    def restore_domains(self, saved_domains):
        for neighbor, domain_values in saved_domains.items():
            self.domains[neighbor] = domain_values



print("="*60)
print("AUSTRALIAN STATES AND TERRITORIES MAP COLORING")
print("="*60)

australian_states = ["Western Australia", "Northern Territory", "Queensland",
                     "South Australia", "New South Wales", "Victoria",
                     "Tasmania", "Australian Capital Territory"]

colors = ["Red", "Green", "Blue"]

domains = {state: list(colors) for state in australian_states}

adjacencies = {
    "Western Australia": ["Northern Territory", "South Australia"],
    "Northern Territory": ["Western Australia", "South Australia", "Queensland"],
    "South Australia": ["Western Australia", "Northern Territory", "Queensland", "New South Wales", "Victoria"],
    "Queensland": ["Northern Territory", "South Australia", "New South Wales"],
    "New South Wales": ["Queensland", "South Australia", "Victoria", "Australian Capital Territory"],
    "Victoria": ["South Australia", "New South Wales"],
    "Tasmania": [],  # Island state, no land neighbors
    "Australian Capital Territory": ["New South Wales"]  # Enclaved within NSW
}

print("\nSolving the map coloring problem for Australian states...")
print(f"Variables: {len(australian_states)} states and territories")
print(f"Colors available: {len(colors)} colors")
print("Using MRV heuristic + Forward Checking")
print("-"*60)

csp = MapColoringCSP(australian_states, domains, adjacencies)
solution = csp.backtrack({})

if solution:
    print("\nSOLUTION FOUND!")
    print("="*60)
    print("STATE/TERRITORY COLOR ASSIGNMENTS:")
    print("-"*60)
    
    for state in sorted(solution.keys()):
        print(f"  {state:25} : {solution[state]}")
    
    print("\n" + "="*60)
    print("CONSTRAINT VERIFICATION:")
    print("-"*60)
    violations = 0
    for state, neighbors in adjacencies.items():
        for neighbor in neighbors:
            if neighbor in solution:
                if solution[state] == solution[neighbor]:
                    print(f"  VIOLATION: {state} and {neighbor} both {solution[state]}")
                    violations += 1
    
    if violations == 0:
        print("  All constraints satisfied!")
        print("  No adjacent states share the same color.")
    
    print("\n" + "="*60)
    print("STATISTICS:")
    print("-"*60)
    unique_colors = len(set(solution.values()))
    print(f"  Colors used: {unique_colors} out of {len(colors)} available")
    print(f"  Total states/territories: {len(solution)}")
    
    from collections import Counter
    color_count = Counter(solution.values())
    print("\n  Color distribution:")
    for color, count in sorted(color_count.items()):
        bar = "|" * count
        print(f"    {color:12} : {bar} ({count})")
    
else:
    print("\nNo solution found with 3 colors!")
    print("Note: Australia's map requires 3 colors, but the graph structure")
    print("may need different initial domain ordering or more colors.")

print("\n" + "="*60)
print("MAP COLORING COMPLETE")
print("="*60)
def visualize_australian_map(solution):
    if not solution:
        return
    
    print("\n" + "="*60)
    print("TEXT-BASED MAP OF AUSTRALIA")
    print("="*60)
    
    print("\n  [WESTERN REGION]:")
    western = ["Western Australia"]
    for state in western:
        if state in solution:
            print(f"    {state:25} : {solution[state]}")
    
    print("\n  [NORTHERN REGION]:")
    northern = ["Northern Territory", "Queensland"]
    for state in northern:
        if state in solution:
            print(f"    {state:25} : {solution[state]}")
    
    print("\n  [CENTRAL REGION]:")
    central = ["South Australia"]
    for state in central:
        if state in solution:
            print(f"    {state:25} : {solution[state]}")
    
    print("\n  [EASTERN REGION]:")
    eastern = ["New South Wales", "Victoria", "Australian Capital Territory"]
    for state in eastern:
        if state in solution:
            print(f"    {state:25} : {solution[state]}")
    
    print("\n  [ISLAND STATE]:")
    island = ["Tasmania"]
    for state in island:
        if state in solution:
            print(f"    {state:25} : {solution[state]}")

if solution:
    visualize_australian_map(solution)


print("\n" + "="*60)
print("TESTING WITH MORE COLORS (4 colors)")
print("="*60)

more_colors = ["Red", "Green", "Blue", "Yellow"]
domains_more = {state: list(more_colors) for state in australian_states}

csp_more = MapColoringCSP(australian_states, domains_more, adjacencies)
solution_more = csp_more.backtrack({})

if solution_more:
    print("\nSolution found with 4 colors!")
    unique_colors = len(set(solution_more.values()))
    print(f"Colors used: {unique_colors} out of 4")
    
    print("\nColor assignments with 4 colors:")
    for state in sorted(solution_more.keys()):
        print(f"  {state:25} : {solution_more[state]}")
else:
    print("No solution found with 4 colors either.")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)



print("="*60)
print("PROGRAM COMPLETED SUCCESSFULLY")
print("="*60)