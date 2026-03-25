"""Complete setup: Create final_model.h5 and run analysis"""
import os
import shutil

# Step 1: Create final_model.h5
print("="*60)
print("STEP 1: Creating final_model.h5")
print("="*60)

src = 'models/best_model.h5'
dst = 'models/final_model.h5'

if os.path.exists(src):
    shutil.copy2(src, dst)
    if os.path.exists(dst):
        size = os.path.getsize(dst) / (1024*1024)  # Size in MB
        print(f"✅ Created final_model.h5 ({size:.2f} MB)")
    else:
        print("❌ Failed to create final_model.h5")
else:
    print(f"❌ Source file not found: {src}")

# Step 2: Run final analysis
print("\n" + "="*60)
print("STEP 2: Running Final Analysis")
print("="*60)

if os.path.exists(dst):
    print("Running generate_final_analysis.py...")
    exec(open('scripts/generate_final_analysis.py').read())
else:
    print("⚠️  Skipping analysis - final_model.h5 not found")

print("\n" + "="*60)
print("SETUP COMPLETE!")
print("="*60)

