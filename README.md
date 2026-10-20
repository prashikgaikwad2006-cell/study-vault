# StudyVault — Digital Study Material Management System

> **T.Y. B.Sc. Computer Science Final Year Project**  
> Built strictly adhering to the requirements, database schemas, and architectural designs specified in the project report.

---

## 🌟 Overview & Problem Solved
As detailed in the Project Report:
Students often receive study materials from disparate classroom groups, messaging apps, and fragmented drives, leading to lost resources and wasted time. **StudyVault** provides a centralized, ultra-premium web portal where:
- **Faculty / Administrators** can manage degree courses, semesters, subjects, and publish study materials (Lecture Notes, Solved PYQs, Lab Manuals, References).
- **Students** can browse hierarchically by **Course &rarr; Semester &rarr; Subject**, conduct instant live searches, preview documents directly in-browser, and download verified study materials with real-time download counters.

---

## 🚀 Key Features

### 🎓 1. Student Portal
- **Hierarchical Academic Browsing**: Filter by degree course (B.Sc. CS, BCA, B.Tech CSE, M.Sc. IT), Semester (Sem 1 to Sem 6), and Subject.
- **Global Instant Search**: Real-time debounced search across titles, descriptions, and subject codes with search query highlights.
- **Document In-App Previewer**: Sleek modal reader displaying syllabus topics, uploader metadata, verified downloads, and built-in PDF document reader.
- **Direct Downloads**: One-click download serving verified PDF documents while tracking download statistics.
- **Bookmark Library**: Save crucial exam notes and access them anytime under "My Saved Notes".
- **View Toggle**: Switch between responsive Grid Cards and high-density List View.

### ⚡ 2. Faculty & Administrator Console
- **Quick Role Switcher Pill**: Instant 1-click toggle between Student Mode and Administrator Mode.
- **Upload Study Material**: Drag-and-drop file upload zone supporting PDF, DOCX, PPTX, TXT, and ZIP (with 32 MB limit and file sanitization).
- **Course Management**: Add and delete degree programs with custom course codes.
- **Subject Management**: Configure subjects linked to courses and semesters (Sem 1 through Sem 8).
- **Real-time Analytics**: Visual metrics showing Total Materials, Degree Courses, Subjects, and Top 5 Most Downloaded Materials.

### 🎨 3. Ultra-Premium Visual Aesthetics & Typography
- **Modern Typography**: Powered by Google Fonts **Plus Jakarta Sans** (headings & UI readability) + **Outfit** (hero displays & badges) + **JetBrains Mono** (subject codes & file metadata).
- **Theme Support**: Seamless **Dark Glassmorphism** (obsidian sapphire with glowing accent orbs) and **Crisp Light Mode** with `localStorage` memory.
- **Micro-animations**: Hover card lift, glowing borders, modal transitions, and responsive toast notifications.

---

## 🗄️ Database Design (As per PDF Section 3.3)
The system uses SQLite (configured with foreign keys enabled, 100% compatible with PostgreSQL):
- `users`: `user_id`, `full_name`, `email`, `password_hash`, `role`, `created_at`
- `courses`: `course_id`, `course_name`, `course_code`, `description`
- `subjects`: `subject_id`, `course_id`, `semester`, `subject_name`, `subject_code`
- `study_materials`: `material_id`, `subject_id`, `uploaded_by`, `title`, `description`, `file_name`, `file_path`, `file_type`, `file_size`, `category`, `uploaded_at`
- `downloads`: `download_id`, `material_id`, `user_id`, `downloaded_at`
- `bookmarks`: `bookmark_id`, `material_id`, `user_id`, `created_at`

---

## 💻 How to Run Locally

### 1. Requirements
- Python 3.10+
- Flask (`pip install flask werkzeug`)

### 2. Run the Application
```bash
# Seed initial T.Y. B.Sc. CS curriculum & sample materials
python seed_data.py

# Start the Flask web server
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser!

### 🔑 Default Demo Accounts
- **Admin**: `admin@studyvault.ac.in` / Password: `admin123`
- **Student**: `aarav.cs@student.ac.in` / Password: `student123`
- *Or simply click the **"⚡ Admin" / "🎓 Student"** role pills at the top right of the navigation bar for instant switching!*
