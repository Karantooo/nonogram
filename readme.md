# Proyecto Nonogram

## Integrantes del grupo
- [Carlos Tomás Álvarez Norambuena](https://github.com/Karantooo)  **(2022433621)**
- [Antonio Jesús Benavides Puentes](https://github.com/AntoCreed777) **(2023455954)**
- [Javier Alejandro Campos Contreras](https://github.com/huebitoo) **(2023432857)**
- [Pablo Esteban Villagrán Hermanns](https://github.com/Pvilla14) **(2023439231)**

## Tecnologías utilizadas en el proyecto
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=git,github,pycharm&perline=12" />
  </a>
</p>
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python&perline=12" />
  </a>
</p>

## Instrucciones de instalación


### Sistemas operativos

**El sistema fue desarrollado en windows de principio a fin. Si bien en teoria no deberia haber problemas de compatibilidad en sistemas linux esta no fue testeado por lo que no aseguramos la misma.**

### Setup inicial
Clone el repositorio en un directorio de su elección. Abra la carpeta con PyCharm.  
Recomendamos crear un nuevo entorno virtual de Python con la versión 3.12.15.

Para instalar las dependencias, ejecute:  
```pip install -r requirements.txt```

Finalmente, **hay que cambiar el directorio de trabajo desde el que se ejecuta el proyecto**, de otra forma no se ejecutará.  
Para esto, vaya al menú de la esquina superior derecha de PyCharm (ver imagen).

![imagen menú principal](imagenes_readme/imagen_proyecto.png)

Haga clic en "Editar configuraciones". Cree una nueva configuración de Python. Debería ver el siguiente menú:

![imagen menú principal](imagenes_readme/Menu_pycharm.png)

Los campos que hay que completar sí o sí son los marcados con las flechas:

- **Name:** Nombre que desea para la configuración (libre elección).  
- **Python interpreter:** Seleccione el entorno virtual con el que desea ejecutar el proyecto.  
- **Script path:** La ubicación de `./nonogram/main.py` en su computador.  
- **Working directory:** Este debe apuntar al directorio base donde se clonó el repositorio. Ejemplo: si el repositorio se clonó en `pythonProject`, este debe ser el directorio de trabajo. Cualquier otro resultará en que el código no se ejecute.

Una vez realizada esta configuración, debería ser posible ejecutar el proyecto.
