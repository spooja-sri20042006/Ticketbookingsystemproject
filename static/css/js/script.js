// Advanced form validation

function validateBooking() {
    const source = document.getElementById('source').value.trim();
    const destination = document.getElementById('destination').value.trim();
    const date = document.getElementById('date').value;

    if (source === "" || destination === "") {
        showNotification('Please fill all required fields!', 'error');
        return false;
    }

    // Check if source and destination are the same
    if (source.toLowerCase() === destination.toLowerCase()) {
        showNotification('Source and destination cannot be the same!', 'error');
        return false;
    }

    // Check if date is in the future
    if (date) {
        const selectedDate = new Date(date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            showNotification('Please select a future date!', 'error');
            return false;
        }
    }

    showNotification('Searching for available bookings...', 'success');
    return true;
}

// Notification function
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        z-index: 9999;
        animation: slideInNotification 0.3s ease-out;
        backdrop-filter: blur(10px);
        ${type === 'error' 
            ? 'background: rgba(244, 67, 54, 0.9); border: 1px solid #f44336;' 
            : 'background: rgba(76, 175, 80, 0.9); border: 1px solid #4caf50;'
        }
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutNotification 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInNotification {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutNotification {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Welcome message and initialization
window.onload = function() {
    console.log("TravelGo Platform Loaded");
    console.log("Modern UI Active");
    
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Initialize tooltips
    initializeTooltips();

    // Transportation dropdown color handling
    const transportSelect = document.getElementById('transportation');
    if (transportSelect) {
        const accentMap = {
            bus: ['#f7b500', '#ff8b2d'],
            car: ['#3ddc97', '#0fd1d8'],
            train: ['#cc5efb', '#6f42c1'],
            flight: ['#47d7ff', '#ff5f87'],
            boat: ['#0ed2ff', '#1a87ff'],
        };

        const applyTransportStyle = (value) => {
            transportSelect.classList.remove('bus', 'car', 'train', 'flight', 'boat');
            if (!value) return;

            transportSelect.classList.add(value);

            const [accent, accent2] = accentMap[value] || [null, null];
            if (accent) {
                document.documentElement.style.setProperty('--accent', accent);
            }
            if (accent2) {
                document.documentElement.style.setProperty('--accent2', accent2);
            }
        };

        transportSelect.addEventListener('change', () => {
            applyTransportStyle(transportSelect.value);
        });

        // Apply initial style if a value is already selected
        if (transportSelect.value) {
            applyTransportStyle(transportSelect.value);
        }
    }
}

// Initialize tooltips
function initializeTooltips() {
    const elements = document.querySelectorAll('[data-tooltip]');
    elements.forEach(el => {
        el.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 0.5rem 0.75rem;
                border-radius: 5px;
                font-size: 0.85rem;
                white-space: nowrap;
                z-index: 1000;
            `;
            this.appendChild(tooltip);
        });
        
        el.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}

// Format phone number
function formatPhoneNumber(input) {
    input.value = input.value.replace(/\D/g, '').replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
}

// Add loading animation
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        backdrop-filter: blur(5px);
    `;
    
    overlay.innerHTML = `
        <div style="
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top: 4px solid #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
    `;
    
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}