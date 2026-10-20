# promosTC

Reintegros en combustible con tarjetas de bancos, financieras y cooperativas de Paraguay.
Sitio estático: `index.html` + `stations.json` + `logos/`.

- Render: https://promostc.onrender.com
- GitHub Pages: https://oscar-santacruz.github.io/promostc-py/

## Regla de datos

Solo se cargan promos publicadas por la propia entidad: sus bases y condiciones, su web de beneficios
o su cuenta oficial de Instagram/Facebook. No se usan agregadores, medios ni posts de estaciones.
Cada promo lleva su fuente en `src`.

## Cómo actualizar una promo

Las promos están en el arreglo `PROMOS` al inicio del `<script>` de `index.html`.

| Campo | Qué es |
|---|---|
| `entidad` | Nombre(s) de la entidad. Cada uno aparece en "Mis tarjetas". |
| `tipo` | `Banco`, `Financiera`, `Cooperativa` o `Mutual`. |
| `emblemas` | Estaciones donde vale. `"Todas las estaciones"` aplica a cualquier emblema. |
| `dias` | `lu ma mi ju vi sa do`, `"todos"`, `"d10"` (día 10 del mes) o `"ver bases"`. |
| `pct`, `limite`, `tope` | Porcentaje máximo, límite de compra y tope de reintegro en Gs. (`null` si no se informa). |
| `per` | Período del tope: `Semanal`, `Mensual`, `Diaria`, `Por vigencia` o `—`. |
| `pos` | Red de pago: `Upay`, `Dinelco` y/o `Bancard` (Infonet). Sin el campo se muestra "Red no indicada". |
| `tiers` | Opcional. Porcentaje por tarjeta: `[{t:"Privilege",pct:25,limite:...,tope:...}]`. |
| `niveles` | Solo ueno: `[% , límite, tope]` por nivel 1 a 5. |
| `desde`, `hasta` | Vigencia (`AAAA-MM-DD`). Con `hasta` vencido la promo pasa a "vencida". |
| `src` | Link a las bases o a la publicación oficial. |

## Estaciones

`stations.json`: `[lat, lon, emblema, nombre, ciudad]`. Fuentes:

- Listados oficiales con coordenadas: Petropar (Google My Maps), Copetrol (API del localizador), Petrobras (planilla de estaciones), Puma (mapa del sitio), Shell (localizador oficial), Petrosur, Petromax, Compasa y Enex (sus sitios).
- OpenStreetMap (amenity=fuel, © colaboradores de OpenStreetMap) para los demás emblemas y para completar lo que falte. Petrochaco publica solo direcciones, sin coordenadas.

Se descartan duplicados a menos de 150 m del mismo emblema y se corrigieron dos coordenadas erróneas de la planilla de Petrobras.

## Logos

`logos/logos.json` guarda nombre, color y archivos por marca. Los logos pertenecen a sus marcas.
