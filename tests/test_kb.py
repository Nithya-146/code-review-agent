import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kb.retriever import retrieve

def test_kb_queries():
    print("Testing Query 1: 'prevent SQL injection'...")
    results_sqli = retrieve("prevent SQL injection", k=3)
    assert len(results_sqli) > 0, "No results returned for SQL injection query"
    assert any("sql" in r["topic"].lower() or "sql" in r["content"].lower() for r in results_sqli)
    print("✓ Successfully retrieved SQL injection prevention rules")

    print("\nTesting Query 2: 'hardcoded passwords'...")
    results_secrets = retrieve("hardcoded passwords", k=3)
    assert len(results_secrets) > 0, "No results returned for secrets query"
    assert any("secret" in r["topic"].lower() or "password" in r["content"].lower() for r in results_secrets)
    print("✓ Successfully retrieved Secrets & Password remediation rules")

    print("\nTop match snippet:")
    print("-" * 50)
    print(results_sqli[0]["content"][:200] + "...")
    print("-" * 50)
    print("\n✅ Step 5 Knowledge Base & Retriever Verified Successfully!")

if __name__ == "__main__":
    test_kb_queries()