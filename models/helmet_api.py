from inference_sdk import InferenceHTTPClient


class HelmetDetector:

    def __init__(self):

        self.client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key="YOUR_API_KEY"
        )

    def detect(self, image_path):

        try:

            result = self.client.run_workflow(
                workspace_name="suyash-vishnoi",
                workflow_id="general-segmentation-api",
                images={
                    "image": image_path
                },
                parameters={
                    "classes": "helmet"
                },
                use_cache=True
            )

            return result

        except Exception as e:

            print("Helmet API Error:", e)

            return None