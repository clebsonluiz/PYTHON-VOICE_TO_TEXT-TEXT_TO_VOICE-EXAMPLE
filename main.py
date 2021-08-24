import pyttsx3 as speaker
import speech_recognition as sr


class VoiceToText:

    def __init__(self) -> None:
        self.recognizer: sr.Recognizer = sr.Recognizer()
    

    def listen(self) -> str:
        self.response = ""
        try:
            with sr.Microphone() as source:
                print("Iniciando captura...")
                audio = self.recognizer.listen(source)
                response = self.recognizer.recognize_sphinx(audio)
                print("Termino da captura...")
        except (sr.UnknownValueError or sr.RequestError) as e:
            response = "Sphinx Error; {0}".format(e)
        finally:
            return response 


class TextToVoice:

    def __init__(self, name : str = None, language: str = None) -> None:
        self.engine: speaker.Engine = speaker.init()
        self.set_language(name=name, language=language)


    def say(self, msg: str):
        assert(msg is not None and len(msg) > 0)
        self.engine.say(msg)
        self.engine.runAndWait()


    def set_language(self, name : str = None, language: str = None):
        voices: list = self.engine.getProperty('voices')
        find = lambda s, voice: s and (len(s) > 0 and s in voice.id)  

        for voice in voices:
            if name and language :
                if find(name, voice) and find(language, voice):
                    self.engine.setProperty('voice', voice.id)
                    return True
            elif (not name or not language) and find(name, voice) or find(language, voice):
                self.engine.setProperty('voice', voice.id)
                return True
        return False



if __name__ == "__main__":
    response: str = VoiceToText().listen()
    print("Response.>> " + response)
    TextToVoice(language="EN-US").say(response)

