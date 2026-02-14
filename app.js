// Navigation toggle for mobile
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // CTA button handlers - handle these BEFORE smooth scroll
    const ctaButtons = document.querySelectorAll('.btn-primary, .btn-secondary');
    ctaButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const href = btn.getAttribute('href');
            const buttonText = btn.textContent.trim();
            
            if (href === '#consultation') {
                alert(`🗓️ Schedule Consultation\n\nThank you for your interest! This would normally open our scheduling system.\n\nYou can reach us at:\nPhone: (555) 123-4567\nEmail: info@gardenofedentax.com`);
            } else if (href === '#resources') {
                alert(`📚 Access Resources\n\nWelcome to our resource center! This would normally provide access to:\n\n• Tax planning guides\n• Compliance checklists\n• Industry updates\n• Client tools\n\nPlease contact us for more information.`);
            } else {
                alert(`Button clicked: ${buttonText}\n\nThis feature is coming soon!`);
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        // Skip if it's a CTA button (already handled above)
        if (anchor.classList.contains('btn-primary') || anchor.classList.contains('btn-secondary')) {
            return;
        }
        
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
            // Close mobile menu if open
            if (navMenu) {
                navMenu.classList.remove('active');
            }
        });
    });

    // Form submission handler
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            console.log('Form submitted:', data);
            alert('Form submitted successfully!\n\nForm data logged to console.');
            form.reset();
        });
    });

    // Add click feedback to all buttons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });

    // Stat card animations on hover
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px) scale(1.02)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });

    // Feature card click handler
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('click', function() {
            const title = this.querySelector('h3').textContent;
            const description = this.querySelector('p').textContent;
            alert(`${title}\n\n${description}\n\nClick OK to learn more about this feature.`);
        });
        
        // Add pointer cursor
        card.style.cursor = 'pointer';
    });

    console.log('✅ App initialized successfully');
});
