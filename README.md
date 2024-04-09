# LLM Assisted Youtube Pipeline

This repo is something I put together to assist with my [100 Days challenge playlist on Youtube](https://www.youtube.com/playlist?list=PLQ_ZWdfWBMKsLgcocR3D_Zboa2C1WhBiy). It's presented as-is with no promises to maintain it, and is presented solely as a professional exercise.

The idea behind the challenge is to create a series of 100 impromptu videos, and use it as an exercise to build an automated pipeline. I start with a video on my iPhone, which I airdrop to my Mac. I then move it to a specific folder with folder actions setup to do some basic processing on the video. 

First, I split the audio from the original file, returning a ffmpeg-compatible audio file to a second folder.  
This folder action passes the audio file to a [Whisper-X ASR pipeline](https://github.com/ahmetoner/whisper-asr-webservice) that I have running in my lab. This returns a txt file of the transcript. 

From there, I manually run main, which runs it through a very simple CrewAI job to read the latest transcript and generate the metadata file. ``

You'll need to add the original file_path to the metadata file and fix it up a bit, but it's a good start. 

I was able to upload a video running uploader in my IDE, which is enough for this iteration. 

## TODO: 
* Validate metadata file using crew AI job. 
* Tags should be included in description, not in the tags field
* Update playlist in metadata
* Auto select proper category from youtube options
* Make proper crewAI job to use the uploader
* Move pipline directories and macos folder actions

