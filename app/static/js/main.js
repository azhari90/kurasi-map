/**
 * Kurasi Map - Main JavaScript
 */

// Auth token management
const TOKEN_KEY = 'access_token';

// Store auth token
function storeToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

// Get auth token
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

// Remove auth token
function removeToken() {
    localStorage.removeItem(TOKEN_KEY);
}

// Check if user is authenticated
function isAuthenticated() {
    return !!getToken();
}

// Logout function
function logout() {
    removeToken();
    window.location.href = '/login';
}

// Add auth header to fetch requests
async function fetchWithAuth(url, options = {}) {
    const token = getToken();
    
    if (token) {
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`
        };
    }
    
    return fetch(url, options);
}

// Handle logout button click
document.addEventListener('DOMContentLoaded', function() {
    const logoutLink = document.querySelector('a[href="/logout"]');
    
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Category icons and colors
const categoryIcons = {
    'restaurants': 'utensils',
    'cafes': 'coffee',
    'sports': 'volleyball-ball',
    'hospitals': 'hospital',
    'shopping': 'shopping-bag'
};

const categoryColors = {
    'restaurants': '#FF5733',
    'cafes': '#C70039',
    'sports': '#900C3F',
    'hospitals': '#581845',
    'shopping': '#FFC300'
};

// Create custom marker for map
function createCustomMarker(category, latlng) {
    const color = categoryColors[category] || '#3388ff';
    const icon = categoryIcons[category] || 'map-marker-alt';
    
    const markerHtml = `
        <div class="marker-pin" style="background-color: ${color}">
            <i class="fas fa-${icon}" style="color: white"></i>
        </div>
    `;
    
    const customIcon = L.divIcon({
        html: markerHtml,
        className: 'custom-marker',
        iconSize: [30, 42],
        iconAnchor: [15, 42]
    });
    
    return L.marker(latlng, { icon: customIcon });
}

// Format operating hours for display
function formatOperatingHours(hours) {
    if (!hours) return '';
    
    let html = '<div class="mt-3"><h6>Operating Hours</h6><ul class="list-unstyled">';
    
    for (const [day, time] of Object.entries(hours)) {
        html += `<li><strong>${day}:</strong> ${time}</li>`;
    }
    
    html += '</ul></div>';
    return html;
}

// Share location
function shareLocation(location) {
    if (navigator.share) {
        navigator.share({
            title: location.name,
            text: `Check out ${location.name} on Kurasi Map!`,
            url: window.location.href
        })
        .catch(error => console.log('Error sharing:', error));
    } else {
        // Fallback for browsers that don't support Web Share API
        const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(`Check out ${location.name} on Kurasi Map!`)}&url=${encodeURIComponent(window.location.href)}`;
        window.open(shareUrl, '_blank');
    }
}

// Handle form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Get user's current location
function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    resolve({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    });
                },
                error => {
                    reject(error);
                }
            );
        } else {
            reject(new Error('Geolocation is not supported by this browser.'));
        }
    });
}

// Calculate distance between two coordinates in kilometers
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the earth in km
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2); 
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    const d = R * c; // Distance in km
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI/180);
}