from flask import Flask, render_template, request, session, redirect, url_for, flash
import random
import json
import os

app = Flask(__name__)
app.secret_key = 'gate_cse_air1_companion_secret_key'

# Load user credentials
def load_credentials():
    try:
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

credentials = load_credentials()

subjects = {
    "Engineering Mathematics": [
    "Set Theory & Relations",
    "Mathematical Logic: Propositional & First-Order",
    "Algebraic Structures: Groups, Rings, Fields",
    "Partial Orders & Lattices",
    "Boolean Algebra",
    "Combinatorics & Counting",
    "Number Theory & Discrete Structures",
    "Recurrence Relations & Generating Functions",
    "Graph Theory: Connectivity, Planarity, Matching, Coloring, Trees",
    "Linear Algebra: Vector Spaces, Matrices, Determinants",
    "Linear Transformations & Rank",
    "LU & QR Decomposition",
    "Eigenvalues, Eigenvectors & Diagonalization",
    "Calculus: Limits, Continuity, Differentiability",
    "Optimization: Maxima-Minima, Lagrange Multipliers",
    "Integration: Definite, Indefinite, Multiple Integrals",
    "Mean Value Theorem",
    "Line, Surface, Volume Integrals",
    "Differential Equations: ODE, PDE",
    "Numerical Methods",
    "Probability Theory: Sample Space, Events, Conditional Probability",
    "Random Variables & Probability Distributions",
    "Bayes Theorem & Applications",
    "Statistics: Descriptive & Inferential",
    "Hypothesis Testing & Confidence Intervals",
    "Moments, Skewness, Kurtosis",
    "Correlation, Regression & Time Series"
  ],
    "Digital Logic": [
        "Number Systems: Binary, Octal, Hexadecimal",
        "Signed Number Representation: 2's Complement",
        "Fixed-Point & Floating-Point Arithmetic",
        "IEEE 754 Standard",
        "Boolean Algebra & De Morgan's Laws",
        "Logic Gates: Universal, Multi-level",
        "Logic Minimization: K-Map, Quine-McCluskey",
        "Multi-level Logic Optimization",
        "Combinational Logic Design",
        "Multiplexers, Demultiplexers, Encoders, Decoders",
        "Adders, Subtractors & Arithmetic Circuits",
        "Comparators & Code Converters",
        "Sequential Logic: Latches & Flip-Flops",
        "Registers: Shift, Storage, Counter",
        "State Machines: Moore & Mealy Models",
        "Timing Analysis & Race Conditions",
        "Hazards in Combinational Circuits",
        "Memory & Programmable Logic Devices",
        "Error Detection & Correction"
    ],
    "Computer Organization and Architecture": [
        "Basic Computer Organization",
        "Instruction Set Architecture (ISA)",
        "Machine Instructions",
        "Addressing Modes",
        "Assembly Language Basics",
        "ALU Design & Implementation",
        "CPU Design",
        "Control Unit Design",
        "Pipelining",
        "Branch Prediction & Speculation",
        "Performance Metrics",
        "Memory Hierarchy",
        "Cache Memory Design",
        "Cache Coherence & Memory Consistency",
        "Virtual Memory & Address Translation",
        "Page Replacement Algorithms",
        "TLB & Memory Management Unit",
        "I/O Organization",
        "Bus Architecture & Protocols",
        "Parallel Processing",
        "Multicore & Multithreading"
    ],
    "Programming and Data Structures": [
    "C Programming: Syntax, Semantics, Memory Model",
    "Data Types, Variables & Operators",
    "Control Structures: Loops, Conditionals",
    "Functions: Parameters, Return Values, Recursion",
    "Pointers: Arithmetic, Arrays, Dynamic Memory",
    "Structures, Unions & Bit Fields",
    "File I/O & Standard Library Functions",
    "Preprocessing & Compilation Process",
    "Time Complexity, Asymptotic Notation",
    "Recurrence Relations (Master Theorem)",
    "Searching Algorithms",
    "Sorting Algorithms",
    "Arrays: 1D, 2D, Multi-dimensional",
    "Strings: Manipulation, Pattern Matching",
    "Linked Lists: Singly, Doubly, Circular",
    "Stack: Implementation, Applications",
    "Queue: Linear, Circular, Priority, Deque",
    "Trees: Binary, n-ary, Expression Trees",
    "Binary Search Tree: Operations, Analysis",
    "Balanced Trees: AVL, Red-Black, Splay",
    "Heap: Min-heap, Max-heap, Heap Sort",
    "B-Trees & B+ Trees for Databases",
    "Tries: Prefix Trees, Compressed Tries",
    "Graph Representations: Adjacency Matrix/List",
    "Graph Traversals: BFS, DFS",
    "Graph Algorithms: Shortest Paths, MST",
    "Hashing",
    "Advanced Data Structures: Segment Tree, Fenwick Tree, Disjoint Set Union"
  ],
    "Algorithms": [
    "Algorithm Analysis: Time & Space Complexity",
    "Asymptotic Notations: Big-O, Omega, Theta",
    "Recurrence Relations & Master Theorem",
    "Loop Analysis & Amortized Complexity",
    "Brute Force & Exhaustive Search",
    "Backtracking",
    "Divide and Conquer: Paradigm & Applications",
    "Sorting: Comparison-based vs Non-comparison",
    "Quick Sort: Analysis, Randomization",
    "Merge Sort: Implementation, External Sorting",
    "Heap Sort & Priority Queue Applications",
    "Linear Time Sorting: Counting, Radix, Bucket",
    "Searching: Linear, Binary, Interpolation",
    "Hashing: Hash Functions, Collision Resolution",
    "Perfect Hashing & Universal Hashing",
    "Greedy Algorithms: Theory & Applications",
    "Activity Selection & Interval Scheduling",
    "Huffman Coding & Data Compression",
    "Minimum Spanning Tree: Kruskal, Prim",
    "Dynamic Programming: Principles & Techniques",
    "Optimal Substructure & Overlapping Subproblems",
    "Classic DP: Knapsack, LCS, LIS, Edit Distance",
    "Matrix Chain Multiplication & Optimal BST",
    "Graph Algorithms: DFS, BFS, Applications",
    "Topological Sorting & Strongly Connected Components",
    "Shortest Path: Dijkstra, Bellman-Ford, Floyd-Warshall",
    "Network Flow: Max Flow, Min Cut",
    "String Algorithms: KMP, Rabin-Karp, Z-algorithm",
    "Advanced Topics: NP-Completeness, Approximation, Randomized Algorithms"
  ],
"Theory of Computation": [
    "Formal Languages & Automata Theory",
    "Alphabets, Strings & Language Operations",
    "Regular Languages & Regular Expressions",
    "Finite Automata: DFA, NFA, ε-NFA",
    "Equivalence of FA & Regular Expressions",
    "Myhill-Nerode Theorem & Decision Properties",
    "Pumping Lemma for Regular Languages",
    "Closure Properties of Regular Languages",
    "Minimization of Finite Automata",
    "Context-Free Languages & Grammars",
    "Simplification of CFGs & Ambiguity",
    "Chomsky Normal Form & Greibach Normal Form",
    "Pushdown Automata: Deterministic & Non-deterministic",
    "Equivalence of CFG & PDA",
    "Pumping Lemma for Context-Free Languages",
    "Closure Properties & Decision Properties of CFLs",
    "Chomsky Hierarchy & Language Classes",
    "Turing Machines: Definition & Variants",
    "Instantaneous Descriptions & Universal TM",
    "Church-Turing Thesis & Computability",
    "Recursive & Recursively Enumerable Languages",
    "Decidable & Undecidable Problems",
    "Halting Problem, Reductions & Mapping Reductions",
    "Rice's Theorem & Applications",
    "Complexity Classes: L, NL, P, NP, PSPACE, NPSPACE",
    "Cook's Theorem & Polynomial Reductions"
],
"Compiler Design": [
    "Compiler Architecture & Phases",
    "Lexical Analysis: Tokens, Patterns, Lexemes",
    "Regular Expressions for Token Recognition",
    "Finite Automata for Lexical Analysis",
    "LEX/FLEX: Lexical Analyzer Generators",
    "Error Handling in Lexical Analysis",
    "Syntax Analysis: Grammar & Parse Trees",
    "Grammar Transformations: Left Recursion, Left Factoring",
    "Predictive Parsing: FIRST, FOLLOW, LL(1) Table",
    "Top-Down Parsing: Recursive Descent, LL(1)",
    "Bottom-Up Parsing: LR(0), SLR(1), LALR(1), Canonical LR(1)",
    "YACC/BISON: Parser Generators",
    "Error Recovery in Parsing",
    "Ambiguity and Resolving Techniques",
    "Semantic Analysis: Type Checking, Scope",
    "Symbol Table: Organization & Management",
    "Syntax-Directed Translation & SDTs",
    "Syntax-Directed Translation Schemes",
    "Intermediate Code Generation: 3-Address Code",
    "Backpatching for Boolean Expressions",
    "Control Flow: Basic Blocks, Flow Graphs, DAG Construction",
    "Code Optimization: Local, Global, Peephole",
    "Data Flow Analysis: Live Variables, Reaching Definitions, Available Expressions",
    "Loop Optimization: Invariant Code Motion, Loop Unrolling, Induction Variable Elimination",
    "Register Allocation & Assignment",
    "Code Generation: Target Code, Instruction Selection, Target Machine Architecture",
    "Runtime Environment: Activation Records, Parameter Passing, Storage Classes, Garbage Collection"
],
    "Operating System": [
    "Introduction & OS Basics",
    "OS Structure: Monolithic, Microkernel, Layered",
    "System Calls & API Interface",
    "Processes & Threads",
    "Process States & PCB",
    "Process Creation: fork(), exec(), wait()",
    "Inter-Process Communication: Pipes, Message Queues, Shared Memory, Sockets",
    "Threads: User-level vs Kernel-level",
    "Multithreading Models & Thread Libraries",
    "CPU Scheduling: Preemptive vs Non-preemptive",
    "Scheduling Algorithms: FCFS, SJF, RR, Priority",
    "Multilevel Queue & Feedback Scheduling",
    "Performance Metrics in Scheduling",
    "Process Synchronization: Critical Section Problem",
    "Mutual Exclusion: Peterson's Algorithm, Hardware Support",
    "Semaphores: Binary, Counting, Implementation",
    "Monitors & Condition Variables",
    "Classical Synchronization Problems",
    "Deadlock: Necessary Conditions, Prevention, Avoidance",
    "Banker's Algorithm & Deadlock Detection",
    "Memory Management Overview",
    "Memory Allocation: Fixed, Variable Partitioning",
    "Swapping & Fragmentation: Internal, External",
    "Paging: Page Tables, TLB, Multi-level Paging",
    "Segmentation: Segment Tables, Segmentation with Paging",
    "Virtual Memory: Demand Paging, Page Faults",
    "Page Replacement: FIFO, LRU, Optimal, Clock",
    "Thrashing & Working Set Model",
    "File System: Directory Structure, File Allocation",
    "File System Implementation: Free Space Management, Inodes, Journaling",
    "Disk Management: Partitioning, Formatting",
    "Disk Scheduling: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK",
    "RAID Levels & Disk Reliability",
    "I/O Systems: I/O Hardware, Controllers, Polling, Interrupts, DMA",
    "Security & Protection: Access Matrix, ACLs, Capabilities"
  ],
    "Databases": [
  "Database Concepts: DBMS vs File System",
  "Data Models: Hierarchical, Network, Relational",
  "Entity-Relationship Model: Entities, Attributes, Relationships",
  "ER Diagram: Strong/Weak Entities, ISA Hierarchy",
  "Relational Model: Tables, Tuples, Domains",
  "Keys: Super, Candidate, Primary, Foreign",
  "Integrity Constraints: Entity, Referential, Domain",
  "Relational Algebra: Selection, Projection, Join",
  "Relational Calculus: Tuple & Domain Calculus",
  "SQL Fundamentals: DDL, DML, DCL, TCL",
  "Join Operations: Inner, Outer, Semi, Anti",
  "Aggregate Functions & Group By",
  "Window Functions & Common Table Expressions",
  "Advanced SQL: Subqueries, Views, Stored Procedures",
  "Functional Dependencies & Armstrong's Axioms",
  "Normalization: 1NF, 2NF, 3NF, BCNF",
  "Multivalued Dependencies & 4NF",
  "Join Dependencies & 5NF",
  "File Organization: Heap, Sorted, Hashing, ISAM",
  "Indexing: Primary, Secondary, Clustered",
  "B-Trees & B+ Trees for Database Indexing",
  "Hash-based Indexing & Bitmap Indexes",
  "Query Processing: Parsing, Optimization, Execution",
  "Join Algorithms: Nested Loop, Sort-Merge, Hash",
  "Transaction Management: ACID Properties",
  "Concurrency Control: Lock-based, Timestamp-based",
  "Deadlock Detection & Resolution",
  "Recovery: Log-based, Shadow Paging, Checkpoints",
  "Database Security & Authorization",
  "Distributed Databases (Optional)",
  "NoSQL Databases (Optional)"
],
    "Computer Networks": [
    "Network Fundamentals: Protocols, Standards",
    "Network Models: OSI 7-layer, TCP/IP 5-layer",
    "Physical Layer: Transmission Media, Signals",
    "Transmission Impairments & Capacity",
    "Bandwidth, Throughput & Latency",
    "Encoding: NRZ, Manchester, Differential Manchester",
    "Multiplexing: FDM, TDM, WDM",
    "Data Link Layer: Framing, Error Detection",
    "Error Correction: Hamming Code, CRC",
    "Flow Control: Stop-and-Wait, Sliding Window",
    "ARQ Protocols: Stop-and-Wait, Go-Back-N, Selective Repeat",
    "Framing Techniques: Bit Stuffing, Byte Stuffing",
    "HDLC, PPP Protocols",
    "Medium Access Control: ALOHA, CSMA/CD, CSMA/CA",
    "Token Ring, Exposed Terminal Problem",
    "Ethernet: Frame Format, Collision Detection",
    "Wireless LANs: IEEE 802.11, Hidden Terminal Problem",
    "Network Layer: Routing, Forwarding",
    "IPv4: Address Classes, Subnetting, CIDR",
    "IPv6: Address Format, Transition Mechanisms",
    "Fragmentation in IP",
    "Datagram vs Virtual Circuit Switching",
    "Routing Algorithms: Distance Vector, Link State",
    "Internet Routing: RIP, OSPF, BGP",
    "Network Address Translation (NAT)",
    "Internet Control Message Protocol (ICMP)",
    "Transport Layer: Connection vs Connectionless",
    "UDP: Header Format, Applications",
    "TCP: Reliable Data Transfer, Flow Control",
    "TCP Congestion Control: Slow Start, Congestion Avoidance",
    "TCP Timers and Segment Details",
    "Ports and Multiplexing/Demultiplexing",
    "Performance Metrics & Queuing Theory",
    "Application Layer Protocols: HTTP, HTTPS, FTP",
    "DNS: Hierarchy, Resolution Process",
    "Email Protocols: SMTP, POP3, IMAP",
    "TELNET, DHCP, SNTP",
    "Network Security: Cryptography, Digital Signatures, SSL/TLS",
    "Network Management: SNMP, Network Monitoring"
  ],
    "Software Engineering": [
        "Software Development Life Cycle (SDLC)", "Software Process Models: Waterfall, Iterative, Agile", 
        "Requirements Engineering: Elicitation, Analysis, Specification", "System Modeling: Use Cases, Class Diagrams",
        "Software Design: Architectural, Detailed Design", "Design Patterns: Creational, Structural, Behavioral",
        "Software Testing: Unit, Integration, System Testing", "Testing Techniques: Black-box, White-box, Gray-box",
        "Test Case Design & Test Coverage", "Software Metrics & Quality Assurance",
        "Configuration Management & Version Control", "Software Project Management: Planning, Estimation",
        "Risk Management & Software Maintenance"
    ],
    "Web Technologies": [
        "Web Fundamentals: Client-Server Architecture", "HTML5: Semantic Elements, Forms, Multimedia", 
        "CSS3: Selectors, Layout, Responsive Design", "JavaScript: ES6+, DOM Manipulation, Events",
        "Frontend Frameworks: React, Angular, Vue.js", "Backend Technologies: Node.js, Express.js",
        "Database Integration: SQL, NoSQL Databases", "RESTful APIs & Web Services",
        "Web Security: XSS, CSRF, SQL Injection", "Performance Optimization & Caching"
    ]
}

# Detailed concept mastery for each topic
concept_mastery = {
    "Set Theory & Relations": [
    "Set operations: Union, Intersection, Complement",
    "Cartesian product and relations",
    "Types of relations: Reflexive, Symmetric, Transitive",
    "Equivalence relations and partitions",
    "Functions: Injective, Surjective, Bijective",
    "Composition of functions and inverse functions"
  ],

  "Mathematical Logic: Propositional & First-Order": [
    "Propositional logic: AND, OR, NOT, IMPLIES",
    "Truth tables and logical equivalences",
    "Normal forms: CNF and DNF",
    "First-order logic: Quantifiers, Predicates",
    "Inference rules and proof techniques",
    "Soundness and completeness"
  ],

  "Algebraic Structures: Groups, Rings, Fields": [
    "Definition of groups, rings, fields",
    "Subgroups, cyclic groups",
    "Cosets and Lagrange’s theorem",
    "Homomorphisms and isomorphisms",
    "Applications in cryptography"
  ],

  "Partial Orders & Lattices": [
    "Posets and Hasse diagrams",
    "Maximal, minimal, greatest, least elements",
    "Lattices and their properties",
    "Modular and distributive lattices"
  ],

  "Boolean Algebra": [
    "Boolean expressions",
    "Canonical forms: SOP, POS",
    "Boolean identities and simplification",
    "Karnaugh maps (K-maps)"
  ],

  "Combinatorics & Counting": [
    "Permutation and combination",
    "Binomial theorem",
    "Principle of inclusion-exclusion",
    "Pigeonhole principle"
  ],

  "Number Theory & Discrete Structures": [
    "Divisibility and prime numbers",
    "Euclidean algorithm",
    "Congruences and modular arithmetic",
    "Chinese remainder theorem"
  ],

  "Recurrence Relations & Generating Functions": [
    "Formulating recurrence relations",
    "Solving linear recurrence relations",
    "Homogeneous and non-homogeneous recurrences",
    "Generating functions and applications"
  ],

  "Graph Theory: Connectivity, Planarity, Matching, Coloring, Trees": [
    "Basic graph definitions and types",
    "Graph representations: adjacency matrix/list",
    "Connectivity and components",
    "Euler and Hamiltonian circuits",
    "Graph coloring and chromatic number",
    "Planar graphs and Euler’s formula",
    "Trees and spanning trees",
    "Counting spanning trees (Cayley’s theorem)",
    "Matching and bipartite graphs"
  ],

  "Linear Algebra: Vector Spaces, Matrices, Determinants": [
    "Matrix operations",
    "Determinants and properties",
    "Rank and nullity",
    "Systems of linear equations"
  ],

  "Linear Transformations & Rank": [
    "Linear maps and matrices",
    "Kernel and image of a transformation",
    "Change of basis",
    "Matrix representation of linear transformations"
  ],

  "LU & QR Decomposition": [
    "LU decomposition method",
    "Solving systems via LU",
    "QR decomposition method"
  ],

  "Eigenvalues, Eigenvectors & Diagonalization": [
    "Eigenvalues and eigenvectors",
    "Characteristic equation",
    "Diagonalization of matrices",
    "Applications in graph theory"
  ],

  "Calculus: Limits, Continuity, Differentiability": [
    "Limit of functions",
    "Continuity of functions",
    "Differentiability and rules of differentiation",
    "Partial derivatives"
  ],

  "Optimization: Maxima-Minima, Lagrange Multipliers": [
    "Finding extrema",
    "Lagrange multipliers for constrained optimization"
  ],

  "Integration: Definite, Indefinite, Multiple Integrals": [
    "Integration techniques",
    "Definite and indefinite integrals",
    "Double and triple integrals"
  ],

  "Mean Value Theorem": [
    "Rolle’s theorem",
    "Lagrange’s mean value theorem",
    "Cauchy’s mean value theorem"
  ],

  "Line, Surface, Volume Integrals": [
    "Line integrals",
    "Surface integrals",
    "Volume integrals",
    "Green’s, Stokes’, Divergence theorems"
  ],

  "Differential Equations: ODE, PDE": [
    "First-order ODEs",
    "Higher-order ODEs",
    "Homogeneous and non-homogeneous equations",
    "Separation of variables",
    "Introduction to PDEs"
  ],

  "Numerical Methods": [
    "Bisection method",
    "Newton-Raphson method",
    "Gauss-Jordan and Gauss-Seidel methods",
    "LU decomposition",
    "Trapezoidal and Simpson’s rule",
    "Numerical differentiation",
    "Euler’s and Runge-Kutta methods for ODEs"
  ],

  "Probability Theory: Sample Space, Events, Conditional Probability": [
    "Sample space and events",
    "Classical and axiomatic probability",
    "Conditional probability and independence",
    "Bayes theorem"
  ],

  "Random Variables & Probability Distributions": [
    "Discrete and continuous random variables",
    "Probability mass and density functions",
    "Expectation and variance",
    "Binomial, Poisson, Normal distributions"
  ],

  "Bayes Theorem & Applications": [
    "Bayesian inference",
    "Applications in machine learning"
  ],

  "Statistics: Descriptive & Inferential": [
    "Mean, median, mode",
    "Standard deviation and variance",
    "Histograms and frequency distributions"
  ],

  "Hypothesis Testing & Confidence Intervals": [
    "Types of errors",
    "Z-test, t-test, chi-square test",
    "Confidence intervals"
  ],

  "Moments, Skewness, Kurtosis": [
    "Central and raw moments",
    "Skewness",
    "Kurtosis"
  ],

  "Correlation, Regression & Time Series": [
    "Correlation coefficient",
    "Simple linear regression",
    "Multiple regression basics",
    "Time series analysis and forecasting"
  ],
    "Basic Computer Organization": [
        "Functional Units of a Computer",
        "Instruction Cycle & Micro-operations",
        "Types of Instructions"
    ],
    "Instruction Set Architecture (ISA)": [
        "RISC vs. CISC",
        "Instruction Types"
    ],
    "Machine Instructions": [
        "Instruction Formats (0, 1, 2, 3-address)",
        "Instruction Encoding"
    ],
    "Addressing Modes": [
        "Immediate Addressing",
        "Direct Addressing",
        "Indirect Addressing",
        "Indexed Addressing",
        "Register Addressing",
        "Relative Addressing"
    ],
    "Assembly Language Basics": [
        "Simple Assembly Programs",
        "Stack vs. Accumulator vs. Register Architectures"
    ],
    "ALU Design & Implementation": [
        "Binary Adders & Subtractors",
        "Multiplication Algorithms (Booth's, Bit-pair recoding)",
        "Division Algorithms (Restoring, Non-restoring)",
        "Floating Point Formats (IEEE-754)",
        "Floating Point Arithmetic Operations"
    ],
    "CPU Design": [
        "Single-cycle CPU",
        "Multi-cycle CPU",
        "Datapath Components",
        "Control Signals"
    ],
    "Control Unit Design": [
        "Hardwired Control",
        "Microprogrammed Control",
        "Control Word & Control Memory"
    ],
    "Pipelining": [
        "5-stage Pipeline",
        "Pipeline Hazards (Structural, Data, Control)",
        "Hazard Handling (Forwarding, Stalling, Prediction)",
        "Pipeline Performance Metrics"
    ],
    "Branch Prediction & Speculation": [
        "Static Prediction",
        "Dynamic Prediction",
        "Branch Target Buffer"
    ],
    "Performance Metrics": [
        "CPI, MIPS, MFLOPS",
        "Speedup & Amdahl's Law",
        "Throughput vs. Latency"
    ],
    "Memory Hierarchy": [
        "Characteristics of Memory Levels",
        "Locality of Reference"
    ],
    "Cache Memory Design": [
        "Direct Mapped Cache",
        "Fully Associative Cache",
        "Set-Associative Cache",
        "Cache Performance Metrics (Hit, Miss, Miss Penalty)",
        "Replacement Policies (LRU, FIFO, Random)"
    ],
    "Cache Coherence & Memory Consistency": [
        "MESI, MOESI Protocols",
        "Memory Consistency Models"
    ],
    "Virtual Memory & Address Translation": [
        "Paging",
        "Segmentation",
        "Page Table Structures",
        "Address Translation Process"
    ],
    "Page Replacement Algorithms": [
        "FIFO",
        "LRU",
        "Optimal"
    ],
    "TLB & Memory Management Unit": [
        "Translation Lookaside Buffer (TLB)",
        "Role of MMU"
    ],
    "I/O Organization": [
        "Programmed I/O",
        "Interrupt-driven I/O",
        "Direct Memory Access (DMA)",
        "Interrupt Priority Schemes"
    ],
    "Bus Architecture & Protocols": [
        "Bus Types",
        "Bus Arbitration",
        "Examples: PCI, PCIe, USB"
    ],
    "Parallel Processing": [
        "Flynn’s Taxonomy",
        "SIMD vs MIMD",
        "Shared vs Distributed Memory"
    ],
    "Multicore & Multithreading": [
        "Benefits of Multicore",
        "Thread-level Parallelism",
        "Cache Sharing in Multicore"
    ],
     "Number Systems: Binary, Octal, Hexadecimal": [
        "Conversions between number systems",
        "Weighted and non-weighted codes",
        "Binary arithmetic operations",
        "Gray code and conversions"
    ],
    "Signed Number Representation: 2's Complement": [
        "Sign-magnitude representation",
        "1's complement representation",
        "2's complement representation",
        "Range and overflow detection"
    ],
    "Fixed-Point & Floating-Point Arithmetic": [
        "Fixed-point representation basics",
        "Fixed-point addition and subtraction",
        "Floating-point representation principles",
        "Normalization and rounding",
        "Floating-point arithmetic operations",
        "Precision and error considerations"
    ],
    "IEEE 754 Standard": [
        "IEEE 754 single precision format",
        "IEEE 754 double precision format",
        "Special cases: zero, infinity, NaN",
        "Bias and exponent concepts"
    ],
    "Boolean Algebra & De Morgan's Laws": [
        "Basic Boolean operations and laws",
        "De Morgan's theorems and applications",
        "Boolean function simplification",
        "Duality principle in Boolean algebra",
        "Boolean expressions from truth tables",
        "Canonical forms: SOP and POS"
    ],
    "Logic Gates: Universal, Multi-level": [
        "Basic gates: AND, OR, NOT, XOR",
        "Universal gates: NAND, NOR",
        "Multi-level gate networks",
        "Fan-in and fan-out considerations",
        "Gate delays and timing analysis",
        "Technology mapping and gate libraries"
    ],
    "Logic Minimization: K-Map, Quine-McCluskey": [
        "K-map simplification (2,3,4,5 variables)",
        "Grouping of minterms and maxterms",
        "Don’t care conditions",
        "Quine–McCluskey tabular method",
        "Prime implicants and essential prime implicants"
    ],
    "Multi-level Logic Optimization": [
        "Multi-level circuit synthesis",
        "Reduction using algebraic methods",
        "Shared terms across logic levels",
        "Cost and delay considerations"
    ],
    "Combinational Logic Design": [
        "Analysis of combinational circuits",
        "Design from specifications",
        "Truth table to Boolean equation",
        "Implementation using gates",
        "Design using universal gates"
    ],
    "Multiplexers, Demultiplexers, Encoders, Decoders": [
        "4x1, 8x1 multiplexers",
        "Cascading multiplexers",
        "Demultiplexers basics",
        "Priority encoders",
        "Decoders and applications",
        "Implementing functions with multiplexers/decoders"
    ],
    "Adders, Subtractors & Arithmetic Circuits": [
        "Half adder, full adder",
        "Ripple carry adder",
        "Carry look-ahead adder",
        "Half subtractor, full subtractor",
        "Adder-subtractor circuit design",
        "BCD adder basics"
    ],
    "Comparators & Code Converters": [
        "1-bit and multi-bit comparators",
        "Design using gates or ICs",
        "Binary-to-Gray and Gray-to-Binary conversions",
        "BCD to excess-3 code conversion",
        "Other common code converters"
    ],
    "Sequential Logic: Latches & Flip-Flops": [
        "SR latch",
        "JK flip-flop",
        "T flip-flop",
        "D flip-flop",
        "Master-slave flip-flop",
        "Setup and hold time concepts"
    ],
    "Registers: Shift, Storage, Counter": [
        "Shift registers: serial-in serial-out, parallel-in parallel-out",
        "Bidirectional shift registers",
        "Storage registers basics",
        "Asynchronous counters",
        "Synchronous counters",
        "Ring counter and Johnson counter",
        "Mod-n counters"
    ],
    "State Machines: Moore & Mealy Models": [
        "State diagram and state table",
        "Moore vs Mealy difference",
        "State reduction techniques",
        "Design examples"
    ],
    "Timing Analysis & Race Conditions": [
        "Setup time and hold time",
        "Propagation delay",
        "Race around condition",
        "Critical race and elimination"
    ],
    "Hazards in Combinational Circuits": [
        "Static 1 hazard",
        "Static 0 hazard",
        "Dynamic hazards",
        "Elimination of hazards"
    ],
    "Memory & Programmable Logic Devices": [
        "ROM, PROM, EPROM basics",
        "Programmable Logic Arrays (PLA)",
        "Programmable Array Logic (PAL)",
        "FPGA basics and architecture"
    ],
    "Error Detection & Correction": [
        "Parity bits (even, odd)",
        "Hamming codes",
        "Single-bit and burst error detection",
        "Error correction capability",
        "Cyclic Redundancy Check (CRC)"
    ],
    "Machine Instructions & Assembly Language": [
        "Instruction format and encoding",
        "Opcode and operand fields",
        "Assembly language syntax",
        "Assembler directives and pseudo-instructions",
        "Symbol table and address resolution",
        "Macro definitions and expansions"
    ],
    "CPU Design: Single-cycle vs Multi-cycle": [
        "Single-cycle datapath design",
        "Multi-cycle implementation benefits",
        "Control signal generation",
        "Critical path analysis",
        "Performance comparison",
        "Pipeline introduction concepts"
    ],
"C Programming: Syntax, Semantics, Memory Model": [
    "Variable declarations and scope rules",
    "Memory layout: Stack, Heap, Data, Code",
    "Automatic vs static storage classes",
    "Pointer arithmetic and dereferencing",
    "Dynamic memory allocation: malloc, free",
    "Memory leaks and dangling pointers"
  ],

  "Time Complexity, Asymptotic Notation": [
    "Big O, Big Ω, Big Θ",
    "Little o, little ω",
    "Best, average, worst-case analysis",
    "Analyzing loops and nested loops"
  ],

  "Recurrence Relations (Master Theorem)": [
    "Writing recurrence for recursive algorithms",
    "Solving recurrences by Master Theorem",
    "Different cases of Master Theorem"
  ],

  "Searching Algorithms": [
    "Linear Search",
    "Binary Search: iterative and recursive",
    "Time complexity analysis"
  ],

  "Sorting Algorithms": [
    "Bubble Sort",
    "Insertion Sort",
    "Selection Sort",
    "Merge Sort",
    "Quick Sort",
    "Heap Sort",
    "Counting Sort",
    "Radix Sort",
    "Comparison of sorting algorithms"
  ],

  "Strings: Manipulation, Pattern Matching": [
    "String storage and character arrays",
    "Common string library functions",
    "Naive pattern matching",
    "Knuth-Morris-Pratt (KMP) Algorithm",
    "Rabin-Karp Algorithm"
  ],

  "Graph Traversals: BFS, DFS": [
    "Breadth-First Search",
    "Depth-First Search",
    "Applications: cycle detection, connectivity"
  ],

  "Graph Algorithms: Shortest Paths, MST": [
    "Dijkstra’s Algorithm",
    "Bellman-Ford Algorithm",
    "Prim’s Algorithm",
    "Kruskal’s Algorithm"
  ],

  "Hashing": [
    "Design of hash functions",
    "Collision resolution using chaining",
    "Open addressing techniques",
    "Linear probing, quadratic probing, double hashing"
  ],
    "Algorithm Analysis: Time & Space Complexity": [
    "Best, average, worst-case analysis",
    "Big-O, Omega, Theta notations",
    "Little-o, little-omega notations",
    "Space complexity analysis",
    "Recursive algorithm analysis",
    "Amortized complexity concepts",
    "Comparison of algorithm complexities",
    "Lower and upper bounds"
  ],
  "Asymptotic Notations: Big-O, Omega, Theta": [
    "Definition of Big-O, Omega, Theta",
    "Graphical interpretation",
    "Usage in proofs",
    "Complexity classes P, NP, NP-Complete"
  ],
  "Recurrence Relations & Master Theorem": [
    "Substitution method",
    "Recursion tree method",
    "Master theorem and cases",
    "Iteration method"
  ],
  "Loop Analysis & Amortized Complexity": [
    "Nested loop analysis",
    "Telescoping series",
    "Aggregate method",
    "Accounting method",
    "Potential method"
  ],
  "Brute Force & Exhaustive Search": [
    "Basic idea and time complexity",
    "When to use brute force",
    "Examples in searching and pattern matching"
  ],
  "Backtracking": [
    "N-Queens Problem",
    "Subset Sum Problem",
    "Graph Coloring",
    "Hamiltonian Cycle",
    "Sudoku Solver"
  ],
  "Divide and Conquer: Paradigm & Applications": [
    "Merge Sort analysis",
    "Quick Sort analysis",
    "Binary Search",
    "Matrix Multiplication (Strassen's)",
    "Count Inversions"
  ],
  "Sorting: Comparison-based vs Non-comparison": [
    "Stability of sorting",
    "In-place vs non-in-place sorting",
    "Lower bound of comparison sorting",
    "Examples of each category"
  ],
  "Quick Sort: Analysis, Randomization": [
    "Worst-case, average-case analysis",
    "Randomized pivot selection",
    "Tail recursion optimization"
  ],
  "Merge Sort: Implementation, External Sorting": [
    "Standard Merge Sort",
    "External sorting strategies",
    "Space complexity considerations"
  ],
  "Heap Sort & Priority Queue Applications": [
    "Binary heap operations",
    "Heapify process",
    "Insert, extract-min complexities",
    "Applications in scheduling"
  ],
  "Linear Time Sorting: Counting, Radix, Bucket": [
    "Stable vs unstable",
    "Suitable input constraints",
    "Implementation details"
  ],
  "Searching: Linear, Binary, Interpolation": [
    "Linear search basics",
    "Binary search proofs",
    "Interpolation search analysis"
  ],
  "Hashing: Hash Functions, Collision Resolution": [
    "Load factor and performance",
    "Open addressing",
    "Separate chaining",
    "Double hashing"
  ],
  "Perfect Hashing & Universal Hashing": [
    "Definition and motivation",
    "Construction methods",
    "Space-time trade-offs"
  ],
  "Greedy Algorithms: Theory & Applications": [
    "Greedy-choice property",
    "Matroids (basic idea)",
    "Proofs of correctness"
  ],
  "Activity Selection & Interval Scheduling": [
    "Earliest finish time strategy",
    "Interval graphs"
  ],
  "Huffman Coding & Data Compression": [
    "Huffman tree construction",
    "Optimality proof",
    "Applications in compression"
  ],
  "Minimum Spanning Tree: Kruskal, Prim": [
    "Kruskal’s algorithm details",
    "Prim’s algorithm details",
    "Union-Find for Kruskal",
    "Cycle detection"
  ],
  "Dynamic Programming: Principles & Techniques": [
    "Memoization vs tabulation",
    "Subproblem graph representation",
    "Time and space analysis"
  ],
  "Optimal Substructure & Overlapping Subproblems": [
    "Definition and examples",
    "Identifying substructure"
  ],
  "Classic DP: Knapsack, LCS, LIS, Edit Distance": [
    "0/1 Knapsack",
    "Unbounded Knapsack",
    "LCS table filling",
    "Edit Distance cost calculation"
  ],
  "Matrix Chain Multiplication & Optimal BST": [
    "DP formulation",
    "Cost matrix computation"
  ],
  "Graph Algorithms: DFS, BFS, Applications": [
    "Graph representation",
    "Connected components",
    "Bipartite checking",
    "Bridges and articulation points"
  ],
  "Topological Sorting & Strongly Connected Components": [
    "Topological sort algorithms",
    "Kosaraju’s algorithm",
    "Tarjan’s algorithm"
  ],
  "Shortest Path: Dijkstra, Bellman-Ford, Floyd-Warshall": [
    "Handling negative weights",
    "Negative cycle detection",
    "Johnson’s algorithm overview"
  ],
  "Network Flow: Max Flow, Min Cut": [
    "Ford-Fulkerson method",
    "Edmonds-Karp algorithm",
    "Residual graph concept",
    "Applications (Bipartite Matching)"
  ],
  "String Algorithms: KMP, Rabin-Karp, Z-algorithm": [
    "Prefix function in KMP",
    "Hashing in Rabin-Karp",
    "Applications of Z-algorithm",
    "Trie data structures",
    "Suffix arrays and suffix trees"
  ],
  "Advanced Topics: NP-Completeness, Approximation, Randomized Algorithms": [
    "NP, NP-Complete, NP-Hard definitions",
    "Reductions among problems",
    "Approximation algorithms for Vertex Cover, etc.",
    "Monte Carlo vs Las Vegas algorithms",
    "Randomized Quick Sort",
    "Randomized hashing"
  ],
    "Formal Languages & Automata Theory": [
    "Alphabet, strings, and languages",
    "Operations on languages (Union, Concatenation, Kleene star, etc.)",
    "Finite automata design principles",
    "Regular language properties",
    "Decision properties of regular languages (Emptiness, Finiteness, Equivalence, Membership)",
    "Context-free language hierarchy",
    "Chomsky hierarchy of languages"
],

"Alphabets, Strings & Language Operations": [
    "Definitions: Alphabet, String, Language",
    "Operations on languages",
    "Properties of language operations"
],

"Regular Languages & Regular Expressions": [
    "Definition and examples",
    "Regular expressions syntax",
    "FA construction from RE",
    "RE construction from FA"
],

"Finite Automata: DFA, NFA, ε-NFA": [
    "Definitions of DFA, NFA, ε-NFA",
    "Conversion NFA → DFA",
    "ε-closure concept",
    "Design examples"
],

"Equivalence of FA & Regular Expressions": [
    "State elimination method",
    "Arden’s theorem"
],

"Myhill-Nerode Theorem & Decision Properties": [
    "Statement and proof of Myhill-Nerode",
    "Minimization based on equivalence classes",
    "Decision properties (emptiness, membership, equivalence, etc.)"
],

"Pumping Lemma for Regular Languages": [
    "Statement of pumping lemma",
    "Applications to prove non-regularity"
],

"Closure Properties of Regular Languages": [
    "Union, Intersection, Complementation, etc.",
    "Closure proofs"
],

"Minimization of Finite Automata": [
    "Partitioning method",
    "Equivalent states"
],

"Context-Free Languages & Grammars": [
    "Definitions and examples",
    "Derivations: leftmost, rightmost",
    "Parse trees"
],

"Simplification of CFGs & Ambiguity": [
    "Removing ε-productions",
    "Removing unit productions",
    "Removing useless symbols",
    "Ambiguity and inherently ambiguous languages"
],

"Chomsky Normal Form & Greibach Normal Form": [
    "Conversions of CFGs",
    "Usage in parsing algorithms"
],

"Pushdown Automata: Deterministic & Non-deterministic": [
    "Definition of PDA",
    "Acceptance by final state / empty stack",
    "Design examples",
    "DPDA vs NPDA"
],

"Equivalence of CFG & PDA": [
    "Proof of equivalence",
    "Conversions both ways"
],

"Pumping Lemma for Context-Free Languages": [
    "Statement and usage",
    "Examples of non-CFLs"
],

"Closure Properties & Decision Properties of CFLs": [
    "Closure under Union, Concatenation, etc.",
    "Decision problems (emptiness, finiteness, membership)"
],

"Chomsky Hierarchy & Language Classes": [
    "Hierarchy of languages",
    "Relation between classes",
    "Recognizers for each class"
],

"Turing Machines: Definition & Variants": [
    "Single tape TM definition",
    "Variants: multi-tape, multi-track, nondeterministic"
],

"Instantaneous Descriptions & Universal TM": [
    "Instantaneous description notation",
    "Universal TM concept"
],

"Church-Turing Thesis & Computability": [
    "Statement of the thesis",
    "Computable functions"
],

"Recursive & Recursively Enumerable Languages": [
    "Definitions",
    "Differences with examples"
],

"Decidable & Undecidable Problems": [
    "Definitions",
    "Examples of undecidable problems"
],

"Halting Problem, Reductions & Mapping Reductions": [
    "Halting problem proof",
    "Mapping reductions",
    "Examples of reductions"
],

"Rice's Theorem & Applications": [
    "Statement of Rice’s theorem",
    "Applications to undecidability proofs"
],

"Complexity Classes: L, NL, P, NP, PSPACE, NPSPACE": [
    "Definitions of complexity classes",
    "Hierarchy relations",
    "Examples"
],

"Cook's Theorem & Polynomial Reductions": [
    "Cook-Levin theorem",
    "NP-Complete definitions",
    "Reduction techniques"
],
    "Compiler Architecture & Phases": [
      "Lexical analysis phase",
      "Syntax analysis phase",
      "Semantic analysis phase",
      "Intermediate code generation",
      "Code optimization phase",
      "Code generation phase"
    ],
    "Lexical Analysis: Tokens, Patterns, Lexemes": [
      "Tokens, patterns, lexemes definitions",
      "Lexical errors",
      "Role of lexical analyzer"
    ],
    "Regular Expressions for Token Recognition": [
      "Regular expression syntax",
      "Operations on regular expressions",
      "Conversion from regular expressions to NFA"
    ],
    "Finite Automata for Lexical Analysis": [
      "NFA and DFA definitions",
      "Subset construction (NFA to DFA)",
      "Minimization of DFA"
    ],
    "LEX/FLEX: Lexical Analyzer Generators": [
      "LEX rules and actions",
      "Regular expressions in LEX",
      "Integration with parser generators"
    ],
    "Error Handling in Lexical Analysis": [
      "Panic mode recovery",
      "Error correction techniques"
    ],
    "Syntax Analysis: Grammar & Parse Trees": [
      "Context-Free Grammar (CFG)",
      "Derivations and parse trees",
      "Ambiguity in grammars"
    ],
    "Grammar Transformations: Left Recursion, Left Factoring": [
      "Elimination of left recursion",
      "Left factoring technique",
      "Impact on parser construction"
    ],
    "Predictive Parsing: FIRST, FOLLOW, LL(1) Table": [
      "Computation of FIRST sets",
      "Computation of FOLLOW sets",
      "Construction of LL(1) parsing table",
      "Conditions for LL(1) grammar"
    ],
    "Top-Down Parsing: Recursive Descent, LL(1)": [
      "Recursive descent parsing method",
      "Predictive parsing without backtracking"
    ],
    "Bottom-Up Parsing: LR(0), SLR(1), LALR(1), Canonical LR(1)": [
      "LR(0) items and closures",
      "SLR parsing table construction",
      "LALR(1) merging lookaheads",
      "Canonical LR(1) parsing table",
      "Shift-reduce and reduce-reduce conflicts"
    ],
    "YACC/BISON: Parser Generators": [
      "YACC grammar rules",
      "Defining actions",
      "Error handling in YACC",
      "Integration with Lex/Flex"
    ],
    "Error Recovery in Parsing": [
      "Panic mode recovery",
      "Phrase-level recovery",
      "Error productions"
    ],
    "Ambiguity and Resolving Techniques": [
      "Examples of ambiguous grammars",
      "Operator precedence rules",
      "Associativity rules",
      "Grammar rewriting for disambiguation"
    ],
    "Semantic Analysis: Type Checking, Scope": [
      "Type systems and type checking",
      "Type compatibility and coercion",
      "Scope resolution (static and dynamic)"
    ],
    "Symbol Table: Organization & Management": [
      "Symbol table operations",
      "Hashing techniques",
      "Handling nested scopes",
      "Storage of attributes"
    ],
    "Syntax-Directed Translation & SDTs": [
      "Syntax-directed definitions (SDD)",
      "Synthesized and inherited attributes",
      "Dependency graphs"
    ],
    "Syntax-Directed Translation Schemes": [
      "SDT vs translation schemes",
      "Embedded actions in grammar rules",
      "Evaluation orders"
    ],
    "Intermediate Code Generation: 3-Address Code": [
      "Three-address instructions",
      "Quadruples, triples, indirect triples",
      "Translation of arithmetic expressions"
    ],
    "Backpatching for Boolean Expressions": [
      "Backpatching algorithm",
      "Generating code for if-else and loops",
      "Handling relational operators"
    ],
    "Control Flow: Basic Blocks, Flow Graphs, DAG Construction": [
      "Identifying basic blocks",
      "Constructing flow graphs",
      "DAG representation for basic blocks"
    ],
    "Code Optimization: Local, Global, Peephole": [
      "Common subexpression elimination",
      "Constant folding and propagation",
      "Dead code elimination",
      "Strength reduction",
      "Peephole optimizations"
    ],
    "Data Flow Analysis: Live Variables, Reaching Definitions, Available Expressions": [
      "Formulating data flow equations",
      "Iterative solutions",
      "Applications in optimization"
    ],
    "Loop Optimization: Invariant Code Motion, Loop Unrolling, Induction Variable Elimination": [
      "Loop invariant code motion",
      "Loop unrolling techniques",
      "Elimination of induction variables"
    ],
    "Register Allocation & Assignment": [
      "Graph coloring approach",
      "Spilling registers",
      "Cost considerations in allocation"
    ],
    "Code Generation: Target Code, Instruction Selection, Target Machine Architecture": [
      "Issues in code generation",
      "Instruction selection strategies",
      "Target machine architecture considerations",
      "Instruction scheduling"
    ],
    "Runtime Environment: Activation Records, Parameter Passing, Storage Classes, Garbage Collection": [
      "Activation record layout",
      "Parameter passing techniques",
      "Storage classes and memory layout",
      "Basics of garbage collection"
    ],
    "OS Structure: Monolithic, Microkernel, Layered": [
    "Monolithic kernel architecture",
    "Microkernel design principles",
    "Layered operating system approach",
    "Hybrid kernel systems",
    "Performance trade-offs",
    "Security implications of each structure"
  ],

  "System Calls & API Interface": [
    "Definition and purpose of system calls",
    "User mode vs kernel mode",
    "Examples of system calls (UNIX, Linux, Windows)",
    "Library wrappers around system calls",
    "Cost of system calls"
  ],

  "Processes & Threads": [
    "Definition of process",
    "PCB (Process Control Block)",
    "Process states and transitions",
    "Context switching",
    "Lightweight vs heavyweight processes",
    "Thread definition and advantages",
    "Concurrency vs parallelism"
  ],

  "Process Creation: fork(), exec(), wait()": [
    "fork() mechanism and child processes",
    "exec() family of functions",
    "wait() and waitpid() functions",
    "Orphan and zombie processes",
    "Process termination"
  ],

  "Inter-Process Communication: Pipes, Message Queues, Shared Memory, Sockets": [
    "Pipes: unnamed and named",
    "Message queues",
    "Shared memory and synchronization",
    "Sockets (brief overview)",
    "Signals"
  ],

  "Threads: User-level vs Kernel-level": [
    "User-level thread models",
    "Kernel-level threads",
    "Advantages and disadvantages of each"
  ],

  "Multithreading Models & Thread Libraries": [
    "Many-to-One model",
    "One-to-One model",
    "Many-to-Many model",
    "Pthreads library",
    "Windows threads",
    "Thread pools"
  ],

  "CPU Scheduling: Preemptive vs Non-preemptive": [
    "Definition and examples",
    "Context switching overheads"
  ],

  "Scheduling Algorithms: FCFS, SJF, RR, Priority": [
    "FCFS characteristics",
    "SJF (preemptive & non-preemptive)",
    "Round Robin (quantum selection)",
    "Priority scheduling",
    "Starvation and aging"
  ],

  "Multilevel Queue & Feedback Scheduling": [
    "Multilevel queue architecture",
    "Multilevel feedback queue principles",
    "Examples and problems"
  ],

  "Performance Metrics in Scheduling": [
    "CPU utilization",
    "Throughput",
    "Turnaround time",
    "Waiting time",
    "Response time",
    "Gantt chart analysis"
  ],

  "Process Synchronization: Critical Section Problem": [
    "Critical section definition",
    "Requirements for a correct solution",
    "Race conditions"
  ],

  "Mutual Exclusion: Peterson's Algorithm, Hardware Support": [
    "Peterson’s algorithm details",
    "Test-and-Set",
    "Compare-and-Swap",
    "Memory barriers"
  ],

  "Semaphores: Binary, Counting, Implementation": [
    "Semaphore operations (wait, signal)",
    "Binary vs counting semaphores",
    "Semaphore implementation issues"
  ],

  "Monitors & Condition Variables": [
    "Monitor structure",
    "Condition variables",
    "Signal vs broadcast semantics"
  ],

  "Classical Synchronization Problems": [
    "Dining Philosophers",
    "Readers-Writers (1st and 2nd variants)",
    "Producer-Consumer (Bounded Buffer)",
    "Sleeping Barber problem"
  ],

  "Deadlock: Necessary Conditions, Prevention, Avoidance": [
    "Coffman conditions",
    "Resource allocation graph",
    "Deadlock prevention techniques",
    "Deadlock avoidance concepts"
  ],

  "Banker's Algorithm & Deadlock Detection": [
    "Banker’s algorithm steps",
    "Safe and unsafe states",
    "Deadlock detection algorithms",
    "Recovery from deadlock"
  ],

  "Memory Management Overview": [
    "Memory hierarchy",
    "Logical vs physical address space",
    "Memory allocation strategies"
  ],

  "Memory Allocation: Fixed, Variable Partitioning": [
    "Fixed partitioning issues",
    "Variable partitioning and external fragmentation",
    "Memory compaction"
  ],

  "Swapping & Fragmentation: Internal, External": [
    "Swapping techniques",
    "Overlays",
    "Internal vs external fragmentation examples"
  ],

  "Paging: Page Tables, TLB, Multi-level Paging": [
    "Paging mechanism",
    "Page tables and entries",
    "Translation Lookaside Buffer (TLB)",
    "Multi-level paging structures"
  ],

  "Segmentation: Segment Tables, Segmentation with Paging": [
    "Segmentation concept",
    "Segment table entries",
    "Advantages of segmentation",
    "Segmentation with paging combined schemes"
  ],

  "Virtual Memory: Demand Paging, Page Faults": [
    "Virtual memory concepts",
    "Demand paging",
    "Handling page faults",
    "Local vs global replacement"
  ],

  "Page Replacement: FIFO, LRU, Optimal, Clock": [
    "FIFO algorithm details",
    "LRU and implementation",
    "Optimal replacement",
    "Clock algorithm and improvements",
    "Belady’s anomaly"
  ],

  "Thrashing & Working Set Model": [
    "Thrashing definition and causes",
    "Working set model",
    "Page fault frequency control"
  ],

  "File System: Directory Structure, File Allocation": [
    "Single-level, two-level, tree structured directories",
    "File allocation methods: contiguous, linked, indexed",
    "Directory implementation issues"
  ],

  "File System Implementation: Free Space Management, Inodes, Journaling": [
    "Free space management methods",
    "Inodes and file metadata",
    "Journaling file systems",
    "Log-structured file systems"
  ],

  "Disk Management: Partitioning, Formatting": [
    "Partition tables (MBR, GPT basics)",
    "Low-level and high-level formatting",
    "Boot blocks"
  ],

  "Disk Scheduling: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK": [
    "Disk geometry basics",
    "Comparison of algorithms",
    "Calculation of seek times"
  ],

  "RAID Levels & Disk Reliability": [
    "RAID 0 to RAID 6",
    "Performance and fault tolerance",
    "Hot spare disks"
  ],

  "I/O Systems: I/O Hardware, Controllers, Polling, Interrupts, DMA": [
    "I/O hardware architecture",
    "Polling vs interrupt-driven I/O",
    "DMA controllers",
    "I/O buffering and spooling"
  ],

  "Security & Protection: Access Matrix, ACLs, Capabilities": [
    "Protection vs security",
    "Access matrix model",
    "Access Control Lists (ACLs)",
    "Capability lists",
    "Security policies and threats"
  ],
    "Database Concepts: DBMS vs File System": [
    "Data independence concept",
    "ACID properties importance",
    "Concurrent access control",
    "Data integrity maintenance",
    "Query optimization benefits",
    "Backup and recovery features"
  ],
  "Data Models: Hierarchical, Network, Relational": [],
  "Entity-Relationship Model: Entities, Attributes, Relationships": [],
  "ER Diagram: Strong/Weak Entities, ISA Hierarchy": [
    "ER to Relational Mapping"
  ],
  "Relational Model: Tables, Tuples, Domains": [],
  "Keys: Super, Candidate, Primary, Foreign": [],
  "Integrity Constraints: Entity, Referential, Domain": [],
  "Relational Algebra: Selection, Projection, Join": [
    "Division operation",
    "Set operations (Union, Intersection, Difference)"
  ],
  "Relational Calculus: Tuple & Domain Calculus": [],
  "SQL Fundamentals: DDL, DML, DCL, TCL": [],
  "Join Operations: Inner, Outer, Semi, Anti": [],
  "Aggregate Functions & Group By": [],
  "Window Functions & Common Table Expressions": [],
  "Advanced SQL: Subqueries, Views, Stored Procedures": [
    "Triggers (optional)"
  ],
  "Functional Dependencies & Armstrong's Axioms": [],
  "Normalization: 1NF, 2NF, 3NF, BCNF": [],
  "Multivalued Dependencies & 4NF": [],
  "Join Dependencies & 5NF": [],
  "File Organization: Heap, Sorted, Hashing, ISAM": [],
  "Indexing: Primary, Secondary, Clustered": [],
  "B-Trees & B+ Trees for Database Indexing": [],
  "Hash-based Indexing & Bitmap Indexes": [],
  "Query Processing: Parsing, Optimization, Execution": [
    "Cost-based vs heuristic optimization"
  ],
  "Join Algorithms: Nested Loop, Sort-Merge, Hash": [],
  "Transaction Management: ACID Properties": [
    "Schedules (serial, serializable, recoverable)",
    "Serializability (Conflict/View)",
    "Cascading Rollback",
    "Isolation Levels"
  ],
  "Concurrency Control: Lock-based, Timestamp-based": [],
  "Deadlock Detection & Resolution": [],
  "Recovery: Log-based, Shadow Paging, Checkpoints": [],
  "Database Security & Authorization": [],
  "Distributed Databases (Optional)": [
    "Basic architecture",
    "Advantages and challenges"
  ],
  "NoSQL Databases (Optional)": [
    "Document Stores",
    "Key-Value Stores"
  ],
    "Network Fundamentals: Protocols, Standards": [
    "Protocol layering principles",
    "Standardization organizations",
    "Protocol data units (PDUs)",
    "Service vs protocol distinction",
    "Connectionless vs connection-oriented",
    "Circuit switching vs packet switching",
    "Network performance metrics"
  ],

  "Physical Layer: Transmission Media, Signals": [
    "Types of transmission media",
    "Analog vs digital signals",
    "Bandwidth concept",
    "Fourier analysis basics"
  ],

  "Transmission Impairments & Capacity": [
    "Noise, attenuation, distortion",
    "Signal-to-Noise Ratio (SNR)",
    "Shannon Capacity theorem",
    "Nyquist theorem"
  ],

  "Framing Techniques: Bit Stuffing, Byte Stuffing": [
    "Character count framing",
    "Flag bytes with byte stuffing",
    "Flag bits with bit stuffing"
  ],

  "HDLC, PPP Protocols": [
    "HDLC frame structure",
    "PPP frame structure",
    "Features of HDLC vs PPP"
  ],

  "Token Ring, Exposed Terminal Problem": [
    "Token Ring working principle",
    "Exposed terminal problem explanation"
  ],

  "Fragmentation in IP": [
    "Need for fragmentation",
    "MF flag, Fragment Offset",
    "Reassembly process"
  ],

  "Datagram vs Virtual Circuit Switching": [
    "Datagram concept",
    "Virtual circuit concept",
    "Comparison and examples"
  ],

  "TCP Timers and Segment Details": [
    "TCP header fields (Flags, Window Size, etc.)",
    "Retransmission timer",
    "Persistence timer",
    "Keep-alive timer"
  ],

  "Performance Metrics & Queuing Theory": [
    "Transmission delay vs propagation delay",
    "Queuing delay",
    "Throughput vs latency",
    "Basics of M/M/1 queue"
  ],

  "TELNET, DHCP, SNTP": [
    "TELNET purpose and working",
    "DHCP process",
    "SNTP basics"
  ],

  "Network Security: Cryptography, Digital Signatures, SSL/TLS": [
    "Symmetric vs Asymmetric cryptography",
    "Digital signatures",
    "Certificates and PKI",
    "SSL/TLS basics"
  ]
}

# Authentication decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in credentials['users'] and credentials['users'][username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            session['user_name'] = credentials['users'][username]['name']
            
            # Show popup on successful login
            return render_template('login.html', show_popup=True)
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', subjects=subjects, concept_mastery=concept_mastery)

@app.route('/select_subject', methods=['POST'])
@login_required
def select_subject():
    subject = request.form['subject']
    session['selected_subject'] = subject
    session.pop('selected_topic', None)  # Clear topic when new subject is selected
    return redirect(url_for('index'))

@app.route('/select_topic', methods=['POST'])
@login_required
def select_topic():
    topic = request.form['topic']
    session['selected_topic'] = topic
    
    # Auto-generate prompt when topic is selected
    prompt = f"You are an expert GATE tutor. Teach me the topic '{topic}' from scratch to expert level. Provide a well-structured learning path and clearly explain the conceptual dependencies. Start with basics and gradually progress. Include theory, real-world examples, step-by-step problem-solving, common mistakes, PYQs, and self-assessment questions."
    session['generated_prompt'] = prompt
    
    return redirect(url_for('index'))

@app.route('/clear_selection')
@login_required
def clear_selection():
    session.clear()
    # Keep login session active
    session['logged_in'] = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
