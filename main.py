from crewai import Agent, Task, Crew, Process
from crewai_tools.tools.directory_read_tool.directory_read_tool import DirectoryReadTool
from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool

directory_read_tool = DirectoryReadTool('/transcription')
file_read_tool = FileReadTool()
producer = Agent(
    role='Producer',
    goal='Generate engaging and relevant YouTube video titles and descriptions based on provided transcriptions, including appropriate tags in the descriptions to optimize visibility and audience engagement',
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in crafting compelling video content for the YouTube channel 'Wade.Digital'. Your expertise lies in analyzing video transcriptions and distilling the essence into captivating titles and informative descriptions that resonate with the target audience. Your work significantly contributes to the channel's growth by enhancing viewer engagement and expanding reach through carefully selected tags."
    ),
    tools=[directory_read_tool, file_read_tool],
    allow_delegation=True
)

copywriting_task = Task(
    description=(
        "From the propvided video transcription directory, find the most recent file and read it. Extract key themes and messages. Based on this analysis, craft a captivating YouTube video title that accurately reflects the video's content while enticing potential viewers. Additionally, write a comprehensive description that provides viewers with a clear overview of the video's content, including any relevant links or call-to-action statements. Append a set of relevant tags within the description to improve the video's searchability and alignment with audience interests."
    ),
    expected_output=(
        "A properly formatted json file with the following keys: title: the YouTube video title, description: a detailed description. The description should include a brief summary of the video's content, relevant links, call-to-action prompts, and a list of tags related to the video's themes and content."
    ),
    agent=producer,
    output_file='youtube_video_metadata.json'
)

# Forming the tech-focused crew with enhanced configurations
crew = Crew(
  agents=[producer],
  tasks=[copywriting_task],
  process=Process.sequential  # Optional: Sequential task execution is default
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'transcription': './transcription.txt'})
print(result)
