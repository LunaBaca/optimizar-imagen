import os
from flask import Flask, render_template, request, flash, redirect, url_for
from PIL import Image

app = Flask(__name__)
app.secret_key = "clave_secreta_para_flash"

# Configuración de carpetas
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta de subida si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def optimizar_imagen(ruta_imagen, ancho_maximo=800, calidad=80):
    """Redimensiona la imagen y la guarda comprimida en formato WebP."""
    with Image.open(ruta_imagen) as img:
        # Convertir a RGB si la imagen tiene canal alfa (PNG/P)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Redimensionar conservando el aspecto original
        ancho, alto = img.size
        if ancho > ancho_maximo:
            nuevo_alto = int((ancho_maximo / float(ancho)) * alto)
            img = img.resize((ancho_maximo, nuevo_alto), Image.Resampling.LANCZOS)
        
        # Generar nombre del archivo WebP
        nombre_base = os.path.splitext(os.path.basename(ruta_imagen))[0]
        nombre_optimizada = f"{nombre_base}_optimizada.webp"
        ruta_optimizada = os.path.join(app.config['UPLOAD_FOLDER'], nombre_optimizada)
        
        # Guardar con compresión WebP
        img.save(ruta_optimizada, "WEBP", quality=calidad, optimize=True)
        return nombre_optimizada

@app.route('/', methods=['GET', 'POST'])
def index():
    nombre_imagen = None
    
    if request.method == 'POST':
        if 'imagen' not in request.files:
            flash("No se subió ningún archivo.", "error")
            return redirect(request.url)
            
        file = request.files['imagen']
        
        if file.filename == '':
            flash("No seleccionaste ningún archivo.", "error")
            return redirect(request.url)
            
        if file:
            # Guardar archivo temporalmente
            ruta_temporal = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(ruta_temporal)
            
            # Optimizar y obtener solo el nombre del archivo resultante
            nombre_imagen = optimizar_imagen(ruta_temporal)
            
            # Eliminar la imagen original no optimizada
            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)
                
            flash("¡Imagen procesada y optimizada con éxito!", "exito")

    return render_template('index.html', imagen_procesada=nombre_imagen)

if __name__ == '__main__':
    app.run(debug=True)