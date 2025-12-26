// Admin Dashboard functionality

// Check if admin is logged in
if (!requireAuth()) {
    window.location.href = 'login.html';
}

// Check if user is admin (you can add this check based on email or role)
const currentUser = API.getUser();
if (!currentUser) {
    window.location.href = 'login.html';
}

// Display admin name
document.getElementById('adminName').textContent = currentUser.full_name;

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadPendingUsers();
    setupMenuNavigation();
    setupFilters();
});

// Menu Navigation
function setupMenuNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const section = item.dataset.section;
            switchSection(section);
        });
    });
}

function switchSection(sectionName) {
    // Update menu active state
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.section === sectionName) {
            item.classList.add('active');
        }
    });

    // Update content sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionName).classList.add('active');

    // Load section data
    switch (sectionName) {
        case 'overview':
            loadStats();
            break;
        case 'pending':
            loadPendingUsers();
            break;
        case 'users':
            loadAllUsers();
            break;
        case 'students':
            loadStudents();
            break;
        case 'alumni':
            loadAlumni();
            break;
    }
}

// Load Statistics
async function loadStats() {
    try {
        const stats = await API.admin.getStats();

        // Update stat cards
        document.getElementById('totalUsers').textContent = stats.total_users || 0;
        document.getElementById('verifiedUsers').textContent = stats.verified_users || 0;
        document.getElementById('pendingUsers').textContent = stats.pending_users || 0;
        document.getElementById('alumniCount').textContent = stats.total_alumni || 0;

        // Update badge
        document.getElementById('pendingBadge').textContent = stats.pending_users || 0;

    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load Pending Users
async function loadPendingUsers() {
    const grid = document.getElementById('pendingUsersGrid');
    grid.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';

    try {
        const response = await API.admin.getPendingUsers();
        const users = response.users || [];

        // Update badge
        document.getElementById('pendingBadge').textContent = users.length;

        if (users.length === 0) {
            grid.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-check-circle"></i>
                    <p>No pending users to verify</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = users.map(user => createUserCard(user, true)).join('');

    } catch (error) {
        console.error('Error loading pending users:', error);
        grid.innerHTML = `<div class="error">Error loading users: ${error.message}</div>`;
    }
}

// Create User Card
function createUserCard(user, isPending = false) {
    const typeClass = user.user_type === 'student' ? 'student' : 'alumni';
    const statusBadge = user.is_verified ?
        '<span class="status-badge verified">Verified</span>' :
        '<span class="status-badge pending">Pending</span>';

    return `
        <div class="user-card">
            <div class="user-header">
                <div class="user-info">
                    <h3>${user.full_name}</h3>
                    <p>${user.email}</p>
                </div>
                <span class="user-badge ${typeClass}">${user.user_type}</span>
            </div>
            
            <div class="user-details">
                <div class="detail-row">
                    <span class="detail-label">College ID:</span>
                    <span class="detail-value">${user.college_id}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">College Email:</span>
                    <span class="detail-value">${user.college_email}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Department:</span>
                    <span class="detail-value">${user.department}</span>
                </div>
                ${user.user_type === 'student' ? `
                    <div class="detail-row">
                        <span class="detail-label">Current Year:</span>
                        <span class="detail-value">Year ${user.current_year || 'N/A'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Passing Year:</span>
                        <span class="detail-value">${user.expected_passing_year || 'N/A'}</span>
                    </div>
                ` : `
                    <div class="detail-row">
                        <span class="detail-label">Passing Year:</span>
                        <span class="detail-value">${user.passing_year || 'N/A'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Company:</span>
                        <span class="detail-value">${user.current_company || 'N/A'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Position:</span>
                        <span class="detail-value">${user.current_position || 'N/A'}</span>
                    </div>
                `}
                <div class="detail-row">
                    <span class="detail-label">Status:</span>
                    ${statusBadge}
                </div>
            </div>
            
            <div class="user-actions">
                ${isPending ? `
                    <button class="btn-verify" onclick="verifyUser(${user.id}, '${user.full_name}')">
                        <i class="fas fa-check"></i> Verify
                    </button>
                    <button class="btn-reject" onclick="rejectUser(${user.id}, '${user.full_name}')">
                        <i class="fas fa-times"></i> Reject
                    </button>
                ` : `
                    ${user.is_active ? `
                        <button class="btn-deactivate" onclick="deactivateUser(${user.id}, '${user.full_name}')">
                            <i class="fas fa-ban"></i> Deactivate
                        </button>
                    ` : `
                        <button class="btn-activate" onclick="activateUser(${user.id}, '${user.full_name}')">
                            <i class="fas fa-check"></i> Activate
                        </button>
                    `}
                    <button class="btn-delete" onclick="deleteUser(${user.id}, '${user.full_name}')">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                `}
            </div>
        </div>
    `;
}

// Verify User
async function verifyUser(userId, userName) {
    if (!confirm(`Verify ${userName}?`)) return;

    try {
        await API.admin.verifyUser(userId);
        showMessage('pendingMessage', `${userName} has been verified successfully!`, 'success');
        loadPendingUsers();
        loadStats();
    } catch (error) {
        showMessage('pendingMessage', `Error verifying user: ${error.message}`, 'error');
    }
}

// Reject User
async function rejectUser(userId, userName) {
    if (!confirm(`Reject and delete ${userName}? This action cannot be undone.`)) return;

    try {
        await API.admin.deleteUser(userId);
        showMessage('pendingMessage', `${userName} has been rejected and deleted.`, 'success');
        loadPendingUsers();
        loadStats();
    } catch (error) {
        showMessage('pendingMessage', `Error rejecting user: ${error.message}`, 'error');
    }
}

// Deactivate User
async function deactivateUser(userId, userName) {
    if (!confirm(`Deactivate ${userName}?`)) return;

    try {
        await fetch(`http://localhost:5001/api/admin/deactivate-user/${userId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${API.getToken()}`
            }
        });
        alert(`${userName} has been deactivated.`);
        loadAllUsers();
    } catch (error) {
        alert(`Error deactivating user: ${error.message}`);
    }
}

// Activate User
async function activateUser(userId, userName) {
    try {
        await fetch(`http://localhost:5001/api/admin/activate-user/${userId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${API.getToken()}`
            }
        });
        alert(`${userName} has been activated.`);
        loadAllUsers();
    } catch (error) {
        alert(`Error activating user: ${error.message}`);
    }
}

// Delete User
async function deleteUser(userId, userName) {
    if (!confirm(`Permanently delete ${userName}? This action cannot be undone.`)) return;

    try {
        await API.admin.deleteUser(userId);
        alert(`${userName} has been deleted.`);
        loadAllUsers();
        loadStats();
    } catch (error) {
        alert(`Error deleting user: ${error.message}`);
    }
}

// Load All Users
async function loadAllUsers() {
    const tbody = document.getElementById('usersTableBody');
    const verifiedFilter = document.getElementById('verifiedFilter').value;

    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center;"><i class="fas fa-spinner fa-spin"></i> Loading...</td></tr>';

    try {
        const params = {};
        if (verifiedFilter) params.is_verified = verifiedFilter;

        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`http://localhost:5001/api/admin/users?${queryString}`, {
            headers: {
                'Authorization': `Bearer ${API.getToken()}`
            }
        });

        const data = await response.json();
        const users = data.users || [];

        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center;">No users found</td></tr>';
            return;
        }

        tbody.innerHTML = users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.full_name}</td>
                <td>${user.email}</td>
                <td>${user.college_id}</td>
                <td><span class="user-badge ${user.user_type}">${user.user_type}</span></td>
                <td>${user.department}</td>
                <td>
                    ${user.is_verified ?
                '<span class="status-badge verified">Verified</span>' :
                '<span class="status-badge pending">Pending</span>'}
                    ${!user.is_active ? '<span class="status-badge inactive">Inactive</span>' : ''}
                </td>
                <td>
                    <button class="btn-delete" onclick="deleteUser(${user.id}, '${user.full_name}')" style="padding: 0.5rem;">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align: center;">Error: ${error.message}</td></tr>`;
    }
}

// Load Students
async function loadStudents() {
    const grid = document.getElementById('studentsGrid');
    grid.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';

    try {
        const response = await fetch('http://localhost:5001/api/admin/users?user_type=student&is_verified=true', {
            headers: {
                'Authorization': `Bearer ${API.getToken()}`
            }
        });
        const data = await response.json();
        const students = data.users || [];

        if (students.length === 0) {
            grid.innerHTML = '<div class="empty-state"><i class="fas fa-user-graduate"></i><p>No students found</p></div>';
            return;
        }

        grid.innerHTML = students.map(user => createUserCard(user, false)).join('');
    } catch (error) {
        grid.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

// Load Alumni
async function loadAlumni() {
    const grid = document.getElementById('alumniGrid');
    grid.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';

    try {
        const response = await fetch('http://localhost:5001/api/admin/users?user_type=alumni&is_verified=true', {
            headers: {
                'Authorization': `Bearer ${API.getToken()}`
            }
        });
        const data = await response.json();
        const alumni = data.users || [];

        if (alumni.length === 0) {
            grid.innerHTML = '<div class="empty-state"><i class="fas fa-user-tie"></i><p>No alumni found</p></div>';
            return;
        }

        grid.innerHTML = alumni.map(user => createUserCard(user, false)).join('');
    } catch (error) {
        grid.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

// Setup Filters
function setupFilters() {
    document.getElementById('verifiedFilter').addEventListener('change', loadAllUsers);
}

// Logout
function logout() {
    API.auth.logout();
}

// Modal functions
function closeModal() {
    document.getElementById('userModal').style.display = 'none';
}
