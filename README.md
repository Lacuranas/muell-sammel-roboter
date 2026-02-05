# muell-sammel-roboter
The Respoitory for our school Project for scailability and reproductation by others

-----------------------------------------------------------------------------------------------------------------------------------------------

Ziel: Bild erkennungs KI die verschiedene Müllsorten erkennen und auseinanderhalten kann und ihre Position im Live Bild angibt.
Der Webserver ist zur Überwachung und Fernsteuerung der Software

Übersicht:
0. Vorbereitung:
	1. Installation von Raspi-OS (64bit) auf dem Rapsi 5 (min 8gb ram)
	2. Paket Update und Upgrade
	3. Installation PyEnv (Python Manage Library)
	4. Installieren von Python 3.9.2 neben System Python
	5. Virtuelle Umgebung erstellen

1. Installation
	1. Installation Tensor Flow Lite Pakete
	2. Installation Webserver Pakete
	3. Setup TF-Lite Objekt Erkennung
	4. Scripts von Github Laden

2. Starten / Laufen lassen
	1. Testen

____

0. Vorbereitung

1. Installation von Raspi-OS (64bit)
Es läuft auch auf 32bit, aber durch 64bit architektur ist es viel schneller

2. Paket Update und Upgrade
sudo apt update && sudo apt upgrade -yvb

3. Installation PyEnv (Python Manage Library)
Installer von pyenv herunterladen und ausführen
curl https://pyenv.run | bash

Edit the .bashrc with the command
    sudo nano ~/.bashrc

Add these three lines to implement pyenv on starting a bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"

Terminal neu starten um .bashrc neu zu laden

Benötigte Pakete für Pyenv installieren
sudo apt-get install --yes libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libgdbm-dev lzma lzma-dev tcl-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev wget curl make build-essential openssl


Pyenv auf die neueste Version updaten
pyenv update

Install Python 3.9.2 on the system belongside every other installation, because only on this version the script runs stable (TF-Lite requires this version to run properly)
pyenv install 3.9.2

pyenv local 3.9.2
 
Das Python venv Module installiere um die virtuelle Umgebung zu ersetllen.
sudo apt install python3-venv -y

Die virtuelle Umgebung erstellen:
python -m venv env

Update pip:
python3 -m pip install --upgrade pip


1. Installation

source ./env/bin/activate

Version überprüfen:
python -V
Erwartete ausgabe: 3.9.2

Install required Packages

picture processing:
python3 -m pip install numpy==1.26.4

TF-Lite runtime:
python3 -m pip install tflite-runtime 

Webserver engine:
python3 -m pip install gevent
python3 -m pip install waitress

Webserver Framework:
python3 -m pip install flask


Fork Github TF-Lite Source Repository:
git clone https://github.com/tensorflow/examples --depth 1

Enter object detection folder for raspi:
cd examples/lite/examples/object_detection/raspberry_pi

Start the setup agent to download the Model and set it up:
sh setup.sh

Test the basic Object Detection:
python detect.py
	Erwartete ausgabe:
	INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
	Ein Fenster öffnet sich und dort ist die Kamera ansicht zu sehen. In den Boxen sind die 	erkannten Objekte mit den Wahrscheinlichkeiten oben links an der 

4. Scripts von Github laden:

Alte datei löschen:
rm detect.py

Neue Dateien herunterladen:
....

2. Running
python roboter.py
	Erwartete Ausgabe:
		INFO: Created TensorFlow Lite XNNPACK delegate for CPU.

		Started Webserver on 0.0.0.0:8080
		Accessible via http://localhost:8080
		
		Press STRG+C to quit

-----------------------------------------------------------------------------------------------------------------------------------------------


This is based on Tensor Flow Lite and this github repo: 
https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi
