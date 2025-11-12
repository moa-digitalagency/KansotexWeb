// KANSOTEX - Main JavaScript

// Testimonials Data - loaded from API
let testimonials = [];
let currentTestimonial = 0;
let currentHeroSlide = 0;
let currentCollectionTwoSlide = 0;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initHeroSlider();
    initCollectionTwoSlider();
    initTestimonials();
    initMobileMenu();
    initContactForm();
    initSmoothScroll();
});

// Initialize Hero Slider
function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.slider-dot');
    
    if (!slides.length || !dots.length) return;
    
    // Auto-rotate slides every 5 seconds
    setInterval(() => {
        currentHeroSlide = (currentHeroSlide + 1) % slides.length;
        showHeroSlide(currentHeroSlide);
    }, 5000);
    
    // Dot click handlers
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentHeroSlide = index;
            showHeroSlide(currentHeroSlide);
        });
    });
}

// Show specific hero slide
function showHeroSlide(index) {
    const slides = document.querySelectorAll('.hero-slide');
    const dots = document.querySelectorAll('.slider-dot');
    
    slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
    });
    
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

// Initialize Testimonials Carousel
async function initTestimonials() {
    const container = document.getElementById('testimonials-container');
    const dotsContainer = document.getElementById('testimonial-dots');
    
    if (!container || !dotsContainer) return;
    
    try {
        // Fetch testimonials from API
        const response = await fetch('/api/testimonials?lang=' + (document.body.getAttribute('data-current-lang') || 'fr'));
        const data = await response.json();
        
        if (data.success && data.testimonials && data.testimonials.length > 0) {
            testimonials = data.testimonials;
            
            // Create testimonial cards
            testimonials.forEach((testimonial, index) => {
                const card = document.createElement('div');
                card.className = `testimonial-card ${index === 0 ? 'active' : ''}`;
                card.style.display = index === 0 ? 'block' : 'none';
                card.innerHTML = `
                    <p class="text-lg text-gray-300 mb-6 italic leading-relaxed">${testimonial.content}</p>
                    <div class="flex items-center space-x-4">
                        ${testimonial.client_photo ? 
                            `<img src="${testimonial.client_photo.url}" alt="${testimonial.client_name}" class="w-16 h-16 rounded-full object-cover">` :
                            `<div class="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold bg-accent-gradient">
                                ${testimonial.client_name.charAt(0)}
                            </div>`
                        }
                        <div>
                            <h4 class="font-bold text-lg">${testimonial.client_name}</h4>
                            <p class="text-gray-400 text-sm">${testimonial.client_title || ''} ${testimonial.client_company ? ', ' + testimonial.client_company : ''}</p>
                        </div>
                    </div>
                    ${testimonial.rating ? `<div class="flex items-center mt-4 text-accent">
                        ${'<i class="fas fa-star"></i>'.repeat(testimonial.rating)}
                    </div>` : ''}
                `;
                container.appendChild(card);
            });
            
            // Create dots
            testimonials.forEach((_, index) => {
                const dot = document.createElement('div');
                dot.className = `dot ${index === 0 ? 'active' : ''}`;
                dot.addEventListener('click', () => showTestimonial(index));
                dotsContainer.appendChild(dot);
            });
            
            // Auto-rotate testimonials every 5 seconds
            if (testimonials.length > 1) {
                setInterval(() => {
                    currentTestimonial = (currentTestimonial + 1) % testimonials.length;
                    showTestimonial(currentTestimonial);
                }, 5000);
            }
        }
    } catch (error) {
        console.error('Error loading testimonials:', error);
    }
}

// Show specific testimonial
function showTestimonial(index) {
    const cards = document.querySelectorAll('.testimonial-card');
    const dots = document.querySelectorAll('.dot');
    
    cards.forEach((card, i) => {
        if (i === index) {
            card.style.display = 'block';
            setTimeout(() => card.classList.add('active'), 10);
        } else {
            card.classList.remove('active');
            setTimeout(() => card.style.display = 'none', 500);
        }
    });
    
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
    
    currentTestimonial = index;
}

// Initialize Mobile Menu
function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    
    if (!btn || !menu) return;
    
    btn.addEventListener('click', () => {
        menu.classList.toggle('hidden');
    });
    
    // Close menu when clicking on a link
    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.add('hidden');
        });
    });
}

// Initialize Contact Form
function initContactForm() {
    const form = document.getElementById('contact-form');
    const messageDiv = document.getElementById('form-message');
    
    if (!form || !messageDiv) return;
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            message: document.getElementById('message').value
        };
        
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                messageDiv.className = 'mt-4 text-center success-message';
                messageDiv.textContent = data.message || 'Votre message a été envoyé avec succès!';
                messageDiv.classList.remove('hidden');
                form.reset();
            } else {
                throw new Error(data.error || 'Une erreur est survenue');
            }
        } catch (error) {
            messageDiv.className = 'mt-4 text-center error-message';
            messageDiv.textContent = error.message || 'Erreur lors de l\'envoi du message. Veuillez réessayer.';
            messageDiv.classList.remove('hidden');
        }
        
        // Hide message after 5 seconds
        setTimeout(() => {
            messageDiv.classList.add('hidden');
        }, 5000);
    });
}

// Initialize Smooth Scroll
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80; // Height of fixed header
                const targetPosition = target.offsetTop - offset;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}


// Initialize Collection Two Column Slider
function initCollectionTwoSlider() {
    const slides = document.querySelectorAll('.collection-two-col-slide');
    const dots = document.querySelectorAll('.collection-two-dot');
    const prevBtn = document.querySelector('.collection-two-prev');
    const nextBtn = document.querySelector('.collection-two-next');
    
    if (!slides.length || !dots.length) return;
    
    // Auto-rotate slides every 5 seconds
    setInterval(() => {
        currentCollectionTwoSlide = (currentCollectionTwoSlide + 1) % slides.length;
        showCollectionTwoSlide(currentCollectionTwoSlide);
    }, 5000);
    
    // Dot click handlers
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentCollectionTwoSlide = index;
            showCollectionTwoSlide(currentCollectionTwoSlide);
        });
    });
    
    // Navigation buttons
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentCollectionTwoSlide = (currentCollectionTwoSlide - 1 + slides.length) % slides.length;
            showCollectionTwoSlide(currentCollectionTwoSlide);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentCollectionTwoSlide = (currentCollectionTwoSlide + 1) % slides.length;
            showCollectionTwoSlide(currentCollectionTwoSlide);
        });
    }
}

// Show specific collection two column slide
function showCollectionTwoSlide(index) {
    const slides = document.querySelectorAll('.collection-two-col-slide');
    const dots = document.querySelectorAll('.collection-two-dot');
    
    slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
    });
    
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

// Scroll animations and header transparency
window.addEventListener('scroll', function() {
    const header = document.getElementById('main-header');
    if (window.scrollY > 50) {
        header.classList.add('header-sticky');
        header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.5)';
    } else {
        header.classList.remove('header-sticky');
        header.style.boxShadow = 'none';
    }
});

// ===== THEME TOGGLE FUNCTIONALITY =====

// Initialize theme on page load
function initTheme() {
    const serverThemeMode = document.body.getAttribute('data-theme-mode-server') || 'dark';
    const allowUserToggle = document.body.getAttribute('data-allow-user-toggle') === 'true';
    
    // Check if user has a saved preference
    const savedTheme = localStorage.getItem('userThemePreference');
    
    let themeToApply = serverThemeMode;
    
    // If auto mode is enabled on server, check browser preference
    if (serverThemeMode === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        themeToApply = prefersDark ? 'dark' : 'light';
    }
    
    // If user has a saved preference and toggle is allowed, use it
    if (savedTheme && allowUserToggle) {
        themeToApply = savedTheme;
    }
    
    applyTheme(themeToApply);
    
    // Setup theme toggle button if allowed
    if (allowUserToggle) {
        setupThemeToggle();
    }
    
    // Listen for system theme changes (auto mode)
    if (serverThemeMode === 'auto' && !savedTheme) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('userThemePreference')) {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
}

// Apply theme
function applyTheme(theme) {
    document.body.setAttribute('data-theme-mode', theme);
    updateThemeToggleIcon(theme);
}

// Setup theme toggle button
function setupThemeToggle() {
    // Add theme toggle class to body
    document.body.classList.add('theme-toggle-enabled');
    
    // Create theme toggle button if it doesn't exist
    let toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) {
        toggleBtn = document.createElement('button');
        toggleBtn.id = 'theme-toggle';
        toggleBtn.setAttribute('aria-label', 'Toggle theme');
        toggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
        
        // Add to floating buttons stack instead of body
        const floatingStack = document.querySelector('.floating-buttons-stack');
        if (floatingStack) {
            floatingStack.appendChild(toggleBtn);
        } else {
            document.body.appendChild(toggleBtn);
        }
    }
    
    // Add click event
    toggleBtn.addEventListener('click', toggleTheme);
    
    // Update initial icon
    const currentTheme = document.body.getAttribute('data-theme-mode') || 'dark';
    updateThemeToggleIcon(currentTheme);
}

// Toggle theme
function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme-mode') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    applyTheme(newTheme);
    localStorage.setItem('userThemePreference', newTheme);
}

// Update theme toggle icon
function updateThemeToggleIcon(theme) {
    const toggleBtn = document.getElementById('theme-toggle');
    if (!toggleBtn) return;
    
    const icon = toggleBtn.querySelector('i');
    if (!icon) return;
    
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
        toggleBtn.setAttribute('title', 'Passer au thème clair');
    } else {
        icon.className = 'fas fa-moon';
        toggleBtn.setAttribute('title', 'Passer au thème sombre');
    }
}

// Add to DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    initHeroSlider();
    initCollectionTwoSlider();
    initTestimonials();
    initMobileMenu();
    initContactForm();
    initSmoothScroll();
    initTheme(); // Initialize theme
});
