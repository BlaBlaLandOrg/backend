import os

import requests
import json


def generate_avatar(prompt: str):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    api_key = os.environ.get("STABLE_DIFFUSION_API_KEY")
    payload = json.dumps({
      "key": f"{api_key}",
      "prompt": f"a avatar for which follows this description {prompt}",
      "negative_prompt": None,
      "width": "512",
      "height": "512",
      "samples": "1",
      "num_inference_steps": "20",
      "seed": None,
      "guidance_scale": 7.5,
      "safety_checker": "yes",
      "multi_lingual": "no",
      "panorama": "no",
      "self_attention": "no",
      "upscale": "no",
      "embeddings_model": None,
      "webhook": None,
      "track_id": None
    })

    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["output"][0]

if __name__ == "__main__":
    print(generate_avatar("a nerd which is surrounded by notebooks and code"))