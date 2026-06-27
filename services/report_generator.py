import json
from io import BytesIO

import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


class ReportGenerator:

    @staticmethod
    def generate_json(report):

        return json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        )

    @staticmethod
    def generate_csv(report):

        rows = []

        for item in report:

            rows.append({

                "Claim": item.get("claim"),

                "Status": item.get("status"),

                "Confidence": item.get("confidence"),

                "Correct Fact": item.get("correct_fact"),

                "Reason": item.get("reason")

            })

        return pd.DataFrame(rows)

    @staticmethod
    def generate_pdf(report):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "<b>AI Fact Checking Report</b>",
                styles["Heading1"]
            )
        )

        for index, item in enumerate(report, start=1):

            elements.append(
                Paragraph(
                    f"<b>Claim {index}</b>",
                    styles["Heading2"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Claim:</b> {item.get('claim', '')}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Status:</b> {item.get('status', '')}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Confidence:</b> {item.get('confidence', 0)}%",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Correct Fact:</b> {item.get('correct_fact', '')}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Reason:</b> {item.get('reason', '')}",
                    styles["BodyText"]
                )
            )

            # Optional: include sources
            if item.get("sources"):

                elements.append(
                    Paragraph("<b>Sources:</b>", styles["BodyText"])
                )

                for source in item["sources"]:

                    elements.append(
                        Paragraph(
                            f"- {source.get('title', '')}<br/>{source.get('url', '')}",
                            styles["BodyText"]
                        )
                    )

            elements.append(
                Paragraph("<br/><br/>", styles["BodyText"])
            )

        doc.build(elements)

        buffer.seek(0)

        return buffer