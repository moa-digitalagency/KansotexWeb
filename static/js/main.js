// KANSOTEX - Main JavaScript

// Testimonials Data
const testimonials = [
    {
        quote: "Kansotex a révolutionné le confort dans notre établissement médical. Leurs produits sont à la fois luxueux et pratiques.",
        name: "Dr. Sophia Leroy",
        position: "Chef de Service, Clinique SantéPlus"
    },
    {
        quote: "En tant qu'architecte d'intérieur, je recommande Kansotex pour leur excellence et leur style unique. Un vrai partenaire de confiance.",
        name: "Claire Dubois",
        position: "Architecte d'Intérieur, Design & Espaces"
    },
    {
        quote: "La qualité des textiles Kansotex a transformé l'expérience de nos clients. Leur durabilité est impressionnante.",
        name: "Julien Moreau",
        position: "Directeur Général, Hôtel Élégance"
    }
];

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
function initTestimonials() {
    const container = document.getElementById('testimonials-container');
    const dotsContainer = document.getElementById('testimonial-dots');
    
    if (!container || !dotsContainer) return;
    
    // Create testimonial cards
    testimonials.forEach((testimonial, index) => {
        const card = document.createElement('div');
        card.className = `testimonial-card ${index === 0 ? 'active' : ''}`;
        card.style.display = index === 0 ? 'block' : 'none';
        card.innerHTML = `
            <p class="text-lg text-gray-300 mb-6 italic leading-relaxed">${testimonial.quote}</p>
            <div class="flex items-center space-x-4">
                <div class="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold bg-accent-gradient">
                    ${testimonial.name.charAt(0)}
                </div>
                <div>
                    <h4 class="font-bold text-lg">${testimonial.name}</h4>
                    <p class="text-gray-400 text-sm">${testimonial.position}</p>
                </div>
            </div>
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
    setInterval(() => {
        currentTestimonial = (currentTestimonial + 1) % testimonials.length;
        showTestimonial(currentTestimonial);
    }, 5000);
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
