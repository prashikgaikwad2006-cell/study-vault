"""
Script to generate the comprehensive StudyVault Use Case & User Guide PDF.
T.Y. B.Sc. Computer Science Academic Project.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# Palette definitions
NAVY = colors.HexColor("#0F172A")
DEEP_INDIGO = colors.HexColor("#1E1B4B")
PRIMARY_INDIGO = colors.HexColor("#312E81")
ACCENT_PURPLE = colors.HexColor("#6366F1")
ACCENT_CYAN = colors.HexColor("#0284C7")
SUCCESS_EMERALD = colors.HexColor("#059669")
WARNING_AMBER = colors.HexColor("#D97706")
LIGHT_BG = colors.HexColor("#F8FAFC")
CARD_BG = colors.HexColor("#F1F5F9")
BORDER_COLOR = colors.HexColor("#CBD5E1")
TEXT_DARK = colors.HexColor("#0F172A")
TEXT_MUTED = colors.HexColor("#475569")
WHITE = colors.HexColor("#FFFFFF")
CALLOUT_BG = colors.HexColor("#EEF2FF")
CALLOUT_BORDER = colors.HexColor("#818CF8")
ADMIN_CALLOUT_BG = colors.HexColor("#FFFBEB")
ADMIN_CALLOUT_BORDER = colors.HexColor("#F59E0B")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas that adds a consistent running header and footer with total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        self.saveState()
        
        # Omit running header on page 1 (cover header)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(PRIMARY_INDIGO)
            self.drawString(36, 816, "STUDYVAULT")
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_MUTED)
            self.drawString(100, 816, "|   Digital Study Material Management System   •   System Use Case & User Guide")
            
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.6)
            self.line(36, 808, 559, 808)

        # Running Footer on all pages
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.6)
        self.line(36, 38, 559, 38)

        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(36, 26, "T.Y. B.Sc. Computer Science Project   •   Dept. of Computer Science")
        
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(559, 26, page_str)
        self.restoreState()


def build_pdf(filename="StudyVault_User_and_Use_Case_Guide.pdf"):
    pdf_path = os.path.abspath(filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=DEEP_INDIGO,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=ACCENT_PURPLE,
        alignment=TA_CENTER
    )

    meta_style = ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_MUTED,
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=DEEP_INDIGO,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13.5,
        textColor=PRIMARY_INDIGO,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        leftIndent=12,
        spaceAfter=3
    )

    callout_text_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=TEXT_DARK
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=WHITE,
        alignment=TA_CENTER
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.5,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10.5,
        textColor=PRIMARY_INDIGO
    )

    caption_style = ParagraphStyle(
        "CaptionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.8,
        leading=10.5,
        textColor=TEXT_MUTED,
        alignment=TA_CENTER
    )

    story = []

    # =========================================================================
    # PAGE 1: HEADER BANNER, EXECUTIVE SUMMARY, ROLES MATRIX, CREDENTIALS
    # =========================================================================
    story.append(Paragraph("STUDYVAULT", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Digital Study Material Management System", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>System Use Case Specification & Complete Operational User Manual</b>", ParagraphStyle("sub2", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=TEXT_DARK, alignment=TA_CENTER)))
    story.append(Spacer(1, 4))
    
    meta_text = (
        "<b>Academic Year:</b> 2025–2026 &nbsp;|&nbsp; "
        "<b>Class:</b> T.Y. B.Sc. Computer Science &nbsp;|&nbsp; "
        "<b>Department:</b> Computer Science<br/>"
        "<b>Live Production URL:</b> <font color='#312E81'><u>https://study-vault-psi-red.vercel.app</u></font> &nbsp;|&nbsp; "
        "<b>GitHub:</b> <font color='#312E81'><u>prashikgaikwad2006-cell/study-vault</u></font>"
    )
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=PRIMARY_INDIGO, spaceBefore=2, spaceAfter=8))

    # SECTION 1
    story.append(Paragraph("1. Executive Overview & Problem Addressed", h1_style))
    p1 = (
        "In collegiate education, essential study assets—such as unit lecture notes, previous years' question papers (PYQs), "
        "syllabus blueprints, and lab assignment guidelines—are scattered across informal WhatsApp groups, temporary Google Drive links, "
        "and unorganized Telegram channels. This causes severe academic hurdles: dead links before examinations, outdated curriculum documents, "
        "and unverified materials lacking departmental authority."
    )
    story.append(Paragraph(p1, body_style))
    
    p2 = (
        "<b>StudyVault</b> solves this challenge by providing a centralized, syllabus-indexed, cloud-native repository. "
        "Built with a sleek glassmorphism web interface and powered by a Python/Flask REST engine with SQLite relational indexing, "
        "StudyVault delivers instant multi-field search, in-browser PDF previews, and role-based permissions where "
        "<b>only authenticated faculty administrators have upload rights</b> to guarantee 100% verified, spam-free study materials."
    )
    story.append(Paragraph(p2, body_style))

    # Callout Box: Live Access Info
    callout_data = [[
        Paragraph(
            "<b>🌐 Official Live Production Deployment:</b> The platform is deployed 24/7 on Vercel at "
            "<b><font color='#312E81'>https://study-vault-psi-red.vercel.app</font></b>. It is fully responsive and runs on mobile phones, "
            "tablets, and desktop browsers without installing any third-party app.",
            callout_text_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[523])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, CALLOUT_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 6))

    # SECTION 2
    story.append(Paragraph("2. System Roles & Access Control Matrix", h1_style))
    role_matrix = [
        [
            Paragraph("System Capability / Feature", table_header_style),
            Paragraph("Student (Learner)", table_header_style),
            Paragraph("Faculty Administrator", table_header_style),
            Paragraph("Technical Enforcement & Security", table_header_style)
        ],
        [
            Paragraph("<b>Browse & Filter Materials</b>", table_cell_bold),
            Paragraph("Full Access (All Courses)", table_cell_style),
            Paragraph("Full Access", table_cell_style),
            Paragraph("Public REST API (/api/materials)", table_cell_style)
        ],
        [
            Paragraph("<b>Live Multi-Field Search</b>", table_cell_bold),
            Paragraph("Instant Debounced Query", table_cell_style),
            Paragraph("Instant Debounced Query", table_cell_style),
            Paragraph("Instant client-side index filtering ('/' shortcut)", table_cell_style)
        ],
        [
            Paragraph("<b>In-App PDF Document Preview</b>", table_cell_bold),
            Paragraph("Embedded HD Modal Reader", table_cell_style),
            Paragraph("Embedded HD Modal Reader", table_cell_style),
            Paragraph("Sandboxed modal overlay; no download forced", table_cell_style)
        ],
        [
            Paragraph("<b>Verified Direct Download</b>", table_cell_bold),
            Paragraph("Unlimited One-Click", table_cell_style),
            Paragraph("Unlimited One-Click", table_cell_style),
            Paragraph("Dynamic download counter tracking in SQLite DB", table_cell_style)
        ],
        [
            Paragraph("<b>Personal Exam Bookmarks</b>", table_cell_bold),
            Paragraph("Personal Starred Drawer", table_cell_style),
            Paragraph("Personal Starred Drawer", table_cell_style),
            Paragraph("Client-side persistent storage synchronization", table_cell_style)
        ],
        [
            Paragraph("<b>Upload New Academic Files</b>", table_cell_bold),
            Paragraph("<font color='#DC2626'><b>DENIED (Disabled)</b></font>", table_cell_style),
            Paragraph("<font color='#059669'><b>AUTHORIZED</b></font>", table_cell_style),
            Paragraph("Server HTTP 403 Forbidden check; Admin Bearer session", table_cell_style)
        ],
        [
            Paragraph("<b>Upload Button & Modal</b>", table_cell_bold),
            Paragraph("Hidden from UI", table_cell_style),
            Paragraph("Active in Navigation Bar", table_cell_style),
            Paragraph("DOM conditionally rendered upon Admin auth", table_cell_style)
        ],
        [
            Paragraph("<b>Supported File Types</b>", table_cell_bold),
            Paragraph("N/A", table_cell_style),
            Paragraph("PDF, DOCX, PPTX, TXT, ZIP", table_cell_style),
            Paragraph("Strict extension & MIME type validation (Max 32MB)", table_cell_style)
        ]
    ]

    role_table = Table(role_matrix, colWidths=[120, 115, 110, 178])
    role_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_INDIGO),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(role_table)
    story.append(Spacer(1, 6))

    # SECTION 3: CREDENTIALS REFERENCE TABLE
    story.append(Paragraph("3. System Credentials & Authentication Reference", h1_style))
    cred_data = [
        [
            Paragraph("Role", table_header_style),
            Paragraph("Email Identifier", table_header_style),
            Paragraph("Password", table_header_style),
            Paragraph("Privileges", table_header_style),
            Paragraph("Fast Access Method", table_header_style)
        ],
        [
            Paragraph("<b>Faculty Admin</b>", table_cell_bold),
            Paragraph("admin@studyvault.ac.in", table_cell_style),
            Paragraph("admin123", table_cell_style),
            Paragraph("Full Admin & Upload", table_cell_style),
            Paragraph("<b>Click '⚡ 1-Click Sign In as Admin'</b> in top bar", table_cell_style)
        ],
        [
            Paragraph("<b>Sample Student</b>", table_cell_bold),
            Paragraph("aarav.cs@student.ac.in", table_cell_style),
            Paragraph("student123", table_cell_style),
            Paragraph("Browse, Read, Download", table_cell_style),
            Paragraph("Click 'Sign In' &rarr; 'Demo Student Login'", table_cell_style)
        ],
        [
            Paragraph("<b>Self-Registered</b>", table_cell_bold),
            Paragraph("&lt;student email&gt;", table_cell_style),
            Paragraph("&lt;user set&gt;", table_cell_style),
            Paragraph("Browse, Read, Download", table_cell_style),
            Paragraph("Click 'Sign In' &rarr; 'Create an Account'", table_cell_style)
        ]
    ]

    cred_table = Table(cred_data, colWidths=[90, 125, 65, 100, 143])
    cred_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DEEP_INDIGO),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(cred_table)

    # Clean Page Break after Page 1
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: FEATURE BREAKDOWN (1-8) & FIGURE 1 (STUDENT PORTAL MOCKUP)
    # =========================================================================
    story.append(Paragraph("4. Feature Breakdown & Operational Mechanisms (Konse Features Kya Work Karte Hai)", h1_style))
    story.append(Paragraph(
        "StudyVault incorporates eight dedicated academic subsystems designed for frictionless student learning and faculty control:",
        body_style
    ))

    features = [
        ("Feature 1: Syllabus-Indexed Cascading Navigation",
         "Organizes materials following university hierarchies: <b>Course &rarr; Semester &rarr; Subject &rarr; Material Type</b>. "
         "Selecting a course dynamically filters available semesters, and picking a semester populates only that semester's subjects. "
         "Students never have to hunt through hundreds of unindexed documents."),
        
        ("Feature 2: Real-Time Debounced Global Search ('/' Shortcut)",
         "An instant client-side search engine searches title, unit description, subject code, and uploader name simultaneously. "
         "Pressing the <b>'/' key</b> focuses the search bar immediately from anywhere on the webpage with a 250ms debounce for high performance."),

        ("Feature 3: Academic Material Classification Badges",
         "Every resource is clearly labeled with color-coded classification chips: <b>Lecture Notes</b> (Indigo), "
         "<b>Question Bank / PYQs</b> (Amber), <b>Syllabus Copies</b> (Emerald), <b>Reference Books</b> (Cyan), and <b>Lab Manuals</b> (Rose)."),

        ("Feature 4: In-Browser PDF Document Previewer",
         "Students can inspect notes without downloading. Clicking <b>'Preview'</b> opens an embedded full-screen modal reader showing "
         "the document, page rendering, file size, semester, subject, and uploading faculty information."),

        ("Feature 5: One-Click Verified Direct Download",
         "Clicking <b>'Download'</b> triggers an immediate binary file download while updating the download counter in the database. "
         "This provides faculty with real-time insight into high-demand exam topics."),

        ("Feature 6: Exam Bookmarks / Saved Revision Drawer",
         "Students click the <b>Bookmark icon (&starf;)</b> to pin important notes into a dedicated drawer for rapid pre-exam revision."),

        ("Feature 7: Faculty Administrator Upload & Integrity Vault",
         "Restricted strictly to authenticated faculty. Enables multi-format uploads (PDF, DOCX, PPTX, TXT, ZIP up to 32MB) with "
         "automatic size calculation, file extension validation, and immediate curriculum database indexing."),

        ("Feature 8: Real-Time Academic Statistics Dashboard",
         "Displays dynamic counters in the header showing Total Materials, Cumulative Student Downloads, Active Courses, and Subjects.")
    ]

    for title, desc in features:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 6))

    # Figure 1: Portal UI Mockup
    img_portal = os.path.join(os.path.dirname(pdf_path), "docs_assets", "studyvault_portal_mockup.jpg")
    if os.path.exists(img_portal):
        story.append(Paragraph("<b>Figure 1: StudyVault Student Portal Interface</b>", h2_style))
        story.append(Paragraph("<i>Modern glassmorphic interface with live search, cascading filters, subject chips, material cards, and preview/download controls.</i>", caption_style))
        story.append(Spacer(1, 3))
        story.append(Image(img_portal, width=520, height=230))

    # Clean Page Break after Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: STEP-BY-STEP USER GUIDE & STUDENT SIGN-IN GUIDE
    # =========================================================================
    story.append(Paragraph("5. Step-by-Step User Guide (Website Kese Use Karni Hai)", h1_style))
    story.append(Paragraph(
        "Students can discover, preview, and download course documents in seconds using the following intuitive workflow:",
        body_style
    ))

    user_steps = [
        ("Step 1: Open the Web Portal", "Navigate to <b>https://study-vault-psi-red.vercel.app</b> in any browser on your laptop or smartphone. No app installation or account creation is required to browse and download."),
        ("Step 2: Choose Your Course & Semester", "In the filter bar, select your degree (e.g., <b>B.Sc. Computer Science</b>) and your semester (e.g., <b>Semester 5</b>). The portal automatically updates to display only matching resources."),
        ("Step 3: Filter by Subject or Resource Type", "Click any Subject pill (e.g., <i>Software Engineering</i>) or use the Type dropdown to isolate <i>Question Banks (PYQs)</i> or <i>Lecture Notes</i>."),
        ("Step 4: Use Fast Search with '/' Key", "Press the forward slash key <b>'/'</b> on your keyboard or tap the search box. Type keywords like <i>'Database'</i>, <i>'Python'</i>, or <i>'Agile'</i> for instantaneous results."),
        ("Step 5: Preview Notes in Your Browser", "Click <b>'Preview'</b> on any card. The built-in PDF viewer displays the full document without consuming device storage."),
        ("Step 6: Download Verified Notes", "Click <b>'Download'</b> on the material card or inside the preview reader to save the verified file directly to your device."),
        ("Step 7: Bookmark for Final Exam Revision", "Click the star / bookmark icon on important documents. Click <b>'Bookmarks'</b> in the top navigation bar to access all pinned notes in one place.")
    ]

    for step_num, step_desc in user_steps:
        story.append(Paragraph(f"<b>{step_num}:</b> {step_desc}", bullet_style))

    story.append(Spacer(1, 10))

    story.append(Paragraph("6. Student Sign-In & Account Registration Guide (Sign In Kese Karna Hai)", h1_style))
    story.append(Paragraph(
        "Students can create an account or sign in to synchronize personalized exam bookmarks across sessions:",
        body_style
    ))

    student_signin_steps = [
        ("Opening the Sign-In Modal", "Click the <b>'Sign In'</b> button at the top-right corner of the navigation header."),
        ("Instant Demo Student Login", "In the modal, click the pre-filled demo student button or type email <b>aarav.cs@student.ac.in</b> with password <b>student123</b>. Click <b>'Sign In to StudyVault'</b>."),
        ("Creating a New Student Account", "Click <b>'Create an Account'</b> at the bottom of the dialog. Enter your Full Name, College Email address, and a secure password. Click <b>'Register'</b>. Your student profile is activated instantly."),
        ("Student Account Permissions", "Students enjoy full, unrestricted read, search, preview, bookmark, and download capabilities across all enrolled subjects.")
    ]

    for title, desc in student_signin_steps:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", bullet_style))

    # Page Break after Page 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ADMIN LOGIN, FACULTY UPLOAD OPERATIONS & FIGURE 2 (ADMIN MODAL)
    # =========================================================================
    story.append(Paragraph("7. Administrator Login & Faculty Upload Operations (Admin Login Kese Karna Hai)", h1_style))
    
    admin_notice = [[
        Paragraph(
            "<b>🔒 Strict Faculty Upload Access Policy:</b> To uphold academic authenticity and prevent counterfeit notes, "
            "unverified documents, or malicious uploads, <b>the Upload feature is restricted to Faculty Administrators</b>. "
            "Public student uploading is deliberately disabled.",
            callout_text_style
        )
    ]]
    admin_table = Table(admin_notice, colWidths=[523])
    admin_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ADMIN_CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, ADMIN_CALLOUT_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(admin_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Two Methods to Sign In as Administrator:</b>", h2_style))
    
    admin_methods = [
        ("Method A: Instant 1-Click Admin Login (Recommended for Demonstrations)",
         "In the top navigation header or inside the Sign-In modal, click the yellow lightning button: "
         "<b>'⚡ 1-Click Sign In as Admin'</b>. The system instantly authenticates you as <b>Prof. Rajesh Sharma</b> (Admin ID: 1), "
         "issues the Bearer session token, unlocks the <b>'+ Upload Material'</b> button in the header, and activates the faculty upload console."),

        ("Method B: Manual Faculty Credential Sign In",
         "1. Click <b>'Sign In'</b> in the top navigation bar.<br/>"
         "2. Enter Faculty Admin Email: <b>admin@studyvault.ac.in</b><br/>"
         "3. Enter Admin Password: <b>admin123</b><br/>"
         "4. Click <b>'Sign In to StudyVault'</b>. Once verified, the Admin upload console is unlocked.")
    ]

    for title, desc in admin_methods:
        story.append(Paragraph(f"<b>• {title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Step-by-Step Document Upload Procedure for Admins:</b>", h2_style))

    upload_steps = [
        ("1. Click '+ Upload Material'", "Once logged in as Admin, a distinct indigo <b>'+ Upload Material'</b> button appears in the top navigation bar. Click it to open the Upload Console."),
        ("2. Select Course & Semester", "Choose the curriculum course (e.g., <i>B.Sc. Computer Science</i>) and semester (<i>Sem 1 to Sem 6</i>). The Subject selector dynamically updates with the corresponding curriculum."),
        ("3. Select Subject & Category", "Select the target Subject (e.g., <i>Advanced Java Programming</i>) and choose the material type: <i>Lecture Notes, Question Bank (PYQ), Syllabus Copy,</i> or <i>Reference Book</i>."),
        ("4. Provide Title & Syllabus Details", "Input a clear title (e.g., <i>Unit 3: Java Concurrency & Multithreading</i>) and a descriptive summary covering key exam concepts."),
        ("5. Drag-and-Drop File", "Drop your PDF, DOCX, PPTX, TXT, or ZIP file (up to 32MB). The interface calculates the file size and verifies format sanitization."),
        ("6. Click 'Publish to StudyVault'", "The server saves and indexes the file in the database. The material is instantly published and accessible to all students across the globe.")
    ]

    for u_title, u_desc in upload_steps:
        story.append(Paragraph(f"<b>{u_title}:</b> {u_desc}", bullet_style))

    story.append(Spacer(1, 6))

    # Figure 2: Admin Modal Mockup
    img_admin = os.path.join(os.path.dirname(pdf_path), "docs_assets", "studyvault_admin_modal.jpg")
    if os.path.exists(img_admin):
        story.append(Paragraph("<b>Figure 2: Faculty Administrator Upload Console & Security Modal</b>", h2_style))
        story.append(Paragraph("<i>Secure upload modal featuring Course/Semester cascading selectors, drag-and-drop file zone, format checks, and 1-click admin authentication.</i>", caption_style))
        story.append(Spacer(1, 3))
        story.append(Image(img_admin, width=520, height=225))

    # Page Break after Page 4
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TECHNICAL ARCHITECTURE, FAQ & SIGN-OFF
    # =========================================================================
    story.append(Paragraph("8. Technical Architecture & Deployment Details", h1_style))
    p_tech = (
        "StudyVault is built using a decoupled architecture engineered for high speed, zero downtime, and low resource overhead:"
    )
    story.append(Paragraph(p_tech, body_style))

    tech_table_data = [
        [
            Paragraph("Subsystem Layer", table_header_style),
            Paragraph("Technologies Used", table_header_style),
            Paragraph("Architectural Role & Key Specifications", table_header_style)
        ],
        [
            Paragraph("<b>Frontend UI / UX</b>", table_cell_bold),
            Paragraph("HTML5, Vanilla CSS3, Modern ES6+ JavaScript", table_cell_style),
            Paragraph("Glassmorphism dark theme, zero bulky dependencies, 60fps micro-animations, instant client-side debounced search indexing.", table_cell_style)
        ],
        [
            Paragraph("<b>Backend REST API</b>", table_cell_bold),
            Paragraph("Python 3.12, Flask Framework", table_cell_style),
            Paragraph("Modular RESTful endpoints for hierarchical filtering, streaming binary downloads, secure file upload processing, and token verification.", table_cell_style)
        ],
        [
            Paragraph("<b>Database & Storage</b>", table_cell_bold),
            Paragraph("SQLite 3 Relational Database Engine", table_cell_style),
            Paragraph("Normalized relational schema (courses, semesters, subjects, materials, users, bookmarks). Automatic database seeding with 11 academic resources.", table_cell_style)
        ],
        [
            Paragraph("<b>Cloud Platform</b>", table_cell_bold),
            Paragraph("Vercel Serverless WSGI Edge Platform", table_cell_style),
            Paragraph("Global CDN edge distribution, 24/7 high availability, automated continuous deployment pipeline synchronized with GitHub.", table_cell_style)
        ],
        [
            Paragraph("<b>Security & Auth</b>", table_cell_bold),
            Paragraph("PBKDF2 Password Hashing, Bearer Token Auth", table_cell_style),
            Paragraph("Role-based authorization restricting file uploads to faculty administrators; server-side whitelist validation preventing unauthorized files.", table_cell_style)
        ]
    ]

    t_tech = Table(tech_table_data, colWidths=[110, 145, 268])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DEEP_INDIGO),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CARD_BG]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 8))

    # SECTION 9: FAQ
    story.append(Paragraph("9. Frequently Asked Questions (FAQ) & Troubleshooting", h1_style))

    faqs = [
        ("Q1: Why is the '+ Upload Material' button not showing on my screen?",
         "<b>Answer:</b> The Upload button is visible only to Faculty Administrators. Click the yellow <b>'⚡ 1-Click Sign In as Admin'</b> button in the top bar or sign in with <b>admin@studyvault.ac.in</b> / <b>admin123</b> to unlock upload capabilities."),

        ("Q2: Can regular students upload their own study notes directly?",
         "<b>Answer:</b> No. Public student uploading is disabled to ensure 100% syllabus alignment and prevent malicious files or spam. Students submit their notes to faculty members, who verify and publish them through the Admin Console."),

        ("Q3: Does the website work on mobile devices and tablets?",
         "<b>Answer:</b> Yes. The layout is built using modern responsive CSS Flexbox and Grid. Filter dropdowns, search bars, and the PDF preview reader automatically adjust to any smartphone or tablet screen."),

        ("Q4: Do students have to pay or install extra apps to download documents?",
         "<b>Answer:</b> No. StudyVault is an open institutional project designed to provide barrier-free access. All notes can be previewed and downloaded completely free."),

        ("Q5: What happens if an Admin uploads an unsupported file format?",
         "<b>Answer:</b> The server enforces strict format validation. Only <b>.pdf, .docx, .pptx, .txt,</b> and <b>.zip</b> files under 32MB are accepted. Unsupported extensions (like .exe or .bat) are blocked with a clear warning.")
    ]

    for q, a in faqs:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))

    story.append(Spacer(1, 6))

    # SIGN-OFF & CERTIFICATION BLOCK
    signoff_data = [[
        Paragraph(
            "<b>Project Certification:</b> This system documentation represents the official Use Case Specification and Operational User Guide "
            "for <b>StudyVault — Digital Study Material Management System</b>, developed as an academic capstone project for "
            "<b>T.Y. B.Sc. Computer Science</b> (Academic Year 2025–2026).<br/>"
            "<b>Live Production URL:</b> https://study-vault-psi-red.vercel.app &nbsp;|&nbsp; "
            "<b>GitHub Repository:</b> https://github.com/prashikgaikwad2006-cell/study-vault",
            callout_text_style
        )
    ]]
    signoff_table = Table(signoff_data, colWidths=[523])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(signoff_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated PDF at {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    build_pdf()
