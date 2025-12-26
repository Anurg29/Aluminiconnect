// Home page functionality
document.addEventListener('DOMContentLoaded', async () => {
    // Animate stats counter
    function animateCounter(element, target, duration = 2000) {
        let current = 0;
        const increment = target / (duration / 16);

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = Math.ceil(target);
                clearInterval(timer);
            } else {
                element.textContent = Math.ceil(current);
            }
        }, 16);
    }

    // Fetch and display stats
    try {
        const stats = await API.users.getStats();

        if (stats) {
            const alumniEl = document.getElementById('alumniCount');
            const studentEl = document.getElementById('studentCount');
            const connectionsEl = document.getElementById('connectionsCount');

            if (alumniEl) animateCounter(alumniEl, stats.total_alumni || 0);
            if (studentEl) animateCounter(studentEl, stats.total_students || 0);
            if (connectionsEl) animateCounter(connectionsEl, stats.total_users || 0);
        }
    } catch (error) {
        console.error('Error fetching stats:', error);
        // Set default values if API fails
        const alumniEl = document.getElementById('alumniCount');
        const studentEl = document.getElementById('studentCount');
        const connectionsEl = document.getElementById('connectionsCount');

        if (alumniEl) alumniEl.textContent = '100+';
        if (studentEl) studentEl.textContent = '500+';
        if (connectionsEl) connectionsEl.textContent = '1000+';
    }

    // Add intersection observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
});
