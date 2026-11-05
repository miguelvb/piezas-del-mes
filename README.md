# Piezas del mes

El dinero del día a día en piezas de colores que se ven y se tocan. Prototipo de [arkinos.net](https://arkinos.net).

- `index.html`: portada para enseñar el proyecto, con la foto de la mesa real.
- `app.html`: la app. Plan del mes, base del mes, base de los gastos, base de la hucha, hoja de reglas y piezas necesarias.
- `manifest.webmanifest`, `sw.js` e iconos: permiten instalarla en iPhone y Android y abrirla sin conexión.

No necesita servidor ni base de datos: son archivos estáticos. Los datos de cada familia se guardan solo en su navegador.

## Publicar

**Por FTP (arkinos.net):** sube todos los archivos a una carpeta, por ejemplo `/piezas-del-mes/`. Quedará en `https://arkinos.net/piezas-del-mes/`.

**Con GitHub Pages:** en el repositorio, Settings → Pages → Deploy from a branch → `main` / `(root)`. Quedará en `https://miguelvb.github.io/piezas-del-mes/`.

La instalación como app y el modo sin conexión necesitan `https`.

## Instalar en el móvil

- **iPhone (Safari):** abre la app, pulsa Compartir y luego «Añadir a pantalla de inicio».
- **Android (Chrome):** abre la app y pulsa «Instalar app» en el menú ⋮.

## Reglas

1. El día 1 se monta la base del mes: una fila por color y una columna por semana. Al lado, vacías, la base de los gastos y la base de la hucha.
2. Cuando alguien de casa paga algo, pasa las piezas de ese color de la columna de esa semana a la base de los gastos.
3. Si se acaba un color, se coge del mismo color de las semanas siguientes. Si ya no queda, la semana queda en rojo. Los imprevistos son solo para imprevistos.
4. Al cerrar la semana, lo que sobra primero tapa los huecos de las semanas siguientes: del mismo color y, si ya están llenos, cambiando de color, solo los que falten. Lo que quede va a la hucha, o se guarda de más en una semana en la que se sabe que viene un gasto.
5. A fin de mes, en la base de la hucha se ve cuánto se ha ahorrado.

## Siguiente paso

Empaquetar la misma app para App Store y Google Play (por ejemplo, con Capacitor) y, si se quiere compartir entre móviles, añadir cuentas y un servidor.
