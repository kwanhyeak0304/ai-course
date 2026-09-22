import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask_server(prompt, temperature=0, max_tokens=300):
    r = client.chat.completions.create(model="gemma4", temperature=temperature, max_tokens=max_tokens,
                                       messages=[{"role": "user", "content": prompt}])
    return r.choices[0].message.content.strip()

print([m.id for m in client.models.list().data])
print(ask_server("안녕? 너는 어떤 모델이야? 한 문장으로."))

# fewshot 비교 (실습 서버 26B)
tests = [("프랑스", "파리"), ("일본", "도쿄"), ("이집트", "카이로"), ("캐나다", "오타와"), ("호주", "캔버라")]
shots = {
    0: "",
    1: "한국 → 서울\n",
    3: "한국 → 서울\n독일 → 베를린\n브라질 → 브라질리아\n",
}
for k, examples in shots.items():
    correct = 0
    for country, capital in tests:
        answer = ask_server(examples + f"{country} →", max_tokens=60).split("\n")[0]
        correct += capital in answer
    print(f"gemma4(26B)  예시 {k}개  정답 {correct}/5")
