// Toggle password visibility
document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', () => {
        const input = button.previousElementSibling;
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

// Fill demo credentials
document.getElementById('fillDemoBtn')?.addEventListener('click', () => {
    document.getElementById('email').value = 'demo@favelas.com';
    document.getElementById('password').value = 'demo123';
    showToast('Credenciales de demo cargadas', 'success');
});

// Handle login form submission
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember')?.checked || false;
    
    // Basic validation
    if (!email || !password) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }
    
    // Disable button while loading
    const submitBtn = document.querySelector('.btn-login');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Iniciando...';
    submitBtn.disabled = true;
    
    try {
        // Replace with your actual API endpoint
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password, remember }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token
            localStorage.setItem('access_token', data.access_token);
            if (remember) {
                localStorage.setItem('refresh_token', data.refresh_token);
            }
            showToast('¡Bienvenido de vuelta!', 'success');
            // Redirect to dashboard
            setTimeout(() => {
                window.location.href = '/';
            }, 1000);
        } else {
            showToast(data.detail || 'Credenciales incorrectas', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Error de conexión con el servidor', 'error');
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const messageEl = toast.querySelector('.toast-message');
    const iconEl = toast.querySelector('.toast-icon');
    
    toast.classList.remove('hidden', 'success', 'error');
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
    if (token && window.location.pathname === '/login') {
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
            // Token invalid, stay on login page
            console.log('Not authenticated');
        }
    }
}

// Run on page load
checkAuth();
