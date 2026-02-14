// Kelli & Nathan Wedding Website - Enhanced JavaScript

// Countdown Timer with better formatting
function updateCountdown() {
    const weddingDate = new Date('2027-09-10T15:00:00').getTime();
    const now = new Date().getTime();
    const distance = weddingDate - now;
    
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    const countdownEl = document.getElementById('countdown');
    
    if (distance > 0) {
        countdownEl.innerHTML = `
            <div>
                <span class="count-number">${days}</span>
                <span class="count-label">Days</span>
            </div>
            <div>
                <span class="count-number">${hours}</span>
                <span class="count-label">Hours</span>
            </div>
            <div>
                <span class="count-number">${minutes}</span>
                <span class="count-label">Minutes</span>
            </div>
            <div>
                <span class="count-number">${seconds}</span>
                <span class="count-label">Seconds</span>
            </div>
        `;
    } else {
        countdownEl.innerHTML = `
            <div style="background: rgba(255,255,255,0.2); padding: 1.5rem 3rem; border-radius: 10px;">
                <span style="font-size: 1.5rem; font-weight: 600;">💒 Today is the Day! 💒</span>
            </div>
        `;
    }
}

// Update countdown every second
setInterval(updateCountdown, 1000);
updateCountdown();

// RSVP Form Submission with animation
const rsvpForm = document.getElementById('rsvpForm');
if (rsvpForm) {
rsvpForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        attendance: document.getElementById('attendance').value,
        guests: document.getElementById('guests').value,
        message: document.getElementById('message').value
    };
    
    // Simulate form submission
    console.log('RSVP Submitted:', formData);
    
    // Show success message with animation
    const messageDiv = document.getElementById('rsvpMessage');
    const submitButton = this.querySelector('.submit-btn');
    const attendanceText = formData.attendance === 'yes' 
        ? "We can't wait to celebrate with you!" 
        : "We'll miss you, but thank you for letting us know.";
    
    messageDiv.className = 'success';
    messageDiv.style.display = 'block';
    messageDiv.innerHTML = `
        <strong>Thank you, ${formData.name}! 💕</strong><br>
        Your RSVP has been received.<br>
        ${attendanceText}
    `;

    submitButton.textContent = 'Sent! 💌';
    submitButton.disabled = true;
    submitButton.style.opacity = '0.7';
    
    // Reset form
    this.reset();
    
    // Scroll to message
    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Hide message after 8 seconds
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            messageDiv.style.display = 'none';
            messageDiv.style.opacity = '1';
            submitButton.textContent = 'Send RSVP 💌';
            submitButton.disabled = false;
            submitButton.style.opacity = '1';
        }, 500);
    }, 8000);
});
} // end rsvpForm guard

// Smooth Scrolling for Navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            // Account for sticky navbar
            const navbarHeight = document.getElementById('navbar').offsetHeight;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Active nav state based on scroll position
const navLinks = document.querySelectorAll('#navbar a[href^="#"]');
const sectionTargets = Array.from(navLinks)
    .map(link => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);

const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        const id = entry.target.getAttribute('id');
        const activeLink = document.querySelector(`#navbar a[href="#${id}"]`);
        if (entry.isIntersecting && activeLink) {
            navLinks.forEach(link => link.classList.remove('active'));
            activeLink.classList.add('active');
        }
    });
}, { rootMargin: '-40% 0px -55% 0px' });

sectionTargets.forEach(section => navObserver.observe(section));

// Add to Calendar Function - Enhanced
function addToCalendar() {
    const event = {
        title: 'Kelli & Nathan Wedding',
        start: '2027-09-10T15:00:00',
        end: '2027-09-10T23:00:00',
        details: 'Join us as we celebrate the wedding of Kelli Marie Tait and Nathan Robert Kleven. We can\'t wait to share this special day with you!',
        location: 'Venue TBD'
    };
    
    // Create calendar event (Google Calendar)
    const googleCalendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(event.title)}&dates=20270910T150000/20270910T230000&details=${encodeURIComponent(event.details)}&location=${encodeURIComponent(event.location)}`;
    
    window.open(googleCalendarUrl, '_blank');
}

// Show Map Function
function showMap() {
    // Open Google Maps with the venue location (placeholder)
    window.open('https://maps.google.com/?q=Wedding+Venue', '_blank');
}

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.getElementById('navbar');

if (navbar) {
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Add shadow when scrolled
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 20px rgba(219, 112, 147, 0.2)';
    } else {
        navbar.style.boxShadow = '0 4px 20px rgba(219, 112, 147, 0.15)';
    }
    
    lastScroll = currentScroll;
});
}

// Back to top button
const backToTop = document.getElementById('backToTop');
if (backToTop) {
window.addEventListener('scroll', () => {
    if (window.scrollY > 600) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
}

// Parallax effect on hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('#hero');
    if (hero && scrolled < window.innerHeight) {
        hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
    }
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe sections for animation
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('section:not(#hero)');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
    
    // Observe timeline items
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`;
        observer.observe(item);
    });
    
    // Observe cards
    const cards = document.querySelectorAll('.card, .registry-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.5s ease ${index * 0.15}s, transform 0.5s ease ${index * 0.15}s`;
        observer.observe(card);
    });
});

// Image lazy loading with fade effect
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.photo-item img, .card-image img, .story-image img');
    
    images.forEach(img => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.5s ease';
        
        if (img.complete) {
            img.style.opacity = '1';
        } else {
            img.addEventListener('load', () => {
                img.style.opacity = '1';
            });
        }
    });
});

// Gallery lightbox
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.querySelector('.lightbox-image');
const lightboxCaption = document.querySelector('.lightbox-caption');
const lightboxClose = document.querySelector('.lightbox-close');

if (lightbox && lightboxImage && lightboxClose) {
document.querySelectorAll('.photo-item').forEach(item => {
    item.setAttribute('tabindex', '0');
    item.addEventListener('click', () => openLightbox(item));
    item.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            openLightbox(item);
        }
    });
});

function openLightbox(item) {
    const img = item.querySelector('img');
    const caption = item.querySelector('.photo-overlay span');
    if (!img) {
        return;
    }
    lightboxImage.src = img.src;
    lightboxImage.alt = img.alt;
    lightboxCaption.textContent = caption ? caption.textContent : img.alt;
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
}

function closeLightbox() {
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
}

lightboxClose.addEventListener('click', closeLightbox);
lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) {
        closeLightbox();
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && lightbox.classList.contains('open')) {
        closeLightbox();
    }
});
} // end lightbox guard

// Console message
console.log('%c💕 Kelli & Nathan Wedding Website 💕', 'font-size: 20px; color: #FF69B4; font-weight: bold;');
console.log('%cSeptember 10, 2027', 'font-size: 14px; color: #DB7093;');
