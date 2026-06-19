from app import TrafficVision


class PipelineService:

    def __init__(self):

        self.app = TrafficVision()

    def run(self, image_path):

        self.app.process_image(
            image_path
        )