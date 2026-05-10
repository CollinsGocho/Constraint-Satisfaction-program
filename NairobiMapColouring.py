class MapColoringCSP:
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.assignments = {}

    def is_consistent(self, var, color, assignment):
        """Check if assigning 'color' to 'var' violates any constraints."""
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
                
                saved_domains = {n: list(self.domains[n]) for n in self.neighbors.get(var, [])}
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


print("="*70)
print("NAIROBI CITY COUNTY - 17 SUB-COUNTIES MAP COLORING")
print("="*70)

nairobi_subcounties = [
    "Westlands", "Dagoretti North", "Dagoretti South", "Lang'ata", "Kibra",
    "Roysambu", "Kasarani", "Ruaraka", "Embakasi North", "Embakasi South",
    "Embakasi East", "Embakasi West", "Embakasi Central", "Makadara",
    "Kamukunji", "Starehe", "Mathare"
]

colors = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange"]

domains_nairobi = {subcounty: list(colors) for subcounty in nairobi_subcounties}

adjacencies_nairobi = {
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

print("\nSolving the map coloring problem for 17 sub-counties...")
print(f"Variables: {len(nairobi_subcounties)} sub-counties")
print(f"Colors available: {len(colors)} colors")
print("Using MRV heuristic + Forward Checking\n")

csp_nairobi = MapColoringCSP(nairobi_subcounties, domains_nairobi, adjacencies_nairobi)
solution_nairobi = csp_nairobi.backtrack({})

if solution_nairobi:
    print("SOLUTION FOUND!")
    print("="*70)
    print("\nSUB-COUNTY COLOR ASSIGNMENTS:")
    print("-"*70)
    
    color_groups = {}
    for subcounty, color in solution_nairobi.items():
        if color not in color_groups:
            color_groups[color] = []
        color_groups[color].append(subcounty)
    
    print("\nCOLOR GROUPS:")
    for color, subcounties_list in sorted(color_groups.items()):
        print(f"\n  {color}:")
        for sc in sorted(subcounties_list):
            print(f"    - {sc}")
    
    print("\n" + "="*70)
    print("DETAILED SUB-COUNTY COLOR MAP:")
    print("-"*70)
    for subcounty in sorted(nairobi_subcounties):
        print(f"  {subcounty:20} : {solution_nairobi[subcounty]}")
    
    print("\n" + "="*70)
    print("CONSTRAINT VERIFICATION:")
    print("-"*70)
    violations = 0
    for subcounty, neighbors in adjacencies_nairobi.items():
        for neighbor in neighbors:
            if neighbor in solution_nairobi:
                if solution_nairobi[subcounty] == solution_nairobi[neighbor]:
                    print(f"VIOLATION: {subcounty} and {neighbor} both {solution_nairobi[subcounty]}")
                    violations += 1
    if violations == 0:
        print("  ALL CONSTRAINTS SATISFIED!")
        print("  No adjacent sub-counties share the same color!")
    
    
    print("\n" + "="*70)
    print("STATISTICS:")
    print("-"*70)
    unique_colors = len(set(solution_nairobi.values()))
    print(f"Colors used: {unique_colors} out of {len(colors)} available")
    print(f"Total sub-counties: {len(solution_nairobi)}")
    
    
    from collections import Counter
    color_count = Counter(solution_nairobi.values())
    print("\nColor distribution:")
    for color, count in sorted(color_count.items()):
        bar = "|" * count
        print(f"    {color:10}: {bar} ({count})")
    
else:
    print("No solution found with the given colors!")
    print("Try adding more colors or adjusting adjacencies.")



def visualize_nairobi_map(solution):
    """Create a simple text-based visualization of Nairobi's sub-counties"""
    if not solution:
        return
    
    print("\n" + "="*70)
    print("TEXT-BASED MAP OF NAIROBI SUB-COUNTIES")
    print("="*70)
    
    # Group by region
    print("\n  [WESTERN CLUSTER]:")
    western = ["Westlands", "Dagoretti North", "Dagoretti South", "Lang'ata", "Kibra"]
    for sc in western:
        if sc in solution:
            print(f"     {sc:18} : {solution[sc]}")
    
    print("\n  [NORTHERN CLUSTER]:")
    northern = ["Roysambu", "Kasarani", "Ruaraka"]
    for sc in northern:
        if sc in solution:
            print(f"     {sc:18} : {solution[sc]}")
    
    print("\n  [EASTERN CLUSTER]:")
    eastern = ["Embakasi North", "Embakasi South", "Embakasi East", "Embakasi West", "Embakasi Central"]
    for sc in eastern:
        if sc in solution:
            print(f"     {sc:18} : {solution[sc]}")
    
    print("\n  [CENTRAL/SOUTHERN CLUSTER]:")
    central = ["Makadara", "Kamukunji", "Starehe", "Mathare"]
    for sc in central:
        if sc in solution:
            print(f"     {sc:18} : {solution[sc]}")

visualize_nairobi_map(solution_nairobi)

print("\n" + "="*70)
print("TRYING WITH MINIMAL COLORS (3 colors)")
print("="*70)

minimal_colors = ["Red", "Green", "Blue"]
domains_minimal = {subcounty: list(minimal_colors) for subcounty in nairobi_subcounties}

csp_minimal = MapColoringCSP(nairobi_subcounties, domains_minimal, adjacencies_nairobi)
solution_minimal = csp_minimal.backtrack({})

if solution_minimal:
    print("Solution found with only 3 colors!")
    unique_colors = len(set(solution_minimal.values()))
    print(f"Colors used: {unique_colors}/3")
else:
    print("No solution exists with only 3 colors!")
    print("(Nairobi's map requires at least 4 colors due to its graph structure)")

print("\n" + "="*70)
print("MAP COLORING COMPLETE!")
print("="*70)