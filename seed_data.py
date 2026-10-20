import os
import sqlite3
from werkzeug.security import generate_password_hash
from database import DB_PATH, init_db

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

def generate_pdf(filepath, title, subject_name, course_info, bullets):
    """Generates a valid, readable PDF file for preview and download."""
    objects = []
    objects.append(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
    objects.append(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n')
    objects.append(b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>\nendobj\n')
    
    stream_lines = [
        'BT',
        '/F1 18 Tf',
        '50 740 Td',
        f'({title}) Tj',
        '0 -24 Td',
        '/F2 12 Tf',
        f'({subject_name} | {course_info}) Tj',
        '0 -18 Td',
        f'(StudyVault Digital Study Material - Department of Computer Science) Tj',
        '0 -30 Td',
        '/F1 13 Tf',
        '(Key Concepts & Highlights:) Tj',
        '0 -20 Td',
        '/F2 10 Tf'
    ]
    for bullet in bullets:
        safe_bullet = bullet.replace('(', '\\(').replace(')', '\\)')
        stream_lines.append(f'(\\204 {safe_bullet}) Tj')
        stream_lines.append('0 -16 Td')
        
    stream_lines.extend([
        '0 -20 Td',
        '/F2 9 Tf',
        '(Generated automatically by StudyVault Academic Portal - Free Educational Distribution) Tj',
        'ET'
    ])
    
    stream_bytes = '\n'.join(stream_lines).encode('latin1')
    stream_len = len(stream_bytes)
    
    objects.append(f'4 0 obj\n<< /Length {stream_len} >>\nstream\n'.encode('latin1') + stream_bytes + b'\nendstream\nendobj\n')
    objects.append(b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n')
    objects.append(b'6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n')
    
    pdf = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    xref_offsets = [0]
    for obj in objects:
        xref_offsets.append(len(pdf))
        pdf.extend(obj)
        
    xref_start = len(pdf)
    pdf.extend(f'xref\n0 {len(objects) + 1}\n0000000000 65535 f \n'.encode('latin1'))
    for offset in xref_offsets[1:]:
        pdf.extend(f'{offset:010d} 00000 n \n'.encode('latin1'))
        
    pdf.extend(f'trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n'.encode('latin1'))
    
    with open(filepath, 'wb') as f:
        f.write(pdf)

def seed_database():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Clear existing data for fresh seed
    cursor.execute("DELETE FROM downloads")
    cursor.execute("DELETE FROM bookmarks")
    cursor.execute("DELETE FROM study_materials")
    cursor.execute("DELETE FROM subjects")
    cursor.execute("DELETE FROM courses")
    cursor.execute("DELETE FROM users")

    # 1. Users
    users_data = [
        (
            'Prof. Rajesh Sharma (Administrator)',
            'admin@studyvault.ac.in',
            generate_password_hash('admin123'),
            'admin'
        ),
        (
            'Aarav Sharma (Student)',
            'aarav.cs@student.ac.in',
            generate_password_hash('student123'),
            'student'
        ),
        (
            'Priya Patel (Student)',
            'priya.patel@student.ac.in',
            generate_password_hash('student123'),
            'student'
        ),
        (
            'Rohan Deshmukh (Student)',
            'rohan.d@student.ac.in',
            generate_password_hash('student123'),
            'student'
        )
    ]
    cursor.executemany(
        'INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)',
        users_data
    )
    admin_id = 1
    aarav_id = 2
    priya_id = 3

    # 2. Courses
    courses_data = [
        (
            'B.Sc. Computer Science',
            'CS-BSC',
            '3-Year Undergraduate Programme covering core computing, algorithmic theory, databases, operating systems, and software engineering.'
        ),
        (
            'Bachelor of Computer Applications',
            'BCA-UG',
            'Comprehensive curriculum emphasizing modern application development, web technologies, and database administration.'
        ),
        (
            'B.Tech Computer Science & Engineering',
            'BTECH-CSE',
            'Engineering degree focused on system architectures, high performance computing, cloud services, and machine learning.'
        ),
        (
            'M.Sc. Information Technology',
            'MSC-IT',
            'Advanced post-graduate degree in distributed systems, cyber security, research paradigms, and artificial intelligence.'
        )
    ]
    cursor.executemany(
        'INSERT INTO courses (course_name, course_code, description) VALUES (?, ?, ?)',
        courses_data
    )

    # Fetch course IDs
    cursor.execute("SELECT course_id, course_code FROM courses")
    courses_map = {code: cid for cid, code in cursor.fetchall()}
    bsc_id = courses_map['CS-BSC']
    bca_id = courses_map['BCA-UG']
    btech_id = courses_map['BTECH-CSE']

    # 3. Subjects
    # Semester 5 & 6 (T.Y. B.Sc. CS as per PDF)
    subjects_data = [
        (bsc_id, 5, 'Operating Systems & Linux Architecture', 'CS501'),
        (bsc_id, 5, 'Advanced Database Management Systems (PostgreSQL)', 'CS502'),
        (bsc_id, 5, 'Software Engineering & Agile Methodologies', 'CS503'),
        (bsc_id, 5, 'Artificial Intelligence & Neural Networks', 'CS504'),
        (bsc_id, 6, 'Cloud Computing & DevOps Architecture', 'CS601'),
        (bsc_id, 6, 'Cybersecurity & Cryptographic Systems', 'CS602'),
        (bsc_id, 6, 'Data Science & Big Data Analytics', 'CS603'),
        (bsc_id, 3, 'Data Structures & Algorithms in C++', 'CS301'),
        (bsc_id, 4, 'Computer Networks & Internet Protocols', 'CS401'),
        (bsc_id, 1, 'Programming in Python & Problem Solving', 'CS101'),
        (bca_id, 5, 'Web Application Frameworks (Flask & React)', 'BCA501'),
        (bca_id, 5, 'Enterprise Java & Spring Boot', 'BCA502'),
        (btech_id, 5, 'Compiler Design & Automata Theory', 'BTCSE501'),
        (btech_id, 6, 'Distributed Systems & Microservices', 'BTCSE601')
    ]
    cursor.executemany(
        'INSERT INTO subjects (course_id, semester, subject_name, subject_code) VALUES (?, ?, ?, ?)',
        subjects_data
    )

    cursor.execute("SELECT subject_id, subject_code FROM subjects")
    subj_map = {code: sid for sid, code in cursor.fetchall()}

    # 4. Study Materials
    materials_catalog = [
        {
            'subject_code': 'CS501',
            'title': 'Complete OS Notes: Process Scheduling & Deadlock Management',
            'desc': 'Detailed lecture notes covering CPU Scheduling (FCFS, SJF, Round Robin), Semaphore locks, Banker\'s Algorithm and Memory Paging.',
            'filename': 'CS501_OS_Process_Scheduling_Notes.pdf',
            'filesize': '3.4 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'Process Life Cycle states and PCB (Process Control Block) layout',
                'CPU Scheduling Algorithms: FCFS, SJF, Priority, Round Robin evaluation',
                'Deadlock conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait',
                'Banker\'s Algorithm for Deadlock Avoidance with step-by-step matrix calculation',
                'Virtual Memory, Page Replacement (FIFO, LRU, Optimal), and Thrashing'
            ]
        },
        {
            'subject_code': 'CS502',
            'title': 'PostgreSQL & Relational Database Architecture Handbook',
            'desc': 'Comprehensive guide on E-R diagrams, Normalization up to BCNF, Relational Algebra, SQL triggers, and ACID transactions.',
            'filename': 'CS502_PostgreSQL_DBMS_Handbook.pdf',
            'filesize': '4.1 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'Entity-Relationship (ER) model conversion to Relational Schema',
                'Functional Dependencies and Normal Forms (1NF, 2NF, 3NF, BCNF)',
                'Transaction Processing: ACID Properties and Serializability schedules',
                'Concurrency Control: Two-Phase Locking (2PL) and Timestamp Ordering',
                'PostgreSQL Indexing: B-Tree, Hash, GIN, and Query Execution Plans (EXPLAIN ANALYZE)'
            ]
        },
        {
            'subject_code': 'CS503',
            'title': 'Software Engineering: SRS Template, UML & Agile Scrum Guide',
            'desc': 'Software Requirement Specification (SRS) IEEE format, Use Case Diagrams, Class Diagrams, and Sprint Planning rituals.',
            'filename': 'CS503_Software_Engineering_Agile_Guide.pdf',
            'filesize': '2.8 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'IEEE 830 Standard for Software Requirements Specification (SRS)',
                'UML 2.0 Diagrams: Use Case, Class, Sequence, and State Machine diagrams',
                'Agile Framework: Scrum ceremonies, Product Backlog, Sprints, and Burndown charts',
                'Software Testing: Unit testing, Integration testing, Black-box vs White-box techniques',
                'Software Maintenance models and DevOps CI/CD pipeline integration'
            ]
        },
        {
            'subject_code': 'CS504',
            'title': 'AI & Machine Learning: Search Algorithms to Deep Neural Nets',
            'desc': 'Uninformed vs Informed search (A*, Heuristics), Minimax, Supervised Learning (Linear/Logistic, SVM), and Neural Network Perceptrons.',
            'filename': 'CS504_AI_Machine_Learning_Notes.pdf',
            'filesize': '5.2 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'State Space Search: Breadth-First, Depth-First, and A* Heuristic Search',
                'Adversarial Search: Minimax algorithm and Alpha-Beta Pruning with examples',
                'Supervised Learning: Linear Regression, Logistic Regression, Decision Trees, and SVMs',
                'Neural Networks: Multi-Layer Perceptrons, Activation Functions (ReLU, Softmax)',
                'Backpropagation Algorithm and Gradient Descent Optimization'
            ]
        },
        {
            'subject_code': 'CS501',
            'title': 'OS Previous 5 Years University Solved Question Papers (2020-2025)',
            'desc': 'University exam question papers with model answers, schematic diagrams, and numerical solutions for Semester 5.',
            'filename': 'CS501_OS_University_Solved_PYQ.pdf',
            'filesize': '6.8 MB',
            'category': 'Previous Year Papers',
            'bullets': [
                'Winter & Summer semester exam questions compiled by Board of Examiners',
                'Complete step-by-step solved numericals on Banker\'s Deadlock Avoidance',
                'Page Replacement algorithms solved with frame traces (LRU vs FIFO)',
                'frequently asked theory questions with high-yield revision summaries'
            ]
        },
        {
            'subject_code': 'CS502',
            'title': 'Advanced DBMS Practical Lab Manual with 15 PostgreSQL Experiments',
            'desc': 'Official laboratory manual covering DDL/DML, complex Joins, PL/pgSQL stored procedures, triggers, and cursor implementations.',
            'filename': 'CS502_DBMS_Practical_Lab_Manual.pdf',
            'filesize': '3.9 MB',
            'category': 'Lab Manuals',
            'bullets': [
                'Experiment 1-3: Table creation, integrity constraints, and multi-table nested queries',
                'Experiment 4-6: Complex JOIN operations, GROUP BY, HAVING, and Window Functions',
                'Experiment 7-9: PL/pgSQL Stored Procedures and Functions with exception handling',
                'Experiment 10-12: BEFORE/AFTER Triggers for automated audit trails and constraint enforcement',
                'Experiment 13-15: Cursor traversal, Views, and Materialized Views performance benchmarks'
            ]
        },
        {
            'subject_code': 'CS601',
            'title': 'Cloud Computing & AWS Architecture Study Blueprint',
            'desc': 'IaaS, PaaS, SaaS paradigms, AWS EC2, S3, RDS, Serverless Lambda, Docker Containers and Kubernetes Orchestration.',
            'filename': 'CS601_Cloud_DevOps_Architecture.pdf',
            'filesize': '4.5 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'Cloud Service Models: IaaS, PaaS, SaaS comparative analysis and security trade-offs',
                'AWS Core Infrastructure: VPC, Subnets, EC2 Instances, S3 Buckets, and IAM Roles',
                'Containerization: Dockerfile syntax, Image layers, and Container networking',
                'Kubernetes: Pods, Deployments, Services, Ingress, and ReplicaSets',
                'CI/CD Pipelines: GitHub Actions automation and automated cloud deployment'
            ]
        },
        {
            'subject_code': 'CS602',
            'title': 'Cryptography & Network Security: RSA, AES & PKI Protocols',
            'desc': 'Classical ciphers, Symmetric encryption (AES/DES), Asymmetric cryptography (RSA, ECC), Hash functions (SHA-256), and SSL/TLS.',
            'filename': 'CS602_Cryptography_Security_Guide.pdf',
            'filesize': '3.7 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'Security Principles: Confidentiality, Integrity, Availability (CIA Triad), and Non-repudiation',
                'Symmetric Cryptography: DES structure, AES substitution-permutation network',
                'Asymmetric Cryptography: RSA mathematical foundation, key generation, and modular arithmetic',
                'Cryptographic Hash Functions: MD5 vulnerabilities vs SHA-256 and HMAC verification',
                'Public Key Infrastructure (PKI): Digital Certificates, X.509 format, and SSL/TLS handshake'
            ]
        },
        {
            'subject_code': 'CS301',
            'title': 'Data Structures & Algorithms Master Cheat Sheet & Code Reference',
            'desc': 'Time complexities Big-O summary, Linked Lists, Binary Search Trees, AVL Trees, Heaps, Graphs (Dijkstra, Prim, Kruskal).',
            'filename': 'CS301_DSA_Master_CheatSheet.pdf',
            'filesize': '2.4 MB',
            'category': 'Reference Material',
            'bullets': [
                'Asymptotic Notation: Big-O, Big-Omega, Big-Theta time and space complexity table',
                'Linear Structures: Arrays, Singly/Doubly Linked Lists, Stacks, and Queues implementation',
                'Non-Linear Structures: Binary Trees, BST operations, AVL Tree self-balancing rotations',
                'Heaps & Priority Queues: Min-Heap, Max-Heap, and HeapSort algorithm',
                'Graph Algorithms: BFS, DFS, Dijkstra\'s Shortest Path, Prim\'s and Kruskal\'s MST'
            ]
        },
        {
            'subject_code': 'CS401',
            'title': 'Computer Networks: OSI 7-Layer & TCP/IP Model Full Notes',
            'desc': 'Physical layer encoding, Data link framing & CRC, IPv4/IPv6 Subnetting, TCP 3-Way Handshake, Congestion Control, DNS and HTTP/3.',
            'filename': 'CS401_Computer_Networks_Complete.pdf',
            'filesize': '4.8 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'OSI Reference Model vs TCP/IP Protocol Suite mapping and protocol headers',
                'Data Link Layer: Sliding Window protocols (Go-Back-N, Selective Repeat) and CRC checksum',
                'Network Layer: IPv4 addressing, CIDR notation, Subnet masking, and IPv6 migration',
                'Transport Layer: UDP vs TCP, TCP 3-Way Handshake, Flow Control, and Congestion Control',
                'Application Layer: DNS resolution hierarchy, HTTP/1.1 vs HTTP/2 vs HTTP/3, SMTP, and SSH'
            ]
        },
        {
            'subject_code': 'BCA501',
            'title': 'Modern Web Architecture: RESTful Flask APIs & Frontend SPA Design',
            'desc': 'Building secure client-server web apps with Flask, SQLite/PostgreSQL, JSON REST endpoints, JWT authentication, and responsive CSS.',
            'filename': 'BCA501_Web_Frameworks_Flask.pdf',
            'filesize': '3.1 MB',
            'category': 'Lecture Notes',
            'bullets': [
                'Client-Server Architecture: HTTP request-response cycle and statelessness',
                'Flask Framework: Application structure, blueprints, request routing, and templating',
                'RESTful API Design: HTTP verbs (GET, POST, PUT, DELETE), status codes, and JSON payloads',
                'Database ORM vs Raw SQL queries with parameterized statements against SQL Injection',
                'Modern Frontend UI: CSS Grid, Flexbox, glassmorphic UI tokens, and asynchronous fetch()'
            ]
        }
    ]

    for item in materials_catalog:
        sub_id = subj_map.get(item['subject_code'])
        if not sub_id:
            continue
        
        filepath = os.path.join(UPLOADS_DIR, item['filename'])
        # Generate the physical PDF file
        generate_pdf(
            filepath=filepath,
            title=item['title'],
            subject_name=item['subject_code'],
            course_info='StudyVault Academic Repository',
            bullets=item['bullets']
        )

        cursor.execute('''
            INSERT INTO study_materials 
            (subject_id, uploaded_by, title, description, file_name, file_path, file_type, file_size, category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sub_id,
            admin_id,
            item['title'],
            item['desc'],
            item['filename'],
            f'uploads/{item["filename"]}',
            'PDF',
            item['filesize'],
            item['category']
        ))

    # 5. Insert simulated download history for analytics
    cursor.execute("SELECT material_id FROM study_materials")
    material_ids = [row[0] for row in cursor.fetchall()]
    
    download_records = []
    # Seed 18 realistic download logs
    import random
    for i in range(24):
        mat_id = random.choice(material_ids)
        usr_id = random.choice([aarav_id, priya_id])
        download_records.append((mat_id, usr_id))
        
    cursor.executemany(
        'INSERT INTO downloads (material_id, user_id) VALUES (?, ?)',
        download_records
    )

    # 6. Seed bookmarks
    if len(material_ids) >= 3:
        cursor.execute("INSERT OR IGNORE INTO bookmarks (material_id, user_id) VALUES (?, ?)", (material_ids[0], aarav_id))
        cursor.execute("INSERT OR IGNORE INTO bookmarks (material_id, user_id) VALUES (?, ?)", (material_ids[1], aarav_id))
        cursor.execute("INSERT OR IGNORE INTO bookmarks (material_id, user_id) VALUES (?, ?)", (material_ids[0], priya_id))

    conn.commit()
    conn.close()
    print("Database successfully seeded with academic materials, courses, subjects, and users!")

if __name__ == '__main__':
    seed_database()
