'''
#title           :README.txt
#description     :instruction manual for CAN Hat module installation (software)
#author          :Nicholas Putra Rihandoko
#date            :2023/04/03
#version         :2.1
#usage           :BMS-python
#notes           :
#==============================================================================
'''

[EN]
This is the installation procedure for Waveshare RS485/CAN HAT (12M Crsytal) module.
It has been tested for:
    - RaspberryPi 3B+/4
    - OS Raspbian Buster/Bullseye
    - Python 3.7

For first installation, after the CAN Hat (hardware) module is installed, power up the RaspberryPi and
copy the folder "canbusMSD700_code" to directory "/home/$(logname)/" or "~/"

Then, do these steps on the terminal:

1) Open terminal, run init_canbusMSD700.bash
~$ bash /home/$(logname)/canbusMSD700_code/init_canbusMSD700.bash
2) Follow the instructions on the terminal.
3) Close terminal when it is done.

After this, the raspberry Pi will automatically run canbusMSD700.py automatically after every boot-up

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[JP]
Waveshare RS485/CAN HAT (12M Crsytal)モジュールのインストール手順です。
動作確認済みです：
    - RaspberryPi 3B+/4
    - OS Raspbian Buster/Bullseye
    - Python 3.7

初回インストール時は、CANハット（ハードウェア）モジュールを初めてインストールしたら、RaspberryPiの電源を入れ、
「canbusMSD700_code」フォルダを「/home/$（logname）/」または「~/」ディレクトリにコピーしてください。

次に、ターミナルで以下の手順を実行します：

1) ターミナルを開き、init_canbusMSD700.bash を実行します。
~$ bash /home/$(logname)/canbusMSD700_code/init_canbusMSD700.bash
2) 端末の指示に従う。
3) 終了したらターミナルを閉じます。

この後、raspberry Piが起動するたびに自動的にcanbusMSD700.pyが実行されます。