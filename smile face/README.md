# Smile Face Frontend

A Flask-based web frontend for smile detection using OpenCV Haar cascades. Upload images or use live webcam to detect smiles and earn points!

## Features

- **Upload Mode**: Analyze static images for smile detection
- **Live Camera Mode**: Real-time smile detection via webcam (5 fps)
- **Score Tracking**: Persistent score stored in `smile_score.txt`
- **Annotated Output**: Visual feedback with boxes and text overlays
- **Responsive Design**: Dark theme, works on desktop and mobile

## Prerequisites

- Python 3.7+
- Webcam (for live camera mode)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Setup

1. **Install dependencies**:
   ```powershell
   python -m pip install -r requirements.txt
   ```

2. **Run the Flask app**:
   ```powershell
   python "c:\Users\meyas\OneDrive\Desktop\smile face\webapp\app.py"
   ```

3. **Open in browser**:
   - Navigate to `http://localhost:5000`

## Usage

### Upload Mode
1. Go to the home page
2. Select an image file (JPEG or PNG)
3. Click **Analyze**
4. View the annotated result with smile detection overlay
5. If a smile was detected, +10 points are added to your score

### Live Camera Mode
1. Click **🎥 Use Live Camera** on the home page
2. Allow browser camera access when prompted
3. Camera starts capturing frames automatically (5 fps)
4. Each frame with a detected smile earns +0.5 points
5. Click **Stop** to end the session
6. Your score is saved automatically

### Reset Score
- Click **Reset saved score** on the home page to set score back to 0

## Project Structure

```
smile face/
├── webapp/
│   ├── app.py                   # Flask application
│   ├── templates/
│   │   ├── index.html          # Home page (upload & camera link)
│   │   ├── result.html         # Upload result page
│   │   └── camera.html         # Live camera page
│   └── static/
│       └── style.css            # Styling
├── lab7up.py                    # Original webcam/desktop app (optional)
├── extract.py                   # Utility script (optional)
├── requirements.txt             # Python dependencies
├── smile_score.txt              # Persisted score file
└── README.md                    # This file
```

## How It Works

1. **Image Upload**: 
   - User selects a file
   - Flask decodes and processes it with OpenCV
   - Haar cascade detects faces and smiles
   - Annotated image is returned with overlay

2. **Live Camera**:
   - Browser captures frames via `getUserMedia` API
   - Frames are base64-encoded and sent to `/process-frame` endpoint
   - Backend runs detection and returns JSON with result
   - Browser displays annotated frame and score in real-time

3. **Scoring**:
   - Upload with smile: +10 points (one-time per upload)
   - Live camera with smile: +0.5 points per frame (~0.5 sec interval)
   - Score persists across sessions in `smile_score.txt`

## API Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page (upload & camera link) |
| `/camera` | GET | Live camera page |
| `/analyze` | POST | Upload image for analysis |
| `/process-frame` | POST | Process single frame (live camera) |
| `/score` | GET | JSON endpoint returning current score |
| `/reset` | POST | Reset score to 0 |

## Troubleshooting

### Camera not starting
- Check browser permissions (allow camera access)
- Ensure you're on HTTPS or localhost
- Try a different browser

### No smile detection
- Ensure good lighting
- Face should be clearly visible
- Smile should be prominent for detection

### Score not updating
- Check that `smile_score.txt` is writable in the project root
- Refresh page to see updated score

## Original Desktop App

The original `lab7up.py` provides continuous webcam monitoring with keyboard control (press 'q' to quit). The Flask frontend offers a web-based alternative with both upload and live camera modes.

## License

Educational project.
