from statistics import mode
import torch
import torch.nn as nn
from torchvision import models,transforms
from PIL import Image
import os
import glob
import urllib.request

path = "./datas/testdata/octopus_test/" # 檔案路徑
path2 = path+"*"
images = glob.glob(path2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
category = ['花枝','章魚','魷魚']

transforms = transforms.Compose([transforms.Resize((224,224)), transforms.ToTensor()])
# 建立 CNN 架構
class CNN_Model(nn.Module):
    #列出需要哪些層
    # Pytorch 最少要定義兩個 function ，一個是 __init__ ，用來建立你 forward 需要用到哪些層，另一個是 forward ，也就是定義路徑要怎麼走，不需另外定義 Backward ， Pytorch 會自動幫你設定 Back-propagation 的路徑。
    def __init__(self):
        super(CNN_Model, self).__init__()

        # 載入 ResNet18 類神經網路結構
        self.model = models.resnet18(pretrained=True)

        # 修改輸出層輸出數量，因為要3類（魷魚、章魚、花枝），所以設3
        self.model.fc = nn.Linear(512, 3)
    def forward(self, x):
        logits = self.model(x)
        return logits
def GoIdentify(img_path):
    # model=model.to(device)
    model = torch.load('./model/Resnet18_dataAgument9600_epoch10.pt', map_location ='cpu')
    model.eval()
    model=model.to(device)
    # model.no_grad()
    img = Image.open(urllib.request.urlopen(img_path))
    # img.show()
    img = transforms(img).unsqueeze(0)
    img_ = img.to(device)
    output = model(img_)
    print("------------------------------------\n")
    print(img_path)
    print(output)
    # 0: 花枝 1:章魚 2:魷魚
    _, predicted = torch.max(output, 1)
    ans = output.argmax() # 取最大值（答案）
    # print(_, "====", predicted)
    # print('this picture maybe :', predicted[0])
    print("此圖為：",category[ans])
    return(category[ans])
# def main():
#     for i in images:
#         Identify(i)
# if __name__ == '__main__':    
#     print("\n")
#     for i in images:
#         main(i)