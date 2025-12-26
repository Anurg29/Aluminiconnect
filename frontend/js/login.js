// Login page functionality
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const demoButtons = document.querySelectorAll('.demo-btn');

    // Redirect if already logged in
    redirectIfAuth();

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideMessage('message');

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Set loading state
        setLoading('submitBtn', true);

        try {
            const response = await API.auth.login(email, password);

            showMessage('message', 'Login successful! Redirecting...', 'success');

            // Redirect based on email (admin check)
            setTimeout(() => {
                if (response.user.email === 'admin@college.edu' || response.user.email.includes('admin@')) {
                    window.location.href = 'admin-dashboard.html';
                } else {
                    window.location.href = 'dashboard.html';
                }
            }, 1000);

        } catch (error) {
            let errorMessage = error.message;

            if (errorMessage.includes('not verified')) {
                errorMessage = 'Your account is pending admin verification. Please wait for approval.';
            } else if (errorMessage.includes('deactivated')) {
                errorMessage = 'Your account has been deactivated. Please contact admin.';
            } else if (errorMessage.includes('Invalid')) {
                errorMessage = 'Invalid email or password. Please check your credentials.';
            }

            showMessage('message', errorMessage, 'error');
        } finally {
            setLoading('submitBtn', false);
        }
    });

    // Demo access buttons (for testing)
    demoButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const role = btn.dataset.role;
            showMessage('message',
                `Demo ${role} account: Please register or use your credentials.`,
                'error'
            );
        });
    });
});
