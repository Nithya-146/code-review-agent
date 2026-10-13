from app.schemas import SecurityFinding, OWASPCategory, SeverityLevel, ReviewReport

def test_data_models():
    finding = SecurityFinding(
        id="SEC-001",
        cwe_id="CWE-89",
        owasp_category=OWASPCategory.A05,
        severity=SeverityLevel.HIGH,
        line_start=14,
        line_end=15,
        title="SQL Injection Detected",
        description="User input concatenated into query string."
    )

    report = ReviewReport(
        submission_id="sub-1001",
        language="python",
        is_valid_syntax=True,
        ast_metadata={"functions": ["get_user"], "loc": 25},
        security_findings=[finding],
        quality_findings=[],
        remediations=[],
        pr_summary_markdown="### Review Passed with 1 finding"
    )

    assert report.is_valid_syntax is True
    assert report.security_findings[0].cwe_id == "CWE-89"
    assert report.security_findings[0].owasp_category == OWASPCategory.A05
    print("✅ Step 2 Schema Validation Test Passed Successfully!")

if __name__ == "__main__":
    test_data_models()