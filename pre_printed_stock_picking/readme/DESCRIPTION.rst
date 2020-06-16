Este modulo permite imprimir remitos preimpresos. Segun la operacion que se
esta realizando se obtienen dos tipos distintos de remito

Movimiento Interno
------------------
Si el deposito al que se envia esta marcado como una ubicacion interna, entonces
el remito sera de tipo Movimiento Interno.
En la cabecera apareran las palabras **Movimiento Interno** y en el cuerpo del
remito aparecen los siguientes datos:

+-----------+--------------------------+--------+
| **Cant**  | **Descripcion/Lote**     | **Kg** |
+-----------+--------------------------+--------+
|   cc      | [DESC] Lote NNN (attrib) |   pp   |
+-----------+--------------------------+--------+

Donde:
- cc: La cantidad de producto en la unidad de medida del producto, puede ser unidades o Kg
- DESC: [Codigo-interno] nombre del producto, el nombre del producto para Amic
- NNN: Numero de lote
- attrib: Todos los atributos del lote
- pp: peso en kg de este item

Remito al cliente
-----------------
Si el deposito al que se envia NO esta marcado como una ubicacion interna, entonces
el remito sera de tipo Movimiento al cliente.
En la cabecera no aparece la palabra **interno** y ademas, si en la orden de
venta se cargo la referencia del cliente en la pestaña **Otra Informacion**
esta aparecera en la cabecera del remito.

En el cuerpo del remito, cada linea de producto tendra los siguientes datos:

+-----------+--------------------------+-----------+
| **Cant**  | **Descripcion/Lote**     | **CAJAS** |
+-----------+--------------------------+-----------+
|   qq      | [DESC] Lote NNN (attrib) |    cc     |
+-----------+--------------------------+-----------+

Donde:
- qq: Cantidad de producto en la unidad de medida del producto, en general seran unidades.
- DESC: [Codigo-interno] nombre del producto Segun se cargo en la oreja Ventas del producto para este cliente
- NNN: Numero de lote
- attrib: Todos los atributos del lote que estan tildados en la ficha del producto
- cc: cantidad de cajas
