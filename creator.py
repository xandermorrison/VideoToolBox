import sys, os
from moviepy.editor import *

if len(sys.argv) != 4:
    print("*Must give directory, fadeOut, and type")
    sys.exit()

d = sys.argv[1]
f = sys.argv[2]
t = sys.argv[3]

class AudioVideo:

    def __init__(self, start_directory, comp_type):
        self.d = start_directory
        self.contents = os.listdir(self.d)
        self.t = comp_type

        if self.t.lower() == 'y':
            self.set_up_composite()
        else:
            self.set_up_regular()

    def set_up_composite(self):
        for content in self.contents:
            if ".png" in content or ".jpg" in content:
                image = content
            elif ".mov" in content or ".mp4" in content:
                video = content
            elif ".wav" in content or ".mp3" in content:
                audio = content

        self.video = os.path.join(d, video)
        self.image = os.path.join(d, image)
        self.audio = os.path.join(d, audio)
        temp_i = ImageClip(self.image)
        temp_i = temp_i.resize(0.5) # comment out for full res
        temp_v = VideoFileClip(self.video, has_mask=True)

        self.a = AudioFileClip(self.audio)
        self.v = CompositeVideoClip([temp_i, temp_v]).set_duration(self.a.duration + 0.1)

        self.f = self.v.set_audio(self.a)

    def set_up_regular(self):

        for content in self.contents:
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
            temp_audiofile="temp-audio.wav",
            remove_temp=True,
            codec="libx264",#"prores_ks",
            audio_codec="pcm_s16le",
            #ffmpeg_params=[
            #    "-pix_fmt", "yuva444p10le",
            #    "-profile:v", "4444",
            #    "-q:v", "50",
            #],
        )

        self.close_video()

    def close_video(self):

        self.f.close()
        self.a.close()

        if self.t.lower() == "y":
            self.temp_i.close()
            self.temp_v.close()
        else:
            self.v.close()


if __name__ == "__main__":

    avideo = AudioVideo(d, t)

    avideo.set_fadeout(float(f))

    try:
        avideo.save_video()
    except:
        print("Error saving video")
        avideo.close_video()
        raise
