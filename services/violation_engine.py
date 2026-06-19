class ViolationEngine:

    def analyze(
        self,
        rider_results,
        helmet_results
    ):

        violations = []

        # --------------------------------
        # Triple Riding
        # --------------------------------

        for bike in rider_results:

            rider_count = bike.get(
                "rider_count",
                0
            )

            helmet_count = bike.get(
                "helmet_count",
                0
            )

            no_helmet_count = bike.get(
                "no_helmet_count",
                0
            )

            # Standard rule
            if rider_count >= 3:

                violations.append({

                    "type":
                    "TRIPLE_RIDING",

                    "confidence":
                    1.0
                })

            # Hackathon fallback:
            # Sometimes one rider is missed but
            # two helmets are detected on a bike.

            elif (
                rider_count >= 2
                and
                helmet_count >= 2
            ):

                violations.append({

                    "type":
                    "TRIPLE_RIDING",

                    "confidence":
                    0.85
                })

        # --------------------------------
        # No Helmet
        # --------------------------------

        for detection in helmet_results:

            class_name = (
                detection
                .get(
                    "class_name",
                    ""
                )
                .lower()
            )

            if class_name == "no_helmet":

                violations.append({

                    "type":
                    "NO_HELMET",

                    "confidence":
                    detection["confidence"]
                })

        return violations