import subprocess
import sys
import os

def main():
    # Ensure Streamlit is run from the correct directory
    script_path = os.path.join(os.path.dirname(__file__), "app.py")
    
    try:
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])
    except Exception as e:
        print("Error launching Streamlit app:", e)
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
