# 魷魚辨識機器人

[![hackmd-github-sync-badge](https://hackmd.io/O4cT1cBvSHSVdRCKPXAGrQ/badge)](https://hackmd.io/O4cT1cBvSHSVdRCKPXAGrQ)

請問被打的是章魚還是透抽？

![](https://i.imgur.com/Wkp5Mn2.gif)
## 事前準備
### 檔案說明：
- `main.py`：bot 主程式
- `Identify.py`：辨識圖片
- `Resnet18_dataAgument9600_epoch10.pt` : 此範例 model

### Telegram BOT：
1. 在 Telegram 上加 `@BotFather` 為好友
2. `/newbot` 設定 `name` `username`
3. 會得到 Bot 的 `token`，請自行保留好，請勿外流！![](https://i.imgur.com/Hu4k9ha.jpg)
4. `/setcommands` 設定你的 bot 要有哪些功能，也可以之後再加

### GCP：
1. [Google Cloud Platform](https://cloud.google.com/) 使用 Compute Engine 建立 VM
    - VM 開機映像檔選用 ubuntu 20.04 LTS
    - ![](https://i.imgur.com/z7hkM5i.png)
2. 利用 SSH 進入設定
    ![](https://i.imgur.com/zyo3sKP.png)

### VM 環境準備
- python3: GCP VM 中原本就有 python3
- 更新 apt: `sudo apt update`
- 安裝 pip3: `sudo apt install python3-pip`
- 安裝 telegram: `$ pip3 install python-telegram-bot --upgrade
`
- 安裝 matplotlib: `python3 -m pip install -U matplotlib`
- 安裝 pytorch: `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu`

### VM 上傳檔案
- 將檔案上傳至 VM:
    1. Identify.py 
    2. main.py
    3. Resnet18_dataAgument9600_epoch10.pt
    4. config.ini
    5. Pipfile
    6. Pipfile.lock
- 新增名為 "model" 的目錄，並將 model 移到此目錄
    1. 建立目錄：`mkdir model`
    2. 移動 model: `mv Resnet18_dataAgument9600_epoch10.pt model`

### 啟動主程式
`python3 main.py`

![](https://i.imgur.com/L1TvGgj.png)
![](https://github.com/NCNU-OpenSource/squid_bot/blob/main/ezgif.com-gif-maker.mp4)

## Special Thanks
題目發想：李漢偉 @UncleHanWei、蔣毓庭 @YuTing0412
