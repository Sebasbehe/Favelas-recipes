// Toggle password visibility for all password fields
document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', () => {
        const targetId = button.getAttribute('data-target');
        const input = document.getElementById(targetId);
        const icon = button.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });
});

// Password validation and strength meter
const passwordInput = document.getElementById('password');
const confirmInput = document.getElementById('confirm_password');
const strengthBars = document.querySelectorAll('.strength-bar');
const strengthText = document.querySelector('.strength-text');

// Password requirements elements
const reqLength = document.getElementById('req-length');
const reqUpper = document.getElementById('req-upper');
const reqNumber = document.getElementById('req-number');
const reqSpecial = document.getElementById('req-special');

function checkPasswordStrength(password) {
    let strength = 0;
    const requirements = {
        length: password.length >= 8,
        upper: /[A-Z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    // Update UI for each requirement
    if (requirements.length) {
        reqLength.classList.add('met');
        reqLength.querySelector('i').classList.remove('fa-circle');
        reqLength.querySelector('i').classList.add('fa-check-circle');
    } else {
        reqLength.classList.remove('met');
        reqLength.querySelector('i').classList.remove('fa-check-circle');
        reqLength.querySelector('i').classList.add('fa-circle');
    }
    
    if (requirements.upper) {
        reqUpper.classList.add('met');
        reqUpper.querySelector('i').classList.remove('fa-circle');
        reqUpper.querySelector('i').classList.add('fa-check-circle');
    } else {
        reqUpper.classList.remove('met');
        reqUpper.querySelector('i').classList.remove('fa-check-circle');
        reqUpper.querySelector('i').classList.add('fa-circle');
    }
    
    if (requirements.number) {
        reqNumber.classList.add('met');
        reqNumber.querySelector('i').classList.remove('fa-circle');
        reqNumber.querySelector('i').classList.add('fa-check-circle');
    } else {
        reqNumber.classList.remove('met');
        reqNumber.querySelector('i').classList.remove('fa-check-circle');
        reqNumber.querySelector('i').classList.add('fa-circle');
    }
    
    if (requirements.special) {
        reqSpecial.classList.add('met');
        reqSpecial.querySelector('i').classList.remove('fa-circle');
        reqSpecial.querySelector('i').classList.add('fa-check-circle');
    } else {
        reqSpecial.classList.remove('met');
        reqSpecial.querySelector('i').classList.remove('fa-check-circle');
        reqSpecial.querySelector('i').classList.add('fa-circle');
    }
    
    // Calculate strength
    if (requirements.length) strength++;
    if (requirements.upper) strength++;
    if (requirements.number) strength++;
    if (requirements.special) strength++;
    
    // Update strength bars
    strengthBars.forEach((bar, index) => {
        bar.classList.remove('weak', 'medium', 'strong', 'active');
        if (index < strength) {
            bar.classList.add('active');
            if (strength <= 2) {
                bar.classList.add('weak');
            } else if (strength === 3) {
                bar.classList.add('medium');
            } else {
                bar.classList.add('strong');
            }
        }
    });
    
    // Update strength text
    if (password.length === 0) {
        strengthText.textContent = 'Ingresa una contraseña';
    } else if (strength <= 2) {
        strengthText.textContent = 'Contraseña débil';
    } else if (strength === 3) {
        strengthText.textContent = 'Contraseña media';
    } else {
        strengthText.textContent = 'Contraseña fuerte';
    }
    
    return strength === 4; // Returns true if all requirements met
}

// Username validation (real-time)
const usernameInput = document.getElementById('username');
const usernameHint = document.getElementById('usernameHint');

usernameInput?.addEventListener('input', () => {
    const username = usernameInput.value;
    const isValid = username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
    
    if (username.length === 0) {
        usernameHint.textContent = 'Mínimo 3 caracteres (letras, números, guión bajo)';
        usernameHint.classList.remove('error', 'success');
        usernameInput.classList.remove('error', 'valid');
    } else if (!isValid) {
        usernameHint.textContent = 'Solo letras, números y guión bajo';
        usernameHint.classList.add('error');
        usernameHint.classList.remove('success');
        usernameInput.classList.add('error');
        usernameInput.classList.remove('valid');
    } else {
        usernameHint.textContent = '✓ Nombre de usuario disponible';
        usernameHint.classList.add('success');
        usernameHint.classList.remove('error');
        usernameInput.classList.add('valid');
        usernameInput.classList.remove('error');
    }
});

// Password input event
passwordInput?.addEventListener('input', () => {
    const isStrong = checkPasswordStrength(passwordInput.value);
    validatePasswordsMatch();
    
    if (isStrong) {
        passwordInput.classList.add('valid');
        passwordInput.classList.remove('error');
    } else {
        passwordInput.classList.remove('valid');
        if (passwordInput.value.length > 0) {
            passwordInput.classList.add('error');
        } else {
            passwordInput.classList.remove('error');
        }
    }
});

// Confirm password validation
function validatePasswordsMatch() {
    const password = passwordInput?.value || '';
    const confirm = confirmInput?.value || '';
    const matchMessage = document.getElementById('match-message');
    
    if (confirm.length === 0) {
        matchMessage.textContent = '';
        matchMessage.classList.remove('error', 'success');
        confirmInput?.classList.remove('error', 'valid');
        return false;
    }
    
    if (password === confirm) {
        matchMessage.textContent = '✓ Las contraseñas coinciden';
        matchMessage.classList.add('success');
        matchMessage.classList.remove('error');
        confirmInput?.classList.add('valid');
        confirmInput?.classList.remove('error');
        return true;
    } else {
        matchMessage.textContent = '✗ Las contraseñas no coinciden';
        matchMessage.classList.add('error');
        matchMessage.classList.remove('success');
        confirmInput?.classList.add('error');
        confirmInput?.classList.remove('valid');
        return false;
    }
}

confirmInput?.addEventListener('input', validatePasswordsMatch);

// Terms checkbox validation
const termsCheckbox = document.getElementById('terms');
const registerBtn = document.getElementById('registerBtn');

function validateForm() {
    const username = usernameInput?.value || '';
    const usernameValid = username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
    const password = passwordInput?.value || '';
    const isStrong = checkPasswordStrength(password);
    const passwordsMatch = validatePasswordsMatch();
    const termsAccepted = termsCheckbox?.checked || false;
    const email = document.getElementById('email').value;
    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    const fullname = document.getElementById('fullname').value;
    const fullnameValid = fullname.trim().length >= 3;
    
    const isValid = fullnameValid && emailValid && usernameValid && isStrong && passwordsMatch && termsAccepted;
    registerBtn.disabled = !isValid;
    
    return isValid;
}

// Add event listeners for form validation
document.getElementById('fullname')?.addEventListener('input', validateForm);
document.getElementById('email')?.addEventListener('input', validateForm);
usernameInput?.addEventListener('input', validateForm);
passwordInput?.addEventListener('input', validateForm);
confirmInput?.addEventListener('input', validateForm);
termsCheckbox?.addEventListener('change', validateForm);

// Handle registration form submission
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
        showToast('Por favor completa todos los campos correctamente', 'error');
        return;
    }
    
    const fullname = document.getElementById('fullname').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Disable button while loading
    const submitBtn = document.querySelector('.btn-register');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creando cuenta...';
    submitBtn.disabled = true;
    
    try {
        // Replace with your actual API endpoint
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                fullname, 
                email, 
                username, 
                password 
            }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('¡Cuenta creada exitosamente! Redirigiendo...', 'success');
            // Redirect to login after 1.5 seconds
            setTimeout(() => {
                window.location.href = '/login';
            }, 1500);
        } else {
            showToast(data.detail || 'Error al crear la cuenta', 'error');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    } catch (error) {
        console.error('Registration error:', error);
        showToast('Error de conexión con el servidor', 'error');
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const messageEl = toast.querySelector('.toast-message');
    const iconEl = toast.querySelector('.toast-icon');
    
    toast.classList.remove('hidden', 'success', 'error', 'info');
    toast.classList.add(type);
    messageEl.textContent = message;
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Check if user is already logged in (redirect to dashboard)
async function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (token && (window.location.pathname === '/register' || window.location.pathname === '/login')) {
        try {
            const response = await fetch('/api/auth/verify', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                window.location.href = '/';
            }
        } catch (error) {
            console.log('Not authenticated');
        }
    }
}

// Run on page load
checkAuth();