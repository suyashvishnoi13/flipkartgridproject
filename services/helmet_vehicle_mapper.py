class HelmetVehicleMapper:

    def map_helmets_to_bikes(
        self,
        vehicles,
        helmets
    ):

        motorcycles = [

            v

            for v in vehicles

            if v["class_name"]
            == "motorcycle"
        ]

        results = []

        for bike in motorcycles:

            bx1, by1, bx2, by2 = (
                bike["bbox"]
            )

            expanded_top = max(
                0,
                by1 - 700
            )

            padding = 250

            helmet_count = 0
            no_helmet_count = 0

            for helmet in helmets:

                hx1, hy1, hx2, hy2 = (
                    helmet["bbox"]
                )

                center_x = (
                    hx1 + hx2
                ) // 2

                center_y = (
                    hy1 + hy2
                ) // 2

                inside = (

                bx1 - 100
                <= center_x <=
                bx2 + 100

                and

                by1 - 500
                <= center_y <=
                by2
            )

                if inside:

                    if (
                        helmet["class_name"]
                        == "helmet"
                    ):

                        helmet_count += 1

                    elif (
                        helmet["class_name"]
                        == "no_helmet"
                    ):

                        no_helmet_count += 1

            # Ignore false motorcycle detections
            if (
                helmet_count == 0
                and
                no_helmet_count == 0
            ):
                continue

            results.append({

                "bike_bbox":
                bike["bbox"],

                "helmet_count":
                helmet_count,

                "no_helmet_count":
                no_helmet_count
            })

        print("\n===== HELMET VEHICLE MAP =====")

        for result in results:

            print(result)

        print("==============================\n")

        return results