from widgets.project_manager_ui import Ui_FormProjectManager
from widgets.annotation_manager import AnnotationWidget
from widgets.annotate_dialog import AnnotateDialog
from widgets.video_stream_manager import VideoStreamer

class object_detector():
    
    def __init__(
            self, 
            parentui: Ui_FormProjectManager,
            projec_data, 
            my_annotator: AnnotationWidget,
            my_video: VideoStreamer,
            parent=None
        ):

        self.project_data = projec_data
        self.my_annotator = my_annotator
        self.my_video = my_video
        self.my_parent = parent