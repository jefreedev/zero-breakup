const customFileInput = document.querySelector('.custom-file-input');
const selectedImage = document.getElementById('selectedImage');

customFileInput.addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (file) {
        selectedImage.src = URL.createObjectURL(file);
        selectedImage.classList.remove('d-none');
    } else {
        selectedImage.src = '';
        selectedImage.classList.add('d-none');
    }
});