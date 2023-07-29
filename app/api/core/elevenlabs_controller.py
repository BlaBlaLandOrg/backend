from elevenlabs import get_api_key
from elevenlabs import voices as elevenlabs_voices
from elevenlabs.api.voice import Voice
from elevenlabs import generate, play
import json
import os
import uuid
# API key Env variable ELEVEN_API_KEY

class ElevenlabsController:

    @staticmethod
    def list_voices():
        # pydantic models to json -> json.loads(voices.json())
        voices = elevenlabs_voices()
        t = Voice(voice_id="test")
        return voices.json()

    def text_to_speach(self, text: str, voice_name: str, model: str = "eleven_multilingual_v1"):
        audio = generate(
            text=f"{text}",
            voice=f"{voice_name}",
            model=f"{model}",
            api_key=get_api_key()
        )

        file_id = f"{os.path.abspath(os.getcwd())}/assets/audio/{voice_name}-{uuid.uuid4()}.wav"

        with open(file_id, 'wb') as f:
            f.write(audio)



if __name__ == "__main__":
    e = ElevenlabsController()
    # print(e.list_voices())
    play(e.text_to_speach(text="Hallo ich bin Patrick von Blablaland", voice_name="Rachel"))