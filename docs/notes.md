# Step 2 Study Notes: Code Review & Security Analysis Agent

## 1. OWASP Top 10 (2021 edition) in one line each
| ID | Category | One-line meaning |
|----|----------|------------------|
| A01 | Broken Access Control | Users can do or see things they should not (e.g. open another user's data by changing an ID) |
| A02 | Cryptographic Failures | Weak or missing encryption, weak hashing, secrets exposed |
| A03 | Injection | Untrusted input is run as code or a query (SQL, OS command, XSS) |
| A04 | Insecure Design | The design itself lacks security controls, so coding well cannot fix it |
| A05 | Security Misconfiguration | Default passwords, debug mode on, open cloud storage |
| A06 | Vulnerable and Outdated Components | Using libraries with known vulnerabilities |
| A07 | Identification and Authentication Failures | Weak passwords, no lockout, broken sessions |
| A08 | Software and Data Integrity Failures | Unsafe deserialization, unverified updates |
| A09 | Security Logging and Monitoring Failures | Attacks happen and nobody notices |
| A10 | Server-Side Request Forgery (SSRF) | Server is tricked into calling internal URLs |

## 2. Five vulnerabilities in depth

### 2.1 SQL Injection (A03, CWE-89)
- **How it works:** user input is joined into a SQL string, so an attacker can change the query (`' OR '1'='1`).
- **Vulnerable (Python):**
```python
  cur.execute("SELECT * FROM users WHERE name = '" + name + "'")
```
- **Fixed:**
```python
  cur.execute("SELECT * FROM users WHERE name = ?", (name,))
```
- **Vulnerable (Java):** `st.executeQuery("SELECT * FROM users WHERE name = '" + name + "'");`
- **Fixed (Java):** `PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE name = ?"); ps.setString(1, name);`
- **Why the fix works:** the query structure is fixed first, and input is treated only as data.

### 2.2 Cross-Site Scripting, XSS (A03, CWE-79)
- **How it works:** user input is placed in a web page without escaping, so the attacker's script runs in other users' browsers.
- **Vulnerable (Flask):**
```python
  return render_template_string("<h1>Hello " + name + "</h1>")
```
- **Fixed:**
```python
  from markupsafe import escape
  return render_template_string("<h1>Hello {{ name }}</h1>", name=name)
```
- **Why the fix works:** the template engine escapes `<script>` into harmless text.

### 2.3 CSRF (CWE-352)
- **How it works:** a malicious site makes your logged-in browser send a request (e.g. change email) without your knowledge.
- **Vulnerable:** a form that changes data with no token check.
- **Fixed:** add a secret per-session token to every form and verify it on the server (Flask-WTF `CSRFProtect(app)`).
- **Extra defence:** `SameSite=Lax` or `Strict` cookies.

### 2.4 Hardcoded Secrets (A02, CWE-798)
- **How it works:** passwords or API keys in source code leak through GitHub.
- **Vulnerable:**
```python
  API_KEY = "sk-12345-secret"
```
- **Fixed:**
```python
  import os
  API_KEY = os.environ["API_KEY"]
```
- **Also:** add `.env` to `.gitignore`, and rotate any key that was ever committed.

### 2.5 Broken Access Control / IDOR (A01, CWE-639)
- **How it works:** the app trusts an ID from the URL and never checks who owns the record.
- **Vulnerable:**
```python
  invoice = db.get_invoice(invoice_id)
```
- **Fixed:**
```python
  invoice = db.get_invoice(invoice_id)
  if invoice.owner_id != current_user.id:
      abort(403)
```

## 3. OWASP cheat sheet takeaways
- **SQL Injection Prevention:** use parameterized queries first, then stored procedures, then allow-list validation. Never build queries by string concatenation.
- **XSS Prevention:** escape output based on where it goes (HTML, attribute, JavaScript, URL). Use frameworks that auto-escape, and add a Content-Security-Policy header.
- **CSRF Prevention:** synchronizer token per session, SameSite cookies, and re-authentication for sensitive actions.
- **Secrets Management:** keep secrets out of code, use environment variables or a vault, rotate regularly, and scan repos for leaked keys.

## 4. Ten code smells
1. **Long Method:** one function does too much; split it.
2. **Large Class (God Class):** one class holds unrelated responsibilities.
3. **Duplicate Code:** the same logic copied in many places.
4. **Long Parameter List:** too many arguments; group them into an object.
5. **Deep Nesting:** many levels of if/for; use early returns.
6. **Magic Numbers:** unexplained constants like `if status == 7`; use named constants.
7. **Dead Code:** unused variables, functions, or branches.
8. **Feature Envy:** a method uses another class's data more than its own.
9. **Data Clumps:** the same group of variables always appears together.
10. **Primitive Obsession:** using raw strings and ints instead of small meaningful types.

## 5. RAG in four steps
1. **Chunk:** split documents into small pieces (about 500 characters, 50 overlap) so each piece holds one idea.
2. **Embed:** turn each chunk into a vector of numbers using an embedding model (`all-MiniLM-L6-v2`), so similar meanings sit close together.
3. **Store:** save the vectors and metadata (source, topic, CWE) in a vector database (ChromaDB).
4. **Retrieve:** embed the user's question, find the closest chunks, and give them to the LLM so its answer is grounded in real sources.

## 6. How these notes feed my project
- Section 2 becomes my test set for measuring detection accuracy.
- Section 4 feeds the Code Analysis Agent.
- Section 3 becomes knowledge base content for the RAG assistant.
- Section 5 is the pipeline I build in the knowledge base module.

## 7. What will make my project different
- Static analysis (AST and taint checks) first, then LLM reasoning, not LLM alone.
- CWE IDs and severity scores with a confidence level for every finding.
- Re-scan every generated fix and only show fixes that pass.
- Report precision and recall from my own vulnerable code samples.
- RAG answers that cite the source chunk.

## 8. Open questions
-