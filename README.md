# Map Coloring CSP - Constraint Satisfaction Problem

Implementation of a backtracking search algorithm with MRV heuristic and forward checking to solve map coloring problems.

## Problem Statement

Color a map so that no two adjacent regions share the same color. This is a classic Constraint Satisfaction Problem (CSP).

## Algorithm Features

- **Backtracking Search**: Recursive DFS with constraint checking
- **MRV Heuristic**: Minimum Remaining Values - picks variable with fewest colors left
- **Forward Checking**: Prunes neighbor domains after each assignment
- **Constraint Propagation**: Restores domains on backtracking

## Implemented Maps

### 1. Australian States & Territories
- 8 regions (WA, NT, Q, SA, NSW, V, T, ACT)
- 3 colors minimum
- Real geographical adjacencies

### 2. Nairobi City County (17 Sub-counties)
Complete list:
- Westlands, Dagoretti North/South, Lang'ata, Kibra
- Roysambu, Kasarani, Ruaraka
- Embakasi (North, South, East, West, Central)
- Makadara, Kamukunji, Starehe, Mathare

## Quick Start

##vpython
# Define your map
variables = ["Region1", "Region2", "Region3"]
colors = ["Red", "Green", "Blue"]
domains = {v: colors.copy() for v in variables}

adjacencies = {
    "Region1": ["Region2"],
    "Region2": ["Region1", "Region3"],
    "Region3": ["Region2"]
}

# Solve
csp = MapColoringCSP(variables, domains, adjacencies)
solution = csp.backtrack({})

## Results
- Australia (3 colors)
- Successfully colors all 8 states/territories
- No adjacent regions share same color
- Tasmania (island) has no constraints
- Nairobi (17 sub-counties)
- Requires 4+ colors (fails with 3)
- All 17 sub-counties properly colored
- Verifies all adjacency constraints

## Key Functions
- Method	Purpose
- backtrack(assignment)	- Main recursive search
 - is_consistent(var, color, assignment)	- Checks adjacency constraints
 - forward_check(var, color)	- Prunes neighbor domains
- restore_domains(saved_domains)	- Undoes pruning on backtrack
# Output Includes
Color assignment for each region
Color grouping by value
Constraint verification
Color distribution statistics
Regional map visualization

## Graph Properties
Australia: 3-colorable planar graph

Nairobi: Requires 4 colors (contains K4 subgraph)

Author
Collins Kimani Gocho
collinskimani482@gmail.com
