# Gaze Tracker Module - The core vision system
# Handles 1-Euro smoothing and MediaPipe Face Landmarks
# Took me forever to get the padding math right lol - Prasu

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import pyautogui
import time
from core.filters import OneEuroFilter

pyautogui.FAILSAFE = False
SCREEN_W, SCREEN_H = pyautogui.size()

class GazeTracker:
    def __init__(self, model_path='face_landmarker.task'):
        self.cap = cv2.VideoCapture(0)
        
        # 1 Euro Filters for butter smooth X and Y movement 
        # (Beta too high causes "drag", forcing neck movement. Beta=0.005 is a sweet spot)
        t = time.time()
        self.filter_x = OneEuroFilter(t, SCREEN_W / 2, min_cutoff=0.005, beta=0.005)
        self.filter_y = OneEuroFilter(t, SCREEN_H / 2, min_cutoff=0.005, beta=0.005)
        
        # Blink detection parameters
        self.last_blink_time = 0
        self.blink_cooldown = 1.0  # Seconds between blinks
        self.ear_threshold = 0.015 

        # Default Calibration bounds
        self.x_min, self.x_max = 0.4, 0.6
        self.y_min, self.y_max = 0.4, 0.6

        # Setup MediaPipe
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def set_calibration_bounds(self, points):
        """Sets the screen bounds based on user's calibrated eye range."""
        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]
        
        # Add padding (e.g. 20%) to the bounds so the mouse isn't hypersensitive
        raw_x_min, raw_x_max = min(x_vals), max(x_vals)
        raw_y_min, raw_y_max = min(y_vals), max(y_vals)
        
        x_range = max(raw_x_max - raw_x_min, 0.02)
        y_range = max(raw_y_max - raw_y_min, 0.02)
        
        # Negative padding makes it EASIER to reach the edges of the screen.
        # -0.2 means the user only needs to move their eyes 80% of the way to reach the edge.
        # This completely eliminates neck strain!
        padding = -0.2 
        
        self.x_min = raw_x_min - (x_range * padding)
        self.x_max = raw_x_max + (x_range * padding)
        self.y_min = raw_y_min - (y_range * padding)
        self.y_max = raw_y_max + (y_range * padding)
        
        print(f"Calibrated Bounds (Padded): X({self.x_min:.3f}-{self.x_max:.3f}), Y({self.y_min:.3f}-{self.y_max:.3f})")

    def calculate_ear(self, landmarks):
        try:
            left_top = np.array([landmarks[159].x, landmarks[159].y])
            left_bottom = np.array([landmarks[145].x, landmarks[145].y])
            right_top = np.array([landmarks[386].x, landmarks[386].y])
            right_bottom = np.array([landmarks[374].x, landmarks[374].y])
            
            left_ear = np.linalg.norm(left_top - left_bottom)
            right_ear = np.linalg.norm(right_top - right_bottom)
            
            return (left_ear + right_ear) / 2.0
        except IndexError:
            return 1.0 

    def get_iris_center(self, landmarks):
        try:
            left_iris = landmarks[468]
            right_iris = landmarks[473]
            avg_x = (left_iris.x + right_iris.x) / 2.0
            avg_y = (left_iris.y + right_iris.y) / 2.0
            return avg_x, avg_y
        except IndexError:
            return None, None

    def get_head_pose(self, transformation_matrix):
        """Extracts Pitch, Yaw, Roll from the 4x4 transformation matrix."""
        R = transformation_matrix[:3, :3]
        sy = np.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
        singular = sy < 1e-6
        if not singular:
            pitch = np.arctan2(R[2,1], R[2,2]) 
            yaw = np.arctan2(-R[2,0], sy)    
            roll = np.arctan2(R[1,0], R[0,0]) 
        else:
            pitch = np.arctan2(-R[1,2], R[1,1])
            yaw = np.arctan2(-R[2,0], sy)
            roll = 0
        return pitch, yaw, roll

    def map_to_screen(self, x, y):
        # Normalize within bounds
        norm_x = (x - self.x_min) / (self.x_max - self.x_min + 1e-6)
        norm_y = (y - self.y_min) / (self.y_max - self.y_min + 1e-6)
        
        # Clamp between 0 and 1
        norm_x = max(0.0, min(1.0, norm_x))
        norm_y = max(0.0, min(1.0, norm_y))
        
        # Invert X because camera is mirrored
        screen_x = (1.0 - norm_x) * SCREEN_W
        screen_y = norm_y * SCREEN_H
        
        return screen_x, screen_y

    def process_frame(self, calibrate_mode=False):
        success, image = self.cap.read()
        if not success:
            return None, False, False, None

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        detection_result = self.detector.detect(mp_image)
        
        click_triggered = False
        raw_iris = None
        
        if detection_result.face_landmarks:
            landmarks = detection_result.face_landmarks[0]
            
            # 1. Blink Detection
            ear = self.calculate_ear(landmarks)
            if ear < self.ear_threshold:
                if time.time() - self.last_blink_time > self.blink_cooldown:
                    click_triggered = True
                    self.last_blink_time = time.time()
                    
            # 2. Face Gestures (Blendshapes)
            jaw_open = False
            brow_raised = False
            mouth_funnel = False
            pain_face = False
            
            if detection_result.face_blendshapes:
                blendshapes = detection_result.face_blendshapes[0]
                
                # Dictionary to hold scores for easy lookup
                scores = {shape.category_name: shape.score for shape in blendshapes}
                
                if scores.get('jawOpen', 0) > 0.4:
                    jaw_open = True
                if scores.get('browInnerUp', 0) > 0.5:
                    brow_raised = True
                if scores.get('mouthFunnel', 0) > 0.5:
                    mouth_funnel = True
                    
                # Silent Pain Detection: Furrowed brows (browDown) + Squinting
                if (scores.get('browDownLeft', 0) > 0.5 and 
                    scores.get('browDownRight', 0) > 0.5 and 
                    scores.get('eyeSquintLeft', 0) > 0.4):
                    pain_face = True

            # 3. Head Pose & Gaze Tracking
            pitch, yaw, roll = 0, 0, 0
            if detection_result.facial_transformation_matrixes:
                matrix = detection_result.facial_transformation_matrixes[0]
                pitch, yaw, roll = self.get_head_pose(matrix)

            iris_x, iris_y = self.get_iris_center(landmarks)
            
            if iris_x is not None:
                # Adjust iris position to compensate for head rotation
                # This scaling factor (0.05) is experimental
                adjusted_x = iris_x + (yaw * 0.05)
                adjusted_y = iris_y - (pitch * 0.05)
                
                raw_iris = (adjusted_x, adjusted_y)

                if not calibrate_mode:
                    raw_screen_x, raw_screen_y = self.map_to_screen(adjusted_x, adjusted_y)
                    
                    # Apply 1 Euro Filter
                    t = time.time()
                    smooth_x = self.filter_x(t, raw_screen_x)
                    smooth_y = self.filter_y(t, raw_screen_y)
                    
                    pyautogui.moveTo(smooth_x, smooth_y)
                    
                # Draw for debug
                cx = int(iris_x * image.shape[1])
                cy = int(iris_y * image.shape[0])
                cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)

        # Return gesture state dict along with other flags
        if 'jaw_open' in locals():
            gestures = {
                'jaw_open': jaw_open, 
                'brow_raised': brow_raised, 
                'mouth_funnel': mouth_funnel,
                'pain_face': pain_face
            }
        else:
            gestures = {'jaw_open': False, 'brow_raised': False, 'mouth_funnel': False, 'pain_face': False}
            
        return image, click_triggered, True, raw_iris, gestures

    def cleanup(self):
        self.cap.release()
