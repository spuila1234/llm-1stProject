import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def return_txt1(data) :
    content = f"""
    주제 예시1 : 전기설계 업무회의
    주제 예시2 : 이번주 일요일 일정 약속
    주제 예시3 : 인공지능이란 무엇인가
    출력양식은 아래와 같다. 
    주제 :
    요약 내용 :
    다음 내용을 보고 위와 같은 형태로 답변해 다른내용은 언급 금지
    내용 : {data}
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini", 
        messages=[
            {"role":"system", "content" : "당신은 30년 경력의 주제 정하기, 요약 전문가 입니다."},
            {"role":"user", "content" : content}
    ])
    return response.choices[0].message.content

def return_txt2(data) :
    content = f"""
    다음 내용을 보고 "누가" "누구에게" "무엇을" "왜" "언제까지(요청사항에 대한 회신 기간)" "언제(strat와 end 기준)"요청하였으며,
    그 내용의 "결정여부" 와 그여부의 "이유"가 무엇인지 작성(없는부분은 제외)
    예시 :
    1) A가 B에게 코드를 완성하라 했으며(13초 ~ 22초), B는 알겠다고 답변했다.(23초 ~ 26초)
    2) C는 A에게 일정을 미뤄달라 했다.(1분 27초 ~ 2분 01초)
    3) B는 C에게 회의가 끝나고 코드를 봐달라 했으며,(2분 20초 ~ 2분 27초), C는 알겠다고 대답했다.(2분 28초)
    출력양식 :
    1) 
    2) 
    3)
    (양식에 맞지 않는내용 언급 금지)
    (작성할 내용이 없을경우 "내용 없음")
    내용 : {data}
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini", 
        temperature=0,
        messages=[
            {"role":"system", "content" : "당신은 30년 회의 전문가 입니다."},
            {"role":"user", "content" : content}
    ])
    return response.choices[0].message.content

def return_txt3(data) :
    content = f"""
    다음 내용을 보고 중복된 사항을 제거 후 나열하고,
    그 사항들중 미비한(ex 기간이 정해지지 않았다, 결정여부가 정해지지 않았다)을 작성해
    미비하지 않은부분은 표시 없이 통과
    예시 :
    1) A가 B에게 코드를 완성하라 했으며(13초 ~ 22초), B는 알겠다고 답변했다.(23초 ~ 26초)
     => 기간이 정해지지 않았다.   
    2) C는 A에게 일정을 미뤄달라 했다.(1분 27초 ~ 2분 01초)
     => 결정여부가 정해지지 않았다.
    3) B는 C에게 회의가 끝나고 코드를 봐달라 했으며,(2분 20초 ~ 2분 27초), C는 알겠다고 대답했다.(2분 28초)
    출력양식 :
    1) 
    2) 
    3)
    (양식에 맞지 않는내용 언급 금지)
    (작성할 내용이 없을경우 "내용 없음")

    내용 : {data}
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini", 
        temperature=0,
        messages=[
            {"role":"system", "content" : "당신은 30년 회의 전문가 입니다."},
            {"role":"user", "content" : content}
    ])
    return response.choices[0].message.content

def return_txt4(data) :
    content = f"""
    다음 내용을 보고 바로 확인해야할 사항(기간, 결정여부 등)과
    이후 회의 및 발표때까지 준비해야할 사항을 작성해
    예시 :
    바로 확인이 필요한 사항
    1) B -> A : 코드 완성 날짜 확인
    2) A -> C and 발주처 : 완성본 제출 기한 확인
    다음 회의(발표)까지 준비해야할 사항
    1) 현재 협의한 내용 반영된 자료
    출력양식 :
    바로 확인이 필요한 사항 :
    1) 
    2) 
    다음 회의(발표)까지 준비해야할 사항 :
    1)
    2)
    (양식에 맞지 않는내용 언급 금지)
    (작성할 내용이 없을경우 "내용 없음")   
    내용 : {data}
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini", 
        temperature=0,
        messages=[
            {"role":"system", "content" : "당신은 30년 회의 전문가 입니다."},
            {"role":"user", "content" : content}
    ])
    return response.choices[0].message.content