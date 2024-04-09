import logging

from oauth2client.client import HttpAccessTokenRefreshError
from youtube_upload import main as youtube_upload
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional


class YouTubeUploadToolSchema(BaseModel):
    file_path: str = Field(..., description='Video file to upload')
    title: Optional[str] = Field(None, description='Video title')
    category: Optional[str] = Field(None, description='Name of video category')
    description: Optional[str] = Field(None, description='Video description')
    description_file: Optional[str] = Field(None, description='Video description file')
    tags: Optional[str] = Field(None, description='Video tags (separated by commas: "tag1, tag2,...")')
    privacy: str = Field("public", description='Privacy status (public | unlisted | private)')
    publish_at: Optional[str] = Field(None, description='Publish date (ISO 8601): YYYY-MM-DDThh:mm:ss.sZ')
    license: str = Field('youtube', description='License for the video, either "youtube" (the default) or "creativeCommon"')
    location: Optional[str] = Field(None, description='Video location"')
    recording_date: Optional[str] = Field(None, description="Recording date (ISO 8601): YYYY-MM-DDThh:mm:ss.sZ")
    default_language: Optional[str] = Field(None, description="Default language (ISO 639-1: en | fr | de | ...)")
    default_audio_language: Optional[str] = Field(None, description="Default audio language (ISO 639-1: en | fr | de | ...)")
    thumb: Optional[str] = Field(None, description='Image file to use as video thumbnail (JPEG or PNG)')
    playlist: Optional[str] = Field(None, description='Playlist title (if it does not exist, it will be created)')
    title_template: str = Field("{title} [{n}/{total}]", description='Template for multiple videos (default: {title} [{n}/{total}])')
    embeddable: bool = Field(True, description='Video is embeddable')
    client_secrets: Optional[str] = Field(None, description='Client secrets JSON file')
    credentials_file: Optional[str] = Field(None, description='Credentials JSON file')
    auth_browser: bool = Field(False, description='Open a GUI browser to authenticate if required')
    chunksize: int = Field(1024 * 1024 * 8, description='Update file chunksize')
    open_link: bool = Field(False, description='Opens a url in a web browser to display the uploaded video')


class CustomTool(BaseTool):

    def _generate_description(self):
        """
        The super's function uses the entire schema to generate the description. This override will leave the default tool class description.
        """
        pass


class YouTubeUploadTool(CustomTool):
    name: str = "YouTube Uploader"
    description: str = "Uploads a video to YouTube"
    args_schema = YouTubeUploadToolSchema

    def init(self, **kwargs):
        super().__init__(**kwargs)
        self.description = "Uploads a video to YouTube"
        self.args_schema = YouTubeUploadToolSchema
        self._generate_description()

    def _run(self, *args, **kwargs):
        from optparse import Values
        # Convert the Pydantic model to a dictionary so it can be used with argparse
        arguments = vars(self.args_schema(**kwargs))

        # Separate the file_path from the rest of the arguments
        file_path = arguments.pop('file_path')

        # Create an options object
        options = Values()

        # Set the attributes of the options object based on your arguments
        for key, value in arguments.items():
            setattr(options, key, value)

        # Call run_main directly
        try:
            youtube_upload.run_main(None, options, [file_path])
        except HttpAccessTokenRefreshError as e:
            logging.error(e)


metadata_path = "youtube_video_metadata.json"

metadata = YouTubeUploadToolSchema.parse_file(metadata_path)

tool = YouTubeUploadTool()

tool.run(**metadata.dict())

pass