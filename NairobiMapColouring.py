class NairobiMapColoring:
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

        # pick next variable
        unassigned = [v for v in self.variables if v not in assignment]
        # mrv heuristic - but i might have bug here
        var = min(unassigned, key=lambda v: len(self.domains[v]))

        for color in self.domains[var][:]:  # copy so we don't modify original
            if self.is_consistent(var, color, assignment):
                assignment[var] = color
                
                # forward checking
                removed = {}
                ok = True
                for nb in self.neighbors.get(var, []):
                    if nb not in assignment:
                        if color in self.domains[nb]:
                            self.domains[nb].remove(color)
                            removed[nb] = color
                            if len(self.domains[nb]) == 0:
                                ok = False
                                break
                
                if ok:
                    result = self.backtrack(assignment)
                    if result:
                        return result
                
                # restore domains - i think this works
                for nb, col in removed.items():
                    self.domains[nb].append(col)
                
                del assignment[var]
        
        return None


# nairobi subcounties - i hope i got all 17
subcounties = [
    "Westlands", "Dagoretti North", "Dagoretti South", "Lang'ata", "Kibra",
    "Roysambu", "Kasarani", "Ruaraka", "Embakasi North", "Embakasi South",
    "Embakasi East", "Embakasi West", "Embakasi Central", "Makadara",
    "Kamukunji", "Starehe", "Mathare"
]

colors = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]

domains = {}
for s in subcounties:
    domains[s] = colors.copy()  # each gets all colors

# adjacency - not 100% sure about these borders
neighbors = {
    "Westlands": ["Dagoretti North", "Lang'ata", "Kibra", "Roysambu", "Starehe"],
    "Dagoretti North": ["Westlands", "Dagoretti South", "Kibra", "Roysambu"],
    "Dagoretti South": ["Dagoretti North", "Lang'ata", "Kibra"],
    "Lang'ata": ["Westlands", "Dagoretti South", "Kibra", "Embakasi South", "Makadara"],
    "Kibra": ["Westlands", "Dagoretti North", "Dagoretti South", "Lang'ata", "Makadara", "Kamukunji"],
    "Roysambu": ["Westlands", "Dagoretti North", "Kasarani", "Ruaraka", "Starehe"],
    "Kasarani": ["Roysambu", "Ruaraka", "Embakasi North", "Embakasi Central"],
    "Ruaraka": ["Roysambu", "Kasarani", "Embakasi North", "Starehe", "Mathare"],
    "Embakasi North": ["Kasarani", "Ruaraka", "Embakasi East", "Embakasi Central"],
    "Embakasi South": ["Lang'ata", "Embakasi West", "Embakasi East", "Makadara"],
    "Embakasi East": ["Embakasi North", "Embakasi South", "Embakasi West", "Embakasi Central"],
    "Embakasi West": ["Embakasi South", "Embakasi East", "Embakasi Central", "Makadara"],
    "Embakasi Central": ["Kasarani", "Embakasi North", "Embakasi East", "Embakasi West", "Kamukunji", "Starehe"],
    "Makadara": ["Lang'ata", "Kibra", "Embakasi South", "Embakasi West", "Kamukunji", "Starehe", "Mathare"],
    "Kamukunji": ["Kibra", "Embakasi Central", "Makadara", "Starehe", "Mathare"],
    "Starehe": ["Westlands", "Roysambu", "Ruaraka", "Embakasi Central", "Makadara", "Kamukunji", "Mathare"],
    "Mathare": ["Ruaraka", "Makadara", "Kamukunji", "Starehe"]
}

csp = MapColoringCSP(subcounties, domains, neighbors)
solution = csp.backtrack({})

if solution:
    print("Solution found!")
    for s in sorted(solution.keys()):
        print(f"{s}: {solution[s]}")
    
    # verify
    errors = 0
    for s in neighbors:
        for n in neighbors[s]:
            if solution[s] == solution[n]:
                print(f"Error: {s} and {n} same color {solution[s]}")
                errors += 1
    
    if errors == 0:
        print("All good - no adjacent same colors")
    else:
        print(f"{errors} conflicts found")
    
    # check color usage
    used_colors = set(solution.values())
    print(f"\nUsed {len(used_colors)} colors")
    
else:
    print("No solution found - need more colors probably")

# try with just 3 colors
print("\nTrying with only 3 colors...")
domains3 = {}
for s in subcounties:
    domains3[s] = ["Red", "Green", "Blue"].copy()

csp3 = MapColoringCSP(subcounties, domains3, neighbors)
sol3 = csp3.backtrack({})

if sol3:
    print("Worked with 3 colors")
else:
    print("3 colors not enough for this map")
