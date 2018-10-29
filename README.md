# Emotiv SDK's bindings for Python
These bindings are meant for researchers to use the Emotiv in custom experiment built in Python with toolboxes such as PsychoPy (http://www.psychopy.org/) or PyGame (https://www.pygame.org/). This code establish the communication between the Emotiv and the computer. With these bindings, recordings could be released from the same python program, and events could also be marked using these functions. Briefly, to establish the communication between the display/data acquisition computer and the Emotiv system we used the research edition SDK (Standard Development Kit) provided by Emotiv, which allows raw data access in real time. Because the SDK was written originally for C++, we developed this bindings for Python. The pipeline consisted of receiving the
electrode signals, adding referential marks about experiments’ stimuli and responses and, finally, saving it for later analysis.


This project is part of a larger collaboration between the Unidad de Neurobiología Aplicada (CEMIC - CONICET, Argentina; http://pobrezaydesarrollocognitivo.blogspot.com/) and the Laboratorio de Inteligencia Artificial Aplicada (Instituto de Cs. de la Computación, Fac. de Cs. Exactas y Naturales, UBA - CONICET, Argentina; https://liaa.dc.uba.ar/). Our general goal is to study the influence of adverse environmental conditions on the organization and reorganization of the brain structure and function, and how it involves distinct neural systems at different levels of organization. Thus, we measure EEG in children from low socio-economic status contexts to evaluate the efficacy of interventions, aimed to enhance cognitive development in children facing unfavorable social conditions (see also Pietto ML, Kamienkowski JE, Lipina S "Electrophysiological approaches in the study of childhood poverty influence on cognition" (2017) book chapter in “Neuroscience and Social Science: The missing link” Springer Books).

# Data and analysis code
Data and analysis code in Matlab from Pietto et al (2018) are available at https://github.com/marcospietto/Piettoetal_EEGApproaches_Data

# How to cite us
#### Please, if you like it / use it cite us:
Pietto ML, Gatti M, Raimondo F, Lipina SJ, and Kamienkowski JE. "Electrophysiological approaches in the study of cognitive development outside the lab" (accepted, 2018)
#### And let us know!!
Marcos L. Pietto (marcos.pietto (arroba) gmail (dot) com)
Mathias Gatti (mathigatti (arroba) gmail (dot) com)
Federico Raimondo
Sebastian Lipina
Juan E. Kamienkowski (juank (arroba) dc (dot) com (dot) ar)

# Installation instructions

## 1. Installation of the Emotiv SDK

We recommend to install the Emotiv SDK in /opt/Emotiv-1.0.0.5, in order to facilitate running following steps. The SDK documentation is also installed with the Emotiv SDK.
    
INSTRUCTIONS:

Copy the installer to /opt:
    
    sudo cp ~/Downloads/Emotiv/Emotiv /opt

Change the installer's permissions to open it:    
    
    sudo chmod a+x /opt/Emotiv/Emotiv 

Open the installer:
    
    sudo /opt/Emotiv/Emotiv

## 2. Bindings for Python

The SVN folder is located at src/emotiv. After the r2 revision, in SVN folder you can find:
* The Emotiv SDK's bindings for Python.
* A Python's lesson on how to use the bindings and how to record sessions to the .edf files

These bindings work with Python 32-bit. If the Linux system is also 32-bit, you just need to compile the bindings. Or, if you have Linux 64-bit, you need to be careful and compile Python in 32-bit.

---
### For Linux 64-bits only 

Compile Python in 32-bit on your Ubuntu system of 64-bit.

Install the ia32-libs:
        
        sudo apt-get install ia32-libs

If the above command fails, then you can check http://stackoverflow.com/questions/23182765/

Download the source code of Python from http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz. And, unzip the file: 

        tar -xvzf Python-2.7.6.tgz

Set up the source code to compile it: CC="gcc -m32" LDFLAGS="-L/lib32 -L/usr/lib32 -Lpwd/lib32 -Wl,-rpath,/lib32 -Wl,-rpath,/usr/lib32" ./configure --prefix=/opt/pym32

Then, compile:

        make

And, Install:
        
        sudo make install

The above command installs the Python 32-bit in the folder /opt/pym32 .

---

## 3. Compile the bindings

To compile, just run 'make' in the folder ./src/emotiv. If your Linux system is 64-bit:
        
    make -f Makefile.linux64
    
Unless it has been installed in the /opt/Emotiv-1.0.0.5 folder, the Linux users will have to edit the Makefile and type to the correct path in the variable EMOTIV_ROOT.

## 4. Run a program using the bindings

In order to run any script that uses the Emotiv's library in Python, you need to prefix the path of those libraries:
    
    LD_LIBRARY_PATH=/opt/Emotiv-1.0.0.5/lib

Then, execute both Python and the script. Here's an example in Linux 64-bits:
    
    LD_LIBRARY_PATH=/opt/Emotiv-1.0.0.5/lib /opt/pym32/bin/python test.py

It's importante that the files emotiv.so, Emotiv.py and EdfWriter.py were in the same directory.
     
---

## Potential issues

#### 1. Once you run the Emotiv's wizard/installer in Ubuntu 14.04 64-bit, it asks you information such as the user and other stuff, you must complete it also with the real 'order number' and 'serial key'.


#### 2. If an error occurs due to a missing required package, despite the Emotiv's folder named 'lib' actually contains it, it could be the case that it has a different name (for example 'ledk' that is 'libedk'). Then, you probably need to do a 'symlink' between the searched file and the file that you have.
    
To do that, you just need to run:

        ln -s EXISTING_FILE SYMLINK_FILE

#### 3. In Ubuntu 14.04 is likely to be necessary to install 'hal', , this package was available in previous version but not in the present one. If not, when running an Emotiv's program you may get an error like: "The narre org.freedesktop.Hal was not provided by any .service files".

To install 'Hal' from the terminal:
        
        sudo add-apt-repository ppa:mjblenner/ppa-hal
        sudo apt-get update
        sudo apt-get install hal
        

#### 4. If also 'libavbin' is missing, you must download the installer from https://avbin.github.io/AVbin/Download.html, and excecute it from the terminal.
    
        sudo chmod +x install-avbin-linux-x86-32-v10
        sudo ./install-avbin-linux-x86-32-v10
    
#### 5. Finally, if Python.h is missing, then install 'python-dev' from the terminal.

         sudo apt-get install python-dev
        
