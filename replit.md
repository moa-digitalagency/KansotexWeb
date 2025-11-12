# KANSOTEX - Site Web

## Overview
The KANSOTEX website showcases the services, products, and expertise of KANSOTEX, a premium textile specialist, across the hotel, medical, and residential sectors. The project aims to provide a professional and visually appealing online presence with dynamic content management capabilities, catering to both public users and administrators.

## User Preferences
I want iterative development. Ask before making major changes. I prefer detailed explanations. Do not make changes to the folder Z. Do not make changes to the file Y.

## System Architecture
The project is built using a Python Flask backend with a PostgreSQL database, following an MVC-like structure. The frontend utilizes HTML5, Tailwind CSS, and Vanilla JavaScript.

**UI/UX Decisions:**
- **Design Theme:** Premium dark and dark gold (`#B8941E`) color scheme, with a responsive light mode providing clear, readable content on light backgrounds.
- **Dynamic Theming:** Users can switch between dark/light modes, with preferences saved in local storage. Admins can set the default theme and enable/disable user theme switching.
- **Responsive Design:** The layout is fully responsive, adapting to desktop, tablet, and mobile screens.
- **Animations & Transitions:** Fluid animations and transitions enhance the user experience.
- **Header:** Transparent header that becomes opaque and sticky with a blur effect on scroll.
- **Image Display:** Hero section with an automatic image slider, and a premium collection carousel with badges, large titles, gradient buttons, and subtle zoom effects.
- **Footer:** Modern 4-column footer with social icons and a golden gradient line.

**Technical Implementations & Feature Specifications:**

**Public Site:**
- **Content Management:** All major sections (Hero, Strengths, Collection, Sectors, Commitment, Contact) are dynamically managed via the admin panel.
- **Multilingual Support:** Automatic browser language detection (FR/EN) with redirection.
- **Contact Form:** Functional contact form with database storage and automatic SMTP email sending to administrators, including HTML-formatted emails.
- **SEO Optimization:** Comprehensive SEO features including:
  - Dynamic sitemap.xml route (`/sitemap.xml`) with all pages and blog articles, proper priorities, change frequencies, and last modification dates
  - Dynamic robots.txt route (`/robots.txt`) that allows public pages, disallows admin/API routes, and references the sitemap
  - Canonical URLs, robots meta, structured data (JSON-LD), Open Graph, and Twitter Cards, all configurable via the admin panel
- **Dynamic Images:** All site images (hero slider, collection, sector backgrounds, engagement background, footer background) are dynamically managed and editable through the admin interface, with a custom Jinja filter for URL handling and robust fallbacks.
- **Accessibility:** Optimized color contrast in light mode for all UI components including strength cards, collection slides, navigation arrows, and contact forms to ensure WCAG compliance.

**Admin Panel:**
- **Secure Access:** Password-protected access via `/admin`.
- **Content Management System (CMS):** Allows editing of all site texts and managing images.
- **Image Management:** Upload, view, delete, and crop images. Automatic optimization (compression, conversion to RGB, quality 85%) using Pillow, supporting JPG, PNG, GIF, WEBP, and with size limits (10 MB).
- **Image Cropping:** Advanced interface with `Cropper.js` integration and preset dimensions for various image types (e.g., Hero Slider, Collection Cards, Open Graph).
- **Site Settings:** Configuration for default theme, user theme switching, language detection, and SMTP email settings (host, port, sender email, recipient email), with secure storage of SMTP credentials in environment variables.
- **Dashboard:** Provides statistics and quick access to administrative functions.
- **Session Management:** Secure sessions with automatic expiration.

**System Design Choices:**
- **Database Schema:** Defined models for `Contact`, `ContentSection`, `ContentField`, `ImageAsset`, `SiteSetting`, and `AdminSession` to support dynamic content and administrative functions.
- **Configuration:** Flask server listens on `0.0.0.0:5000`. Key configurations handled via environment variables (DATABASE_URL, SESSION_SECRET, ADMIN_PASSWORD, SMTP_USERNAME, SMTP_PASSWORD).

## External Dependencies
- **Python 3.11**
- **Flask (Python Web Framework)**
- **Tailwind CSS**
- **PostgreSQL (Database)**
- **SQLAlchemy (ORM)**
- **Pillow (Python Imaging Library)** for image processing
- **Cropper.js (JavaScript Library)** for image cropping
- **SMTP (Simple Mail Transfer Protocol)** for sending emails