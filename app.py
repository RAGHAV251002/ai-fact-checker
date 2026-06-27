import traceback
import streamlit as st

from services.fact_checker import FactChecker
from services.report_generator import ReportGenerator

# --------------------------------------------------
# Initialize
# --------------------------------------------------

checker = FactChecker()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Fact Checker",
    page_icon="🕵️",
    layout="wide"
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🕵️ AI Fact Checker")

    st.markdown("---")

    st.markdown("### Features")

    st.write("📄 Upload PDF")
    st.write("🔍 Extract Claims")
    st.write("🌐 Verify using Live Web")
    st.write("📊 Verification Report")
    st.write("⬇️ Download JSON")
    st.write("⬇️ Download CSV")

    st.markdown("---")

    st.success("Ready")

# --------------------------------------------------
# Main Page
# --------------------------------------------------

st.title("🕵️ Automated Fact-Checking Web App")

st.markdown("""
Upload a PDF containing business, marketing, financial or technical content.

The application will:

- 📄 Extract factual claims
- 🌐 Verify using live web evidence
- ✅ Detect outdated or false claims
- 📊 Generate a verification report
""")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# --------------------------------------------------
# Processing
# --------------------------------------------------

if uploaded_file:

    st.success(f"Uploaded: **{uploaded_file.name}**")

    try:

        with st.spinner("🤖 Extracting claims and verifying with live web..."):

            result = checker.fact_check_pdf(uploaded_file)

        st.success("Analysis Complete!")

        extracted_text = result["text"]
        claims = result["claims"]
        report = result["report"]

        json_report = ReportGenerator.generate_json(report)
        csv_report = ReportGenerator.generate_csv(report)
        pdf_report = ReportGenerator.generate_pdf(report)

        tab1, tab2, tab3 = st.tabs(
            [
                "📄 Extracted Text",
                "📌 Claims",
                "📊 Verification Report"
            ]
        )

        # ======================================================
        # TAB 1
        # ======================================================

        with tab1:

            st.subheader("Extracted PDF Text")

            st.text_area(
                "PDF Content",
                extracted_text,
                height=450
            )

        # ======================================================
        # TAB 2
        # ======================================================

        with tab2:

            st.subheader("Extracted Claims")

            if claims:

                for i, claim in enumerate(claims, start=1):

                    with st.expander(f"Claim {i}"):

                        st.write(claim.get("claim", ""))

                        if "type" in claim:
                            st.caption(
                                f"Type: {claim['type']}"
                            )

            else:

                st.warning("No factual claims detected.")

        # ======================================================
        # TAB 3
        # ======================================================

        with tab3:

            st.subheader("Fact-Checking Report")

            total = len(report)

            verified = sum(
                1 for r in report
                if r["status"] == "Verified"
            )

            false = sum(
                1 for r in report
                if r["status"] == "False"
            )

            outdated = sum(
                1 for r in report
                if r["status"] == "Outdated"
            )

            insufficient = sum(
                1 for r in report
                if r["status"] == "Insufficient Evidence"
            )

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric("Total", total)
            c2.metric("Verified", verified)
            c3.metric("False", false)
            c4.metric("Outdated", outdated)
            c5.metric("Unknown", insufficient)

            st.divider()

            if report:

                for i, item in enumerate(report, start=1):

                    with st.expander(f"Verification {i}"):

                        st.markdown("### 📝 Claim")
                        st.write(item.get("claim", ""))

                        status = item.get("status", "")

                        if status == "Verified":
                            st.success(f"✅ {status}")

                        elif status == "False":
                            st.error(f"❌ {status}")

                        elif status == "Outdated":
                            st.warning(f"🟡 {status}")

                        else:
                            st.info(f"⚪ {status}")

                        st.write(
                            f"**Confidence:** {item.get('confidence', 0)}%"
                        )

                        st.markdown("### ✅ Correct Fact")
                        st.write(
                            item.get("correct_fact", "N/A")
                        )

                        st.markdown("### 📖 Reason")
                        st.write(
                            item.get("reason", "N/A")
                        )

                        if item.get("sources"):

                            st.markdown("### 🔗 Sources")

                            for source in item["sources"]:

                                title = source.get("title", "Source")

                                url = source.get("url", "")

                                st.markdown(
                                    f"- [{title}]({url})"
                                )

            else:

                st.warning("No verification results available.")

            st.divider()

            st.subheader("⬇️ Download Reports")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_report,
                    file_name="fact_check_report.json",
                    mime="application/json"
                )

            with col2:

                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_report.to_csv(index=False),
                    file_name="fact_check_report.csv",
                    mime="text/csv"
                )
            with col3:

                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_report,
                    file_name="fact_check_report.pdf",
                    mime="application/pdf"
                )    
    except Exception as e:

        st.error(f"❌ Error: {e}")

        st.code(traceback.format_exc())

        st.stop()