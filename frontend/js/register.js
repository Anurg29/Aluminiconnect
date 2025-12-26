// Register page functionality
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const userTypeRadios = document.querySelectorAll('input[name="user_type"]');
    const studentFields = document.getElementById('studentFields');
    const alumniFields = document.getElementById('alumniFields');

    // Toggle between student and alumni fields
    userTypeRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'student') {
                studentFields.style.display = 'block';
                alumniFields.style.display = 'none';

                // Make student fields required
                document.getElementById('current_year').required = true;
                document.getElementById('expected_passing_year').required = true;

                // Remove required from alumni fields
                document.getElementById('passing_year').required = false;
                document.getElementById('current_company').required = false;
                document.getElementById('current_position').required = false;
            } else {
                studentFields.style.display = 'none';
                alumniFields.style.display = 'block';

                // Remove required from student fields
                document.getElementById('current_year').required = false;
                document.getElementById('expected_passing_year').required = false;

                // Make alumni fields required
                document.getElementById('passing_year').required = true;
            }
        });
    });

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideMessage('message');

        // Get form data
        const formData = new FormData(form);
        const userType = formData.get('user_type');
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');

        // Validate password match
        if (password !== confirmPassword) {
            showMessage('message', 'Passwords do not match!', 'error');
            return;
        }

        // Prepare user data
        const userData = {
            full_name: formData.get('full_name'),
            email: formData.get('email'),
            password: password,
            college_id: formData.get('college_id'),
            college_email: formData.get('college_email'),
            department: formData.get('department'),
            user_type: userType,
        };

        // Add type-specific fields
        if (userType === 'student') {
            userData.current_year = parseInt(formData.get('current_year'));
            userData.expected_passing_year = parseInt(formData.get('expected_passing_year'));
        } else {
            userData.passing_year = parseInt(formData.get('passing_year'));
            userData.current_company = formData.get('current_company');
            userData.current_position = formData.get('current_position');
        }

        // Set loading state
        setLoading('submitBtn', true);

        try {
            const response = await API.auth.register(userData);

            showMessage('message',
                response.message || 'Registration successful! Please wait for admin verification.',
                'success'
            );

            // Reset form
            form.reset();

            // Redirect to login after 3 seconds
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 3000);

        } catch (error) {
            showMessage('message', error.message || 'Registration failed. Please try again.', 'error');
        } finally {
            setLoading('submitBtn', false);
        }
    });
});
