
# Reform Movie Datasets with SN
LSMDC_dir=/data1/movie/LSMDC
CMD_dir=/data1/movie/CMD

python LSMDC_processing.py $LSMDC_dir
python CMD_processing.py $CMD_dir


video_dir=$data_base/videos/sep1
frame_dir=$data_base/frames/sep1


# extract audio(.wav) from mkv files
python3 extract/extract_audio.py $video_dir
mv $video_dir/*.wav $audio_dir

# # separate speech and bgm
python3 -m bytesep separate \
       --source_type="vocals" \
       --audio_path="$audio_dir" \
       --output_path="./data/$year/speech"


