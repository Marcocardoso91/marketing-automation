// Authentication Helper
// Dashboard Sabrina Blogueira

const Auth = {
    // Check if user is authenticated
    isAuthenticated() {
        const token = localStorage.getItem('token');
        return !!token;
    },

    // Get current user
    getUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    // Get token
    getToken() {
        return localStorage.getItem('token');
    },

    // Save authentication data
    saveAuth(token, user) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
    },

    // Clear authentication data
    clearAuth() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    },

    // Logout
    logout() {
        this.clearAuth();
        window.location.href = '/index.html';
    },

    // Protect page (redirect to login if not authenticated)
    protectPage() {
        if (!this.isAuthenticated()) {
            window.location.href = '/index.html';
        }
    },

    // Redirect to dashboard if already authenticated
    redirectIfAuthenticated() {
        if (this.isAuthenticated()) {
            window.location.href = '/dashboard.html';
        }
    }
};

// Check authentication on page load for protected pages
document.addEventListener('DOMContentLoaded', () => {
    // Get current page
    const currentPage = window.location.pathname.split('/').pop();
    
    // Pages that require authentication
    const protectedPages = [
        'dashboard.html',
        'cronograma.html',
        'ganchos.html',
        'checklist.html',
        'relatorios.html',
        'configuracoes.html'
    ];

    // Protect page if needed
    if (protectedPages.includes(currentPage)) {
        Auth.protectPage();
    }

    // Redirect if already authenticated on login page
    if (currentPage === 'index.html' || currentPage === '') {
        Auth.redirectIfAuthenticated();
    }
});

// Export for use in other scripts
if (typeof window !== 'undefined') {
    window.Auth = Auth;
}

