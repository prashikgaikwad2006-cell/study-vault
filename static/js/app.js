/**
 * StudyVault - Digital Study Material Management System
 * Interactive Client Application
 */

// Application State
const state = {
    user: null,
    courses: [],
    subjects: [],
    materials: [],
    activeFilters: {
        course_id: 'all',
        semester: 'all',
        subject_id: 'all',
        category: 'all',
        q: '',
        sort: 'latest',
        bookmarksOnly: false
    },
    currentView: 'grid'
};

// ==================== DOM ELEMENTS ====================
const DOM = {
    // Header & Nav
    themeToggleBtn: document.getElementById('themeToggleBtn'),
    globalSearchInput: document.getElementById('globalSearchInput'),
    clearSearchBtn: document.getElementById('clearSearchBtn'),
    roleIndicatorBadge: document.getElementById('roleIndicatorBadge'),
    roleBadgeIcon: document.getElementById('roleBadgeIcon'),
    roleBadgeText: document.getElementById('roleBadgeText'),
    adminLoginBtn: document.getElementById('adminLoginBtn'),
    openAdminPanelBtn: document.getElementById('openAdminPanelBtn'),
    userProfileBtn: document.getElementById('userProfileBtn'),
    userDropdown: document.getElementById('userDropdown'),
    userAvatar: document.getElementById('userAvatar'),
    headerUserName: document.getElementById('headerUserName'),
    dropdownUserName: document.getElementById('dropdownUserName'),
    dropdownUserEmail: document.getElementById('dropdownUserEmail'),
    dropdownUserRole: document.getElementById('dropdownUserRole'),
    logoutBtn: document.getElementById('logoutBtn'),
    filterMyBookmarksBtn: document.getElementById('filterMyBookmarksBtn'),
    resetDemoBtn: document.getElementById('resetDemoBtn'),
    openAuthModalBtn: document.getElementById('openAuthModalBtn'),

    // Hero & Stats
    statMaterials: document.getElementById('statMaterials'),
    statCourses: document.getElementById('statCourses'),
    statSubjects: document.getElementById('statSubjects'),
    statDownloads: document.getElementById('statDownloads'),
    browseNowBtn: document.getElementById('browseNowBtn'),
    heroUploadBtn: document.getElementById('heroUploadBtn'),
    heroSavedNotesBtn: document.getElementById('heroSavedNotesBtn'),
    viewPyqBtn: document.getElementById('viewPyqBtn'),

    // Filter controls
    courseTabsContainer: document.getElementById('courseTabsContainer'),
    semesterPillsContainer: document.getElementById('semesterPillsContainer'),
    subjectFilterSelect: document.getElementById('subjectFilterSelect'),
    categoryPillsContainer: document.getElementById('categoryPillsContainer'),
    sortBySelect: document.getElementById('sortBySelect'),
    viewGridBtn: document.getElementById('viewGridBtn'),
    viewListBtn: document.getElementById('viewListBtn'),
    activeFilterTagsBar: document.getElementById('activeFilterTagsBar'),
    tagsList: document.getElementById('tagsList'),
    clearAllFiltersBtn: document.getElementById('clearAllFiltersBtn'),

    // Materials Grid
    materialsGrid: document.getElementById('materialsGrid'),
    emptyState: document.getElementById('emptyState'),
    emptyResetBtn: document.getElementById('emptyResetBtn'),

    // Modals
    previewModal: document.getElementById('previewModal'),
    closePreviewModalBtn: document.getElementById('closePreviewModalBtn'),
    closePreviewFooterBtn: document.getElementById('closePreviewFooterBtn'),
    previewFileType: document.getElementById('previewFileType'),
    previewTitle: document.getElementById('previewTitle'),
    previewSubmeta: document.getElementById('previewSubmeta'),
    previewCourseName: document.getElementById('previewCourseName'),
    previewSemester: document.getElementById('previewSemester'),
    previewUploader: document.getElementById('previewUploader'),
    previewSize: document.getElementById('previewSize'),
    previewDownloads: document.getElementById('previewDownloads'),
    previewDescription: document.getElementById('previewDescription'),
    previewIframe: document.getElementById('previewIframe'),
    previewOpenTabBtn: document.getElementById('previewOpenTabBtn'),
    previewDownloadBtn: document.getElementById('previewDownloadBtn'),

    // Admin Console
    adminModal: document.getElementById('adminModal'),
    closeAdminModalBtn: document.getElementById('closeAdminModalBtn'),
    uploadMaterialForm: document.getElementById('uploadMaterialForm'),
    uploadCourseSelect: document.getElementById('uploadCourseSelect'),
    uploadSemesterSelect: document.getElementById('uploadSemesterSelect'),
    uploadSubjectSelect: document.getElementById('uploadSubjectSelect'),
    fileDropZone: document.getElementById('fileDropZone'),
    materialFileInput: document.getElementById('materialFileInput'),
    dropZoneTitle: document.getElementById('dropZoneTitle'),
    adminMaterialsTableBody: document.getElementById('adminMaterialsTableBody'),
    adminMaterialsCounter: document.getElementById('adminMaterialsCounter'),
    addCourseForm: document.getElementById('addCourseForm'),
    newCourseCode: document.getElementById('newCourseCode'),
    newCourseName: document.getElementById('newCourseName'),
    newCourseDesc: document.getElementById('newCourseDesc'),
    coursesManageList: document.getElementById('coursesManageList'),
    addSubjectForm: document.getElementById('addSubjectForm'),
    newSubjectCourse: document.getElementById('newSubjectCourse'),
    newSubjectSem: document.getElementById('newSubjectSem'),
    newSubjectCode: document.getElementById('newSubjectCode'),
    newSubjectName: document.getElementById('newSubjectName'),
    subjectsManageList: document.getElementById('subjectsManageList'),
    analyticsPopularList: document.getElementById('analyticsPopularList'),
    analyticsCategoryBars: document.getElementById('analyticsCategoryBars'),

    // Auth Modal
    authModal: document.getElementById('authModal'),
    closeAuthModalBtn: document.getElementById('closeAuthModalBtn'),
    tabShowLogin: document.getElementById('tabShowLogin'),
    tabShowRegister: document.getElementById('tabShowRegister'),
    loginForm: document.getElementById('loginForm'),
    registerForm: document.getElementById('registerForm'),
    instantAdminLoginBtn: document.getElementById('instantAdminLoginBtn'),
    fillAdminDemo: document.getElementById('fillAdminDemo'),
    fillStudentDemo: document.getElementById('fillStudentDemo'),
    toastContainer: document.getElementById('toastContainer')
};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    await checkCurrentUser();
    await Promise.all([
        loadCourses(),
        loadSubjects(),
        loadStats()
    ]);
    await fetchMaterials();
    setupEventListeners();
});

// ==================== THEME MANAGEMENT ====================
function initTheme() {
    const savedTheme = localStorage.getItem('studyvault_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('studyvault_theme', next);
    showToast(`Switched to ${next} theme`, 'info');
}

// ==================== TOAST NOTIFICATIONS ====================
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let iconSvg = '';
    if (type === 'success') {
        iconSvg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><polyline points="20 6 9 17 4 12"></polyline></svg>';
    } else if (type === 'error') {
        iconSvg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>';
    } else {
        iconSvg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>';
    }

    toast.innerHTML = `
        ${iconSvg}
        <span class="toast-msg">${escapeHtml(message)}</span>
    `;

    DOM.toastContainer.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(40px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ==================== AUTH & USER SESSIONS ====================
async function checkCurrentUser() {
    try {
        const headers = {};
        const savedUid = localStorage.getItem('studyvault_user_id');
        if (savedUid) headers['Authorization'] = `Bearer ${savedUid}`;

        const res = await fetch('/api/auth/me', { headers });
        const data = await res.json();
        state.user = data.user;
        updateUserUI();
    } catch (e) {
        console.error('Failed checking user session:', e);
    }
}

function updateUserUI() {
    if (state.user) {
        DOM.headerUserName.textContent = state.user.full_name.split(' ')[0];
        DOM.dropdownUserName.textContent = state.user.full_name;
        DOM.dropdownUserEmail.textContent = state.user.email;
        DOM.dropdownUserRole.textContent = state.user.role.toUpperCase();
        DOM.userAvatar.textContent = state.user.full_name.charAt(0).toUpperCase();

        if (state.user.role === 'admin') {
            DOM.openAdminPanelBtn.style.display = 'inline-flex';
            if (DOM.heroUploadBtn) DOM.heroUploadBtn.style.display = 'inline-flex';
            if (DOM.heroSavedNotesBtn) DOM.heroSavedNotesBtn.style.display = 'none';
            if (DOM.adminLoginBtn) DOM.adminLoginBtn.style.display = 'none';
            if (DOM.roleBadgeIcon) DOM.roleBadgeIcon.textContent = '⚡';
            if (DOM.roleBadgeText) DOM.roleBadgeText.textContent = 'Faculty Admin';
            if (DOM.roleIndicatorBadge) DOM.roleIndicatorBadge.classList.add('admin-active');
            DOM.dropdownUserRole.style.color = '#F59E0B';
            DOM.dropdownUserRole.style.background = 'rgba(245, 158, 11, 0.15)';
        } else {
            DOM.openAdminPanelBtn.style.display = 'none';
            if (DOM.heroUploadBtn) DOM.heroUploadBtn.style.display = 'none';
            if (DOM.heroSavedNotesBtn) DOM.heroSavedNotesBtn.style.display = 'inline-flex';
            if (DOM.adminLoginBtn) DOM.adminLoginBtn.style.display = 'inline-flex';
            if (DOM.roleBadgeIcon) DOM.roleBadgeIcon.textContent = '🎓';
            if (DOM.roleBadgeText) DOM.roleBadgeText.textContent = 'Student Portal';
            if (DOM.roleIndicatorBadge) DOM.roleIndicatorBadge.classList.remove('admin-active');
            DOM.dropdownUserRole.style.color = '#6366F1';
            DOM.dropdownUserRole.style.background = 'rgba(99, 102, 241, 0.15)';
        }

        DOM.userProfileBtn.style.display = 'flex';
        DOM.openAuthModalBtn.style.display = 'none';
    } else {
        DOM.headerUserName.textContent = 'Guest';
        DOM.userProfileBtn.style.display = 'none';
        DOM.openAuthModalBtn.style.display = 'inline-flex';
        DOM.openAdminPanelBtn.style.display = 'none';
        if (DOM.heroUploadBtn) DOM.heroUploadBtn.style.display = 'none';
        if (DOM.heroSavedNotesBtn) DOM.heroSavedNotesBtn.style.display = 'inline-flex';
        if (DOM.adminLoginBtn) DOM.adminLoginBtn.style.display = 'inline-flex';
        if (DOM.roleBadgeIcon) DOM.roleBadgeIcon.textContent = '🎓';
        if (DOM.roleBadgeText) DOM.roleBadgeText.textContent = 'Student Portal';
        if (DOM.roleIndicatorBadge) DOM.roleIndicatorBadge.classList.remove('admin-active');
    }
}

// ==================== DATA FETCHING ====================
async function loadCourses() {
    try {
        const res = await fetch('/api/courses');
        state.courses = await res.json();
        renderCourseTabs();
        populateCourseDropdowns();
    } catch (e) {
        console.error('Failed loading courses:', e);
    }
}

function renderCourseTabs() {
    DOM.courseTabsContainer.innerHTML = `
        <button class="course-tab ${state.activeFilters.course_id === 'all' ? 'active' : ''}" data-course-id="all">
            <span>All Programs (${state.courses.reduce((acc, c) => acc + (c.material_count || 0), 0)})</span>
        </button>
    `;

    state.courses.forEach(c => {
        const btn = document.createElement('button');
        btn.className = `course-tab ${state.activeFilters.course_id == c.course_id ? 'active' : ''}`;
        btn.dataset.courseId = c.course_id;
        btn.innerHTML = `
            <span>${escapeHtml(c.course_name)}</span>
            <span style="font-size:0.75rem; opacity:0.7; font-family:var(--font-mono)">[${c.course_code}]</span>
        `;
        DOM.courseTabsContainer.appendChild(btn);
    });
}

function populateCourseDropdowns() {
    // For subject filter
    // For Admin upload
    DOM.uploadCourseSelect.innerHTML = '<option value="">Select Degree Course...</option>';
    DOM.newSubjectCourse.innerHTML = '<option value="">Select Course...</option>';

    state.courses.forEach(c => {
        const opt1 = new Option(`${c.course_name} (${c.course_code})`, c.course_id);
        const opt2 = new Option(`${c.course_name} (${c.course_code})`, c.course_id);
        DOM.uploadCourseSelect.appendChild(opt1);
        DOM.newSubjectCourse.appendChild(opt2);
    });
}

async function loadSubjects() {
    try {
        const res = await fetch('/api/subjects');
        state.subjects = await res.json();
        updateSubjectFilterSelect();
        renderSubjectsManageList();
    } catch (e) {
        console.error('Failed loading subjects:', e);
    }
}

function updateSubjectFilterSelect() {
    DOM.subjectFilterSelect.innerHTML = '<option value="all">All Subjects</option>';
    
    let filtered = state.subjects;
    if (state.activeFilters.course_id !== 'all') {
        filtered = filtered.filter(s => s.course_id == state.activeFilters.course_id);
    }
    if (state.activeFilters.semester !== 'all') {
        filtered = filtered.filter(s => s.semester == state.activeFilters.semester);
    }

    filtered.forEach(s => {
        const opt = new Option(`${s.subject_code} - ${s.subject_name}`, s.subject_id);
        if (state.activeFilters.subject_id == s.subject_id) {
            opt.selected = true;
        }
        DOM.subjectFilterSelect.appendChild(opt);
    });
}

async function loadStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        DOM.statMaterials.textContent = data.total_materials;
        DOM.statCourses.textContent = data.total_courses;
        DOM.statSubjects.textContent = data.total_subjects;
        DOM.statDownloads.textContent = data.total_downloads + '+';

        renderAnalytics(data);
    } catch (e) {
        console.error('Failed loading stats:', e);
    }
}

function renderAnalytics(data) {
    // Popular downloads
    if (DOM.analyticsPopularList) {
        DOM.analyticsPopularList.innerHTML = '';
        if (data.popular && data.popular.length > 0) {
            data.popular.forEach((p, idx) => {
                const row = document.createElement('div');
                row.className = 'popular-row';
                row.innerHTML = `
                    <div>
                        <strong>#${idx + 1} ${escapeHtml(p.title)}</strong>
                        <div style="font-size:0.75rem; color:var(--text-muted)">${escapeHtml(p.subject_name)}</div>
                    </div>
                    <span class="file-type-pill">${p.dl_count || 0} Downloads</span>
                `;
                DOM.analyticsPopularList.appendChild(row);
            });
        } else {
            DOM.analyticsPopularList.innerHTML = '<p class="text-muted">No downloads recorded yet.</p>';
        }
    }

    // Category distribution
    if (DOM.analyticsCategoryBars) {
        DOM.analyticsCategoryBars.innerHTML = '';
        const total = data.total_materials || 1;
        if (data.categories) {
            data.categories.forEach(cat => {
                const percent = Math.round((cat.count / total) * 100);
                const bar = document.createElement('div');
                bar.className = 'bar-row';
                bar.innerHTML = `
                    <div style="display:flex; justify-content:space-between;">
                        <span>${escapeHtml(cat.category)}</span>
                        <span>${cat.count} files (${percent}%)</span>
                    </div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: ${percent}%;"></div>
                    </div>
                `;
                DOM.analyticsCategoryBars.appendChild(bar);
            });
        }
    }
}

// ==================== MATERIALS FETCH & RENDER ====================
async function fetchMaterials() {
    DOM.materialsGrid.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Querying StudyVault repository...</p>
        </div>
    `;
    DOM.emptyState.style.display = 'none';

    try {
        const params = new URLSearchParams();
        if (state.activeFilters.course_id !== 'all') params.append('course_id', state.activeFilters.course_id);
        if (state.activeFilters.semester !== 'all') params.append('semester', state.activeFilters.semester);
        if (state.activeFilters.subject_id !== 'all') params.append('subject_id', state.activeFilters.subject_id);
        if (state.activeFilters.category !== 'all') params.append('category', state.activeFilters.category);
        if (state.activeFilters.q) params.append('q', state.activeFilters.q);
        if (state.activeFilters.sort) params.append('sort', state.activeFilters.sort);

        const res = await fetch(`/api/materials?${params.toString()}`);
        let materials = await res.json();

        if (state.activeFilters.bookmarksOnly) {
            materials = materials.filter(m => m.is_bookmarked);
        }

        state.materials = materials;
        renderMaterials(materials);
        renderAdminMaterialsTable(materials);
        updateActiveFilterTags();
    } catch (e) {
        console.error('Failed fetching materials:', e);
        DOM.materialsGrid.innerHTML = '<p class="text-danger" style="text-align:center; padding:2rem;">Failed to load materials. Please check server.</p>';
    }
}

function renderMaterials(materials) {
    DOM.materialsGrid.innerHTML = '';

    if (materials.length === 0) {
        DOM.emptyState.style.display = 'block';
        return;
    }

    DOM.emptyState.style.display = 'none';

    materials.forEach(m => {
        const card = document.createElement('article');
        card.className = 'material-card';
        card.dataset.materialId = m.material_id;

        let catClass = 'notes';
        if (m.category === 'Previous Year Papers') catClass = 'pyq';
        else if (m.category === 'Lab Manuals') catClass = 'lab';
        else if (m.category === 'Reference Material') catClass = 'ref';

        card.innerHTML = `
            <div>
                <div class="card-top-meta">
                    <div style="display:flex; align-items:center; gap:0.4rem;">
                        <span class="subject-code-badge">${escapeHtml(m.subject_code)}</span>
                        <span class="category-tag ${catClass}">${escapeHtml(m.category)}</span>
                    </div>
                    <button class="bookmark-btn ${m.is_bookmarked ? 'active' : ''}" title="${m.is_bookmarked ? 'Remove from saved' : 'Save note'}" data-id="${m.material_id}">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                        </svg>
                    </button>
                </div>

                <div class="card-content">
                    <div class="card-subject-name">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13">
                            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                        </svg>
                        <span>${escapeHtml(m.subject_name)} • Sem ${m.semester}</span>
                    </div>
                    <h3 class="card-title">${highlightQuery(m.title, state.activeFilters.q)}</h3>
                    <p class="card-desc">${highlightQuery(m.description || 'No description provided for this academic reference.', state.activeFilters.q)}</p>
                </div>
            </div>

            <div>
                <div class="card-meta-bar">
                    <div class="file-spec">
                        <span class="file-type-pill">${escapeHtml(m.file_type || 'PDF')}</span>
                        <span>${escapeHtml(m.file_size || '1.5 MB')}</span>
                    </div>
                    <div class="download-stat" title="Total Verified Downloads">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                        <span class="dl-count-num">${m.download_count || 0}</span>
                    </div>
                </div>

                <div class="card-actions">
                    <button class="btn btn-secondary btn-sm preview-trigger-btn" data-id="${m.material_id}">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                        <span>Preview</span>
                    </button>
                    <a href="/api/materials/${m.material_id}/download" class="btn btn-primary btn-sm direct-download-btn" data-id="${m.material_id}">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                        <span>Download</span>
                    </a>
                </div>
            </div>
        `;

        DOM.materialsGrid.appendChild(card);
    });
}

function highlightQuery(text, query) {
    if (!query || !text) return escapeHtml(text);
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return escapeHtml(text).replace(regex, '<mark style="background:rgba(99,102,241,0.3); color:#fff; padding:0 3px; border-radius:3px;">$1</mark>');
}

function updateActiveFilterTags() {
    DOM.tagsList.innerHTML = '';
    let count = 0;

    if (state.activeFilters.course_id !== 'all') {
        const c = state.courses.find(x => x.course_id == state.activeFilters.course_id);
        if (c) addTag(`Course: ${c.course_code}`, () => setCourseFilter('all'));
        count++;
    }

    if (state.activeFilters.semester !== 'all') {
        addTag(`Semester ${state.activeFilters.semester}`, () => setSemesterFilter('all'));
        count++;
    }

    if (state.activeFilters.subject_id !== 'all') {
        const s = state.subjects.find(x => x.subject_id == state.activeFilters.subject_id);
        if (s) addTag(`Subject: ${s.subject_code}`, () => {
            state.activeFilters.subject_id = 'all';
            DOM.subjectFilterSelect.value = 'all';
            fetchMaterials();
        });
        count++;
    }

    if (state.activeFilters.category !== 'all') {
        addTag(`Type: ${state.activeFilters.category}`, () => setCategoryFilter('all'));
        count++;
    }

    if (state.activeFilters.q) {
        addTag(`Search: "${state.activeFilters.q}"`, () => {
            state.activeFilters.q = '';
            DOM.globalSearchInput.value = '';
            DOM.clearSearchBtn.style.display = 'none';
            fetchMaterials();
        });
        count++;
    }

    if (state.activeFilters.bookmarksOnly) {
        addTag(`Saved Materials`, () => {
            state.activeFilters.bookmarksOnly = false;
            fetchMaterials();
        });
        count++;
    }

    DOM.activeFilterTagsBar.style.display = count > 0 ? 'flex' : 'none';
}

function addTag(label, removeCallback) {
    const chip = document.createElement('div');
    chip.className = 'filter-tag-chip';
    chip.innerHTML = `
        <span>${escapeHtml(label)}</span>
        <button aria-label="Remove filter">&times;</button>
    `;
    chip.querySelector('button').addEventListener('click', removeCallback);
    DOM.tagsList.appendChild(chip);
}

// ==================== FILTER ACTIONS ====================
function setCourseFilter(courseId) {
    state.activeFilters.course_id = courseId;
    document.querySelectorAll('.course-tab').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.courseId == courseId);
    });
    updateSubjectFilterSelect();
    fetchMaterials();
}

function setSemesterFilter(sem) {
    state.activeFilters.semester = sem;
    document.querySelectorAll('.sem-pill').forEach(pill => {
        pill.classList.toggle('active', pill.dataset.sem == sem);
    });
    updateSubjectFilterSelect();
    fetchMaterials();
}

function setCategoryFilter(cat) {
    state.activeFilters.category = cat;
    document.querySelectorAll('.cat-pill').forEach(pill => {
        pill.classList.toggle('active', pill.dataset.cat == cat);
    });
    fetchMaterials();
}

function resetAllFilters() {
    state.activeFilters = {
        course_id: 'all',
        semester: 'all',
        subject_id: 'all',
        category: 'all',
        q: '',
        sort: 'latest',
        bookmarksOnly: false
    };
    DOM.globalSearchInput.value = '';
    DOM.clearSearchBtn.style.display = 'none';
    DOM.sortBySelect.value = 'latest';

    document.querySelectorAll('.course-tab').forEach(b => b.classList.toggle('active', b.dataset.courseId === 'all'));
    document.querySelectorAll('.sem-pill').forEach(p => p.classList.toggle('active', p.dataset.sem === 'all'));
    document.querySelectorAll('.cat-pill').forEach(p => p.classList.toggle('active', p.dataset.cat === 'all'));

    updateSubjectFilterSelect();
    fetchMaterials();
    showToast('Filters reset to default', 'info');
}

// ==================== IN-APP DOCUMENT PREVIEW MODAL ====================
async function openPreviewModal(materialId) {
    try {
        const res = await fetch(`/api/materials/${materialId}`);
        if (!res.ok) {
            showToast('Unable to load document details', 'error');
            return;
        }
        const m = await res.json();

        DOM.previewTitle.textContent = m.title;
        DOM.previewFileType.textContent = m.file_type || 'PDF';
        DOM.previewSubmeta.textContent = `${m.subject_code} • ${m.subject_name}`;
        DOM.previewCourseName.textContent = m.course_name;
        DOM.previewSemester.textContent = `Semester ${m.semester}`;
        DOM.previewUploader.textContent = m.uploader_name;
        DOM.previewSize.textContent = m.file_size || '1.5 MB';
        DOM.previewDownloads.textContent = m.download_count || '0';
        DOM.previewDescription.textContent = m.description || 'Comprehensive syllabus notes prepared for computer science students.';

        const fileUrl = `/${m.file_path}`;
        DOM.previewIframe.src = fileUrl;
        DOM.previewOpenTabBtn.href = fileUrl;
        DOM.previewDownloadBtn.href = `/api/materials/${m.material_id}/download`;
        DOM.previewDownloadBtn.onclick = () => {
            // Track download increment locally
            setTimeout(() => {
                const num = parseInt(DOM.previewDownloads.textContent, 10) || 0;
                DOM.previewDownloads.textContent = num + 1;
                loadStats();
            }, 800);
        };

        DOM.previewModal.classList.add('show');
    } catch (e) {
        showToast('Error opening document preview', 'error');
    }
}

function closePreviewModal() {
    DOM.previewModal.classList.remove('show');
    DOM.previewIframe.src = '';
}

// ==================== BOOKMARK TOGGLE ====================
async function toggleBookmark(materialId, btnElement) {
    if (!state.user) {
        showToast('Please sign in to save materials', 'info');
        openAuthModal('login');
        return;
    }

    try {
        const res = await fetch(`/api/materials/${materialId}/bookmark`, { method: 'POST' });
        const data = await res.json();
        if (res.ok) {
            btnElement.classList.toggle('active', data.bookmarked);
            showToast(data.message, 'success');
        } else {
            showToast(data.error || 'Failed to update bookmark', 'error');
        }
    } catch (e) {
        showToast('Error saving bookmark', 'error');
    }
}

function openAdminModal() {
    if (!state.user || state.user.role !== 'admin') {
        showToast('Access Denied: Study material upload is restricted to Faculty / Admins.', 'error');
        openAuthModal('admin-login');
        return;
    }
    DOM.adminModal.classList.add('show');
    renderCoursesManageList();
    renderSubjectsManageList();
    renderAdminMaterialsTable(state.materials);
}

function closeAdminModal() {
    DOM.adminModal.classList.remove('show');
}

function renderAdminMaterialsTable(materials) {
    if (!DOM.adminMaterialsTableBody) return;
    DOM.adminMaterialsTableBody.innerHTML = '';
    DOM.adminMaterialsCounter.textContent = `${materials.length} items`;

    materials.forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <div style="font-weight:600; color:var(--text-primary);">${escapeHtml(m.title)}</div>
                <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(m.file_name)} • ${m.file_size}</div>
            </td>
            <td><span class="subject-code-badge">${escapeHtml(m.subject_code)}</span></td>
            <td>${escapeHtml(m.course_code)}</td>
            <td><span class="category-tag notes">${escapeHtml(m.category)}</span></td>
            <td><strong>${m.download_count}</strong></td>
            <td>${m.uploaded_at ? m.uploaded_at.split(' ')[0] : 'Today'}</td>
            <td>
                <button class="btn-icon-danger delete-material-btn" data-id="${m.material_id}" title="Delete Material">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            </td>
        `;
        DOM.adminMaterialsTableBody.appendChild(tr);
    });
}

function renderCoursesManageList() {
    if (!DOM.coursesManageList) return;
    DOM.coursesManageList.innerHTML = '';
    state.courses.forEach(c => {
        const item = document.createElement('div');
        item.className = 'manage-item-card';
        item.innerHTML = `
            <div>
                <div class="manage-item-title">${escapeHtml(c.course_name)} <span class="subject-code-badge">${escapeHtml(c.course_code)}</span></div>
                <div class="manage-item-sub">${c.subject_count || 0} Subjects • ${c.material_count || 0} Materials</div>
            </div>
            <button class="btn-icon-danger delete-course-btn" data-id="${c.course_id}" title="Delete Course">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
            </button>
        `;
        DOM.coursesManageList.appendChild(item);
    });
}

function renderSubjectsManageList() {
    if (!DOM.subjectsManageList) return;
    DOM.subjectsManageList.innerHTML = '';
    state.subjects.forEach(s => {
        const item = document.createElement('div');
        item.className = 'manage-item-card';
        item.innerHTML = `
            <div>
                <div class="manage-item-title">${escapeHtml(s.subject_name)} <span class="subject-code-badge">${escapeHtml(s.subject_code)}</span></div>
                <div class="manage-item-sub">${escapeHtml(s.course_code)} • Sem ${s.semester} • ${s.material_count || 0} Materials</div>
            </div>
            <button class="btn-icon-danger delete-subject-btn" data-id="${s.subject_id}" title="Delete Subject">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
            </button>
        `;
        DOM.subjectsManageList.appendChild(item);
    });
}

// ==================== AUTH MODAL ====================
function openAuthModal(tab = 'login') {
    DOM.authModal.classList.add('show');
    if (tab === 'admin-login') {
        switchAuthTab('login');
        document.getElementById('authModalTitle').textContent = 'Faculty & Admin Sign In';
        document.getElementById('loginEmail').value = 'admin@studyvault.ac.in';
        document.getElementById('loginPassword').value = '';
        setTimeout(() => document.getElementById('loginPassword').focus(), 150);
    } else {
        switchAuthTab(tab);
    }
}

function closeAuthModal() {
    DOM.authModal.classList.remove('show');
}

function switchAuthTab(tab) {
    if (tab === 'login') {
        DOM.tabShowLogin.classList.add('active');
        DOM.tabShowRegister.classList.remove('active');
        DOM.loginForm.style.display = 'flex';
        DOM.registerForm.style.display = 'none';
        document.getElementById('authModalTitle').textContent = 'Sign In to StudyVault';
    } else {
        DOM.tabShowRegister.classList.add('active');
        DOM.tabShowLogin.classList.remove('active');
        DOM.registerForm.style.display = 'flex';
        DOM.loginForm.style.display = 'none';
        document.getElementById('authModalTitle').textContent = 'Create Academic Account';
    }
}

// ==================== EVENT LISTENERS ====================
function setupEventListeners() {
    // Theme toggle
    DOM.themeToggleBtn.addEventListener('click', toggleTheme);

    // Global Search with debounce
    let searchTimer = null;
    DOM.globalSearchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimer);
        const val = e.target.value.trim();
        DOM.clearSearchBtn.style.display = val ? 'block' : 'none';
        searchTimer = setTimeout(() => {
            state.activeFilters.q = val;
            fetchMaterials();
        }, 280);
    });

    DOM.clearSearchBtn.addEventListener('click', () => {
        DOM.globalSearchInput.value = '';
        DOM.clearSearchBtn.style.display = 'none';
        state.activeFilters.q = '';
        fetchMaterials();
    });

    // Keyboard shortcut '/' to search
    window.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== DOM.globalSearchInput && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
            e.preventDefault();
            DOM.globalSearchInput.focus();
        }
        if (e.key === 'Escape') {
            closePreviewModal();
            closeAdminModal();
            closeAuthModal();
            DOM.userDropdown.classList.remove('show');
        }
    });

    // Admin Login button in header
    if (DOM.adminLoginBtn) {
        DOM.adminLoginBtn.addEventListener('click', () => openAuthModal('admin-login'));
    }

    // Admin console triggers (Strictly protected)
    DOM.openAdminPanelBtn.addEventListener('click', openAdminModal);
    if (DOM.heroUploadBtn) {
        DOM.heroUploadBtn.addEventListener('click', () => {
            if (!state.user || state.user.role !== 'admin') {
                showToast('Access Denied: Only Administrator accounts can upload study materials.', 'error');
                openAuthModal('admin-login');
            } else {
                openAdminModal();
            }
        });
    }

    if (DOM.heroSavedNotesBtn) {
        DOM.heroSavedNotesBtn.addEventListener('click', () => {
            state.activeFilters.bookmarksOnly = true;
            fetchMaterials();
            showToast('Showing your saved bookmarks', 'info');
            document.getElementById('materialsBrowseSection').scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Browse button scroll
    DOM.browseNowBtn.addEventListener('click', () => {
        document.getElementById('materialsBrowseSection').scrollIntoView({ behavior: 'smooth' });
    });

    // Solved PYQs filter button
    DOM.viewPyqBtn.addEventListener('click', () => {
        setCategoryFilter('Previous Year Papers');
        document.getElementById('materialsBrowseSection').scrollIntoView({ behavior: 'smooth' });
    });

    // User profile menu toggle
    DOM.userProfileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        DOM.userDropdown.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!DOM.userMenuWrap.contains(e.target)) {
            DOM.userDropdown.classList.remove('show');
        }
    });

    // Logout
    DOM.logoutBtn.addEventListener('click', async () => {
        await fetch('/api/auth/logout', { method: 'POST' });
        state.user = null;
        localStorage.removeItem('studyvault_user_id');
        localStorage.removeItem('studyvault_user');
        updateUserUI();
        DOM.userDropdown.classList.remove('show');
        showToast('Signed out successfully.', 'info');
        fetchMaterials();
    });

    // Filter my bookmarks
    DOM.filterMyBookmarksBtn.addEventListener('click', () => {
        state.activeFilters.bookmarksOnly = true;
        DOM.userDropdown.classList.remove('show');
        fetchMaterials();
        showToast('Showing your saved bookmarks', 'info');
    });

    // Reset demo database
    DOM.resetDemoBtn.addEventListener('click', async () => {
        DOM.userDropdown.classList.remove('show');
        showToast('Restoring academic sample data...', 'info');
        try {
            const res = await fetch('/api/system/reset-demo', { method: 'POST' });
            if (res.ok) {
                showToast('Demo data restored successfully!', 'success');
                await Promise.all([loadCourses(), loadSubjects(), loadStats()]);
                fetchMaterials();
            }
        } catch (e) {
            showToast('Failed to reset demo data', 'error');
        }
    });

    // Auth modal triggers
    DOM.openAuthModalBtn.addEventListener('click', () => openAuthModal('login'));
    DOM.closeAuthModalBtn.addEventListener('click', closeAuthModal);
    DOM.tabShowLogin.addEventListener('click', () => switchAuthTab('login'));
    DOM.tabShowRegister.addEventListener('click', () => switchAuthTab('register'));

    // Perform Login Function
    async function performLogin(email, password) {
        try {
            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            if (res.ok) {
                state.user = data.user;
                localStorage.setItem('studyvault_user_id', data.user.user_id);
                localStorage.setItem('studyvault_user', JSON.stringify(data.user));
                updateUserUI();
                closeAuthModal();
                showToast(`Welcome back, ${data.user.full_name}!`, 'success');
                await fetchMaterials();
                if (data.user.role === 'admin') {
                    setTimeout(() => openAdminModal(), 200);
                }
            } else {
                showToast(data.error || 'Login failed. Check email & password.', 'error');
            }
        } catch (err) {
            showToast('Network error during sign in', 'error');
        }
    }

    // Instant One-Click Admin Sign-In Button
    if (DOM.instantAdminLoginBtn) {
        DOM.instantAdminLoginBtn.addEventListener('click', () => {
            performLogin('admin@studyvault.ac.in', 'admin123');
        });
    }

    // Quick fill credentials triggers
    DOM.fillAdminDemo.addEventListener('click', () => {
        performLogin('admin@studyvault.ac.in', 'admin123');
    });
    DOM.fillStudentDemo.addEventListener('click', () => {
        performLogin('aarav.cs@student.ac.in', 'student123');
    });

    // Login form submit
    DOM.loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;
        await performLogin(email, password);
    });

    // Register form submit
    DOM.registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const full_name = document.getElementById('regFullName').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;
        const role = 'student';

        try {
            const res = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_name, email, password, role })
            });
            const data = await res.json();
            if (res.ok) {
                state.user = data.user;
                localStorage.setItem('studyvault_user_id', data.user.user_id);
                localStorage.setItem('studyvault_user', JSON.stringify(data.user));
                updateUserUI();
                closeAuthModal();
                showToast('Account registered successfully!', 'success');
                fetchMaterials();
                loadStats();
            } else {
                showToast(data.error || 'Registration failed', 'error');
            }
        } catch (err) {
            showToast('Network error during registration', 'error');
        }
    });

    // Course Tabs Delegation
    DOM.courseTabsContainer.addEventListener('click', (e) => {
        const tab = e.target.closest('.course-tab');
        if (tab) {
            setCourseFilter(tab.dataset.courseId);
        }
    });

    // Semester Pills Delegation
    DOM.semesterPillsContainer.addEventListener('click', (e) => {
        const pill = e.target.closest('.sem-pill');
        if (pill) {
            setSemesterFilter(pill.dataset.sem);
        }
    });

    // Category Pills Delegation
    DOM.categoryPillsContainer.addEventListener('click', (e) => {
        const pill = e.target.closest('.cat-pill');
        if (pill) {
            setCategoryFilter(pill.dataset.cat);
        }
    });

    // Subject Dropdown
    DOM.subjectFilterSelect.addEventListener('change', (e) => {
        state.activeFilters.subject_id = e.target.value;
        fetchMaterials();
    });

    // Sort Dropdown
    DOM.sortBySelect.addEventListener('change', (e) => {
        state.activeFilters.sort = e.target.value;
        fetchMaterials();
    });

    // View toggles
    DOM.viewGridBtn.addEventListener('click', () => {
        DOM.viewGridBtn.classList.add('active');
        DOM.viewListBtn.classList.remove('active');
        DOM.materialsGrid.classList.remove('list-view');
    });

    DOM.viewListBtn.addEventListener('click', () => {
        DOM.viewListBtn.classList.add('active');
        DOM.viewGridBtn.classList.remove('active');
        DOM.materialsGrid.classList.add('list-view');
    });

    // Clear filters
    DOM.clearAllFiltersBtn.addEventListener('click', resetAllFilters);
    DOM.emptyResetBtn.addEventListener('click', resetAllFilters);

    // Card delegation (preview, download, bookmark)
    DOM.materialsGrid.addEventListener('click', (e) => {
        const previewBtn = e.target.closest('.preview-trigger-btn');
        if (previewBtn) {
            openPreviewModal(previewBtn.dataset.id);
            return;
        }

        const bookmarkBtn = e.target.closest('.bookmark-btn');
        if (bookmarkBtn) {
            e.stopPropagation();
            toggleBookmark(bookmarkBtn.dataset.id, bookmarkBtn);
            return;
        }

        const dlBtn = e.target.closest('.direct-download-btn');
        if (dlBtn) {
            // increment live counter on card
            const countEl = dlBtn.closest('.material-card').querySelector('.dl-count-num');
            if (countEl) {
                countEl.textContent = (parseInt(countEl.textContent, 10) || 0) + 1;
            }
            setTimeout(loadStats, 800);
            return;
        }

        const card = e.target.closest('.material-card');
        if (card && !e.target.closest('a') && !e.target.closest('button')) {
            openPreviewModal(card.dataset.materialId);
        }
    });

    // Modal Close
    DOM.closePreviewModalBtn.addEventListener('click', closePreviewModal);
    DOM.closePreviewFooterBtn.addEventListener('click', closePreviewModal);
    DOM.previewModal.addEventListener('click', (e) => {
        if (e.target === DOM.previewModal) closePreviewModal();
    });

    DOM.closeAdminModalBtn.addEventListener('click', closeAdminModal);
    DOM.adminModal.addEventListener('click', (e) => {
        if (e.target === DOM.adminModal) closeAdminModal();
    });

    DOM.authModal.addEventListener('click', (e) => {
        if (e.target === DOM.authModal) closeAuthModal();
    });

    // Admin Console Tabs
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.admin-tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.admin-tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const target = document.getElementById(btn.dataset.tab);
            if (target) target.classList.add('active');
        });
    });

    // Admin upload: dynamic subject chaining by course and semester
    function updateUploadSubjectOptions() {
        const courseId = DOM.uploadCourseSelect.value;
        const sem = DOM.uploadSemesterSelect.value;
        DOM.uploadSubjectSelect.innerHTML = '<option value="">Select Subject...</option>';

        if (!courseId || !sem) return;

        const filtered = state.subjects.filter(s => s.course_id == courseId && s.semester == sem);
        if (filtered.length === 0) {
            DOM.uploadSubjectSelect.innerHTML = '<option value="">No subjects found for this semester</option>';
            return;
        }
        filtered.forEach(s => {
            DOM.uploadSubjectSelect.appendChild(new Option(`${s.subject_code} - ${s.subject_name}`, s.subject_id));
        });
    }

    DOM.uploadCourseSelect.addEventListener('change', updateUploadSubjectOptions);
    DOM.uploadSemesterSelect.addEventListener('change', updateUploadSubjectOptions);

    // Drag and drop file upload
    const dropZone = DOM.fileDropZone;
    const fileInput = DOM.materialFileInput;

    ['dragenter', 'dragover'].forEach(name => {
        dropZone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(name => {
        dropZone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            DOM.dropZoneTitle.textContent = `Attached: ${e.dataTransfer.files[0].name}`;
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files && fileInput.files.length > 0) {
            DOM.dropZoneTitle.textContent = `Attached: ${fileInput.files[0].name}`;
        }
    });

    // Upload Study Material Form Submit
    DOM.uploadMaterialForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const submitBtn = document.getElementById('uploadSubmitBtn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<div class="spinner" style="width:16px;height:16px;margin:0 6px 0 0;display:inline-block;"></div> Uploading...';

        const formData = new FormData(DOM.uploadMaterialForm);
        const headers = {};
        const uid = localStorage.getItem('studyvault_user_id');
        if (uid) headers['Authorization'] = `Bearer ${uid}`;

        try {
            const res = await fetch('/api/materials', {
                method: 'POST',
                headers: headers,
                body: formData
            });
            const data = await res.json();
            if (res.ok) {
                showToast('Study Material published to repository!', 'success');
                DOM.uploadMaterialForm.reset();
                DOM.dropZoneTitle.innerHTML = 'Drag &amp; drop study file here, or <span class="browse-link">browse</span>';
                await fetchMaterials();
                await loadStats();
                closeAdminModal();
            } else {
                showToast(data.error || 'Upload failed', 'error');
            }
        } catch (err) {
            showToast('Network error during file upload', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                <span>Publish Study Material</span>
            `;
        }
    });

    // Admin Delete Material
    DOM.adminMaterialsTableBody.addEventListener('click', async (e) => {
        const delBtn = e.target.closest('.delete-material-btn');
        if (delBtn) {
            if (!confirm('Are you sure you want to delete this study material?')) return;
            const matId = delBtn.dataset.id;
            try {
                const res = await fetch(`/api/materials/${matId}`, { method: 'DELETE' });
                if (res.ok) {
                    showToast('Material removed from repository', 'info');
                    await fetchMaterials();
                    await loadStats();
                }
            } catch (err) {
                showToast('Failed to delete material', 'error');
            }
        }
    });

    // Add Course Form Submit
    DOM.addCourseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const course_name = DOM.newCourseName.value.trim();
        const course_code = DOM.newCourseCode.value.trim().toUpperCase();
        const description = DOM.newCourseDesc.value.trim();

        try {
            const res = await fetch('/api/courses', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ course_name, course_code, description })
            });
            const data = await res.json();
            if (res.ok) {
                showToast(`Course ${course_code} added!`, 'success');
                DOM.addCourseForm.reset();
                await loadCourses();
                renderCoursesManageList();
                await loadStats();
            } else {
                showToast(data.error || 'Failed to add course', 'error');
            }
        } catch (err) {
            showToast('Error adding course', 'error');
        }
    });

    // Delete Course
    DOM.coursesManageList.addEventListener('click', async (e) => {
        const delBtn = e.target.closest('.delete-course-btn');
        if (delBtn) {
            if (!confirm('Delete this course and all its subjects & study materials?')) return;
            const cid = delBtn.dataset.id;
            try {
                const res = await fetch(`/api/courses/${cid}`, { method: 'DELETE' });
                if (res.ok) {
                    showToast('Course deleted', 'info');
                    await loadCourses();
                    await loadSubjects();
                    renderCoursesManageList();
                    fetchMaterials();
                    loadStats();
                }
            } catch (err) {
                showToast('Failed to delete course', 'error');
            }
        }
    });

    // Add Subject Form Submit
    DOM.addSubjectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const course_id = DOM.newSubjectCourse.value;
        const semester = DOM.newSubjectSem.value;
        const subject_code = DOM.newSubjectCode.value.trim().toUpperCase();
        const subject_name = DOM.newSubjectName.value.trim();

        try {
            const res = await fetch('/api/subjects', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ course_id, semester, subject_code, subject_name })
            });
            const data = await res.json();
            if (res.ok) {
                showToast(`Subject ${subject_code} added!`, 'success');
                DOM.addSubjectForm.reset();
                await loadSubjects();
                renderSubjectsManageList();
                await loadStats();
            } else {
                showToast(data.error || 'Failed to add subject', 'error');
            }
        } catch (err) {
            showToast('Error adding subject', 'error');
        }
    });

    // Delete Subject
    DOM.subjectsManageList.addEventListener('click', async (e) => {
        const delBtn = e.target.closest('.delete-subject-btn');
        if (delBtn) {
            if (!confirm('Delete this subject and its study materials?')) return;
            const sid = delBtn.dataset.id;
            try {
                const res = await fetch(`/api/subjects/${sid}`, { method: 'DELETE' });
                if (res.ok) {
                    showToast('Subject deleted', 'info');
                    await loadSubjects();
                    renderSubjectsManageList();
                    fetchMaterials();
                    loadStats();
                }
            } catch (err) {
                showToast('Failed to delete subject', 'error');
            }
        }
    });

    // Quick links in footer
    document.querySelectorAll('.quick-course-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const code = link.dataset.course;
            const c = state.courses.find(x => x.course_code === code);
            if (c) {
                setCourseFilter(c.course_id);
                document.getElementById('materialsBrowseSection').scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Helper: Escape HTML
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
