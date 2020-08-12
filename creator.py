import sys, os
from moviepy.editor import *

if len(sys.argv) < 2:
    print("*Must give directory")
    sys.exit()

d = sys.argv[1]

class AudioVideo:

    def __init__(self, start_directory):
        self.d = start_directory
        contents = os.listdir(self.d)

        for content in contents:
            if ".png" in content or ".jpg" in content or ".mov" in content or ".mp4" in content:
                media = content
            elif ".wav" in content or ".mp3" in content:
                audio = content

        self.media = os.path.join(d, media)
        self.audio = os.path.join(d, audio)

        self.a = AudioFileClip(self.audio)

        if ".mov" in self.media or ".mp4" in self.media:
            self.v = VideoFileClip(self.media).set_duration(self.a.duration + 0.1)
        else:
            self.v = ImageClip(self.media).set_duration(self.a.duration + 0.1)

        self.f = self.v.set_audio(self.a)

    def set_fadeout(self, duration):
        self.f = self.f.fx(vfx.fadeout, duration=duration)

    def save_video(self):

        filename = self.d.strip("/") + ".mov"

        self.f.write_videofile(
            filename, 
            fps=24,
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            codec="libx264",
            audio_codec="aac",
        )

        self.f.close()

    def close_video(self):

        self.f.close()


if __name__ == "__main__":

    avideo = AudioVideo(d)

    if len(sys.argv) == 3:
        avideo.set_fadeout(float(sys.argv[2]))

    try:
        avideo.save_video()
    except:
        print("Error saving video")
        avideo.close_video()
        raise
