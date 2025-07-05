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
        "Boolean Algebra & De Morgan's Laws", "Logic Gates: Universal, Multi-level", 
        "Combinational Logic Design", "Multiplexers, Demultiplexers, Encoders, Decoders",
        "Adders, Subtractors & Arithmetic Circuits", "Comparators & Code Converters",
        "Sequential Logic: Latches & Flip-Flops", "Registers: Shift, Storage, Counter",
        "State Machines: Moore & Mealy Models", "Timing Analysis & Race Conditions",
        "Logic Minimization: K-Map, Quine-McCluskey", "Multi-level Logic Optimization",
        "Number Systems: Binary, Octal, Hexadecimal", "Signed Number Representation: 2's Complement",
        "Fixed-Point & Floating-Point Arithmetic", "IEEE 754 Standard", "Error Detection & Correction"
    ],
    "Computer Organization and Architecture": [
        "Instruction Set Architecture (ISA)", "Machine Instructions & Assembly Language", 
        "Addressing Modes: Immediate, Direct, Indirect", "Instruction Formats & Encoding",
        "CPU Design: Single-cycle vs Multi-cycle", "ALU Design & Implementation", 
        "Control Unit: Hardwired vs Microprogrammed", "Datapath Design & Control Signals",
        "Pipelining: 5-stage, Hazards, Forwarding", "Branch Prediction & Speculation",
        "Memory Hierarchy: Cache, Main Memory", "Cache Design: Direct, Associative, Set-Associative",
        "Cache Coherence & Memory Consistency", "Virtual Memory & Address Translation",
        "Page Replacement Algorithms", "TLB & Memory Management Unit",
        "I/O Organization: Programmed, Interrupt-driven, DMA", "Bus Architecture & Protocols",
        "Parallel Processing: SIMD, MIMD", "Multicore & Multithreading"
    ],
    "Programming and Data Structures": [
        "C Programming: Syntax, Semantics, Memory Model", "Data Types, Variables & Operators", 
        "Control Structures: Loops, Conditionals", "Functions: Parameters, Return Values, Recursion",
        "Pointers: Arithmetic, Arrays, Dynamic Memory", "Structures, Unions & Bit Fields",
        "File I/O & Standard Library Functions", "Preprocessing & Compilation Process",
        "Arrays: 1D, 2D, Multi-dimensional", "Strings: Manipulation, Pattern Matching",
        "Linked Lists: Singly, Doubly, Circular", "Stack: Implementation, Applications",
        "Queue: Linear, Circular, Priority, Deque", "Trees: Binary, n-ary, Expression Trees",
        "Binary Search Tree: Operations, Analysis", "Balanced Trees: AVL, Red-Black, Splay",
        "Heap: Min-heap, Max-heap, Heap Sort", "B-Trees & B+ Trees for Databases",
        "Tries: Prefix Trees, Compressed Tries", "Graph Representations: Adjacency Matrix/List",
        "Advanced Data Structures: Segment Tree, Fenwick Tree, Disjoint Set Union"
    ],
    "Algorithms": [
        "Algorithm Analysis: Time & Space Complexity", "Asymptotic Notations: Big-O, Omega, Theta", 
        "Recurrence Relations & Master Theorem", "Loop Analysis & Amortized Complexity",
        "Brute Force & Exhaustive Search", "Divide and Conquer: Paradigm & Applications",
        "Sorting: Comparison-based vs Non-comparison", "Quick Sort: Analysis, Randomization",
        "Merge Sort: Implementation, External Sorting", "Heap Sort & Priority Queue Applications",
        "Linear Time Sorting: Counting, Radix, Bucket", "Searching: Linear, Binary, Interpolation",
        "Hashing: Hash Functions, Collision Resolution", "Perfect Hashing & Universal Hashing",
        "Greedy Algorithms: Theory & Applications", "Activity Selection & Interval Scheduling",
        "Huffman Coding & Data Compression", "Minimum Spanning Tree: Kruskal, Prim",
        "Dynamic Programming: Principles & Techniques", "Optimal Substructure & Overlapping Subproblems",
        "Classic DP: Knapsack, LCS, LIS, Edit Distance", "Matrix Chain Multiplication & Optimal BST",
        "Graph Algorithms: DFS, BFS, Applications", "Topological Sorting & Strongly Connected Components",
        "Shortest Path: Dijkstra, Bellman-Ford, Floyd-Warshall", "Network Flow: Max Flow, Min Cut",
        "String Algorithms: KMP, Rabin-Karp, Z-algorithm", "Advanced Topics: Approximation, Randomized Algorithms"
    ],
    "Theory of Computation": [
        "Formal Languages & Automata Theory", "Alphabets, Strings & Language Operations", 
        "Regular Languages & Regular Expressions", "Finite Automata: DFA, NFA, ε-NFA",
        "Equivalence of FA & Regular Expressions", "Pumping Lemma for Regular Languages",
        "Closure Properties of Regular Languages", "Minimization of Finite Automata",
        "Context-Free Languages & Grammars", "Chomsky Normal Form & Greibach Normal Form",
        "Pushdown Automata: Deterministic & Non-deterministic", "Equivalence of CFG & PDA",
        "Pumping Lemma for Context-Free Languages", "Closure Properties of CFLs",
        "Turing Machines: Definition & Variants", "Church-Turing Thesis & Computability",
        "Decidable & Undecidable Problems", "Halting Problem & Reduction",
        "Recursive & Recursively Enumerable Languages", "Rice's Theorem & Applications",
        "Complexity Classes: P, NP, NP-Complete", "Cook's Theorem & Polynomial Reductions",
        "Space Complexity: PSPACE, NPSPACE"
    ],
    "Compiler Design": [
        "Compiler Architecture & Phases", "Lexical Analysis: Tokens, Patterns, Lexemes", 
        "Regular Expressions for Token Recognition", "Finite Automata for Lexical Analysis",
        "LEX/FLEX: Lexical Analyzer Generators", "Error Handling in Lexical Analysis",
        "Syntax Analysis: Grammar & Parse Trees", "Top-Down Parsing: Recursive Descent, LL(1)",
        "Bottom-Up Parsing: LR(0), SLR(1), LALR(1)", "YACC/BISON: Parser Generators",
        "Error Recovery in Parsing", "Semantic Analysis: Type Checking, Scope",
        "Symbol Table: Organization & Management", "Syntax-Directed Translation & SDTs",
        "Intermediate Code Generation: 3-Address Code", "Control Flow: Basic Blocks, Flow Graphs",
        "Code Optimization: Local, Global, Peephole", "Data Flow Analysis: Live Variables, Reaching Definitions",
        "Loop Optimization: Invariant Code Motion", "Register Allocation & Assignment",
        "Code Generation: Target Code, Instruction Selection", "Runtime Environment: Activation Records, Parameter Passing"
    ],
    "Operating System": [
        "OS Structure: Monolithic, Microkernel, Layered", "System Calls & API Interface", 
        "Process Management: PCB, Process States", "Process Creation: fork(), exec(), wait()",
        "Inter-Process Communication: Pipes, Message Queues", "Threads: User-level vs Kernel-level",
        "Multithreading Models & Thread Libraries", "CPU Scheduling: Preemptive vs Non-preemptive",
        "Scheduling Algorithms: FCFS, SJF, RR, Priority", "Multilevel Queue & Feedback Scheduling",
        "Process Synchronization: Critical Section Problem", "Mutual Exclusion: Peterson's Algorithm, Hardware Support",
        "Semaphores: Binary, Counting, Implementation", "Monitors & Condition Variables",
        "Classical Synchronization Problems", "Deadlock: Necessary Conditions, Prevention, Avoidance",
        "Banker's Algorithm & Deadlock Detection", "Memory Management: Logical vs Physical Address",
        "Memory Allocation: Fixed, Variable Partitioning", "Paging: Page Tables, TLB, Multi-level Paging",
        "Segmentation: Segment Tables, Segmentation with Paging", "Virtual Memory: Demand Paging, Page Faults",
        "Page Replacement: FIFO, LRU, Optimal, Clock", "Thrashing & Working Set Model",
        "File System: Directory Structure, File Allocation", "Disk Management: Partitioning, Formatting",
        "Disk Scheduling: FCFS, SSTF, SCAN, C-SCAN", "I/O Hardware: Controllers, Interrupts, DMA"
    ],
    "Databases": [
        "Database Concepts: DBMS vs File System", "Data Models: Hierarchical, Network, Relational", 
        "Entity-Relationship Model: Entities, Attributes, Relationships", "ER Diagram: Strong/Weak Entities, ISA Hierarchy",
        "Relational Model: Tables, Tuples, Domains", "Keys: Super, Candidate, Primary, Foreign",
        "Integrity Constraints: Entity, Referential, Domain", "Relational Algebra: Selection, Projection, Join",
        "Relational Calculus: Tuple & Domain Calculus", "SQL Fundamentals: DDL, DML, DCL, TCL",
        "Advanced SQL: Subqueries, Views, Stored Procedures", "Join Operations: Inner, Outer, Semi, Anti",
        "Aggregate Functions & Group By", "Window Functions & Common Table Expressions",
        "Functional Dependencies & Armstrong's Axioms", "Normalization: 1NF, 2NF, 3NF, BCNF",
        "Multivalued Dependencies & 4NF", "Join Dependencies & 5NF",
        "Indexing: Primary, Secondary, Clustered", "B-Trees & B+ Trees for Database Indexing",
        "Hash-based Indexing & Bitmap Indexes", "Query Processing: Parsing, Optimization, Execution",
        "Join Algorithms: Nested Loop, Sort-Merge, Hash", "Transaction Management: ACID Properties",
        "Concurrency Control: Lock-based, Timestamp-based", "Deadlock Detection & Resolution",
        "Recovery: Log-based, Shadow Paging, Checkpoints", "Database Security & Authorization"
    ],
    "Computer Networks": [
        "Network Fundamentals: Protocols, Standards", "Network Models: OSI 7-layer, TCP/IP 5-layer", 
        "Physical Layer: Transmission Media, Signals", "Bandwidth, Throughput & Latency",
        "Encoding: NRZ, Manchester, Differential Manchester", "Multiplexing: FDM, TDM, WDM",
        "Data Link Layer: Framing, Error Detection", "Error Correction: Hamming Code, CRC",
        "Flow Control: Stop-and-Wait, Sliding Window", "ARQ Protocols: Stop-and-Wait, Go-Back-N, Selective Repeat",
        "Medium Access Control: ALOHA, CSMA/CD, CSMA/CA", "Ethernet: Frame Format, Collision Detection",
        "Wireless LANs: IEEE 802.11, Hidden Terminal Problem", "Network Layer: Routing, Forwarding",
        "IPv4: Address Classes, Subnetting, CIDR", "IPv6: Address Format, Transition Mechanisms",
        "Routing Algorithms: Distance Vector, Link State", "Internet Routing: RIP, OSPF, BGP",
        "Network Address Translation (NAT)", "Internet Control Message Protocol (ICMP)",
        "Transport Layer: Connection vs Connectionless", "UDP: Header Format, Applications",
        "TCP: Reliable Data Transfer, Flow Control", "TCP Congestion Control: Slow Start, Congestion Avoidance",
        "Application Layer Protocols: HTTP, HTTPS, FTP", "DNS: Hierarchy, Resolution Process",
        "Email Protocols: SMTP, POP3, IMAP", "Network Security: Cryptography, Digital Signatures",
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
    "Algorithm Analysis: Time & Space Complexity": [
        "Best, average, worst-case analysis",
        "Big-O, Omega, Theta notations",
        "Space complexity analysis",
        "Recursive algorithm analysis",
        "Amortized complexity concepts",
        "Comparison of algorithm complexities"
    ],
    "Formal Languages & Automata Theory": [
        "Alphabet, strings, and languages",
        "Operations on languages",
        "Finite automata design principles",
        "Regular language properties",
        "Context-free language hierarchy",
        "Chomsky hierarchy of languages"
    ],
    "Compiler Architecture & Phases": [
        "Lexical analysis phase",
        "Syntax analysis phase",
        "Semantic analysis phase",
        "Intermediate code generation",
        "Code optimization phase",
        "Code generation phase"
    ],
    "OS Structure: Monolithic, Microkernel, Layered": [
        "Monolithic kernel architecture",
        "Microkernel design principles",
        "Layered operating system approach",
        "Hybrid kernel systems",
        "Performance trade-offs",
        "Security implications of each structure"
    ],
    "Database Concepts: DBMS vs File System": [
        "Data independence concept",
        "ACID properties importance",
        "Concurrent access control",
        "Data integrity maintenance",
        "Query optimization benefits",
        "Backup and recovery features"
    ],
    "Network Fundamentals: Protocols, Standards": [
        "Protocol layering principles",
        "Standardization organizations",
        "Protocol data units (PDUs)",
        "Service vs protocol distinction",
        "Connectionless vs connection-oriented",
        "Network performance metrics"
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
