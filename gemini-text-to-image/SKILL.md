---
name: gemini-text-to-image
description: |
  Generate images from text prompts using Google Gemini's native image generation (Nano Banana).
  Use for: (1) Creating images from text descriptions, (2) Image editing with text prompts, (3) Multi-image composition,
  (4) Iterative image refinement through conversation. Requires google-genai SDK and Gemini API key.
---

# Gemini Text-to-Image Skill

## Quick Start

```python
from google import genai
from google.genai import types

client = genai.Client()  # Uses GEMINI_API_KEY env var

prompt = "A cute cat wearing a fedora in a coffee shop"

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

# Save the generated image
for part in response.parts:
    if part.inline_data is not None:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
```

## API Key Configuration

### Method 1: Environment Variable (Recommended)
```bash
export GEMINI_API_KEY="your_api_key_here"
```
Or on Windows:
```cmd
set GEMINI_API_KEY=your_api_key_here
```

### Method 2: Direct in Code
```python
client = genai.Client(api_key="YOUR_API_KEY")
```

### Get API Key
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `gemini-2.5-flash-image` | Nano Banana - fast, efficient | High-volume generation |
| `gemini-3.1-flash-image-preview` | Nano Banana 2 - speed optimized | High-volume, fast response |
| `gemini-3-pro-image-preview` | 4K resolution output | Professional, high-res needs |

## Image Generation Examples

### Basic Text-to-Image
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A serene mountain lake at sunset with reflection",
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
)
```

### With Aspect Ratio
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A modern logo design",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="16:9")
    )
)
```

### Image Editing (Text + Image Input)
```python
from PIL import Image

# Load an existing image
image = Image.open("input.png")

# Edit with text prompt
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Add a vintage filter and make it black and white",
        image
    ],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
)
```

### Multi-Image Composition
```python
image1 = Image.open("image1.png")
image2 = Image.open("image2.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Compose these two images into a single scene with smooth blending",
        image1,
        image2
    ],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
)
```

## Prompt Writing Tips

1. **Describe the scene, don't just list keywords**
   - ❌ "cat, fedora, coffee"
   - ✅ "A ginger cat wearing a brown fedora sitting on a wooden counter in a cozy coffee shop, looking at the camera"

2. **For realistic images, think like a photographer**
   - Mention camera angles, lens types, lighting
   - Example: "A wide-angle shot of a sunset over the ocean, golden hour lighting"

3. **For text rendering**
   - Be explicit: "A restaurant menu that says 'Welcome' in elegant cursive font"

4. **For style control**
   - Specify art style: "oil painting", "watercolor", "3D render", "photorealistic"

## Common Issues

| Error | Solution |
|-------|----------|
| `API_KEY_INVALID` | Check your API key at https://aistudio.google.com/app/apikey |
| `Model not found` | Use correct model name: `gemini-2.5-flash-image` |
| `No image in response` | Check `response_modalities=["TEXT", "IMAGE"]` in config |

## Installation

```bash
pip install google-genai pillow
```

Minimum Python version: 3.11
