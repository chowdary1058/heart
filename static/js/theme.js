// Persistent Light/Dark theme switching for HeartCare.ai

function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.toggle('dark');
    const newTheme = isDark ? 'dark' : 'light';
    localStorage.setItem('theme', newTheme);
    
    // Update theme toggle buttons icon and labels
    updateToggleButtons(newTheme);
    
    // Dispatch custom event for Three.js and Chart.js to listen to
    window.dispatchEvent(new CustomEvent('theme-changed', { detail: { theme: newTheme } }));
}

function updateToggleButtons(theme) {
    const buttons = document.querySelectorAll('.theme-toggle-btn');
    buttons.forEach(btn => {
        const icon = btn.querySelector('i');
        if (icon) {
            if (theme === 'dark') {
                icon.className = 'fa-solid fa-sun text-amber-400 text-lg';
            } else {
                icon.className = 'fa-solid fa-moon text-slate-600 dark:text-slate-300 text-lg';
            }
        }
    });
}

// Set initial buttons state on page load
document.addEventListener('DOMContentLoaded', () => {
    const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    updateToggleButtons(currentTheme);
    
    // Also bind event listener to any elements with .theme-toggle-btn
    document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
        btn.addEventListener('click', toggleTheme);
    });
});
