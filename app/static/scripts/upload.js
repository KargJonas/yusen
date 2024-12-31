
// Code for custom file upload button.
// This updates the file name in the interface as soon as a file is selected.
document.addEventListener('change', async (e) => {
    if (!e.target.classList.contains('file-selector-input')) return;
    // const fileName = e.target.files.length > 0 ? e.target.files[0].name : 'No file chosen';
    const fileName = e.target.files.length > 0 ? 'File selected' : 'No file chosen';
    document.querySelector('.file-name').textContent = fileName;
});
