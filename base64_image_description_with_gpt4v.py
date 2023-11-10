import base64
import requests
import os
from PIL import Image
import matplotlib.pyplot as plt

# OpenAI API 키 설정
api_key = os.environ["OPENAI_API_KEY"]

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