import os
import assemblyai as aai

# Doesnt work! @ASSEMBLYAI -> Python SDK broken ? :D
class AssemblyAiController:

    @staticmethod
    def speach_to_text(audio_file: str):
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        return {"text": transcript.text, "summary": transcript.summary, "duration": transcript.audio_duration,
                "entities": transcript.entities, "sentiment": transcript.sentiment_analysis}

if __name__ == "__main__":
    print(AssemblyAiController.speach_to_text(audio_file="assets/audio/Rachel-d203778a-f5fb-4368-942e-8b00cd898c64.mp3"))