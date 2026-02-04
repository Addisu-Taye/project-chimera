import pytest 
from skills.skill_download_youtube import download_youtube 
from skills.skill_transcribe_audio import transcribe_audio 
def test_skills_interfaces(): 
    with pytest.raises(NotImplementedError): 
        download_youtube("https://youtube.com/video") 
    with pytest.raises(NotImplementedError): 
        transcribe_audio("video.mp4") 
