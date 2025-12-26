// API Configuration - automatically switches between local and production
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001/api'
    : 'https://YOUR-RENDER-APP-NAME.onrender.com/api'; // Update this with your Render backend URL

// API utility functions
const API = {
    // Helper to get auth token
    getToken() {
        return localStorage.getItem('access_token');
    },

    // Helper to set auth token
    setToken(token) {
        localStorage.setItem('access_token', token);
    },

    // Helper to remove auth token
    removeToken() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
    },

    // Helper to get current user
    getUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },

    // Helper to set current user
    setUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
    },

    // Helper to make authenticated requests
    async request(endpoint, options = {}) {
        const token = this.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'An error occurred');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Authentication endpoints
    auth: {
        async register(userData) {
            return await API.request('/auth/register', {
                method: 'POST',
                body: JSON.stringify(userData),
            });
        },

        async login(email, password) {
            const data = await API.request('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password }),
            });

            if (data.access_token) {
                API.setToken(data.access_token);
                API.setUser(data.user);
            }

            return data;
        },

        async logout() {
            API.removeToken();
            window.location.href = 'index.html';
        },

        async getCurrentUser() {
            return await API.request('/auth/me');
        },

        async updateProfile(userData) {
            return await API.request('/auth/update-profile', {
                method: 'PUT',
                body: JSON.stringify(userData),
            });
        },
    },

    // User endpoints
    users: {
        async getAlumni(filters = {}) {
            const params = new URLSearchParams(filters);
            return await API.request(`/users/alumni?${params}`);
        },

        async getStudents(filters = {}) {
            const params = new URLSearchParams(filters);
            return await API.request(`/users/students?${params}`);
        },

        async getUserProfile(userId) {
            return await API.request(`/users/${userId}`);
        },

        async getStats() {
            return await API.request('/users/stats');
        },
    },

    // Job endpoints
    jobs: {
        async getJobs(filters = {}) {
            const params = new URLSearchParams(filters);
            return await API.request(`/jobs/?${params}`);
        },

        async getJob(jobId) {
            return await API.request(`/jobs/${jobId}`);
        },

        async createJob(jobData) {
            return await API.request('/jobs/', {
                method: 'POST',
                body: JSON.stringify(jobData),
            });
        },

        async updateJob(jobId, jobData) {
            return await API.request(`/jobs/${jobId}`, {
                method: 'PUT',
                body: JSON.stringify(jobData),
            });
        },

        async deleteJob(jobId) {
            return await API.request(`/jobs/${jobId}`, {
                method: 'DELETE',
            });
        },

        async applyToJob(jobId, applicationData) {
            return await API.request(`/jobs/${jobId}/apply`, {
                method: 'POST',
                body: JSON.stringify(applicationData),
            });
        },

        async getMyJobs() {
            return await API.request('/jobs/my-jobs');
        },

        async getMyApplications() {
            return await API.request('/jobs/my-applications');
        },
    },

    // Chat endpoints
    chat: {
        async getConversations() {
            return await API.request('/chat/conversations');
        },

        async getMessages(userId) {
            return await API.request(`/chat/messages/${userId}`);
        },

        async sendMessage(receiverId, content) {
            return await API.request('/chat/send', {
                method: 'POST',
                body: JSON.stringify({ receiver_id: receiverId, content }),
            });
        },

        async getUnreadCount() {
            return await API.request('/chat/unread-count');
        },
    },

    // Admin endpoints
    admin: {
        async getPendingUsers() {
            return await API.request('/admin/pending-users');
        },

        async verifyUser(userId) {
            return await API.request(`/admin/verify-user/${userId}`, {
                method: 'PUT',
            });
        },

        async deleteUser(userId) {
            return await API.request(`/admin/delete-user/${userId}`, {
                method: 'DELETE',
            });
        },

        async getStats() {
            return await API.request('/admin/stats');
        },
    },
};

// Utility functions
function showMessage(elementId, message, type = 'success') {
    const messageEl = document.getElementById(elementId);
    if (!messageEl) return;

    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'block';

    // Auto hide after 5 seconds
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}

function hideMessage(elementId) {
    const messageEl = document.getElementById(elementId);
    if (messageEl) {
        messageEl.style.display = 'none';
    }
}

function setLoading(buttonId, loading = true) {
    const button = document.getElementById(buttonId);
    if (!button) return;

    const textEl = button.querySelector('.btn-text');
    const loadingEl = button.querySelector('.btn-loading');

    if (loading) {
        button.disabled = true;
        textEl.style.display = 'none';
        loadingEl.style.display = 'inline-block';
    } else {
        button.disabled = false;
        textEl.style.display = 'inline-block';
        loadingEl.style.display = 'none';
    }
}

// Check if user is logged in
function checkAuth() {
    const token = API.getToken();
    const user = API.getUser();
    return token && user;
}

// Redirect if not authenticated
function requireAuth() {
    if (!checkAuth()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Redirect if authenticated
function redirectIfAuth() {
    if (checkAuth()) {
        window.location.href = 'dashboard.html';
        return true;
    }
    return false;
}
