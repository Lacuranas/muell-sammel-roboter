# muell-sammel-roboter
The Respoitory for our school Project for scailability


# Ziel: Bild erkennungs KI die verschiedene Müllsorten erkennen und auseinanderhalten kann und ihre Position im Live Bild angibt.
Der Webserver ist zur Überwachung und Fernsteuerung der Software

Übersicht:
1. Vorbereitung:
	1. Installation von Raspi-OS (64bit) auf dem Rapsi 5 (min 4GB ram, empfohlen 8GB ram)
	2. Paket Update und Upgrade
	3. Installation PyEnv (Python Manage Library)
	4. Installieren von Python 3.9.2 neben System Python

2. Installation
	1. Github Repository klonen
	2. Virtuelle Python Umgebung erstellen
	3. Benötigte Pakete installieren

3. Starten / Laufen lassen
	1. Testen

4. Abschluss

____

# 1. Vorbereitung

1.1 Installation von Raspi-OS (64bit)
Es läuft auch auf 32bit, aber durch 64bit architektur ist es viel schneller

1.2 Paket Update und Upgrade
sudo apt update && sudo apt upgrade -y

1.3 Installation PyEnv (Python Manage Library)
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


# 2. Installation

2.1 Github Repository klonen
git clone https://github.com/Lacuranas/muell-sammel-roboter.git ./ --depth 1

2.2 Virtuelle Umgebung erstellen
python -m venv env

source ./env/bin/activate

Version überprüfen:
python -V
Erwartete ausgabe: 3.9.2

2.3 Benötigte Pakete installieren
Update pip:
python3 -m pip install --upgrade pip

Install required Packages:
python3 -m pip install -r requirements.txt


# 3. Running
python main.py
	Erwartete Ausgabe:
		INFO: Created TensorFlow Lite XNNPACK delegate for CPU.

		Started Webserver on 0.0.0.0:8080
		Accessible via http://localhost:8080

		Press STRG+C to quit

		Es öffnet sich ein Fenster mit der live Kamera Ansicht. Die Rechtecke umgeben jeweils ein erkanntes Müll Objekt, darüber steht die Müllsorte.
		Ein Webserver wird auf Port 8080 gestartet, der die Webseite bereitstellt.


# 4. Abschluss
Du hast nun eine Bilderkennung die Müll über eine Tensor Flow Lite KI erkennt und die Position und Müllsorte von diesem Anzeigt.
Außerdem hast du einen Webserver mit dem du den Roboter vernsteuern kannst und sein Live Bild siehst.


This is based on Tensor Flow Lite and this github repo: 
https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi

Please give credits if you use our work as base
