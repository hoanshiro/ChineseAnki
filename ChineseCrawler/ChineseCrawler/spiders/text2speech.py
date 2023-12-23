# from paddlespeech.cli.tts import TTSExecutor
# from base import BaseSpider

# class Text2SpeechSpider(BaseSpider):
#     name = "text2speech"

#     def __init__(self, *args, **kwargs):
#         super(Text2SpeechSpider, self).__init__(*args, **kwargs)
#         self.save_dir = self.base_dir.joinpath("media/text2speech")
#         self.make_dir()
#         self.tts_executor = self.load_executors()

#     def load_executors(self):
#         executor = TTSExecutor()
#         wav = executor(
#             lang="zh",
#             am="fastspeech2_male",
#             voc="hifigan_male",
#             device="cpu",
#             text="有事同群众商量。」",
#             output="./test_2.mp3",
#         )
#         return executor

#     def text2speech(self, text):
#         file_name = f"{self.save_dir}/tts_{text}.mp3"
#         self.tts_executor(
#             lang="zh",
#             am="fastspeech2_male",
#             voc="hifigan_male",
#             device="cpu",
#             text=text,
#             output=file_name,
#         )

#     def parse(self, response):
#         vocab = self.extract_vocab(response)
#         audio_content = self.tts_executor.get_audio(vocab)
#         with open(f"{self.save_dir}/tts_{vocab}.mp3", "wb") as f:
#             f.write(audio_content)

# if __name__ == "__main__":
#     spider = Text2SpeechSpider()
#     spider.load_executors()
