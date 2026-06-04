// Toggle password visibility
document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', () => {
        const targetId = button.getAttribute('data-target');
        const input = document.getElementById(targetId);
        const icon = button.querySelector('i');

        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    });
});

// Password validation
const passwordInput = document.getElementById('password');
const confirmInput = document.getElementById('confirm_password');

function validatePasswordsMatch() {
    const password = passwordInput?.value || '';
    const confirm = confirmInput?.value || '';

    if (!confirm) return false;

    return password === confirm;
}

confirmInput?.addEventListener('input', validatePasswordsMatch);

// Handle registration form submission
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (!email || !username || !password) {
        showToast('Completa todos los campos', 'error');
        return;
    }

    if (password !== confirmPassword) {
        showToast('Las contraseñas no coinciden', 'error');
        return;
    }

    const submitBtn = document.querySelector('.btn-register');
    const originalText = submitBtn.innerHTML;

    submitBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> Registrando...';
    submitBtn.disabled = true;

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                email,
                password
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast(
                'Usuario registrado correctamente',
                'success'
            );

            setTimeout(() => {
                window.location.href = '/login';
            }, 1500);

        } else {
            showToast(
                data.detail || 'Error al registrar usuario',
                'error'
            );
        }

    } catch (error) {
        console.error(error);

        showToast(
            'Error de conexión con el servidor',
            'error'
        );

    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Toast
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');

    if (!toast) {
        alert(message);
        return;
    }

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
// Habilitar botón cuando se acepten términos
const termsCheckbox = document.getElementById('terms');
const registerBtn = document.getElementById('registerBtn');

termsCheckbox?.addEventListener('change', () => {
    registerBtn.disabled = !termsCheckbox.checked;
});