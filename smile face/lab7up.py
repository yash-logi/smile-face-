import cv2
import time
import os

# Load Haar cascade classifiers for face and smile detection (optimized parameters)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# === Load previously saved smile score (if file exists) ===
score_file = "smile_score.txt"
if os.path.exists(score_file):
    with open(score_file, "r") as f:
        try:
            smile_score = float(f.read().strip())
        except:
            smile_score = 0
else:
    smile_score = 0

# Variables for tracking smile score
smiling_start_time = None
reward_100 = False
reward_1000 = False
last_save_time = time.time()

print(f"Smile Score Tracker Started! Current Score: {int(smile_score)}")
print("Smile to earn points quickly! Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Reduce frame size for faster processing
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces with faster settings
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(100, 100))
    smiling = False

    for (x, y, w, h) in faces:
        roi_gray = gray[y + int(h/3):y + h, x:x + w]  # detect in lower 2/3 of face
        roi_color = frame[y + int(h/3):y + h, x:x + w]

        # Faster smile detection (less sensitivity but better real-time)
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.4, minNeighbors=20, minSize=(25, 25))

        if len(smiles) > 0:
            smiling = True
            cv2.putText(frame, "😊 Smiling!", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 255, 0), 2)
        else:
            cv2.putText(frame, "😐 Not Smiling", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Track smile score (faster growth)
    current_time = time.time()
    if smiling:
        if smiling_start_time is None:
            smiling_start_time = current_time
        else:
            elapsed = current_time - smiling_start_time
            smile_score += elapsed * 25  # 🚀 score multiplier (increase speed here)
            smiling_start_time = current_time
    else:
        smiling_start_time = None

    # Save progress every few seconds
    if time.time() - last_save_time > 3:
        with open(score_file, "w") as f:
            f.write(str(smile_score))
        last_save_time = time.time()

    # ✅ Rewards (every 100 and then every 500)
    milestones = []
    messages = []

    # Every 100 up to 1000
    for i in range(100, 1001, 100):
        milestones.append(i)
        messages.append(f"🎉 Great job! You've reached {i} points!")

    # Every 500 after 1000
    for i in range(1500, 1000001, 500):
        milestones.append(i)
        messages.append(f"🔥 Awesome! You've hit {i} points!")

    for i, milestone in enumerate(milestones):
        key = f"reward_{milestone}"
        if smile_score >= milestone and not globals().get(key, False):
            print(messages[i])
            globals()[key] = True

    # Display smile score as integer
    cv2.putText(frame, f"Smile Score: {int(smile_score)}",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow('Smile Score Tracker 😊', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save final score on exit
with open(score_file, "w") as f:
    f.write(str(smile_score))

cap.release()
cv2.destroyAllWindows()

print(f"Session ended. Final Smile Score: {int(smile_score)}")
print("✅ Progress saved successfully!")
