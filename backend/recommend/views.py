from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

@api_view(['POST'])
def character_recommendation(request):
    try:
        character_info = request.data.get('character_info')  # ex: "해리포터 - 해리포터"
        if not character_info:
            return Response({'error': 'character_info is required.'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"""
당신은 '{character_info}' 캐릭터입니다.

다음 조건에 따라 '{character_info}'의 관점에서 영화 추천을 해주세요:

- 반드시 **실제로 존재하는 영화**만 추천하세요.
- 추천 영화는 **TMDB에 등록된 영화**여야 하며, **한글 제목으로** 응답하세요.
- **영문 제목이 아닌, TMDB에서 사용하는 한국어 제목**을 그대로 써 주세요.
- 존재하지 않는 영화나 가상의 영화는 절대 포함하지 마세요.
- 추천 영화는 TMDB에 등록된 영화 제목과 일치해야 합니다.
- 당신이 좋아할 만한 영화 10개를 추천하세요 (Top 10)
- 각 영화의 추천 이유를 8줄로 서술하세요
- 각 영화에 대해 10점 만점 기준의 평점을 부여하세요 (정수로 표현하세요)
- 당신이 싫어할 영화도 5개 추천하세요 (Bottom 5)
- 각 비추천 영화에 대해서도 8줄로 설명하세요
- 작성 어투를 진짜 영화 속 당신의 말투 처럼 바꿔서 설명을 적어주세요 (나이나 살았던 시대의 말투도 반영하세요)
- 비어 있거나, 값이 없거나, 문법이 틀린 JSON 응답 을 절대 작성하지 마세요

응답은 아래와 같은 JSON 형식으로만 출력하세요. 주석이나 설명은 절대 포함하지 마세요:
{{
  "top": [
    {{ "title": "한글 영화 제목", "score": 9, "reason": "추천 이유 8줄" }},
    ... (10개)
  ],
  "bottom": [
    {{ "title": "한글 영화 제목", "score": 2, "reason": "비추천 이유 8줄" }},
    ... (5개)
  ]
}}
"""



        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 영화 캐릭터입니다."},
                {"role": "user", "content": prompt},
            ],
            # response_format="json"
        )
        
        gpt_response = completion.choices[0].message.content
        print("GPT 응답 원문:", gpt_response)
        result = json.loads(gpt_response)
        return Response(result)

    except Exception as e:
        print("GPT 요청 중 오류 발생:", e)  # 로그 확인용
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)