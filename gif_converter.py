from moviepy.editor import VideoFileClip

def convert_mp4_to_gif(input_file, output_file, duration=15, frame_rate=60):
    # Load the MP4 video clip
    video_clip = VideoFileClip(input_file)
    
    # Trim the video clip to the specified duration
    trimmed_clip = video_clip.subclip(0, duration)
    
    # Convert the trimmed video clip to a GIF with the specified frame rate
    trimmed_clip.write_gif(output_file, fps=frame_rate)

if __name__ == "__main__":
    input_file_path = input("Enter the path to the input MP4 file: ")
    output_file_path = input("Enter the path to save the output GIF file: ")
    
    convert_mp4_to_gif(input_file_path, output_file_path)
    print("Conversion complete!")
