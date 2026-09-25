"""
HHGOA Submission Verification Script
Run this before submitting to verify all requirements are met
"""
import json
import os
from pathlib import Path

def verify_submission():
    print("🔍 HHGOA Submission Verification\n")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. Check cases folder exists
    print("\n1. Checking cases/ folder...")
    if not os.path.exists("cases"):
        errors.append("❌ cases/ folder not found at repository root")
        print("   ❌ cases/ folder NOT FOUND")
    else:
        print("   ✅ cases/ folder exists")
        
        # 2. Check all 20 files
        print("\n2. Checking case files...")
        expected_files = [f"HHG-{i:03d}.json" for i in range(1, 21)]
        found_files = sorted([f for f in os.listdir("cases") if f.endswith(".json")])
        
        if found_files != expected_files:
            errors.append(f"❌ Expected files: {expected_files}")
            errors.append(f"   Found files: {found_files}")
            print(f"   ❌ File mismatch!")
            print(f"      Expected: {len(expected_files)} files")
            print(f"      Found: {len(found_files)} files")
        else:
            print(f"   ✅ All 20 files present")
            
            # 3. Validate JSON structure
            print("\n3. Validating JSON structure...")
            required_fields = [
                "case_id",
                "investigation_summary",
                "key_findings",
                "evidence",
                "recommendations"
            ]
            
            invalid_files = []
            for filename in found_files:
                filepath = os.path.join("cases", filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Check required fields
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        invalid_files.append(f"{filename}: missing {missing_fields}")
                    
                    # Check case_id matches filename
                    expected_id = filename.replace('.json', '')
                    if data.get('case_id') != expected_id:
                        invalid_files.append(f"{filename}: case_id mismatch (expected {expected_id}, got {data.get('case_id')})")
                        
                except json.JSONDecodeError:
                    invalid_files.append(f"{filename}: invalid JSON")
                except Exception as e:
                    invalid_files.append(f"{filename}: {str(e)}")
            
            if invalid_files:
                errors.extend([f"   ❌ {err}" for err in invalid_files])
                print(f"   ❌ {len(invalid_files)} files have issues")
            else:
                print("   ✅ All JSON files are valid")
    
    # 4. Check README exists
    print("\n4. Checking README.md...")
    if not os.path.exists("README.md"):
        warnings.append("⚠️  README.md not found")
        print("   ⚠️  README.md not found")
    else:
        print("   ✅ README.md exists")
    
    # 5. Check .gitignore
    print("\n5. Checking .gitignore...")
    if not os.path.exists(".gitignore"):
        warnings.append("⚠️  .gitignore not found")
        print("   ⚠️  .gitignore not found")
    else:
        with open(".gitignore", 'r') as f:
            gitignore_content = f.read()
        if ".env" not in gitignore_content:
            errors.append("❌ .env not in .gitignore (risk of committing secrets)")
            print("   ❌ .env not in .gitignore")
        else:
            print("   ✅ .gitignore properly configured")
    
    # 6. Check for .env file (should NOT be committed)
    print("\n6. Checking for secrets...")
    if os.path.exists(".env"):
        warnings.append("⚠️  .env file found - make sure it's in .gitignore!")
        print("   ⚠️  .env file found - verify it's in .gitignore")
    else:
        print("   ✅ No .env file in repo (good!)")
    
    # 7. Check requirements.txt
    print("\n7. Checking requirements.txt...")
    if not os.path.exists("requirements.txt"):
        warnings.append("⚠️  requirements.txt not found")
        print("   ⚠️  requirements.txt not found")
    else:
        print("   ✅ requirements.txt exists")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if not errors and not warnings:
        print("\n🎉 ALL CHECKS PASSED! You're ready to submit!")
        print("\n✅ Next steps:")
        print("   1. Push to GitHub: git push origin main")
        print("   2. Make repository PUBLIC")
        print("   3. Record demo video (3-5 min)")
        print("   4. Post on social media")
        print("   5. Write technical blog")
        print("   6. Submit form")
        return True
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for warning in warnings:
            print(f"   {warning}")
    
    if errors:
        print(f"\n❌ {len(errors)} ERROR(S) - MUST FIX BEFORE SUBMITTING:")
        for error in errors:
            print(f"   {error}")
        print("\n❌ Fix these errors and run this script again")
        return False
    else:
        print("\n✅ No critical errors. You can submit!")
        return True

if __name__ == "__main__":
    success = verify_submission()
    exit(0 if success else 1)
