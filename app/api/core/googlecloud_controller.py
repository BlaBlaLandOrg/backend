from google.cloud import speech
from google.oauth2 import service_account

class GoogleCloudController:


    @staticmethod
    def transcribe_audio_file(file_path):
        service_account_file = '/Users/patrickgerard/Documents/GitHub/cosmic-reserve-394312-ff870bcd49d4.json'
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        client = speech.SpeechClient(credentials=credentials)

        with open(file_path, 'rb') as audio_file:
            audio_content = audio_file.read()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
        )

        response = client.recognize(config=config, audio=audio)
        for result in response.results:
            print("Transcript: {}".format(result.alternatives[0].transcript))


if __name__ == "__main__":
    print(GoogleCloudController.transcribe_audio_file(file_path="assets/audio/Rachel-3cf28684-8470-4277-b94e-a4f2645f74ad.mp3"))