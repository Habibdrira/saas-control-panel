/**
 * SaaS Control Panel - Main JavaScript
 * Handles confirmations, form validation, and UI interactions
 */

// ============================================
// CONFIRMATION DIALOGS
// ============================================

/**
 * Show a confirmation dialog for destructive actions
 * @param {string} message - The message to display
 * @param {string} action - The action being performed (for UX)
 * @returns {boolean}
 */
function confirmAction(message = 'Are you sure?', action = 'this action') {
  return confirm(`${message}\n\nThis operation cannot be undone.`);
}

/**
 * Confirm stopping a container
 * @returns {boolean}
 */
function confirmStop() {
  return confirmAction('Stop this container?', 'stop');
}

/**
 * Confirm deleting a container
 * @returns {boolean}
 */
function confirmDelete() {
  return confirmAction('Delete this container permanently?', 'delete');
}

// ============================================
// FORM VALIDATION
// ============================================

/**
 * Validate username format
 * @param {string} username
 * @returns {boolean}
 */
function validateUsername(username) {
  const minLength = 3;
  const maxLength = 50;
  const regex = /^[a-zA-Z0-9_-]+$/;
  
  if (!username || username.length < minLength || username.length > maxLength) {
    return false;
  }
  return regex.test(username);
}

/**
 * Initialize form validations on page load
 */
function initFormValidation() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const usernameInput = form.querySelector('input[name="username"]');
      
      if (usernameInput && !validateUsername(usernameInput.value)) {
        e.preventDefault();
        alert('Username must be 3-50 characters, alphanumeric with underscores or hyphens only.');
        usernameInput.focus();
      }
    });
  });
}

// ============================================
// INITIALIZATION
// ============================================

/**
 * Initialize on DOM content loaded
 */
document.addEventListener('DOMContentLoaded', function() {
  initFormValidation();
  addAccessibilityFeatures();
  initContainerFilter();
});

// ============================================
// ACCESSIBILITY & UX
// ============================================

/**
 * Add accessibility and UX enhancements
 */
function addAccessibilityFeatures() {
  // Add keyboard navigation to buttons
  const buttons = document.querySelectorAll('button, a.btn');
  
  buttons.forEach(button => {
    button.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

/**
 * Copy text to clipboard
 * @param {string} text
 */
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert('Copied to clipboard!');
  }).catch(err => {
    console.error('Failed to copy:', err);
  });
}

/**
 * Format date for display
 * @param {string} dateString
 * @returns {string}
 */
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

// ============================================
// TABLE FILTERING
// ============================================

/**
 * Initialize container table filtering
 */
function initContainerFilter() {
  const input = document.getElementById('container-filter');
  const table = document.getElementById('containers-table');
  if (!input || !table) return;

  const rows = Array.from(table.querySelectorAll('tbody tr'));
  input.addEventListener('input', function() {
    const q = input.value.toLowerCase().trim();
    rows.forEach(row => {
      const user = (row.querySelector('.cell-user')?.textContent || '').toLowerCase();
      const name = (row.querySelector('.cell-name')?.textContent || '').toLowerCase();
      const status = (row.querySelector('.cell-status')?.textContent || '').toLowerCase();
      const port = (row.querySelector('.cell-port')?.textContent || '').toLowerCase();
      const match = !q || user.includes(q) || name.includes(q) || status.includes(q) || port.includes(q);
      row.style.display = match ? '' : 'none';
    });
  });
}
