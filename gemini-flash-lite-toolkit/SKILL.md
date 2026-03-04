---
name: gemini-flash-lite-toolkit
description: |
  Gemini 3.1/2.5 Flash-Lite 多功能工具集，包含文档处理、翻译、语音转录、数据提取、模型路由、思考模式和批量处理。
  使用场景：(1) 文本翻译，(2) 音频转文字，(3) PDF文档摘要，(4) 结构化数据提取，(5) 智能模型路由，
  (6) 思考模式问答，(7) 批量异步处理。依赖google-genai SDK。
---

# Gemini Flash-Lite Toolkit

快速使用Google Gemini Flash-Lite模型完成各种AI任务。

## 基础配置

```python
# pip install -U google-genai
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")
MODEL = "gemini-3.1-flash-lite-preview"  # 或 "gemini-2.5-flash-lite"
```

### API Key 配置

**方式1: 环境变量 (推荐)**
```bash
export GEMINI_API_KEY="your_api_key"
```

**方式2: 代码中传入**
```python
client = genai.Client(api_key="AIza...")
```

---

## 1. Translation (翻译)

批量翻译用户生成内容 (聊天、评论、工单)

```python
text = "Hey, are you down to grab some pizza later? I'm starving!"

response = client.models.generate_content(
    model=MODEL,
    config={"system_instruction": "Only output the translated text"},
    contents=f"Translate the following text to German: {text}"
)

print(response.text)
```

**提示**: 使用system instruction约束只输出翻译文本，无额外说明

---

## 2. Transcription (语音转文字)

将音频文件转录为文本，支持多种格式

```python
# 上传音频文件
uploaded_file = client.files.upload(file="sample.mp3")

prompt = "Generate a transcript of the audio."
# prompt = "Generate a transcript. Remove filler words such as 'um', 'uh', 'like'."

response = client.models.generate_content(
    model=MODEL,
    contents=[prompt, uploaded_file]
)

print(response.text)
```

**支持格式**: MP3, WAV, M4A等音频文件

---

## 3. Data Extraction (数据提取)

从文本中提取结构化JSON数据

```python
from pydantic import BaseModel, Field

prompt = "Analyze the user review and determine the aspect, sentiment score, summary quote, and return risk"
input_text = "The boots look amazing and the leather is high quality, but they run way too small. I'm sending them back."

class ReviewAnalysis(BaseModel):
    aspect: str = Field(description="The feature mentioned (e.g., Price, Comfort, Style, Shipping)")
    summary_quote: str = Field(description="The specific phrase from the review about this aspect")
    sentiment_score: int = Field(description="1 to 5 (1=worst, 5=best)")
    is_return_risk: bool = Field(description="True if the user mentions returning the item")

response = client.models.generate_content(
    model=MODEL,
    contents=[prompt, input_text],
    config={
        "response_mime_type": "application/json",
        "response_json_schema": ReviewAnalysis.model_json_schema(),
    },
)

print(response.text)
```

**适用场景**: 评论分析、实体识别、分类、订单处理

---

## 4. Document Processing & Summarization (文档处理)

解析PDF并生成摘要

```python
import httpx

# 下载PDF文档
doc_url = "https://storage.googleapis.com/generativeai-downloads/data/med_gemini.pdf"
doc_data = httpx.get(doc_url).content

prompt = "Summarize this document"
response = client.models.generate_content(
    model=MODEL,
    contents=[
        types.Part.from_bytes(data=doc_data, mime_type='application/pdf'),
        prompt
    ]
)

print(response.text)
```

**功能**: PDF摘要、文档分类、快速筛选、数据提取

---

## 5. Model Routing (智能路由)

使用Flash-Lite作为分类器，根据任务复杂度路由到合适的模型

```python
FLASH_MODEL = 'flash'
PRO_MODEL = 'pro'

CLASSIFIER_SYSTEM_PROMPT = f"""
You are a specialized Task Routing AI. Your sole function is to analyze the user's request and classify its complexity. Choose between `{FLASH_MODEL}` (SIMPLE) or `{PRO_MODEL}` (COMPLEX).
1. `{FLASH_MODEL}`: A fast, efficient model for simple, well-defined tasks.
2. `{PRO_MODEL}`: A powerful, advanced model for complex, open-ended, or multi-step tasks.

A task is COMPLEX if it meets ONE OR MORE of the following criteria:
1. High Operational Complexity (Est. 4+ Steps/Tool Calls)
2. Strategic Planning and Conceptual Design
3. High Ambiguity or Large Scope
4. Deep Debugging and Root Cause Analysis

A task is SIMPLE if it is highly specific, bounded, and has Low Operational Complexity (Est. 1-3 tool calls).
"""

user_input = "I'm getting an error 'Cannot read property 'map' of undefined' when I click the save button. Can you fix it?"

response_schema = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string", "description": "Step-by-step explanation for the model choice"},
        "model_choice": {"type": "string", "enum": [FLASH_MODEL, PRO_MODEL]}
    },
    "required": ["reasoning", "model_choice"]
}

response = client.models.generate_content(
    model=MODEL,
    contents=user_input,
    config={
        "system_instruction": CLASSIFIER_SYSTEM_PROMPT,
        "response_mime_type": "application/json",
        "response_json_schema": response_schema
    },
)

print(response.text)
```

---

## 6. Thinking Mode (思考模式)

配置思考级别，让模型进行更深入的推理

```python
response = client.models.generate_content(
    model=MODEL,
    contents="How does AI work?",
    config={
        "thinking_config": {"thinking_level": "high"}
        # 可选值: "minimal", "low", "medium", "high"
    },
)

print(response.text)
```

**适用场景**: 数学问题、编程任务、多约束问题、需要高准确性的任务

---

## 7. Batch API (批量处理)

异步批量处理大量数据，50%标准成本，24小时内完成

```python
# Step 1: 创建JSONL请求文件 (batch_requests.jsonl)
# 格式: {"contents": ["prompt1"]}
#       {"contents": ["prompt2"]}

# Step 2: 上传并创建批量任务
uploaded_batch_requests = client.files.upload(file="batch_requests.jsonl")

batch_job = client.batches.create(
    model=MODEL,
    src=uploaded_batch_requests.name,
    config={'display_name': "batch_job-1"}
)

print(f"Created batch job: {batch_job.name}")

# Step 3: 等待完成并获取结果 (最长24小时)
if batch_job.state.name == 'JOB_STATE_SUCCEEDED':
    result_file_name = batch_job.dest.file_name
    file_content_bytes = client.files.download(file=result_file_name)
    file_content = file_content_bytes.decode('utf-8')
    
    for line in file_content.splitlines():
        print(line)
```

**JSONL文件格式**:
```json
{"contents": ["Translate this to French: Hello"]}
{"contents": ["Summarize: The quick brown fox..."]}
{"contents": ["Extract entities: John works at Google"]}
```

---

## 快速参考表

| 功能 | 模型 | 关键参数 |
|------|------|----------|
| 翻译 | flash-lite | `system_instruction` |
| 语音转录 | flash-lite | `client.files.upload()` |
| 数据提取 | flash-lite | `response_mime_type: json` |
| 文档摘要 | flash-lite | `Part.from_bytes(mime_type='pdf')` |
| 智能路由 | flash-lite | JSON schema + system prompt |
| 思考模式 | flash-lite | `thinking_config.thinking_level` |
| 批量处理 | flash-lite | `client.batches.create()` |

## 安装

```bash
pip install google-genai httpx pillow pydantic
```

## API Key 获取

访问: https://aistudio.google.com/app/apikey
