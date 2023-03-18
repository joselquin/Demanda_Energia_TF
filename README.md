# Proyecto Demanda de Energía en TF

Iniciamos un proyecto con el objeto de estudiar y definir una previsión de consumo energético futuro en Tenerife.

Se trata de un problema de análisis de series temporales y me basaré en los datos de demanda energética disponibles en la página de Red Eléctrica Española (REE). 

Estos datos permiten hacer muchos análisis, centrándonos en diferentes situaciones y podemos crear muchas historias con ellos. Aquí nos centraremos en la creación de un forecast de demanda para un mes siguiente a los datos de que disponemos.

Los pasos a dar son:

1. Extracción del dataset de al menos 10 años de consumo. 
2. Limpieza de datos.
3. Estudio descriptivo del dataset.
4. Estudio con Sarima y creación de un forecast para un mes.
5. Estudio con Sarima con una variable exógena con los dias festivos.
6. Comparación de forecast con datos agrupados en horas.
7. Comparación de forecast si en el modelo usamos menos datos históricos. ¿Hasta dónde necesitamos remontarnos con el histórico para tener un forecast utilizable?

En una segunda parte, utilizaremos otros algoritmos clásicos de machine learning para estudiar los datos y crear un forecast. Y en una tercera parte, usaremos técnicas de deep learning. Con todo, estudiaremos diversos aspectos relacionados con análisis de series temporales:

- La diferencia de eficacia de tres tipos diferentes de técnicas (estadística clásica, machine learning “clásico” y deep learning).
- Técnicas de webscrapping con páginas dinámicas.
- Diferencia en el forecast utilizando datos con diferente granularidad.
- Afección en los resultados con y sin variables exógenas.
- Afección en la exactitud del forecast en función del tamaño del histórico que utilicemos para entrenar el modelo.

Más información en este [enlace](https://lily-quart-224.notion.site/Proyecto-Demanda-de-Energ-a-en-TF-a0730fbc9a794a50803a636d26e8d638).
