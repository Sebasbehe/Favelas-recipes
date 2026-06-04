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
    document.getElementById('email').value = 'demo';
    document.getElementById('password').value = 'demo123';
    showToast('Credenciales de demo cargadas', 'success');
});

// Handle login form submission
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember')?.checked || false;

    // Basic validation
    if (!username || !password) {
        showToast('Por favor completa todos los campos', 'error');
        return;
    }

    // Disable button while loading
    const submitBtn = document.querySelector('.btn-login');
    const originalText = submitBtn.innerHTML;

    submitBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> Iniciando...';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem(
                'access_token',
                data.access_token
            );

            if (remember) {
                localStorage.setItem(
                    'remember_user',
                    username
                );
            }

            showToast(
                '¡Bienvenido de vuelta!',
                'success'
            );

            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);

        } else {
            showToast(
                data.detail || 'Credenciales incorrectas',
                'error'
            );
        }

    } catch (error) {
        console.error('Login error:', error);

        showToast(
            'Error de conexión con el servidor',
            'error'
        );

    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');

    if (!toast) return;

    const messageEl = toast.querySelector('.toast-message');

    toast.classList.remove(
        'hidden',
        'success',
        'error'
    );

    toast.classList.add(type);

    if (messageEl) {
        messageEl.textContent = message;
    }

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}