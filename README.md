# BMS-MSD700 (CAN-BUS with Python)

This python code is used for the back-end system: CAN Bus protocol communication data logging.
The installation procedure for Waveshare RS485/CAN HAT (12M Crsytal) module and the CAN-BUS program has been tested for:
* RaspberryPi 3B+/4
* OS Raspbian Buster/Bullseye
* Python 3.7

## Installation
For first installation, after the CAN Hat (hardware) module is installed, power up the RaspberryPi and
copy the folder `canbus_code` to directory `/home/$(logname)/` or `~/`

Then, do these steps on the terminal:

1. Open terminal, run `init_canbus.bash`
```
sudo bash canbus_code/init_canbus.bash
```
1. Follow the instructions on the terminal.
2. Close terminal when it is done.

You still need to prepare the script to automatically run this program after each bootup. Check [key_code] (https://github.com/itbdelaboprogramming/IoT-Gateway) for related features.

## 設置方法
Waveshare RS485/CAN HAT (12M Crsytal)モジュールのインストール手順です。
動作確認済みです：
    - RaspberryPi 3B+/4
    - OS Raspbian Buster/Bullseye
    - Python 3.7

初回インストール時は、CANハット（ハードウェア）モジュールを初めてインストールしたら、RaspberryPiの電源を入れ、`canbus_code` フォルダを `/home/$(logname)/` または `~/` ディレクトリにコピーしてください。

次に、ターミナルで以下の手順を実行します：

1. ターミナルを開き、`init_canbus.bash` を実行します。
```
sudo bash canbus_code/init_canbus.bash
```
2. 端末の指示に従う。
3. 終了したらターミナルを閉じます。

各起動後にこのプログラムを自動的に実行するスクリプトを準備する必要があります。関連する機能については[key_code](https://github.com/itbdelaboprogramming/IoT-Gateway)をチェックしてください。