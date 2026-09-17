document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('uploadForm');
    const inputImagen = document.getElementById('imagen');
    const errorContainer = document.getElementById('errorContainer');

    form.addEventListener('submit', (e) => {
        errorContainer.innerHTML = '';
        let errores = [];
        const file = inputImagen.files[0];

        if (!file) {
            errores.push("Debe seleccionar un archivo de imagen.");
        } else {
            // Formatos permitidos
            const tiposPermitidos = ['image/jpeg', 'image/png', 'image/webp'];
            if (!tiposPermitidos.includes(file.type)) {
                errores.push("Solo se admiten imágenes en formato JPG, PNG o WEBP.");
            }

            // Tamaño máximo de 5 MB
            const maxPesoBytes = 5 * 1024 * 1024;
            if (file.size > maxPesoBytes) {
                errores.push("El archivo es demasiado grande (máximo 5 MB).");
            }
        }

        if (errores.length > 0) {
            e.preventDefault();
            errores.forEach(msg => {
                const p = document.createElement('p');
                p.className = 'text-red-500 font-medium text-sm mt-1';
                p.textContent = msg;
                errorContainer.appendChild(p);
            });
        }
    });
});