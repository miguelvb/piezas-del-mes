#!/usr/bin/env python3
"""Librito «Piezas del mes» v2 (21 nov 2026) -> librito.html (A5). Render to PDF with render.js."""
import segno, io, base64

C = dict(G='#237841', R='#D64A3A', Y='#F2B632', B='#0055BF', W='#F4F2EC', K='#3A3B3F')
EDGE = dict(G='#1a5c31', R='#a8392c', Y='#c99421', B='#003f8f', W='#bdb9ae', K='#232427')
ROWS = [('Comida', 'G'), ('Gasolina', 'R'), ('Ocio', 'Y'), ('Hogar', 'B'), ('Bolsillo', 'W')]


def board(cells, rows=ROWS, marks=(), caption=''):
    """cells[(row, week)] = number of pieces; marks = [(row, week, colour)] dashed boxes."""
    W, lx, top, cw, rh = 470, 92, 34, 88, 36
    H = top + rh * len(rows) + 14
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" class="board">',
         f'<rect x="{lx-6}" y="{top-8}" width="{cw*4+12}" height="{rh*len(rows)+12}" rx="10" fill="#E9A9C9"/>']
    for w in range(4):
        s.append(f'<text x="{lx+cw*w+cw/2}" y="20" class="bh">S{w+1}</text>')
    for r, (lab, col) in enumerate(rows):
        y0 = top + r * rh
        s.append(f'<text x="{lx-14}" y="{y0+rh/2+4}" class="bl">{lab}</text>')
        for w in range(4):
            n = cells.get((r, w), 0)
            for k in range(n):
                row2, i = divmod(k, 4)
                x = lx + cw * w + 4 + i * 20; y = y0 + 4 + row2 * 12
                s.append(f'<rect x="{x}" y="{y}" width="18" height="10" rx="3" fill="{C[col]}" stroke="{EDGE[col]}" stroke-width="1"/>')
    for r, w, colr in marks:
        y0 = top + r * rh
        s.append(f'<rect x="{lx+cw*w+2}" y="{y0+1}" width="{cw-8}" height="{rh-8}" rx="5" fill="none" stroke="{colr}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    s.append('</svg>')
    cap = f'<p class="cap">{caption}</p>' if caption else ''
    return f'<div class="fig">{"".join(s)}</div>{cap}'


PLAN = {'G': 7, 'R': 3, 'Y': 2, 'B': 3, 'W': 2}
def full():
    return {(r, w): PLAN[c] for r, (_, c) in enumerate(ROWS) for w in range(4)}

def sw(c):
    return f'<span class="sw" style="background:{C[c]};border-color:{EDGE[c]}"></span>'

qr = segno.make('https://miguelvb.github.io/piezas-del-mes/', error='m')
buf = io.BytesIO(); qr.save(buf, kind='svg', scale=4, border=0, dark='#22211D')
QR = buf.getvalue().decode()

def b64(p):
    return base64.b64encode(open(p, 'rb').read()).decode()

SYM = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><rect width="100" height="100" rx="22" fill="#F7F5F1"/>
<g stroke-width="1.2"><rect x="16" y="56" width="14" height="9" rx="2.5" fill="#F2B632" stroke="#c99421"/><rect x="16" y="66" width="14" height="9" rx="2.5" fill="#0055BF" stroke="#003f8f"/><rect x="16" y="76" width="14" height="9" rx="2.5" fill="#237841" stroke="#1a5c31"/>
<rect x="33" y="66" width="14" height="9" rx="2.5" fill="#237841" stroke="#1a5c31"/><rect x="33" y="76" width="14" height="9" rx="2.5" fill="#D64A3A" stroke="#a8392c"/>
<rect x="50" y="46" width="14" height="9" rx="2.5" fill="#237841" stroke="#1a5c31"/><rect x="50" y="56" width="14" height="9" rx="2.5" fill="#F2B632" stroke="#c99421"/><rect x="50" y="66" width="14" height="9" rx="2.5" fill="#0055BF" stroke="#003f8f"/><rect x="50" y="76" width="14" height="9" rx="2.5" fill="#0055BF" stroke="#003f8f"/>
<rect x="67" y="76" width="14" height="9" rx="2.5" fill="#237841" stroke="#1a5c31"/>
<rect x="70" y="20" width="14" height="9" rx="2.5" fill="#F2B632" stroke="#c99421" transform="rotate(-18 77 24)"/></g>
<rect x="14" y="87" width="70" height="4" rx="2" fill="#22211D"/></svg>"""
ICON = None; MESA = b64('../mesa-real.jpg')

pages = []
def page(body, n=None, cls=''):
    num = f'<div class="num">{n}</div>' if n else ''
    pages.append(f'<section class="page {cls}">{body}{num}</section>')

# 1 · portada
page(f'''<div class="icon">{SYM}</div>
<h1 class="cover">piezas<br>del <span>mes</span></h1>
<h2 class="sub">Guía de uso</h2>
<p class="lead">El dinero del mes en piezas de colores que se ven y se tocan.</p>
<p class="ed">EDICIÓN PARA QUIENES LO PRUEBAN · 2026</p>''', cls='cover')

# 2 · hola
page(f'''<h1>Hola</h1>
<p>Gracias por probar <b>Piezas del mes</b>. Durante un mes vas a tener encima de la mesa el dinero de tus gastos del día a día, en piezas de colores. Cada pieza es dinero de verdad: cuando alguien de casa paga algo, una pieza cambia de sitio.</p>
<p>Sirve igual si vives solo, en pareja, con tu familia o compartiendo piso. La idea es sencilla: lo que se ve, se entiende.</p>
<div class="photo"><img src="data:image/jpeg;base64,{MESA}"></div>
<p class="cap">Una mesa de verdad: delante la base del mes, detrás la de los gastos.</p>
<h3>Qué necesitas</h3>
<ul><li>Las piezas de construcción de colores y las tres bases.</li>
<li>Un cuaderno y un lápiz. La app es opcional: gratis y sin registrarse.</li>
<li>Diez minutos el día 1 y cinco minutos cada domingo.</li>
<li>Si quieres, una hoja en la nevera para apuntar gastos.</li></ul>''', 2)

# 3 · la mesa
rows3 = [('G', 'Verde', 'Comida y súper'), ('R', 'Rojo', 'Gasolina y transporte'), ('Y', 'Amarillo', 'Ocio: bares, planes, cumpleaños'),
         ('B', 'Azul', 'Hogar: farmacia, cosas de casa'), ('W', 'Blanco', 'Bolsillo: dinero suelto'), ('K', 'Gris oscuro', 'Imprevistos (solo para imprevistos)')]
t3 = ''.join(f'<tr><td>{sw(c)}</td><td><b>{a}</b></td><td>{b}</td></tr>' for c, a, b in rows3)
page(f'''<h1>La mesa: tres bases</h1>
<div class="bases">
<div class="bx"><div class="tag pink">Base del mes</div><p>Una fila para cada cosa en la que gastas y una columna para cada semana. El día 1 está llena: es todo el dinero disponible del mes.</p></div>
<div class="bx"><div class="tag grey">Base de los gastos</div><p>Cuando alguien paga, las piezas cambian a esta base, a la columna de esa semana. Se ve qué semana ha ido cara.</p></div>
<div class="bx"><div class="tag yel">Base de la hucha</div><p>Lo que sobra al cerrar cada semana. A fin de mes, aquí está lo que has ahorrado.</p></div></div>
<h3>Cada color es una cosa</h3>
<table class="t colors">{t3}</table>
<p class="note">Esto es un ejemplo. Tú eliges cuántas categorías usar, cómo se llaman y qué color va a cada una. Lo único fijo es que un color significa una sola cosa durante todo el mes.</p>''', 3)

# 4 · plan
page('''<p class="eye">PASO 1 · ANTES DEL DÍA 1</p><h1>Haz el plan</h1>
<ol><li><b>Descuenta los gastos fijos.</b> Alquiler o hipoteca, luz, seguros: no entran en la mesa. Las piezas son lo que te queda para el mes una vez descontados.</li>
<li><b>Elige cuánto vale una pieza.</b> Lo normal es 10 €. Con poco dinero en efectivo, 5 €.</li>
<li><b>Decide cuánto va a cada color</b> en el mes. Las cuentas son sencillas y están en la página 10; también las hace la app.</li></ol>
<h3>Un ejemplo, con piezas de 10 €</h3>
<table class="t"><tr class="h"><td>COLOR</td><td>AL MES</td><td>PIEZAS</td><td>POR SEMANA</td></tr>
<tr><td>Comida</td><td>280 €</td><td>28</td><td>7</td></tr><tr><td>Gasolina</td><td>120 €</td><td>12</td><td>3</td></tr>
<tr><td>Ocio</td><td>80 €</td><td>8</td><td>2</td></tr><tr><td>Hogar</td><td>120 €</td><td>12</td><td>3</td></tr>
<tr><td>Bolsillo</td><td>80 €</td><td>8</td><td>2</td></tr><tr><td>Imprevistos</td><td>150 €</td><td>15</td><td>todo el mes, o 4, 4, 4 y 3</td></tr></table>
<h3>Imprevistos: elige cómo</h3>
<ul><li><b>En un montón aparte</b>, al lado de la base, para todo el mes.</li>
<li><b>Por semanas</b>, como una fila gris oscuro más en la base: 15 piezas son 4, 4, 4 y 3. Así se ve mejor cuánto queda cada semana.</li></ul>''', 4)

# 5 · montar
page(f'''<p class="eye">PASO 2 · EL DÍA 1</p><h1>Monta la mesa</h1>
<p>Con tu plan del cuaderno (o la app) sabes cuántas piezas de cada color van en cada semana. Ponlas en la base del mes, una fila por color y una columna por semana. La base de los gastos y la hucha empiezan vacías.</p>
{board(full(), caption='La base del mes del ejemplo, el día 1. Cada montón es el dinero de ese color para esa semana.')}
<p>Si compartes los gastos, montadla juntos. Contar las piezas es la primera conversación sobre el dinero del mes, y suele ser la más útil.</p>''', 5)

# 6 · regla 1
page('''<p class="eye">REGLA 1</p><h1>Al pagar, la pieza cambia de base</h1>
<p>Cuando alguien de casa paga algo, coge piezas del color de lo que ha comprado, de la semana en la que estás, y las cambia a la base de los gastos, en la misma columna.</p>
<h3>Se redondea</h3>
<table class="t"><tr class="h"><td>GASTO</td><td>PIEZAS DE 10 €</td></tr>
<tr><td>23 € en el súper</td><td>2 verdes</td></tr><tr><td>27 € en el súper</td><td>3 verdes</td></tr>
<tr><td>8 € en el bar</td><td>1 amarilla</td></tr><tr><td>3 € de pan</td><td>se apunta en «sueltos» y se suma el domingo</td></tr></table>
<p>Apunta cada gasto al momento en la hoja de la nevera (página 11) o en la app. Así el domingo las cuentas cuadran.</p>
<div class="box"><b>Ver cómo la pieza cambia de base</b> explica más que cualquier cuenta. Si en casa hay niños, que sean ellos quienes la muevan.</div>''', 6)

# 7 · regla 2
c7 = full(); c7[(2, 0)] = 0; c7[(2, 1)] = 0
page(f'''<p class="eye">REGLA 2</p><h1>Si se acaba un color</h1>
<p>Si en una semana se acaba un color, se cogen piezas <b>del mismo color</b> de otra semana, normalmente la siguiente. Con sus consecuencias: esa semana tendrá menos. También puedes repartirlo entre varias semanas, pero procura que sea la excepción.</p>
{board(c7, marks=[(2, 1, '#D64A3A')], caption='El ocio de la semana 1 se ha gastado y se han cogido las 2 piezas amarillas de la semana 2. La semana 2 se queda sin ocio.')}
<h3>Semana en rojo</h3>
<p>Si ya no queda de ese color en ninguna semana, la semana se queda <b>en rojo</b>. No pasa nada malo: es un aviso. Se habla en casa y se ajusta el plan del mes siguiente.</p>
<div class="box"><b>Los imprevistos son solo para imprevistos.</b> Una avería o una visita al médico, sí. Un capricho porque se acabó el ocio, no. Si los tienes por semanas y un imprevisto no cabe, se coge gris oscuro de las semanas siguientes, como con cualquier color.</div>''', 7)

# 8 · regla 3
c8 = full(); c8.update({(r, 0): 0 for r in range(5)}); c8[(2, 2)] = 4
page(f'''<p class="eye">REGLA 3 · CADA DOMINGO</p><h1>Al cerrar la semana, lo que sobra se mueve</h1>
<p>Lo que queda en la columna de la semana no se puede quedar ahí. Se mueve siempre, en este orden:</p>
<ol><li><b>Rellena los colores que tienen menos de lo que les toca</b> en las semanas siguientes (los huecos que dejó la regla 2). La pieza cambia de color si hace falta.</li>
<li><b>Si aún sobra, repártelo como quieras</b> en las semanas siguientes, en su color o en otro (por ejemplo, para un cumpleaños o un viaje), <b>o llévalo a la hucha.</b></li></ol>
{board(c8, marks=[(1, 1, '#237841'), (2, 2, '#C9668F')], caption='Semana 1 cerrada. La semana 2 tenía un hueco de 3 rojas (regla 2): 2 verdes y 1 amarilla que sobraban se convierten en rojas y lo rellenan. Lo que aún sobraba, a elección: 2 blancas se guardan como amarillas para un cumpleaños en la semana 3 y el resto va a la hucha.')}
<p class="cap">Los grises oscuros que sobran el domingo se quedan para imprevistos. A fin de mes, los que no hayas usado se pueden ahorrar o pasar al mes siguiente.</p>''', 8)

# 9 · fin de mes
page('''<p class="eye">FIN DE MES</p><h1>Mira la hucha</h1>
<p>El último día, cuenta las piezas de la hucha. Cada una es dinero que no se ha gastado. Decide qué hacer con él: guardarlo, un plan o, si compartes los gastos, una parte para cada uno.</p>
<p>Los imprevistos que no hayas usado se pueden ahorrar o pasar al mes siguiente.</p>
<p>Mira también la base de los gastos. ¿Qué semana fue más cara? ¿Qué color se acabó antes? Con eso se hace el plan del mes siguiente.</p>
<h3>Preguntas que suelen salir</h3>
<p class="q">¿Y si pago con tarjeta?</p><p class="a">Da igual cómo se pague: la pieza cambia de base igual.</p>
<p class="q">¿Y si se me olvida mover una pieza?</p><p class="a">Si está apuntado en la hoja, el domingo se pone al día.</p>
<p class="q">¿Y si me faltan piezas de un color?</p><p class="a">Suma las piezas del plan. Conviene tener un 20 o 30 % de repuesto, porque las piezas cambian de color al rellenar huecos o al guardar de más.</p>
<p class="q">¿Quién mueve las piezas?</p><p class="a">Quien paga. Cualquiera de casa.</p>''', 9)

# 10 · todo a mano
t10 = [('Verde', 280, 28, '7', '7', '7', '7'), ('Rojo', 120, 12, '3', '3', '3', '3'), ('Amarillo', 80, 8, '2', '2', '2', '2'),
       ('Azul', 120, 12, '3', '3', '3', '3'), ('Blanco', 80, 8, '2', '2', '2', '2')]
r10 = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td><td>{g}</td></tr>' for a, b, c, d, e, f, g in t10)
page(f'''<p class="eye">SIN PANTALLAS · 1</p><h1>Todo a mano: el plan</h1>
<p>La app ayuda, pero no hace falta: con un cuaderno, un lápiz y una hoja en la nevera se lleva el mes entero sin pantallas.</p>
<h3>Las cuentas del plan</h3>
<ol><li><b>Euros de cada color ÷ valor de la pieza = piezas del mes.</b><br>Comida: 280 € ÷ 10 € = 28 piezas.</li>
<li><b>Piezas del mes ÷ 4 = piezas por semana.</b><br>28 ÷ 4 = 7 piezas verdes cada semana.</li>
<li><b>Si no sale exacto, lo que sobra va a las primeras semanas.</b><br>300 € = 30 piezas; 30 ÷ 4 = 7 y sobran 2: semanas de 8, 8, 7 y 7.</li>
<li><b>Imprevistos:</b> 150 € = 15 piezas gris oscuro, en un montón o por semanas (4, 4, 4 y 3).</li></ol>
<div class="card"><p class="ct">Así queda en el cuaderno</p>
<table class="t sm"><tr class="h"><td>COLOR</td><td>€ AL MES</td><td>PIEZAS</td><td>S1</td><td>S2</td><td>S3</td><td>S4</td></tr>{r10}
<tr><td>Gris oscuro</td><td>150</td><td>15</td><td colspan="4">aparte, o 4 · 4 · 4 · 3</td></tr>
<tr class="tot"><td>Total</td><td>830</td><td>83</td><td colspan="4"></td></tr></table></div>
<p class="cap"><b>¿Cuántas piezas necesitas?</b> Las del plan más un 25 % de repuesto, porque al cerrar la semana algunas cambian de color: 83 + 21 = unas 104 piezas.</p>''', 10)

# 11 · hoja nevera
t11 = [('lun 2', 'Súper', 'verde', '38,50', '4'), ('mar 3', 'Gasolina', 'rojo', '28,00', '3'), ('jue 5', 'Cañas', 'amarillo', '12,00', '1'),
       ('vie 6', 'Pan y fruta', 'verde', '4,20', 'sueltos'), ('vie 6', 'Gasolina', 'rojo', '30,00', '3 ⚑'), ('sáb 7', 'Farmacia', 'azul', '9,80', '1'),
       ('dom 8', 'Pan', 'verde', '3,10', 'sueltos')]
r11 = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in t11)
page(f'''<p class="eye">SIN PANTALLAS · 2</p><h1>Apuntar los gastos: la hoja de la nevera</h1>
<p>Una hoja por semana, sujeta con un imán en la nevera (tienes una para fotocopiar en la página 14). O una página del cuaderno. Quien paga, apunta y mueve la pieza.</p>
<ul><li><b>5 € o más:</b> se redondea y la pieza cambia de base al momento. 38,50 € son 4 piezas; 12 € es 1.</li>
<li><b>Menos de 5 €:</b> se apunta en <b>sueltos</b>. El domingo se suman los sueltos de cada color y se redondean.</li></ul>
<div class="card"><p class="ct">Ejemplo · semana 1 · piezas de 10 €</p>
<table class="t sm"><tr class="h"><td>DÍA</td><td>QUÉ</td><td>COLOR</td><td>€</td><td>PIEZAS</td></tr>{r11}</table>
<p class="cs">Sueltos verdes: 4,20 + 3,10 = 7,30 € → 1 pieza verde más.</p>
<p class="cs">⚑ El rojo de la semana 1 ya se había acabado: las 3 piezas se cogen de la semana 2 (regla 2). La semana 2 se queda con 0 rojas.</p></div>
<p class="cap">Si los sueltos de un color no llegan a 5 €, se pasan a la semana siguiente.</p>''', 11)

# 12 · domingo con lápiz
t12 = [('Verde', '7', '4 + 1 = 5', '2'), ('Rojo', '3', '3 (+3 de la S2)', '0'), ('Amarillo', '2', '1', '1'), ('Azul', '3', '1', '2'), ('Blanco', '2', '0', '2')]
r12 = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in t12)
page(f'''<p class="eye">SIN PANTALLAS · 3</p><h1>El domingo, con lápiz</h1>
<p>Cuenta lo que queda en la columna de la semana y apúntalo. Después, aplica la regla 3 paso a paso.</p>
<div class="card"><p class="ct">Cierre de la semana 1</p>
<table class="t sm"><tr class="h"><td>COLOR</td><td>PLAN</td><td>GASTADO</td><td>SOBRA</td></tr>{r12}
<tr class="tot"><td>Total</td><td></td><td></td><td>7</td></tr></table>
<ol><li><b>¿Algún color tiene menos de lo que le toca?</b> El rojo de la semana 2: le faltan 3. 2 verdes + 1 amarilla se convierten en 3 rojas y van a la semana 2.</li>
<li><b>Lo que aún sobra, como quieras:</b> el sábado de la semana 3 hay un cumpleaños, así que las 2 blancas se guardan como amarillas en la semana 3, y las 2 azules van a la hucha: <b>20 €</b>.</li></ol>
<p class="cs">Si lo llevas todo a la hucha, son 4 piezas: 40 €.</p></div>''', 12)

# 13 · cuentas fin de mes
t13 = [('Verde', '28', '24', '+4'), ('Rojo', '12', '14', '−2'), ('Amarillo', '8', '7', '+1'), ('Azul', '12', '8', '+4'), ('Blanco', '8', '4', '+4'), ('Gris oscuro', '15', '6', '+9')]
r13 = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>' for row in t13)
page(f'''<p class="eye">SIN PANTALLAS · 4</p><h1>Las cuentas de fin de mes</h1>
<p>Con las cuatro hojas de la semana y el cuaderno, en diez minutos tienes el resumen del mes.</p>
<div class="card"><p class="ct">Ejemplo de resumen</p>
<table class="t sm"><tr class="h"><td>COLOR</td><td>PLAN</td><td>GASTADO</td><td>DIFERENCIA</td></tr>{r13}</table>
<p class="cs">Hucha: 20 + 40 + 10 + 40 = <b>11 piezas = 110 €</b>.</p>
<p class="cs">Imprevistos sin usar: 9 piezas = 90 €. Se pueden ahorrar o pasar al mes siguiente.</p>
<p class="cs">Rojo: se gastaron 2 piezas más de lo previsto (20 €). El mes que viene, 14 piezas rojas.</p></div>
<h3>Comprobación rápida</h3>
<p>Piezas del plan (sin los grises oscuros) = gastadas + hucha. En el ejemplo: 68 = 57 + 11 (las guardadas de más ya cuentan como gastadas o vuelven a la hucha). Si no cuadra, falta apuntar algún gasto.</p>''', 13)

# 14 · hoja fotocopiable
rows14 = ''.join('<tr><td></td><td></td><td></td><td></td><td></td></tr>' for _ in range(13))
page(f'''<div class="sh"><h1>Semana ____</h1><span>Del ____ al ____ · pieza = ____ €</span></div>
<table class="t blank"><tr class="h"><td>DÍA</td><td>QUÉ</td><td>COLOR</td><td>€</td><td>PIEZAS</td></tr>{rows14}</table>
<div class="two"><div><p class="ct">Sueltos (menos de 5 €)</p><table class="t lines"><tr><td>Verde</td></tr><tr><td>Rojo</td></tr><tr><td>Amarillo</td></tr><tr><td>Azul</td></tr><tr><td>Blanco</td></tr></table></div>
<div><p class="ct">Cierre del domingo</p><table class="t lines"><tr><td>Sobran</td></tr><tr><td>Rellenan huecos</td></tr><tr><td>Guardadas de más</td></tr><tr><td>A la hucha</td></tr><tr><td>Semana en rojo <span class="sn">sí · no</span></td></tr></table></div></div>
<p class="foot">Hoja de la nevera · fotocopia una por semana</p>''', 14)

# 15 · app
page(f'''<p class="eye">OPCIONAL</p><h1>La app</h1>
<div class="app"><div class="qr">{QR}</div><p>Escanea el código con la cámara del móvil.<br><b class="pk">miguelvb.github.io/piezas-del-mes/</b><br>En el móvil, usa «Añadir a pantalla de inicio» y quedará como una app más.</p></div>
<ul><li>Haces el plan y la app reparte las piezas por semanas.</li><li>Apuntas cada gasto y te dice qué piezas mover.</li>
<li>El domingo te dice qué hacer con lo que sobra.</li><li>Los datos se guardan solo en tu móvil. No hay que registrarse.</li></ul>
<h1 class="mt">Lo que te pedimos</h1>
<p>Que lo uses un mes entero y que, al final, nos cuentes qué tal en una charla de diez minutos. Lo que no se entienda, lo que sobre y lo que falte nos ayuda muchísimo.</p>
<h3>Notas del mes</h3><div class="rl"></div><div class="rl"></div><div class="rl"></div><div class="rl"></div>''', 15)

# 16 · reglas en corto
page(f'''<div class="rh"><div class="ri">{SYM}</div><h1>Las reglas, en corto</h1></div>
<p class="eye">PARA LA NEVERA</p>
<ol class="rules"><li><b>Antes del día 1:</b> descuenta los gastos fijos y reparte lo que queda entre tus colores.</li>
<li><b>Día 1:</b> monta la mesa con tu plan.</li>
<li><b>Al pagar:</b> se apunta y la pieza cambia a la base de los gastos, en su semana. Se redondea; lo de menos de 5 €, a «sueltos».</li>
<li><b>Si se acaba un color:</b> se coge del mismo color de otra semana, normalmente la siguiente. Si no queda, la semana se queda en rojo.</li>
<li><b>Imprevistos:</b> solo para imprevistos, en un montón o por semanas.</li>
<li><b>Cada domingo:</b> lo que sobra rellena primero los colores que tienen menos de lo que les toca; si aún sobra, se reparte como quieras o va a la hucha.</li>
<li><b>Fin de mes:</b> mira la hucha, decide qué hacer con los imprevistos que sobran y haz el plan siguiente.</li></ol>
<p class="legal">Piezas del mes · prototipo de arkinos.net · Usa piezas de construcción compatibles; no tiene relación con ninguna marca de juguetes. Contiene piezas pequeñas: no apto para menores de 3 años.</p>''', 16)

CSS = open('fonts/fonts.css').read() + '''
@page { size: 148mm 210mm; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font-family: 'Atkinson Hyperlegible', sans-serif; color: #22211D; font-size: 9.6pt; line-height: 1.5; }
.page { width: 148mm; height: 210mm; padding: 13mm 12mm 14mm; background: #F7F5F1; position: relative; overflow: hidden; page-break-after: always; }
.page.cover { background: #E9A9C9; }
h1 { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 21pt; line-height: 1.08; margin: 0 0 4mm; letter-spacing: -0.02em; }
h1.mt { margin-top: 6mm; }
h3 { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 11.5pt; margin: 4.5mm 0 2mm; }
p { margin: 0 0 2.5mm; }
ul, ol { margin: 0 0 3mm; padding-left: 5mm; } li { margin-bottom: 1.2mm; }
.eye { color: #C9668F; font-weight: 700; font-size: 7pt; letter-spacing: 0.12em; margin-bottom: 1mm; }
.num { position: absolute; bottom: 7mm; left: 0; right: 0; text-align: center; font-size: 7pt; color: #9a978f; }
.cap { font-size: 7.6pt; color: #6b6860; line-height: 1.45; }
.note { font-size: 7.8pt; color: #6b6860; margin-top: 2mm; }
.icon { width: 30mm; margin-top: 2mm; } .icon svg, .ri svg { width: 100%; display: block; }
h1.cover { font-size: 46pt; line-height: 0.95; margin-top: 22mm; letter-spacing: -0.03em; } h1.cover span { color: #fff; }
.sub { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 14pt; margin: 8mm 0 3mm; }
.lead { font-size: 10pt; max-width: 80mm; }
.ed { position: absolute; bottom: 12mm; font-weight: 700; font-size: 6.8pt; letter-spacing: 0.12em; }
.photo { border: 2.5mm solid #E9A9C9; border-radius: 4mm; overflow: hidden; height: 50mm; margin: 2mm 0 1.5mm; }
.photo img { width: 100%; height: 100%; object-fit: cover; object-position: center 60%; }
.bases .bx { display: flex; gap: 4mm; align-items: flex-start; margin-bottom: 2.5mm; }
.tag { flex: 0 0 34mm; border-radius: 3mm; padding: 3mm; font-weight: 700; font-size: 8.5pt; min-height: 12mm; background-image: radial-gradient(rgba(255,255,255,.35) 1px, transparent 1.4px); background-size: 3mm 3mm; }
.tag.pink { background-color: #E9A9C9; } .tag.grey { background-color: #8f8f93; color: #fff; } .tag.yel { background-color: #F2B632; }
.bx p { margin: 0; font-size: 9pt; }
.t { width: 100%; border-collapse: collapse; font-size: 8.8pt; }
.t td { padding: 1.6mm 1.5mm; border-bottom: 0.3mm solid #dedad1; vertical-align: top; }
.t tr.h td { font-size: 6.6pt; font-weight: 700; letter-spacing: 0.08em; color: #6b6860; border-bottom: 0.4mm solid #22211D; }
.t tr.tot td { font-weight: 700; }
.t.sm { font-size: 8pt; } .t.sm td { padding: 1.2mm 1.2mm; }
.colors td:first-child { width: 7mm; }
.sw { display: inline-block; width: 5mm; height: 2.6mm; border-radius: 0.8mm; border: 0.25mm solid; vertical-align: middle; }
.fig { background: #fff; border: 0.3mm solid #e3dfd6; border-radius: 3mm; padding: 3mm 2mm 1mm; margin: 3mm 0 1.5mm; }
.board { width: 100%; display: block; }
.board .bh { font: 700 11px 'Bricolage Grotesque', sans-serif; text-anchor: middle; fill: #22211D; }
.board .bl { font: 400 10px 'Atkinson Hyperlegible', sans-serif; text-anchor: end; fill: #22211D; }
.box { background: #F9DDE9; border-radius: 3mm; padding: 3mm 3.5mm; font-size: 8.4pt; margin-top: 3mm; }
.q { font-weight: 700; margin: 2mm 0 0.5mm; } .a { color: #4d4a43; }
.card { background: #fff; border: 0.3mm solid #e3dfd6; border-radius: 3mm; padding: 3mm 3mm 2mm; margin: 3mm 0 2mm; }
.ct { color: #C9668F; font-family: 'Bricolage Grotesque', sans-serif; font-weight: 800; font-size: 9.5pt; margin-bottom: 1.5mm; }
.cs { font-size: 8pt; margin: 1.5mm 0 0; }
.card ol { font-size: 8.4pt; margin-top: 2mm; }
.sh { display: flex; justify-content: space-between; align-items: baseline; } .sh span { font-size: 8pt; color: #6b6860; }
.t.blank td { height: 7.6mm; border-right: 0.3mm solid #dedad1; } .t.blank td:last-child { border-right: 0; }
.t.blank td:nth-child(2) { width: 45%; }
.two { display: flex; gap: 5mm; margin-top: 4mm; } .two > div { flex: 1; }
.t.lines td { padding: 1.4mm 1.5mm; font-size: 8pt; color: #6b6860; } .sn { float: right; color: #22211D; }
.foot { position: absolute; bottom: 12mm; font-size: 7pt; color: #6b6860; }
.app { display: flex; gap: 5mm; align-items: center; margin-bottom: 3mm; }
.qr { background: #fff; border-radius: 3mm; padding: 3mm; width: 34mm; flex: 0 0 34mm; } .qr svg { width: 100%; height: auto; display: block; }
.app p { font-size: 9pt; margin: 0; } .pk { color: #C9668F; }
.rl { border-bottom: 0.3mm solid #cfcbc1; height: 8mm; }
.rh { display: flex; align-items: center; gap: 3.5mm; margin-bottom: 3mm; } .ri { width: 11mm; } .rh h1 { margin: 0; }
.rules li { margin-bottom: 2.5mm; } .rules li::marker { color: #C9668F; font-weight: 700; }
.legal { position: absolute; bottom: 12mm; left: 12mm; right: 12mm; font-size: 6.6pt; color: #6b6860; }
'''

html = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Piezas del mes · Guía de uso</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
open('librito.html', 'w').write(html)
print(len(pages), 'pages')
