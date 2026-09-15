import ollama, time, sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


t = time.time()
n = 0
for chunk in ollama.chat(model="qwen3:8b", think=False, stream=True,
                         messages=[{"role": "user", "content": "봄에 대한 짧은 시를 4줄로 써줘."}],
                         options={"temperature": 0}):
    print(chunk.message.content, end="", flush=True)
    n += 1
print(f"\n{n} 조각, {time.time() - t:.1f}초")
