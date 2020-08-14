from moviepy.editor import *
import sys, os
from ast import literal_eval

if len(sys.argv) < 4:
    print("*Must provide video and start and end time")
    sys.exit()

v = sys.argv[1]
s = literal_eval(sys.argv[2])
e = literal_eval(sys.argv[3])

if len(sys.argv) == 5:
    d = float(sys.argv[4])
else:
    d = None

class VideoTrimmer:

    def __init__(self, video, start, end):
        self.video = VideoFileClip(video)
        self.start = start
        self.end = end
        self.filename = "CLIP_{}_{}_{}".format(start, end, video.replace("mp4", "mov"))

    def trim_video(self):
        self.video = self.video.subclip(self.start, self.end)

    def set_fadeout(self, duration):
        self.video = self.video.fx(vfx.fadeout, duration=duration)

    def save_video(self):
        self.video.write_videofile(
            self.filename, 
            fps=24,
            temp_audiofile="temp-trim-audio.wav",
            remove_temp=True,
            codec="libx264",#"prores_ks",
            audio_codec="pcm_s16le",
            #ffmpeg_params=[
            #    "-pix_fmt", "yuva444p10le",
            #    "-profile:v", "4444",
            #    "-q:v", "50",
            #],
        )

        self.video.close()

    def close_video(self):
        self.video.close()

if __name__ == "__main__":

    video = VideoTrimmer(v, s, e)

    video.trim_video()

    if d:
        video.set_fadeout(d)

    try:
        video.save_video()
    except:
        video.close_video()
