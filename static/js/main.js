/**
 * ParadiseRide - Main JavaScript File
 * Global functionality, animations, and utilities
 */

// Global variables
let isLoading = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    setupGlobalEventListeners();
    initializeAnimations();
    setupFormValidation();
    setupTooltips();
    
    console.log('ParadiseRide initialized successfully! ✈️');
}

/**
 * Setup global event listeners
 */
function setupGlobalEventListeners() {
    // Smooth scrolling for anchor links
    setupSmoothScrolling();
    
    // Handle escape key for modals and overlays
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAllModals();
            hideAllTooltips();
        }
    });
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            handleWindowResize();
        }, 250);
    });
    
    // Handle online/offline status
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
}

/**
 * Setup smooth scrolling for anchor links
 */
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize animations using Intersection Observer
 */
function initializeAnimations() {
    // Fade-in animation observer
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-active');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe elements with fade-in class
    document.querySelectorAll('.fade-in').forEach(el => {
        fadeObserver.observe(el);
    });
    
    // Slide-up animation observer
    const slideObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-up-active');
                slideObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe elements with slide-up class
    document.querySelectorAll('.slide-up').forEach(el => {
        slideObserver.observe(el);
    });
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Real-time validation on blur
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            // Clear validation on focus
            input.addEventListener('focus', function() {
                clearFieldValidation(this);
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}

/**
 * Validate individual form field
 */
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.getAttribute('name');
    const fieldType = field.getAttribute('type');
    let isValid = true;
    let message = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required';
    }
    
    // Email validation
    else if (fieldType === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        message = 'Please enter a valid email address';
    }
    
    // Password validation
    else if (fieldType === 'password' && value && value.length < 6) {
        isValid = false;
        message = 'Password must be at least 6 characters long';
    }
    
    // Phone validation
    else if (fieldType === 'tel' && value && !isValidPhone(value)) {
        isValid = false;
        message = 'Please enter a valid phone number';
    }
    
    // Apply validation styling
    if (!isValid) {
        showFieldError(field, message);
    } else {
        clearFieldValidation(field);
    }
    
    return isValid;
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    field.classList.add('error');
    
    // Remove existing error message
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

/**
 * Clear field validation
 */
function clearFieldValidation(field) {
    field.classList.remove('error');
    const errorMsg = field.parentNode.querySelector('.field-error');
    if (errorMsg) {
        errorMsg.remove();
    }
}

/**
 * Validate entire form
 */
function validateForm(form) {
    const fields = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    fields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Setup tooltips
 */
function setupTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
        element.addEventListener('focus', showTooltip);
        element.addEventListener('blur', hideTooltip);
    });
}

/**
 * Show tooltip
 */
function showTooltip(e) {
    const element = e.target;
    const text = element.getAttribute('data-tooltip');
    
    if (!text) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.id = 'tooltip-' + Date.now();
    
    document.body.appendChild(tooltip);
    
    // Position tooltip
    const rect = element.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltipRect.width / 2) + 'px';
    tooltip.style.top = rect.top - tooltipRect.height - 10 + 'px';
    
    // Store tooltip reference
    element.tooltipElement = tooltip;
    
    // Show tooltip
    setTimeout(() => {
        tooltip.classList.add('show');
    }, 50);
}

/**
 * Hide tooltip
 */
function hideTooltip(e) {
    const element = e.target;
    if (element.tooltipElement) {
        element.tooltipElement.remove();
        element.tooltipElement = null;
    }
}

/**
 * Hide all tooltips
 */
function hideAllTooltips() {
    document.querySelectorAll('.tooltip').forEach(tooltip => {
        tooltip.remove();
    });
}

/**
 * Utility function to check if email is valid
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Utility function to check if phone is valid
 */
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

/**
 * Handle window resize
 */
function handleWindowResize() {
    // Recalculate any dynamic layouts
    hideAllTooltips();
    
    // Dispatch custom resize event
    window.dispatchEvent(new CustomEvent('app:resize'));
}

/**
 * Handle online status
 */
function handleOnline() {
    showNotification('You\'re back online! 🌐', 'success');
    document.body.classList.remove('offline');
}

/**
 * Handle offline status
 */
function handleOffline() {
    showNotification('You\'re currently offline. Some features may not work. 📵', 'warning');
    document.body.classList.add('offline');
}

/**
 * Show notification
 */
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-message">${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to page
    let container = document.querySelector('.notifications-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notifications-container';
        document.body.appendChild(container);
    }
    
    container.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto remove
    if (duration > 0) {
        setTimeout(() => {
            notification.classList.add('hide');
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, duration);
    }
    
    return notification;
}

/**
 * Close all modals
 */
function closeAllModals() {
    document.querySelectorAll('.modal.show').forEach(modal => {
        modal.classList.remove('show');
    });
}

/**
 * Debounce function
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Format date for display
 */
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    const formatOptions = { ...defaultOptions, ...options };
    return new Intl.DateTimeFormat('en-IN', formatOptions).format(new Date(date));
}

/**
 * Format currency for Indian Rupees
 */
function formatCurrency(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard! 📋', 'success', 2000);
        return true;
    } catch (err) {
        console.error('Failed to copy text: ', err);
        showNotification('Failed to copy text', 'error', 3000);
        return false;
    }
}

/**
 * Share content using Web Share API
 */
async function shareContent(data) {
    if (navigator.share) {
        try {
            await navigator.share(data);
            return true;
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error('Error sharing:', err);
            }
            return false;
        }
    } else {
        // Fallback to clipboard
        const shareText = `${data.title}\n${data.text}\n${data.url}`;
        return await copyToClipboard(shareText);
    }
}

/**
 * Animate counter numbers
 */
function animateCounter(element, start, end, duration = 2000) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

/**
 * Lazy load images
 */
function setupLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * Initialize lazy loading when DOM is ready
 */
document.addEventListener('DOMContentLoaded', setupLazyLoading);

/**
 * Export utilities for use in other scripts
 */
window.ParadiseRide = {
    showNotification,
    copyToClipboard,
    shareContent,
    formatDate,
    formatCurrency,
    animateCounter,
    debounce,
    throttle,
    validateField,
    isValidEmail,
    isValidPhone
};

// Add custom CSS for notifications and tooltips
const customStyles = `
/* Notifications */
.notifications-container {
    position: fixed;
    top: 80px;
    right: 1rem;
    z-index: 10000;
    max-width: 400px;
}

.notification {
    background: white;
    border-radius: 0.75rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #3b82f6;
    padding: 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transform: translateX(100%);
    opacity: 0;
    transition: all 0.3s ease;
}

.notification.show {
    transform: translateX(0);
    opacity: 1;
}

.notification.hide {
    transform: translateX(100%);
    opacity: 0;
}

.notification-success {
    border-left-color: #10b981;
}

.notification-warning {
    border-left-color: #f59e0b;
}

.notification-error {
    border-left-color: #ef4444;
}

.notification-close {
    background: none;
    border: none;
    font-size: 0.875rem;
    cursor: pointer;
    opacity: 0.5;
    transition: opacity 0.2s;
}

.notification-close:hover {
    opacity: 1;
}

/* Tooltips */
.tooltip {
    position: absolute;
    background: #1f2937;
    color: white;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    z-index: 10001;
    opacity: 0;
    transform: translateY(5px);
    transition: all 0.2s ease;
    pointer-events: none;
}

.tooltip.show {
    opacity: 1;
    transform: translateY(0);
}

.tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #1f2937 transparent transparent transparent;
}

/* Field errors */
.field-error {
    color: #ef4444;
    font-size: 0.75rem;
    margin-top: 0.25rem;
    animation: shake 0.5s ease-in-out;
}

/* Offline styles */
.offline {
    filter: grayscale(0.3);
}

.offline::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.1);
    z-index: 9999;
    pointer-events: none;
}

/* Animation classes */
.fade-in-active {
    opacity: 1;
    transform: translateY(0);
}

.slide-up-active {
    opacity: 1;
    transform: translateY(0);
}

@media (max-width: 768px) {
    .notifications-container {
        left: 1rem;
        right: 1rem;
        max-width: none;
    }
}
`;

// Inject custom styles
const styleSheet = document.createElement('style');
styleSheet.textContent = customStyles;
document.head.appendChild(styleSheet);