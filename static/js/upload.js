document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const loadingIndicator = document.getElementById('loadingIndicator');

    form.addEventListener('submit', () => {
        loadingIndicator.style.display = 'block';
    })
})

document.addEventListener('DOMContentLoaded', () => {
    fetch('/upload/all_video', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    })
        .then(response => response.json())
        .then(data => {
            const fileList = document.getElementById('file-list');
            data.forEach(filename => {
                const li = document.createElement('li');
                // li.textContent = filename;
                aLink = document.createElement('a');
                aLink.href = URL.createObjectURL(`/upload/video/${filename}`);
                aLink.textContent = filename;
                li.appendChild(aLink);
                fileList.appendChild(li);
            });
        })
        .catch(error => {
            console.error("Error fetching file list");
        })
})