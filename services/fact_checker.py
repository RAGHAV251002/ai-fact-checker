from services.pdf_parser import extract_text_from_pdf
from services.gemini_service import extract_claims_with_gemini
from services.search_service import search_claim
from services.verification_service import verify_claims


class FactChecker:
    """
    Main orchestration class for the AI Fact-Checking pipeline.
    """

    def fact_check_pdf(self, uploaded_file):
        """
        Pipeline:

        1. Extract text from PDF
        2. Extract factual claims using Gemini
        3. Search live web for evidence
        4. Verify all claims in ONE Gemini request
        5. Return final report
        """

        # -----------------------------------------
        # Step 1 - Extract PDF Text
        # -----------------------------------------

        text = extract_text_from_pdf(uploaded_file)

        # -----------------------------------------
        # Step 2 - Extract Claims
        # -----------------------------------------

        claims = extract_claims_with_gemini(text)

        if not isinstance(claims, list):
            raise Exception("Gemini did not return a valid list of claims.")

        claims_with_evidence = []

        # -----------------------------------------
        # Step 3 - Search Evidence
        # -----------------------------------------

        for item in claims:

            # Skip invalid claim objects
            if not isinstance(item, dict):
                continue

            claim = item.get("claim", "").strip()

            if not claim:
                continue

            search_result = search_claim(claim)

            evidence = search_result.get("answer", "")

            sources = []

            for source in search_result.get("results", []):

                sources.append(
                    {
                        "title": source.get("title", ""),
                        "url": source.get("url", "")
                    }
                )

            claims_with_evidence.append(
                {
                    "claim": claim,
                    "evidence": evidence,
                    "sources": sources
                }
            )

        # -----------------------------------------
        # Step 4 - Verify ALL Claims
        # -----------------------------------------

        report = verify_claims(claims_with_evidence)

        # Safety checks
        if isinstance(report, dict):
            report = [report]

        if not isinstance(report, list):
            raise Exception("Verification service returned an invalid response.")

        # -----------------------------------------
        # Step 5 - Attach Sources
        # -----------------------------------------

        final_report = []

        for verification, original in zip(report, claims_with_evidence):

            # Skip malformed Gemini output
            if not isinstance(verification, dict):
                continue

            verification["sources"] = original.get("sources", [])

            final_report.append(verification)

        # -----------------------------------------
        # Final Response
        # -----------------------------------------

        return {
            "text": text,
            "claims": claims,
            "report": final_report
        }