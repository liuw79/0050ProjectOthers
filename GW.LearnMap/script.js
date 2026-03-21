// JavaScript 代码将在此处添加，用于加载和处理课程数据

// Store loaded data or error for debugging
let debugData = { error: null, firstCourse: null, allCoursesLoaded: false };

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');
    loadAndDisplayCourses('courses.json'); // Fetch courses.json (plural) again, matching current file listing
    setupDebugButton(); // Setup debug button listener regardless of load success
});

async function loadAndDisplayCourses(jsonPath) {
    const container = document.getElementById('course-table-container');
    try {
        const response = await fetch(jsonPath);
        if (!response.ok) {
            // Store detailed error info
            const errorText = await response.text(); // Attempt to get response body
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}. Response: ${errorText.substring(0, 200)}`);
        }
        const allCourses = await response.json();

        if (allCourses && Array.isArray(allCourses) && allCourses.length > 0) {
            // Store first course for debugging
            debugData.firstCourse = allCourses[0];
            debugData.allCoursesLoaded = true;
            debugData.error = null;
            console.log("Successfully loaded courses data. First course:", debugData.firstCourse);

            // Render all courses (restored original logic)
            renderTable(allCourses, container);
            setupExportButton();
        } else {
             const warningMsg = 'Loaded data is not a non-empty array or JSON format is incorrect.';
             container.innerHTML = `<p>${warningMsg}</p>`;
             console.warn(warningMsg, allCourses);
             // Store this info for debugging
             debugData.error = new Error(warningMsg);
             debugData.firstCourse = allCourses; // Store whatever was loaded
             debugData.allCoursesLoaded = false;
        }
    } catch (error) {
        console.error('Error loading or parsing course data:', error);
        container.innerHTML = `<p style="color: red;">加载课程数据失败: ${error.message}</p>`;
        // Store the error for debugging
        debugData.error = error;
        debugData.firstCourse = null;
        debugData.allCoursesLoaded = false;
    }
}

function renderTable(courses, container) {
    if (!courses || courses.length === 0) {
        container.innerHTML = '<p>没有找到课程数据。</p>';
        return;
    }

    container.innerHTML = ''; // Clear loading message

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Create header row
    const headerRow = document.createElement('tr');
    const selectHeader = document.createElement('th');
    selectHeader.textContent = '选择';
    headerRow.appendChild(selectHeader);

    // Use the keys from the first course object as headers (excluding 'schedules')
    const headers = Object.keys(courses[0])
                          .filter(key => key !== 'schedules');
    headers.push('上课安排'); // Add dedicated schedule header

    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);

    // Create data rows
    courses.forEach(course => {
        const row = document.createElement('tr');

        // Add checkbox cell
        const selectCell = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        const courseName = course['课程名称'] || '';
        checkbox.value = courseName;
        checkbox.name = 'selected_course';
        selectCell.appendChild(checkbox);
        row.appendChild(selectCell);

        // Add data cells based on headers (excluding '上课安排')
        const originalHeaders = headers.filter(h => h !== '上课安排');
        originalHeaders.forEach(header => {
            const cell = document.createElement('td');
            const content = course[header] || '';
            const isLongTextColumn = ['课程名称', '老师简介', '适学对象', '课程价值'].includes(header);
            const maxLength = 60;

            if (isLongTextColumn && typeof content === 'string' && content.length > maxLength) {
                // Handle long text with expand/collapse
                const contentDiv = document.createElement('div');
                contentDiv.classList.add('collapsible-content');
                const shortTextSpan = document.createElement('span');
                shortTextSpan.textContent = content.substring(0, maxLength);
                contentDiv.appendChild(shortTextSpan);
                const fullTextSpan = document.createElement('span');
                fullTextSpan.textContent = content.substring(maxLength);
                fullTextSpan.style.display = 'none';
                contentDiv.appendChild(fullTextSpan);
                const toggleLink = document.createElement('span');
                toggleLink.textContent = '... 查看更多';
                toggleLink.classList.add('toggle-link');
                toggleLink.addEventListener('click', () => {
                    const isExpanded = fullTextSpan.style.display !== 'none';
                    fullTextSpan.style.display = isExpanded ? 'none' : 'inline';
                    toggleLink.textContent = isExpanded ? '... 查看更多' : ' 收起';
                });
                contentDiv.appendChild(toggleLink);
                cell.appendChild(contentDiv);
            } else {
                cell.textContent = typeof content === 'string' ? content : JSON.stringify(content);
            }
            row.appendChild(cell);
        });

        // Add combined schedule cell
        const scheduleCell = document.createElement('td');
        if (course.schedules && Array.isArray(course.schedules)) {
             scheduleCell.innerHTML = course.schedules
                 .map(s => `${s.date || ''}${s.date && s.city ? ' / ' : ''}${s.city || ''}`.trim())
                 .filter(Boolean)
                 .join('<br>');
        }
        row.appendChild(scheduleCell);

        tbody.appendChild(row);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    container.appendChild(table);
}

function setupExportButton() {
    const exportBtn = document.getElementById('export-selected-btn');
    if (!exportBtn) {
        console.error('Export button not found!');
        return;
    }

    exportBtn.addEventListener('click', () => {
        const selectedCheckboxes = document.querySelectorAll('input[name="selected_course"]:checked');
        const selectedCourseNames = [];

        selectedCheckboxes.forEach(checkbox => {
            selectedCourseNames.push(checkbox.value);
        });

        if (selectedCourseNames.length > 0) {
            alert('已选课程:\n\n' + selectedCourseNames.join('\n'));
        } else {
            alert('请先勾选您需要选择的课程。');
        }
    });
}

// New function to setup the debug button
function setupDebugButton() {
    const debugBtn = document.getElementById('debug-info-btn');
    if (!debugBtn) {
        console.error('Debug button not found!');
        return;
    }

    debugBtn.addEventListener('click', async () => {
        let infoToCopy = ''
        if (debugData.error) {
            infoToCopy = `数据加载/解析错误:\n${debugData.error.stack || debugData.error.message}`;
            if (debugData.firstCourse) { // Include raw loaded data if error occurred after loading
                try {
                     infoToCopy += `\n\n原始加载内容 (部分):\n${JSON.stringify(debugData.firstCourse, null, 2).substring(0, 1000)}...`;
                } catch {}
            }
        } else if (debugData.allCoursesLoaded && debugData.firstCourse) {
            infoToCopy = '数据加载成功。第一个课程对象内容:\n\n';
            try {
                infoToCopy += JSON.stringify(debugData.firstCourse, null, 2); // Pretty print JSON
            } catch (e) {
                infoToCopy += '无法序列化第一个课程对象。'
            }
        } else {
            infoToCopy = '调试信息尚未准备好或加载未完成。'
        }

        try {
            await navigator.clipboard.writeText(infoToCopy);
            alert('调试信息已复制到剪贴板！请将其粘贴给我。');
        } catch (err) {
            console.error('无法复制到剪贴板: ', err);
            alert('无法自动复制调试信息，请手动从控制台获取错误信息或数据。');
            // Fallback: Log to console if copy fails
            console.log("--- 调试信息 ---", infoToCopy);
        }
    });
}

// Optional: Function to display selected courses in a div
// function displaySelectedCourses(courseNames) {
//     let outputDiv = document.getElementById('selected-courses-output');
//     if (!outputDiv) {
//         outputDiv = document.createElement('div');
//         outputDiv.id = 'selected-courses-output';
//         outputDiv.style.marginTop = '20px';
//         outputDiv.style.padding = '15px';
//         outputDiv.style.border = '1px solid #ccc';
//         // Insert after the button
//         document.getElementById('export-selected-btn').parentNode.after(outputDiv);
//     }
//     outputDiv.innerHTML = '<h3>已选课程:</h3><ul>' +
//                           courseNames.map(name => `<li>${name}</li>`).join('') +
//                           '</ul>';
// }

// function loadCourseData() {
//     // 实现数据加载逻辑
// } 