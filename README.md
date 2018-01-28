# INSTRUCCIONES DE INSTALACIÓN

## 1. Instalación del SDK de Emotiv

Se recomiendo instalar el SDK de Emotiv en /opt/Emotiv-1.0.0.5 así el resto es mas sencillo.
La documentación del SDK se instala con el SDK.
    
INSTRUCCIONES:

Copiar el instalador a /opt:
    
    sudo cp ~/Downloads/Emotiv/Emotiv /opt

Cambiar los permisos del instalador para poder ejecutarlo:
    
    sudo chmod a+x /opt/Emotiv/Emotiv 

Ejecutar el instalador:
    
    sudo /opt/Emotiv/Emotiv

## 2. Bindings para python

Desde la revisión r2, en el svn se encuentran los bindings para python sobre el SDK de Emotiv y una clase de python para utilizar los bindings con mayor facilidad y grabar las sesiones en archivos EDF.

La carpeta del svn es src/emotiv.

Estos bindings funcionan con python de 32 bits. Si el linux es de 32 bits, entonces sólo hay que compilar los bindings. En el caso de 64 bits, hay que compilar python en 32 bits.

---

### Solo para linux 64 bits

Compilar python de 32 bits en ubuntu de 64 bits.
Instalar ia32-libs:
        
        sudo apt-get install ia32-libs

Si no es posible, recurrir a http://stackoverflow.com/questions/23182765/how-to-install-ia32-libs-in-ubuntu-14-04-lts-trusty-tahr

Descargar el código fuente de python desde http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
Descomprimir el archivo: 

        tar -xvzf Python-2.7.6.tgz

Configurar el código fuente para compilarlo: CC="gcc -m32" LDFLAGS="-L/lib32 -L/usr/lib32 -Lpwd/lib32 -Wl,-rpath,/lib32 -Wl,-rpath,/usr/lib32" ./configure --prefix=/opt/pym32

Compilar:
        
        make
Instalar:
        
        sudo make install

Esto instala python de 32 bits en /opt/pym32

---

## 3.Compilar los binding

Para compilar, basta con ejecutar make en la carpeta ./src/emotiv. Si es linux de 64 bits:
        
    make -f Makefile.linux64
    
Los usuarios de linux van a tener que editar el Makefile y poner el path correspondiente en la variable EMOTIV_ROOT, salvo que lo tengan instalado en /opt/Emotiv-1.0.0.5.
    
## 4.Ejecutar un programa usando los bindings

Para ejecutar cualquier script de Python que utilice la biblioteca de Emotiv en python hay que anteponer el path de ubicación de las librerías:
    
    LD_LIBRARY_PATH=/opt/Emotiv-1.0.0.5/lib
    
Luego, ejecutar python y el script. Ejemplo para linux de 64 bits:
    
    LD_LIBRARY_PATH=/opt/Emotiv-1.0.0.5/lib /opt/pym32/bin/python test.py
    
En ese mismo directorio tienen que estar los archivos emotiv.so, Emotiv.py y EdfWriter.py.

---
## Posibles inconvenientes

### 1.Al correr el wizard/instalador de emotiv en ubuntu 64 bits 14.04 te pide datos como usuario y demás cosas, de todas maneras hay que completarlo con el order number y la serial key.
    
### 2.Si surge algun error sobre la falta de alguna libreria a pesar de que esta se encuentra en la carpeta lib de emotiv, por ejemplo ledk la cual es libedk, entonces probablemente haya que hacer un symlink entre el archivo buscado, el cual no se encontró y el archivo que si tenemos.
    
Para hacer esto se utiliza: 

        ln -s EXISTING_FILE SYMLINK_FILE
    
### 3.En ubuntu 14.04 probablemente sea necesario instalar hal, este paquete estaba en versiones anteriores y ahora no. Al correr algun programa de emotiv quizas surja algun tipo de error como: "The narre org.freedesktop.Hal was not provided by any .service files"
        
Para solucionarlo se puede instalar Hal escribiendo en la terminal: 
        
        sudo add-apt-repository ppa:mjblenner/ppa-hal
        sudo apt-get update
        sudo apt-get install hal
        
### 4.Si falta libavbin bajar el instalador de https://avbin.github.io/AVbin/Download.html y ejecutarlo
    
        sudo chmod +x install-avbin-linux-x86-32-v10
        sudo ./install-avbin-linux-x86-32-v10
    
### 5.Si falta Python.h agregarlo instalando python-dev

         sudo apt-get install python-dev
        
