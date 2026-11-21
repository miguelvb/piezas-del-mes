# Librito «Piezas del mes · Guía de uso»

Fuente del librito en A5 (16 páginas). Genera `librito.html` y lo imprime a PDF con Chromium.

```
cd librito
python3 build.py          # necesita: pip install segno (código QR)
node render.js "$PWD/librito.html" "$PWD/librito-piezas-del-mes.pdf"   # necesita playwright
```

Letras: Bricolage Grotesque y Atkinson Hyperlegible (Google Fonts, licencia OFL), en `fonts/`.
v2 (21 nov 2026): reglas revisadas por Miguel: gastos fijos fuera, la pieza «cambia de base», imprevistos en gris oscuro,
el domingo lo que sobra va a la hucha o se guarda de más en otra semana, y no solo para familias.
