document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById('id_photo');
  const fileName = document.getElementById('selected-file-name');

  if (fileInput && fileName) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length > 0) {
        fileName.textContent = fileInput.files[0].name;
      } else {
        fileName.textContent = 'Няма избран файл';
      }
    });
  }
});
