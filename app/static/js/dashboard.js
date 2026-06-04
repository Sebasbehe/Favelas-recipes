// Actualizar reloj en tiempo real
function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    
    document.getElementById('current-time').textContent = `${hours}:${minutes}`;
    document.getElementById('current-date').textContent = 
        `${days[now.getDay()]}, ${now.getDate()} ${months[now.getMonth()]}`;
}

updateClock();
setInterval(updateClock, 60000);

// Animar números de estadísticas
function animateNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(element => {
        const target = parseInt(element.dataset.value);
        let current = 0;
        const increment = target / 30;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 30);
    });
}

// Ejecutar animación cuando se carga la página
window.addEventListener('load', animateNumbers);

// Datos para el gráfico
const weekData = {
    labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sab', 'Dom'],
    ingredientes: [3, 2, 4, 2, 1, 2, 3],
    recetas: [1, 2, 1, 3, 2, 1, 2]
};

const monthData = {
    labels: ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'],
    ingredientes: [12, 15, 18, 14],
    recetas: [7, 9, 8, 11]
};

// Inicializar gráfico
let chart = null;
const chartCanvas = document.getElementById('activityChart');

if (chartCanvas) {
    const ctx = chartCanvas.getContext('2d');
    
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weekData.labels,
            datasets: [
                {
                    label: 'Ingredientes añadidos',
                    data: weekData.ingredientes,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#059669'
                },
                {
                    label: 'Recetas generadas',
                    data: weekData.recetas,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#4f46e5'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#9ca3af',
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#9ca3af',
                        font: {
                            size: 12
                        },
                        stepSize: 2
                    }
                }
            }
        }
    });
}

// Cambiar entre vista semanal y mensual
document.querySelectorAll('.period-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Actualizar botón activo
        document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Actualizar gráfico
        const period = btn.dataset.period;
        
        if (period === 'week') {
            chart.data.labels = weekData.labels;
            chart.data.datasets[0].data = weekData.ingredientes;
            chart.data.datasets[1].data = weekData.recetas;
        } else {
            chart.data.labels = monthData.labels;
            chart.data.datasets[0].data = monthData.ingredientes;
            chart.data.datasets[1].data = monthData.recetas;
        }
        
        chart.update();
    });
});

// Manejar clics en acciones rápidas
document.querySelectorAll('.action-card').forEach(card => {
    card.addEventListener('click', (e) => {
        // Si no es un enlace, navegar
        if (!card.href) {
            e.preventDefault();
        }
    });
});

// Manejar clics en botones de recetas
document.querySelectorAll('.btn-icon').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const icon = btn.querySelector('i');
        
        if (icon.classList.contains('fa-eye')) {
            // Ver receta
            console.log('Ver receta');
        } else if (icon.classList.contains('fa-heart')) {
            // Toggle favorito
            icon.classList.toggle('far');
            icon.classList.toggle('fas');
            const isFavorite = icon.classList.contains('fas');
            showToast(
                isFavorite ? 'Agregado a favoritos' : 'Eliminado de favoritos',
                'success'
            );
        } else if (icon.classList.contains('fa-trash')) {
            // Eliminar
            const recipeItem = btn.closest('.recipe-item');
            recipeItem.style.animation = 'slideUp 0.3s ease-in reverse';
            setTimeout(() => {
                recipeItem.remove();
                showToast('Receta eliminada', 'success');
            }, 300);
        }
    });
});

// Toast de notificaciones
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    const style = document.createElement('style');
    style.textContent = `
        .toast {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 1rem 1.5rem;
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            font-size: 0.95rem;
            font-weight: 500;
            animation: slideInToast 0.3s ease-out;
            z-index: 1000;
            max-width: 400px;
        }
        
        .toast-success {
            border-left: 4px solid #10b981;
            color: #10b981;
        }
        
        .toast-error {
            border-left: 4px solid #ef4444;
            color: #ef4444;
        }
        
        @keyframes slideInToast {
            from {
                transform: translateX(500px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @media (max-width: 640px) {
            .toast {
                left: 1rem;
                right: 1rem;
                bottom: 1rem;
            }
        }
    `;
    
    if (!document.querySelector('style[data-toast]')) {
        style.setAttribute('data-toast', 'true');
        document.head.appendChild(style);
    }
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInToast 0.3s ease-in reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Botón de siguiente consejo
document.querySelector('.tip-footer .btn')?.addEventListener('click', () => {
    const tips = [
        '✨ Mantén tus ingredientes organizados por categoría para generar recetas más rápidamente.',
        '🌟 Los ingredientes frescos siempre dan mejores resultados en tus platos.',
        '🎯 Prueba generar recetas con combinaciones inesperadas de ingredientes.',
        '💡 Califica tus recetas para mejorar las recomendaciones del sistema.',
        '📱 Usa la búsqueda para encontrar recetas generadas anteriormente.',
        '🍽️ Comparte tus recetas favoritas con amigos y familia.'
    ];
    
    const tipElement = document.querySelector('.tip-content p');
    const randomTip = tips[Math.floor(Math.random() * tips.length)];
    
    tipElement.style.animation = 'fadeOut 0.3s ease-in';
    setTimeout(() => {
        tipElement.textContent = randomTip;
        tipElement.style.animation = 'fadeIn 0.3s ease-out';
    }, 150);
});

// Agregar animaciones CSS para los tips
const tipStyles = document.createElement('style');
tipStyles.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
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
`;
document.head.appendChild(tipStyles);

// Cargar datos reales desde la API (opcional)
async function loadDashboardData() {
    try {
        // Ejemplo: cargar estadísticas desde el servidor
        // const response = await fetch('/api/dashboard/stats');
        // const data = await response.json();
        // Actualizar elementos con los datos reales
    } catch (error) {
        console.error('Error cargando datos:', error);
    }
}

// Ejecutar al cargar
window.addEventListener('load', () => {
    console.log('Dashboard cargado correctamente');
    // loadDashboardData();
});
document.getElementById('logoutBtn')?.addEventListener('click', () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    window.location.href = '/login';
});