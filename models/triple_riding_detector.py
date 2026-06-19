class TripleRidingDetector:

    def count_riders(
        self,
        vehicle_helmet_map
    ):

        results = []

        for bike in vehicle_helmet_map:

            helmet_count = bike.get(
                "helmet_count",
                0
            )

            no_helmet_count = bike.get(
                "no_helmet_count",
                0
            )

            rider_count = (
                helmet_count +
                no_helmet_count
            )

            results.append({

                "bike_bbox":
                bike["bike_bbox"],

                "helmet_count":
                helmet_count,

                "no_helmet_count":
                no_helmet_count,

                "rider_count":
                rider_count,

                "violation":
                rider_count >= 3
            })

        return results