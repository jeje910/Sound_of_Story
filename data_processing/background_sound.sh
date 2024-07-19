# Extract Background Sound
video_dir=./processed_data
audio_dir=../data/audio_files
bgs_dir=../data/bgs

# extract audio(.wav) from mkv files
# python3 extract/extract_audio.py $video_dir

cd /home1/s20225168/Sound_of_Story/data_processing

# Separate Vocals
python -m bytesep separate \
       --source_type="accompaniment" \
       --audio_path="$audio_dir" \
       --output_path="$bgs_dir" \

       
