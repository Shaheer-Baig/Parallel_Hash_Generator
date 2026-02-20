# GUI Usage Guide

## Starting the GUI

Simply run the Python script:

```bash
python hash_generator_gui.py
```

No additional dependencies needed - tkinter comes built-in with Python!

## Using the Application

### 1. Select Directory
- Click the **"Browse..."** button
- Navigate to the folder containing files you want to hash
- Select the folder and click "Select Folder"

### 2. Choose Hash Algorithm
- **SHA-256** (recommended): More secure, industry standard
- **MD5**: Faster, but less secure (legacy systems)

### 3. Start Processing
- Click **"▶ Start Hashing"**
- Watch the progress bar and log messages
- Processing happens in the background, GUI stays responsive

### 4. View Results
- Click **"📄 Open Results"** when complete
- Results are saved to `hash_results_<algorithm>_gui.txt`
- File contains hash values and file paths

## Features

✅ **User-Friendly Interface**
- Simple, clean design
- No command-line knowledge needed
- Visual feedback with progress bar

✅ **Real-Time Progress**
- Progress bar shows completion percentage
- Status updates show current file count
- Timestamped log messages

✅ **Multi-Threaded**
- Hashing runs in background thread
- GUI remains responsive during processing
- Can stop processing at any time

✅ **Error Handling**
- Gracefully handles locked/inaccessible files
- Shows error messages in log
- Continues processing remaining files

## Keyboard Shortcuts

- **Ctrl+C**: Copy selected text from log
- **Ctrl+A**: Select all text in log

## Tips

💡 **Large Directories**: For directories with 1000+ files, processing may take several minutes. The progress bar will keep you updated.

💡 **Stop Processing**: Click the "⏹ Stop" button if you need to interrupt the process.

💡 **Results Location**: Results are saved in the same folder as the GUI script.

## Example Workflow

1. Launch: `python hash_generator_gui.py`
2. Click "Browse..." and select `C:\Users\YourName\Documents`
3. Keep SHA-256 selected (default)
4. Click "▶ Start Hashing"
5. Wait for completion (see progress bar)
6. Click "📄 Open Results" to view the hash file
7. Use the hash file for integrity verification

## Troubleshooting

**GUI doesn't start:**
- Make sure Python is installed: `python --version`
- tkinter should be included with Python by default

**"Permission Denied" errors:**
- Some system folders require administrator privileges
- Try selecting a folder you own (like Documents)

**GUI freezes:**
- This shouldn't happen (multi-threaded design)
- If it does, close and restart the application
