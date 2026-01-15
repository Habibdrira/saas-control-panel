/**
 * SaaS Authentication Service - Main JavaScript
 * Handles form validation and accessibility features
 */

document.addEventListener('DOMContentLoaded', function() {
  initFormValidation();
  addPasswordToggle();
  addAccessibilityFeatures();
});

/**
 * Initialize form validations
 */
function initFormValidation() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      if (!validateForm(form)) {
        e.preventDefault();
      }
    });
  });
}

/**
 * Validate form inputs
 */
function validateForm(form) {
  const username = form.querySelector('input[name="username"]');
  const email = form.querySelector('input[name="email"]');
  const password = form.querySelector('input[name="password"]');
  
  let isValid = true;
  
  if (username && !validateUsername(username.value)) {
    showError(username, 'Username must be 3-50 characters');
    isValid = false;
  }
  
  if (email && !validateEmail(email.value)) {
    showError(email, 'Please enter a valid email address');
    isValid = false;
  }
  
  if (password && !validatePassword(password.value)) {
    showError(password, 'Password must be at least 6 characters');
    isValid = false;
  }
  
  return isValid;
}

/**
 * Validate username format
 */
function validateUsername(username) {
  return username && username.length >= 3 && username.length <= 50;
}

/**
 * Validate email format
 */
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate password strength
 */
function validatePassword(password) {
  return password && password.length >= 6;
}

/**
 * Show error on input
 */
function showError(input, message) {
  input.style.borderColor = '#ef4444';
  input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
  
  // Reset on focus
  input.addEventListener('focus', function() {
    this.style.borderColor = '';
    this.style.boxShadow = '';
  }, { once: true });
}

/**
 * Add password visibility toggle
 */
function addPasswordToggle() {
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  
  passwordInputs.forEach(input => {
    const container = input.parentElement;
    const toggleButton = document.createElement('button');
    toggleButton.type = 'button';
    toggleButton.textContent = '👁';
    toggleButton.style.cssText = 'position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 16px;';
    
    container.style.position = 'relative';
    container.appendChild(toggleButton);
    
    toggleButton.addEventListener('click', function(e) {
      e.preventDefault();
      const newType = input.type === 'password' ? 'text' : 'password';
      input.type = newType;
    });
  });
}

/**
 * Add accessibility features
 */
function addAccessibilityFeatures() {
  const buttons = document.querySelectorAll('button, a');
  
  buttons.forEach(button => {
    button.addEventListener('keydown', function(e) {
      if ((e.key === 'Enter' || e.key === ' ') && this.tagName === 'BUTTON') {
        e.preventDefault();
        this.click();
      }
    });
  });
}
