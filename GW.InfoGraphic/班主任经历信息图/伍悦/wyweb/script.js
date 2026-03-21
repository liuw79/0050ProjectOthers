document.addEventListener('DOMContentLoaded', () => {
    // Music Control
    const musicControl = document.getElementById('music-control');
    const bgm = document.getElementById('bgm');
    const playHint = musicControl.querySelector('.play-hint');

    // Function to update hint text
    const updateHint = (text) => {
        if (playHint) playHint.textContent = text;
    };

    // Initialize state
    updateHint('点击播放 · 许巍《家》');
    
    musicControl.addEventListener('click', () => {
        // Normal toggle logic
        if (bgm.paused) {
            bgm.play();
            musicControl.classList.add('playing');
            updateHint('点击暂停 · 许巍《家》');
        } else {
            bgm.pause();
            musicControl.classList.remove('playing');
            updateHint('点击播放 · 许巍《家》');
        }
    });

    // Add timestamp to prevent caching
    fetch('data.json?t=' + new Date().getTime())
        .then(response => response.json())
        .then(data => {
            console.log("Data loaded:", data); // Debug
            renderSummary(data.summary);
            renderTimeline(data.timeline);
            renderNewCourses(data.new_courses_by_year);
            renderTermMilestones(data.term_milestones);
            renderTeachers(data.teacher_first_met);
        })
        .catch(error => console.error('Error loading data:', error));
});

function renderSummary(summary) {
    const container = document.getElementById('metrics-container');
    
    const metrics = [
        { label: '服务期数', value: summary.total_sessions, suffix: '期' },
        { label: '服务学员', value: summary.total_students.toLocaleString(), suffix: '人' },
        { label: '服务企业', value: summary.total_companies.toLocaleString(), suffix: '家' },
        { label: '涉及课程', value: summary.course_count, suffix: '门' }
    ];

    if (container) {
        container.innerHTML = metrics.map(m => `
            <div class="metric-card">
                <span class="metric-value">${m.value}</span>
                <span class="metric-label">${m.label}</span>
            </div>
        `).join('');
    }
    
    const teacherCountEl = document.getElementById('teacher-count');
    if (teacherCountEl) teacherCountEl.textContent = summary.teacher_count;

    const newCourseCountEl = document.getElementById('new-course-count');
    if (newCourseCountEl) newCourseCountEl.textContent = summary.new_course_count;
}

function renderTimeline(timeline) {
    const container = document.getElementById('timeline-container');
    if (!container) return;
    
    container.innerHTML = timeline.map(item => {
        if (item.type === 'summary') {
            return `
                <div class="timeline-year-summary">
                    <span class="year-label">${item.year}</span>
                    ${item.desc ? `<p>${item.desc}</p>` : ''}
                </div>
            `;
        } else {
            return `
                <div class="timeline-item ${item.type}">
                    <div class="date">${item.date}</div>
                    <div class="content">
                        <h3>${item.title}</h3>
                        ${item.desc ? `<p>${item.desc}</p>` : ''}
                    </div>
                </div>
            `;
        }
    }).join('');
}

function renderNewCourses(coursesByYear) {
    const container = document.getElementById('new-course-grid');
    
    // Reverse chronological order for art
    coursesByYear.sort((a, b) => b.year - a.year);
    
    const palette = [
        '#e3f2fd', '#e8f5e9', '#fff3e0', '#fce4ec', 
        '#f3e5f5', '#e0f7fa', '#f1f8e9', '#fff8e1'
    ];
    
    container.innerHTML = coursesByYear.map((yearGroup, index) => `
        <div class="year-group">
            <div class="year-label">${yearGroup.year}</div>
            <div class="course-list">
                ${yearGroup.courses.map(course => {
                    // Hash string to pick a consistent color
                    let hash = 0;
                    for (let i = 0; i < course.length; i++) hash = course.charCodeAt(i) + ((hash << 5) - hash);
                    const colorIndex = Math.abs(hash) % palette.length;
                    const bg = palette[colorIndex];
                    
                    return `<span class="course-pill" style="background-color: ${bg}; border-color: transparent;">${course}</span>`;
                }).join('')}
            </div>
        </div>
    `).join('');
}

function renderTermMilestones(milestones) {
    const container = document.getElementById('term-milestone-grid');
    
    // Sort by term number (descending importance) or date
    // Let's sort by date
    milestones.sort((a, b) => new Date(a.date) - new Date(b.date));
    
    // Only show significant ones to save space or layout them in a grid
    // Filter for >= 10
    const significant = milestones.filter(m => parseInt(m.term) >= 10);
    
    container.innerHTML = significant.map(m => `
        <div class="milestone-card term-${m.term}">
            <div class="term-badge">第${m.term}期</div>
            <div class="course-name">${m.course}</div>
            <div class="date">${m.date}</div>
        </div>
    `).join('');
}

function renderTeachers(teachers) {
    const container = document.getElementById('teacher-grid');
    teachers.sort((a, b) => new Date(a.date) - new Date(b.date));

    // Group by year
    const teachersByYear = {};
    teachers.forEach(t => {
        const year = t.date.split('/')[0];
        if (!teachersByYear[year]) teachersByYear[year] = [];
        teachersByYear[year].push(t.teacher);
    });

    container.innerHTML = Object.keys(teachersByYear).sort().map(year => `
        <div class="teacher-year-group">
            <div class="year-badge">
                <span class="icon">🤝</span> ${year}
            </div>
            <div class="teacher-list">
                ${teachersByYear[year].map(name => `<span class="teacher-name">${name}</span>`).join('')}
            </div>
        </div>
    `).join('');
}
