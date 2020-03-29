Este modulo extiende la funcionalidad de los lotes agregando atributos y
comportamientos.

Los atributos del lote son propagados de un lote entrante a un lote saliente
en produccion al oprimir el boton record_production

Peso de los productos en remito
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

En cada linea del remito se muestra la cantidad de producto y el peso. Como
los productos remitidos pueden ser medios que contienen una cantidad no siempre
definida de productos, el peso debe ser calculado al momento de la fabricacion.

Un caso de uso de este problema es el remito de los capachos que van a thermal,
se requiere tener el peso del capacho en el remito. Para eso se define el
siguiente metodo de calculo.

El peso de un producto que tiene seguimiento por lotes esta definido en el
lote, y se calcula al fabricar el producto sumando los pesos de los productos
componentes, que a su vez tambien estan en los lotes.

De esta manera se calculan los pesos de todos los productos de la cadena de
fabricacion desde la materia prima.

Si un producto tiene definido su peso en el apartado **Inventario** de la ficha
del producto, entonces se toma ese peso en lugar del peso definido en el lote.
Esto ultimo se usa para definir el peso del primer producto de la cadena de
fabricacion o el producto desde donde se quiere empezar a definir pesos.
