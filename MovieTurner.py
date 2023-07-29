from moviepy.editor import VideoFileClip, AudioFileClip, vfx
import random

def GetVideo(input_video_path, input_audio_path, output_path):
    # Load the video and audio clips
    video_clip = VideoFileClip(input_video_path)
    audio_clip = AudioFileClip(input_audio_path)

    # Calculate the maximum possible start time for the video clip
    max_start_time = video_clip.duration - audio_clip.duration

    # Generate a random start time within the valid range
    start_time = random.uniform(0, max_start_time)

    # Crop the video to match the duration of the audio
    cropped_video = video_clip.subclip(start_time, start_time + audio_clip.duration)

    # Set the audio of the cropped video to the same as the input audio
    final_video = cropped_video.set_audio(audio_clip)

    # Save the final video with the audio combined
    final_video.write_videofile(output_path, codec='libx264')

    # Close the video and audio clips
    video_clip.close()
    audio_clip.close()

def adjust_video_for_phone(input_path, phone_width, phone_height, output_path):
    try:
        video_clip = VideoFileClip(input_path)

        # Calculate the aspect ratios of the video and the phone screen
        video_aspect_ratio = video_clip.w / video_clip.h
        phone_aspect_ratio = phone_width / phone_height

        if video_aspect_ratio > phone_aspect_ratio:
            # If the video aspect ratio is wider than the phone's, add black bars to the top and bottom
            video_clip = video_clip.resize(height=phone_height)
            video_clip = vfx.center(video_clip, (phone_width, phone_height))
        else:
            # If the video aspect ratio is narrower than the phone's, add black bars to the sides
            video_clip = video_clip.resize(width=phone_width)
            video_clip = vfx.center(video_clip, (phone_width, phone_height))

        # Save the adjusted video
        video_clip.write_videofile(output_path, codec="libx264")

        print("Video adjustment completed successfully.")
    except Exception as e:
        print("Error occurred while adjusting the video:", e)


if __name__ == "__main__":
    input_video_pathh = r"C:\Users\PC\Desktop\RedditVideoMaker\Parkour.mp4"
    input_audio_path = r"C:\Users\PC\Desktop\RedditVideoMaker\example.mp3"
    output_path = r"C:\Users\PC\Desktop\RedditVideoMaker\Output\output.mp4"

    # GetVideo(input_video_pathh, input_audio_path, output_path)

    input_video_path = r"C:\Users\PC\Desktop\RedditVideoMaker\Output\output.mp4"
    output_video_path = r"C:\Users\PC\Desktop\RedditVideoMaker\Output\output.mp4"
    phone_width, phone_height = 720, 1280  # Replace with your phone's resolution

    adjust_video_for_phone(input_video_path, phone_width, phone_height, output_video_path)
