<h2 align="center">
GPT-4V-Examples
</h2>

<div align="center">
  <img src="https://img.shields.io/badge/python-v3.9.18-blue.svg"/>
  <img src="https://img.shields.io/badge/openai-v1.2.2-blue.svg"/>
</div>

2023년 11월 6일, OpenAI 개발자 컨퍼런스에서 소개된 후 많은 개발자들의 관심을 끌고 있는 GPT-4의 새로운 기능, 'GPT-4 with Vision'은 이미지를 입력으로 받아 질문에 답변할 수 있는 능력을 제공합니다. 이전까지 언어 모델 시스템은 단일 입력 모달리티, 텍스트에 한정되어 있었지만, 이제 'gpt-4-vision-preview' 모델을 이용하여 이미지와 텍스트 모두를 처리할 수 있게 되었습니다.

### GPT-4V의 이미지 이해

GPT-4V는 이미지와 관련된 텍스트 정보를 처리하여 이미지 내의 객체, 장면, 상황 등을 이해하고 설명할 수 있습니다. 이를 위해 우리는 GPT-4에게 이미지와 관련된 질문을 할 수 있으며, 모델은 이미지 내용을 분석하여 답변을 제공합니다.

------

### 이미지 처리를 위한 Python 기본코드

먼저 openai 라이브러리를 설치해야 합니다. 이는 pip install openai를 통해 설치할 수 있습니다. 추가적으로 결과를 확인하기 위해 몇가지 라이브러리를 추가로 설치하였습니다.

```lua
pip install openai
pip install Pillow
pip install matplotlib
pip install requests
```

이제 GPT-4를 사용하여 이미지를 처리하는 기본코드를 살펴보겠습니다. 코드 내에서 client를 생성할 때 API 키를 제공해야 합니다. 이 키는 OpenAI에서 얻을 수 있습니다.

```python
import os
import openai
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
 
# OpenAI API 키 설정
openai.api_key = "YOUR_API_KEY"
 
client = openai.OpenAI()
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
 
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 그림에 대해 설명해줘."},
                {
                    "type": "image_url",
                    "image_url": image_url
                }
            ]
        }
    ],
    max_tokens=1000
)
```

이 코드는 주어진 이미지 URL에서 이미지를 다운로드하고, matplotlib을 사용하여 화면에 표시합니다. 그 후에 GPT-4의 응답을 출력합니다.

```python
# 이미지 다운로드
download_img = requests.get(image_url)
img = Image.open(BytesIO(download_img.content))
 
# 이미지 출력
plt.imshow(img)
plt.axis('off') # 축 정보 숨기기
plt.show()
 
# 응답 출력
print(response.choices[0].message.content)
```

Output : 

![img](https://blog.kakaocdn.net/dn/O132d/btsz6fJAGar/CEOk8lrgsQkrO35qHGonF0/img.png)

### Base 64로 인코딩된 이미지 업로드

Local에 이미지가 있는 경우 이를 Base 64 인코딩 형식으로 모델에 전달할 수 있습니다.

```python
import base64
import requests
import os
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
 
# OpenAI API 키 설정
api_key = "YOUR_API_KEY"
 
# 이미지를 base64로 인코딩하는 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
 
# 이미지 경로
image_path = "asset/images/test_1.jpg"
 
# base64 문자열 얻기
base64_image = encode_image(image_path)
 
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
 
payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "이 사진에 대해 설명해줘"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 1000
}
 
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
# 'content' 부분만 추출하여 출력
content = response.json()['choices'][0]['message']['content']
 
# 이미지 표시
img = Image.open(image_path)
plt.imshow(img)
plt.axis('off')  # 축 정보 숨기기
plt.show()
 
# 응답 출력
print(content)
```

Output :

![img](https://blog.kakaocdn.net/dn/4XxWZ/btsz83aT5vA/TkTUITrAOKIu51E0NLkjzK/img.png)

### 다중 이미지 입력

base64로 인코딩된 형식이나 이미지 URL로 여러 이미지 입력을 가져와 처리할 수 있습니다.

```python
import os
import openai
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
 
# OpenAI API 키 설정
openai.api_key = os.environ["OPENAI_API_KEY"]
 
client = openai.OpenAI()
 
# 이미지 경로
image_path1 = "https://github.com/yunwoong7/getting_started_with_pynecone/assets/69428232/94d9f9d6-e28f-42c1-ab83-b5ef4f1001b2"
image_path2 = "https://github.com/yunwoong7/getting_started_with_pynecone/assets/69428232/56bd5b07-ee0e-4a1c-9745-9afd0c0b26a0"
 
response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "이 이미지에는 무엇이 있나요? 두 이미지 사이에 어떤 차이가 있나요? 파사드 관점에서 알려주세요.",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_path1,
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_path2,
                    },
                },
            ],
        }
    ],
    max_tokens=1000,
)
 
# 이미지 로딩
# 이미지 다운로드
download_img1 = requests.get(image_path1)
download_img2 = requests.get(image_path2)
img1 = Image.open(BytesIO(download_img1.content))
img2 = Image.open(BytesIO(download_img2.content))
 
# 서브플롯 생성
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
 
# 첫 번째 이미지 표시
axes[0].imshow(img1)
axes[0].axis('off')  # 첫 번째 이미지의 축 정보 숨기기
axes[0].set_title('First Image')
 
# 두 번째 이미지 표시
axes[1].imshow(img2)
axes[1].axis('off')  # 두 번째 이미지의 축 정보 숨기기
axes[1].set_title('Second Image')
 
# 전체 플롯 표시
plt.show()
 
# 응답 출력
print(response.choices[0].message.content)
```

Output : 

![img](https://blog.kakaocdn.net/dn/mUt8f/btsz6dSAbC9/L4HXp6AyfagsxN18QBKWG1/img.png)

------

여기까지, GPT-4 with Vision API를 활용하여 이미지를 인식하는 기본 방법부터 이미지를 base64로 인코딩하고, OpenAI의 GPT-4 모델에 전송하는 방법과 모델이 반환하는 데이터를 처리하는 방법에 대해 알아보았습니다.

이러한 기술들은 다양한 분야에서 활용될 수 있는 놀라운 잠재력을 가지고 있습니다. 예를 들어, 이미지 기반 질문에 대한 답변을 얻거나, 이미지 내 특정 객체를 식별하고 위치를 파악하는 등의 작업을 자동화할 수 있습니다. 이는 예술, 의료, 보안, 교육 등 다양한 분야에서 응용될 수 있으며, 향후 더욱 발전된 기능과 함께 더욱 광범위한 영역에서 활용될 것으로 기대됩니다.

GPT-4V API를 활용한 이미지 인식은 단순히 이미지를 '보는' 것을 넘어서, 이미지가 담고 있는 정보와 맥락을 '이해'하고 이를 활용하는 것에 중점을 두고 있습니다. Python과 같은 프로그래밍 언어를 통해 이러한 기술을 접하고 이해하는 것은 개발자들에게 무궁무진한 가능성을 열어주며, 앞으로의 발전을 위한 중요한 발판이 될 것입니다.
