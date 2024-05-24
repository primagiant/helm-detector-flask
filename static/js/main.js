document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const loadingIndicator = document.getElementById('loadingIndicator');

    form.addEventListener('submit', () => {
        loadingIndicator.style.display = 'block';
    })
})