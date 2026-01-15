# SaaS Control Panel - Reusable Components & Code Snippets

## CSS Components

### 1. Alert Box
```html
<div class="alert alert-success">
  ✅ Operation completed successfully
</div>
```

```css
.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  border-left: 4px solid;
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  border-color: #10b981;
  color: #065f46;
}

.alert-danger {
  background: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
  color: #7f1d1d;
}

.alert-warning {
  background: rgba(245, 158, 11, 0.1);
  border-color: #f59e0b;
  color: #78350f;
}

.alert-info {
  background: rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
  color: #1e3a8a;
}
```

### 2. Stats Card
```html
<div class="stats-card">
  <div class="stat-value">42</div>
  <div class="stat-label">Active Containers</div>
  <div class="stat-change positive">+5 this week</div>
</div>
```

```css
.stats-card {
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.stat-change {
  font-size: 12px;
  font-weight: 600;
}

.stat-change.positive {
  color: var(--success-color);
}

.stat-change.negative {
  color: var(--danger-color);
}
```

### 3. Progress Bar
```html
<div class="progress">
  <div class="progress-bar" style="width: 65%;"></div>
</div>
```

```css
.progress {
  width: 100%;
  height: 8px;
  background: var(--light-bg);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.progress-bar.success {
  background: var(--success-color);
}

.progress-bar.danger {
  background: var(--danger-color);
}
```

### 4. Badge with Icon
```html
<span class="badge badge-success">
  <span class="badge-icon">✓</span>
  Running
</span>
```

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-icon {
  font-size: 10px;
}
```

### 5. Tooltip
```html
<button class="btn btn-primary" title="Click to refresh">
  Refresh
</button>
```

```css
[title] {
  position: relative;
  cursor: help;
}

[title]:hover::after {
  content: attr(title);
  position: absolute;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  background: #1f2937;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  white-space: nowrap;
  z-index: 1000;
  animation: slideUp 0.2s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}
```

---

## JavaScript Components

### 1. Confirmation Dialog
```javascript
function confirmDelete(itemName) {
  return confirm(
    `Are you sure you want to delete "${itemName}"?\n\nThis action cannot be undone.`
  );
}

// Usage:
// <a href="/delete/user-123" onclick="return confirmDelete('User 123')">Delete</a>
```

### 2. Form Validator
```javascript
class FormValidator {
  constructor(formSelector) {
    this.form = document.querySelector(formSelector);
    this.errors = [];
  }

  validateEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }

  validateUsername(username) {
    return username && username.length >= 3 && username.length <= 50;
  }

  validatePassword(password) {
    return password && password.length >= 6;
  }

  showError(inputElement, message) {
    inputElement.style.borderColor = '#ef4444';
    inputElement.setAttribute('aria-invalid', 'true');
    
    inputElement.addEventListener('focus', () => {
      inputElement.style.borderColor = '';
      inputElement.removeAttribute('aria-invalid');
    }, { once: true });
  }

  validate() {
    this.errors = [];
    
    const inputs = this.form.querySelectorAll('input[required]');
    inputs.forEach(input => {
      if (!input.value.trim()) {
        this.errors.push(`${input.name} is required`);
        this.showError(input, `${input.name} cannot be empty`);
      }
    });

    return this.errors.length === 0;
  }
}

// Usage:
// const validator = new FormValidator('form');
// form.addEventListener('submit', (e) => {
//   if (!validator.validate()) e.preventDefault();
// });
```

### 3. Toast Notification
```javascript
function showToast(message, type = 'info', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('show');
  }, 10);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// CSS for toast:
/*
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 16px 20px;
  background: #1f2937;
  color: white;
  border-radius: 8px;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 9999;
}

.toast.show {
  opacity: 1;
}

.toast-success {
  background: var(--success-color);
}

.toast-danger {
  background: var(--danger-color);
}

.toast-warning {
  background: var(--warning-color);
}
*/

// Usage:
// showToast('Container started successfully', 'success');
```

### 4. Debounce Function
```javascript
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// Usage:
// const handleSearch = debounce((e) => {
//   // Perform search
//   console.log(e.target.value);
// }, 300);
//
// searchInput.addEventListener('input', handleSearch);
```

### 5. Copy to Clipboard
```javascript
function copyToClipboard(text, onSuccess) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text)
      .then(() => {
        if (onSuccess) onSuccess();
        showToast('Copied to clipboard!', 'success');
      })
      .catch(() => {
        showToast('Failed to copy', 'danger');
      });
  } else {
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showToast('Copied to clipboard!', 'success');
  }
}

// Usage:
// <button onclick="copyToClipboard('user-container-123')">Copy ID</button>
```

---

## HTML Templates

### 1. Empty State
```html
<div class="empty-state">
  <p class="empty-icon">📦</p>
  <h3 class="empty-title">No containers yet</h3>
  <p class="empty-text">Create your first container to get started</p>
  <a href="/create" class="btn btn-primary">Create Container</a>
</div>

<style>
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.empty-text {
  color: var(--text-secondary);
  margin-bottom: 24px;
}
</style>
```

### 2. Loading Spinner
```html
<div class="spinner"></div>

<style>
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--light-bg);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
```

### 3. Modal Dialog
```html
<div class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h2>Dialog Title</h2>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <!-- Content here -->
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">Confirm</button>
    </div>
  </div>
</div>

<style>
.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  align-items: center;
  justify-content: center;
}

.modal.show {
  display: flex;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow: auto;
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--text-secondary);
}
</style>
```

---

## API Response Handlers

### 1. Fetch with Error Handling
```javascript
async function apiCall(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    showToast('An error occurred. Please try again.', 'danger');
    throw error;
  }
}

// Usage:
// const data = await apiCall('/api/containers');
```

---

## Utility Functions

### 1. Format Date and Time
```javascript
function formatDate(dateString, format = 'short') {
  const date = new Date(dateString);
  const options = {
    short: { year: 'numeric', month: 'short', day: 'numeric' },
    long: { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    },
    time: { hour: '2-digit', minute: '2-digit', second: '2-digit' },
  };
  
  return date.toLocaleDateString('en-US', options[format] || options.short);
}

// Usage:
// formatDate('2026-01-15'); // Jan 15, 2026
// formatDate('2026-01-15T10:30:00', 'long'); // January 15, 2026, 10:30 AM
```

### 2. Truncate Text
```javascript
function truncate(text, length = 50, suffix = '...') {
  if (text.length <= length) return text;
  return text.slice(0, length).trim() + suffix;
}

// Usage:
// truncate('Very long container name...', 20); // Very long container...
```

### 3. Get Query Parameters
```javascript
function getQueryParam(name) {
  const params = new URLSearchParams(window.location.search);
  return params.get(name);
}

// Usage:
// getQueryParam('user_id'); // From ?user_id=123
```

---

## Animation Keyframes Library

```css
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
```

---

## Browser Compatibility

These components are compatible with:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari 13+, Chrome Android 90+)

---

## Testing Examples

### 1. CSS Testing Checklist
- [ ] All colors are readable (contrast ratio ≥ 4.5:1)
- [ ] Hover states are clearly visible
- [ ] Focus states work with keyboard
- [ ] Responsive at 320px, 768px, 1920px
- [ ] No horizontal scrolling on mobile

### 2. JavaScript Testing
```javascript
// Test form validation
function testFormValidation() {
  const input = document.querySelector('input[name="username"]');
  input.value = 'a'; // Too short
  
  console.assert(
    !validateUsername(input.value),
    'Should reject short usernames'
  );
  
  input.value = 'validuser123';
  console.assert(
    validateUsername(input.value),
    'Should accept valid usernames'
  );
}

testFormValidation();
```

---

**Last Updated:** January 2026
