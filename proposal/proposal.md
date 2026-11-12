# Project Proposal: Event Scheduling and Venue Allocation System

**Module:** AINL3001 Knowledge-Driven AI  
**Program:** TU850 BSc in Data Science and Artificial Intelligence  
**Lecturer:** Dr. Bianca Schoen-Phelan  

## 1. Team Information
### **Group Name:** Team HHEJ

**Team Members:**
| Name | Student ID | Github |
| :--- | :---: | ---: |
| Harry McGoona | C24342003 | @harrymcgoona |
| Eric Meagher | C24733845 | @ericmeagher |
| Henry Guinane | C24464042 | @hguinan1 |
| Jack Shun | [...] | @JackSh28 |

**Task Allocation:**
| Name | Primary Focus | Deliverables |
| :--- | :---: | ---: |
| Harry McGoona | [...] | [...] |
| Eric Meagher | [...] | [...] |
| Henry Guinane | [...] | [...] |
| Jack Shun | [...] | [...] |

## 2. Problem Description
Manual event scheduling and venue allocation is tedious and error prone. Organisers frequently struggle with double bookings, room capacity overflows, conflicting time slots, and unmet equipment requirements.

Our system intends to solve this by automating the scheduling process. By representing events, rooms, and constraints explicitly in a knowledge base, the system uses search and constraint satisfaction techniques to generate conflict-free, optimised schedules instantly.

### Core Objectives
- **Primary Goal:** Automatically assign events to valid venues and time slots with zero constraint violations.
- **Challenges Addressed:** Managing hard operational limits (i.e., room capacity, equipment matching, time clashes) within a complex search space.
- **Value & Impact:** Eliminates manual scheduling errors, saves administrative time, and maximises efficient venue utilisation.

## 3. Proposed AI Approach & AIMA Framework
To maintain alignment with the Artificial Intelligence: A Modern Approach (AIMA) framework covered in the module, our system defines a rigorous problem-solving architecture combining explicit constraint satisfaction and search reasoning.

### AIMA Problem Formulation
- **State Representation:** A mapping of events to specific venues and time slots, alongside unassigned events.
- **Initial State:** An empty schedule where all events are unassigned, alongside the raw pool of venues, times, and requests.
- **Actions:** Assigning an unassigned event to a valid venue and time slot without breaking hard rules.
- **Transition Model:** Adds the valid assignment to the schedule and updates resource availability.
- **Goal Test:** Verifies that all events are scheduled and all hard constraints are satisfied.
- **Path Cost:** Evaluates schedule quality based on soft constraints (i.e., minimising gaps or wasted capacity).

### Core AI Techniques Used
1. **Constraint Satisfaction Problem (CSP) Solver**
   - **Purpose:** Handles hard operational limits like room capacity and non-overlapping schedules.
   - **Implementation:** Backtracking search with forward checking to prune invalid branches early.
2. **Heuristic Search & Optimization**
   - **Purpose:** Finds high quality schedules efficiently when multiple valid options exist.
   - **Implementation:** Uses heuristic evaluation functions to prioritize heavily constrained events.
3. **Rule-Based Knowledge Representation**
   - **Purpose:** Encodes institutional logic (e.g., IF event is a lab, THEN venue must have computers).

## 4. High-Level System Architecture

The system is structured modularly inside the `src/` directory to separate data handling, rule validation, and search execution.

```text
                          +-------------------------+
                          |   User / Event Requests  |
                          +------------+------------+
                                       |
                                       v
                          +-------------------------+
                          | Knowledge Base & Rules  |
                          | (Venues, Capacities,    |
                          |  Equipment Constraints) |
                          +------------+------------+
                                       |
                                       v
                          +-------------------------+
                          |    CSP & Search Engine   |
                          |  (Backtracking / AIMA)  |
                          +------------+------------+
                                       |
                                       v
                          +-------------------------+
                          |  Optimised Schedule &   |
                          |   Conflict Report Out   |
                          +-------------------------+
