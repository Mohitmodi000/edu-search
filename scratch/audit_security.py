import os
import re

templates_dir = "c:/Users/HP/Desktop/z/edusearch/template"
views_file = "c:/Users/HP/Desktop/z/edusearch/school/views.py"

print("=== STARTING TEMPLATE SECURITY AUDIT ===")

# Audit templates
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            # Check for form tag without csrf_token
            # Find all <form ...> tags
            forms = re.findall(r'<form[^>]*>', content, re.IGNORECASE)
            for form in forms:
                # Find the form block up to the next form tag or close tag or some reasonable limit
                idx = content.find(form)
                block = content[idx:idx+1000] # search next 1000 characters
                if "csrf_token" not in block and "method=\"post\"" in form.lower():
                    print(f"[WARN] Missing CSRF token in POST form in {file}:")
                    print(f"       Form: {form}")
            
            # Check for unsafe usage (using |safe on variables)
            safes = re.findall(r'\{\{[^}]*\|safe[^}]*\}\}', content)
            if safes:
                print(f"[INFO] Found |safe filters in {file}:")
                for s in safes:
                    print(f"       {s}")

print("\n=== STARTING VIEWS SECURITY AUDIT ===")

# Audit views.py for raw queries or unsafe executes
with open(views_file, "r", encoding="utf-8") as f:
    views_content = f.read()

if "raw(" in views_content or "execute(" in views_content:
    print("[WARN] Raw SQL execution or raw query detected in views.py!")
else:
    print("[SUCCESS] No raw SQL execution or raw queries found (standard ORM used).")

if "csrf_exempt" in views_content:
    print("[WARN] csrf_exempt decorator found in views.py!")
else:
    print("[SUCCESS] No csrf_exempt decorators found in views.py.")
