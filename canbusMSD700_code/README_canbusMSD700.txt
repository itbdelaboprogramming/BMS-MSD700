
[EN]
This is the installation procedure for Waveshare RS485/CAN HAT (12M Crsytal) module.
It has been tested for:
    - RaspberryPi 3B+/4
    - OS Raspbian Buster/Bullseye
    - Python 3.7

For first installation, copy the source code (.sh .py) on directory "/home/$(logname)/" or "~/"

Then, do these steps on the terminal:

1) Open terminal, then enable execute privilege for all .txt and .sh files
~$ sudo chmod +x init_canbusMSD700.sh

2) Run init_canbusMSD700.sh
~$ sudo sh init_canbusMSD700.sh

3) Reboot theRaspberry Pi to complete installation
~$ sudo reboot now

After this, the raspberry Pi will automatically run canbusMSD700.py automatically after every boot-up

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[JP]
Waveshare RS485/CAN HAT (12M Crsytal)モジュールのインストール手順です。
動作確認済みです：
    - RaspberryPi 3B+/4
    - OS Raspbian Buster/Bullseye
    - Python 3.7

初回インストール時は、ソースコード（.py .sh）をディレクトリ「/home/$(logname)/」または「~/」にコピーします。

次に、ターミナルで以下の手順を実行します：

1) ターミナルを開き、すべての .txt と .sh ファイルの実行権限を有効にします。
~$ sudo chmod +x init_canbusMSD700.sh

2) init_canbusMSD700.sh を実行します。
~$ sudo sh init_canbusMSD700.sh.

3) Raspberry Piを再起動して、インストールを完了します。
~$ sudo reboot now

この後、raspberry Piが起動するたびに自動的にcanbusMSD700.pyが実行されます。