**Poshmark Lister Readme**

---

## Overview

The PoshmarkLister script automates the process of listing items on Poshmark, a popular online marketplace. The script reads item information from a CSV file, logs into a Poshmark account, and creates individual listings for each item.

## Prerequisites

1. **Python:** Ensure that Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

   ```bash
   # Verify Python installation
   python --version
   ```

2. **Git Bash:** Install Git Bash to run the script on a Windows environment. Download it from [gitforwindows.org](https://gitforwindows.org/).

3. **Create Virtual Environment (Optional):** It's recommended to use a virtual environment to manage dependencies.

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   source venv/bin/activate  # On Linux/Mac
   .\venv\Scripts\activate   # On Windows
   ```

4. **Dependencies:** Install the dependencies

   ```bash
   # Install dependencies
   pip install -r requirements.txt
   ```

5. **Chrome Browser:** The script uses the Chrome browser. Ensure it is installed on your machine.

6. **ChromeDriver:** Download the appropriate ChromeDriver version from [here](https://sites.google.com/chromium.org/driver/) and place it in your system's PATH.

## Usage

1. **CSV File:** Prepare a CSV file containing item details, following the structure specified in the script's constants.

2. **Photo Storage:**
   - Create a folder named `photos` in the script directory.
   - Store images for each product in a subfolder named after the product within the `photos` folder.

3. **Run Script:**

   ```bash
   # Navigate to script directory
   cd /path/to/poshmark_lister
   
   # Run the script
   python poshmark_lister.py
   ```

   Make sure to update the `LISTING_PATH`, `ALLOW_MANUAL_PHOTO_ADJUST`, and `AUTO_RUN` variables in the script according to your needs.

4. **Execution:**

   - The script will log into your Poshmark account.
   - It reads the CSV file to gather item details.
   - For each item, it creates a listing with the provided information, including photos.
   - The script then marks the listing status as "TRUE" in the CSV file to track completed items.

5. **Review Before Uploading:**
   - To review each product before uploading, set the `AUTO_RUN` variable to `True`.
   - The script will pause before the final submission, allowing you to review each listing.

## Script Customization

- **CSV Structure:** Adjust the script constants if your CSV structure differs.

- **Execution Flow:**
  - Toggle `ALLOW_MANUAL_PHOTO_ADJUST` if you want manual adjustments during photo upload.
  - Toggle `AUTO_RUN` to allow the script to proceed without user input.

## Important Notes

- The script relies on XPATHs, which might be subject to changes in Poshmark's website structure. If the script fails, consider checking and updating the XPATHs accordingly.

- Be cautious about listing items on Poshmark, as violating their terms of service may lead to account suspension.

## License

This script is provided under the [MIT License](LICENSE). Use it responsibly and at your own risk.
