# ============================================================
# AI GYM — PREMIUM STREAMLIT APP
# Real-Time AI Computer Vision Personal Trainer
# ============================================================

import html
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime

import cv2
import streamlit as st
import mediapipe as mp

from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

from exercises.exercise_manager import ExerciseManager
from recognition.exercise_detector import ExerciseDetector
from recognition.exercise_stabilizer import ExerciseStabilizer


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI GYM — Intelligent Fitness",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML HELPER
# IMPORTANT:
# We use st.html() instead of st.markdown(... unsafe_allow_html=True)
# so custom HTML is never displayed as raw code.
# ============================================================

def ui_html(content: str):
    st.html(content)


# ============================================================
# PREMIUM CSS
# ============================================================

ui_html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #05070d;
    --bg-soft: #080c16;
    --panel: #0b1120;
    --panel-2: #10182a;
    --border: rgba(148, 163, 184, .12);
    --purple: #8b5cf6;
    --purple-light: #a78bfa;
    --blue: #38bdf8;
    --cyan: #22d3ee;
    --green: #22c55e;
    --green-light: #4ade80;
    --yellow: #facc15;
    --red: #fb7185;
    --white: #f8fafc;
    --muted: #94a3b8;
    --muted-2: #64748b;
}

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(124,58,237,.16), transparent 28%),
        radial-gradient(circle at 90% 8%, rgba(14,165,233,.12), transparent 26%),
        radial-gradient(circle at 50% 100%, rgba(168,85,247,.08), transparent 35%),
        var(--bg);
    color: var(--white);
}

.block-container {
    max-width: 1750px;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(8,11,20,.99), rgba(4,6,12,.99));
    border-right: 1px solid rgba(139,92,246,.18);
}

.brand {
    padding: 12px 8px 25px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 48px;
    height: 48px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    background: linear-gradient(135deg, rgba(139,92,246,.30), rgba(56,189,248,.18));
    border: 1px solid rgba(139,92,246,.42);
    box-shadow: 0 0 28px rgba(139,92,246,.20);
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -.8px;
}

.brand-subtitle {
    margin-top: 3px;
    color: #7dd3fc;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.7px;
}

.nav-title {
    margin: 12px 5px 9px;
    color: var(--muted-2);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

div.stButton > button {
    border-radius: 13px;
    border: 1px solid rgba(148,163,184,.10);
    background: transparent;
    color: #cbd5e1;
    font-weight: 650;
    min-height: 42px;
    transition: .2s ease;
}

div.stButton > button:hover {
    border-color: rgba(139,92,246,.48);
    color: white;
    background: rgba(139,92,246,.09);
    transform: translateY(-1px);
}

.sidebar-promo {
    margin-top: 25px;
    padding: 19px;
    border-radius: 20px;
    background:
        radial-gradient(circle at 90% 10%, rgba(139,92,246,.28), transparent 42%),
        linear-gradient(145deg, rgba(21,17,46,.96), rgba(8,11,22,.96));
    border: 1px solid rgba(139,92,246,.27);
    box-shadow: 0 18px 50px rgba(0,0,0,.30);
}

.sidebar-promo-title {
    font-size: 17px;
    font-weight: 800;
}

.sidebar-promo-text {
    margin-top: 8px;
    color: var(--muted);
    font-size: 11px;
    line-height: 1.65;
}

.system-status {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 20px 5px 0;
    color: var(--muted);
    font-size: 11px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 12px var(--green);
}

/* ---------------- TOP BAR ---------------- */

.topbar {
    min-height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
    gap: 20px;
}

.search-box {
    min-width: 300px;
    max-width: 450px;
    padding: 12px 17px;
    border-radius: 14px;
    background: rgba(10,17,31,.80);
    border: 1px solid rgba(56,189,248,.16);
    color: #64748b;
    font-size: 12px;
}

.user-area {
    display: flex;
    align-items: center;
    gap: 13px;
}

.date-text {
    text-align: right;
    color: var(--muted);
    font-size: 10px;
    line-height: 1.55;
}

.notification,
.avatar {
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
}

.notification {
    background: rgba(15,23,42,.8);
    border: 1px solid rgba(148,163,184,.12);
    font-size: 17px;
}

.avatar {
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(139,92,246,.46), rgba(37,99,235,.42));
    border: 1px solid rgba(139,92,246,.58);
    font-weight: 800;
}

/* ---------------- HERO ---------------- */

.hero {
    position: relative;
    overflow: hidden;
    padding: 29px;
    border-radius: 25px;
    background:
        radial-gradient(circle at 82% 0%, rgba(37,99,235,.21), transparent 34%),
        radial-gradient(circle at 18% 100%, rgba(139,92,246,.17), transparent 36%),
        linear-gradient(135deg, rgba(9,16,31,.97), rgba(7,10,20,.95));
    border: 1px solid rgba(56,189,248,.16);
    box-shadow: 0 20px 70px rgba(0,0,0,.25);
}

.hero:after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -90px;
    top: -110px;
    border-radius: 50%;
    background: rgba(139,92,246,.16);
    filter: blur(75px);
}

.hero-label {
    color: var(--purple-light);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.hero-title {
    font-size: 40px;
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -1.7px;
}

.hero-title span {
    background: linear-gradient(90deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 9px;
    color: var(--muted);
    font-size: 13px;
    max-width: 800px;
}

.feature-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 21px;
}

.feature-pill {
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(15,23,42,.65);
    border: 1px solid rgba(148,163,184,.12);
    color: #cbd5e1;
    font-size: 10px;
}

/* ---------------- COMMON ---------------- */

.section-title {
    margin: 25px 0 11px;
    color: #cbd5e1;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.card,
.control-card,
.coach-card,
.rep-panel,
.score-panel,
.metric-card,
.tip-card {
    border-radius: 20px;
}

.card {
    padding: 19px;
    background: linear-gradient(145deg, rgba(17,24,39,.84), rgba(8,12,23,.82));
    border: 1px solid rgba(148,163,184,.10);
    box-shadow: 0 15px 50px rgba(0,0,0,.20);
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 14px;
}

.card-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: .25px;
}

.live-badge,
.coach-status {
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 9px;
    font-weight: 800;
}

.live-badge {
    background: rgba(34,197,94,.08);
    border: 1px solid rgba(34,197,94,.20);
    color: var(--green-light);
}

.live-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 5px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 10px var(--green);
}

/* ---------------- CAMERA ---------------- */

.camera-shell {
    padding: 5px;
    border-radius: 21px;
    background: linear-gradient(135deg, rgba(34,211,238,.42), rgba(139,92,246,.38), rgba(34,197,94,.18));
    box-shadow: 0 0 60px rgba(56,189,248,.07);
}

.camera-note {
    margin-top: 8px;
    color: var(--muted-2);
    font-size: 9px;
    text-align: center;
}

/* ---------------- METRICS ---------------- */

.rep-panel {
    min-height: 174px;
    padding: 18px;
    text-align: center;
    background: linear-gradient(145deg, rgba(12,18,34,.94), rgba(7,10,18,.92));
    border: 1px solid rgba(139,92,246,.16);
}

.rep-label {
    color: var(--muted);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.4px;
}

.rep-number {
    margin-top: 25px;
    font-size: 47px;
    line-height: 1;
    font-weight: 800;
    background: linear-gradient(135deg, white, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.rep-target {
    margin-top: 5px;
    color: var(--muted-2);
    font-size: 10px;
}

.score-panel {
    min-height: 174px;
    padding: 18px;
    text-align: center;
    background: linear-gradient(145deg, rgba(8,25,26,.94), rgba(7,12,20,.92));
    border: 1px solid rgba(34,197,94,.15);
}

.score-number {
    margin-top: 24px;
    color: var(--green-light);
    font-size: 41px;
    line-height: 1;
    font-weight: 800;
    text-shadow: 0 0 30px rgba(34,197,94,.22);
}

.score-status {
    margin-top: 10px;
    color: var(--green-light);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
}

.metric-card {
    position: relative;
    overflow: hidden;
    min-height: 132px;
    padding: 19px;
    background: linear-gradient(145deg, rgba(13,20,37,.90), rgba(7,10,18,.90));
    border: 1px solid rgba(148,163,184,.10);
}

.metric-card:after {
    content: "";
    position: absolute;
    width: 110px;
    height: 110px;
    right: -42px;
    bottom: -52px;
    border-radius: 50%;
    background: rgba(139,92,246,.10);
    filter: blur(25px);
}

.metric-icon {
    font-size: 21px;
}

.metric-label {
    margin-top: 12px;
    color: var(--muted-2);
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1px;
}

.metric-value {
    margin-top: 4px;
    font-size: 25px;
    font-weight: 800;
}

.metric-unit {
    color: var(--muted-2);
    font-size: 10px;
}

/* ---------------- CONTROL ---------------- */

.control-card {
    padding: 20px;
    background: linear-gradient(145deg, rgba(13,21,38,.96), rgba(7,10,18,.94));
    border: 1px solid rgba(56,189,248,.14);
    box-shadow: 0 20px 60px rgba(0,0,0,.22);
}

.control-title {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 16px;
    font-size: 12px;
    font-weight: 800;
}

.control-title-icon {
    color: var(--purple-light);
    font-size: 17px;
}

/* ---------------- COACH ---------------- */

.coach-card {
    position: relative;
    min-height: 155px;
    padding: 20px;
    background:
        radial-gradient(circle at 0% 100%, rgba(139,92,246,.17), transparent 36%),
        linear-gradient(145deg, rgba(23,18,50,.94), rgba(8,11,22,.94));
    border: 1px solid rgba(139,92,246,.24);
    box-shadow: 0 15px 50px rgba(0,0,0,.24);
}

.coach-status {
    position: absolute;
    right: 16px;
    top: 16px;
    color: #67e8f9;
    background: rgba(34,211,238,.07);
    border: 1px solid rgba(34,211,238,.20);
}

.coach-row {
    display: flex;
    align-items: center;
    gap: 13px;
}

.coach-avatar {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(139,92,246,.38), rgba(37,99,235,.25));
    border: 1px solid rgba(139,92,246,.35);
    font-size: 22px;
}

.coach-caption {
    margin-top: 3px;
    color: var(--muted-2);
    font-size: 9px;
}

.coach-text {
    margin-top: 13px;
    color: #e2e8f0;
    font-size: 12px;
    line-height: 1.65;
}

/* ---------------- PROGRESS ---------------- */

.progress-track {
    height: 8px;
    overflow: hidden;
    border-radius: 999px;
    background: rgba(30,41,59,.80);
}

.progress-fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #8b5cf6, #38bdf8);
    box-shadow: 0 0 18px rgba(139,92,246,.42);
}

.rep-dots {
    margin-top: 13px;
    text-align: center;
    line-height: 1.9;
}

.rep-dot {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    margin: 3px;
    border-radius: 50%;
    font-size: 8px;
    font-weight: 700;
}

.rep-dot.done {
    color: #4ade80;
    background: rgba(34,197,94,.15);
    border: 1px solid rgba(34,197,94,.45);
}

.rep-dot.pending {
    color: #64748b;
    background: rgba(30,41,59,.45);
    border: 1px solid rgba(148,163,184,.10);
}

/* ---------------- TIPS ---------------- */

.tip-card {
    padding: 19px;
    background:
        radial-gradient(circle at 100% 0%, rgba(139,92,246,.16), transparent 40%),
        rgba(12,16,28,.90);
    border: 1px solid rgba(139,92,246,.13);
}

.tip {
    padding: 8px 0;
    color: #cbd5e1;
    font-size: 10px;
    border-bottom: 1px solid rgba(148,163,184,.06);
}

.tip:last-child {
    border-bottom: none;
}

/* ---------------- INPUTS ---------------- */

div[data-baseweb="select"] > div {
    background: rgba(30,35,50,.90) !important;
    border-color: rgba(148,163,184,.12) !important;
    border-radius: 12px !important;
}

div[data-testid="stNumberInput"] input {
    background: rgba(30,35,50,.90) !important;
    color: white !important;
    border-radius: 12px !important;
}

.stButton button[kind="primary"] {
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    border: 1px solid rgba(167,139,250,.50);
    color: white;
    box-shadow: 0 10px 30px rgba(124,58,237,.25);
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(90deg, #8b5cf6, #3b82f6);
    box-shadow: 0 12px 40px rgba(124,58,237,.38);
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* ---------------- MOBILE ---------------- */

@media (max-width: 900px) {
    .hero-title {
        font-size: 30px;
    }

    .topbar {
        flex-direction: column;
        align-items: stretch;
    }

    .search-box {
        max-width: none;
    }
}
</style>
"""
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "page": "Workout",
    "exercise": "Bicep Curl",
    "sets": 3,
    "target_reps": 10,
    "weight": 10.0,
    "workout_started": False,
    "start_time": None,
    "voice_enabled": True,
    "pose_enabled": True,
    "form_enabled": True,
    "recognition_enabled": True,
    "show_skeleton": True,
    "show_confidence": True,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# THREAD-SAFE AI STATE
# ============================================================

@dataclass
class AIState:
    lock: threading.Lock = field(default_factory=threading.Lock)

    exercise: str = "Unknown"
    reps: int = 0
    stage: str = "up"
    form_score: int = 0
    feedback: str = "Position yourself in front of the camera."
    confidence: int = 0
    set_number: int = 1
    calories: float = 0.0
    active: bool = False
    workout_enabled: bool = False
    last_rep_time: float = 0.0
    show_skeleton: bool = True

    def update(self, **kwargs):
        with self.lock:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def snapshot(self):
        with self.lock:
            return {
                "exercise": self.exercise,
                "reps": self.reps,
                "stage": self.stage,
                "form_score": self.form_score,
                "feedback": self.feedback,
                "confidence": self.confidence,
                "set_number": self.set_number,
                "calories": self.calories,
                "active": self.active,
                "workout_enabled": self.workout_enabled,
                "last_rep_time": self.last_rep_time,
                "show_skeleton": self.show_skeleton,
            }


@st.cache_resource
def get_ai_state():
    return AIState()


ai_state = get_ai_state()


# ============================================================
# AI ENGINE
# ============================================================

@st.cache_resource
def get_ai_engine():
    return ExerciseDetector(), ExerciseStabilizer(), ExerciseManager()


detector, stabilizer, exercise_manager = get_ai_engine()


# ============================================================
# RESET AI
# ============================================================

def reset_ai():
    detector.current_exercise = "Unknown"
    stabilizer.reset()
    exercise_manager.reset()

    ai_state.update(
        exercise="Unknown",
        reps=0,
        stage="up",
        form_score=0,
        feedback="Position yourself in front of the camera.",
        confidence=0,
        set_number=1,
        calories=0.0,
        active=False,
        workout_enabled=False,
    )


# ============================================================
# MEDIAPIPE PROCESSOR
# ============================================================

class AIWorkoutProcessor(VideoProcessorBase):

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.current_exercise = "Unknown"
        self.previous_reps = 0

    def draw_text(self, image, text, position, scale=0.6,
                  color=(235, 245, 255), thickness=2):
        cv2.putText(
            image,
            str(text),
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            color,
            thickness,
            cv2.LINE_AA,
        )

    def draw_hud(self, image, state):
        h, w = image.shape[:2]

        # AI active badge
        cv2.rectangle(
            image,
            (18, 18),
            (300, 70),
            (8, 15, 28),
            -1,
        )
        cv2.rectangle(
            image,
            (18, 18),
            (300, 70),
            (40, 200, 150),
            1,
        )
        cv2.circle(
            image,
            (40, 44),
            7,
            (40, 220, 120),
            -1,
        )
        self.draw_text(
            image,
            "AI VISION ACTIVE",
            (58, 51),
            0.60,
            (220, 240, 255),
            2,
        )

        # Exercise panel
        hud_x = max(20, w - 350)

        cv2.rectangle(
            image,
            (hud_x, 18),
            (w - 18, 150),
            (8, 15, 28),
            -1,
        )
        cv2.rectangle(
            image,
            (hud_x, 18),
            (w - 18, 150),
            (70, 120, 255),
            1,
        )

        self.draw_text(
            image,
            "EXERCISE DETECTED",
            (hud_x + 18, 45),
            0.44,
            (150, 170, 190),
            1,
        )

        exercise = state["exercise"]
        if exercise == "Unknown":
            exercise = self.current_exercise

        self.draw_text(
            image,
            exercise,
            (hud_x + 18, 82),
            0.70,
            (255, 255, 255),
            2,
        )

        self.draw_text(
            image,
            f"CONFIDENCE  {state['confidence']}%",
            (hud_x + 18, 116),
            0.43,
            (80, 220, 255),
            1,
        )

        self.draw_text(
            image,
            f"REPS  {state['reps']}",
            (hud_x + 18, 139),
            0.40,
            (130, 240, 160),
            1,
        )

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image = cv2.flip(image, 1)

        # Streamlit UI buttons and the WebRTC worker run in different
        # execution contexts. Use shared AI state as the real start/stop gate.
        state = ai_state.snapshot()
        if not state["workout_enabled"]:
            self.draw_text(
                image,
                "PRESS START TO BEGIN",
                (35, 90),
                0.75,
                (80, 220, 255),
                2,
            )
            return frame.from_ndarray(image, format="bgr24")

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if not results.pose_landmarks:
            ai_state.update(
                active=False,
                confidence=0,
                feedback="Move into the camera frame.",
            )

            self.draw_text(
                image,
                "NO PERSON DETECTED",
                (35, 90),
                0.75,
                (80, 190, 255),
                2,
            )

            return frame.from_ndarray(image, format="bgr24")

        landmarks = results.pose_landmarks.landmark

        # Skeleton
        if ai_state.snapshot()["show_skeleton"]:
            self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(
                    color=(80, 210, 255),
                    thickness=2,
                    circle_radius=3,
                ),
                self.mp_drawing.DrawingSpec(
                    color=(160, 80, 255),
                    thickness=2,
                    circle_radius=2,
                ),
            )

        # Detection
        detected = detector.detect(landmarks)
        stable = stabilizer.update(detected)

        if stable != "Unknown":

            if stable != self.current_exercise:
                self.current_exercise = stable
                exercise_manager.set_exercise(stable)

            result = exercise_manager.update(landmarks)

            reps = int(result.get("reps", 0))
            form_score = int(result.get("form_score", 0))
            stage = result.get("stage", "up")
            feedback = result.get("feedback", "Keep moving.")

            scores = detector.get_scores(landmarks)
            confidence = int(scores.get(stable, 0))

            # Simple local estimate for the demo.
            # The existing WorkoutSession remains responsible
            # for the real workout/session calorie calculation.
            calories = reps * 0.35

            rep_changed = reps > self.previous_reps
            now = time.time()

            ai_state.update(
                exercise=stable,
                reps=reps,
                stage=stage,
                form_score=form_score,
                feedback=feedback,
                confidence=confidence,
                calories=calories,
                active=True,
                last_rep_time=now if rep_changed else ai_state.snapshot()["last_rep_time"],
            )

            self.previous_reps = reps

        else:
            # Never replace a stable exercise with Unknown.
            ai_state.update(
                active=True,
                confidence=0,
            )

        self.draw_hud(image, ai_state.snapshot())

        return frame.from_ndarray(image, format="bgr24")


# ============================================================
# WEBRTC
# ============================================================

RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": ["stun:stun.l.google.com:19302"]
            }
        ]
    }
)


# ============================================================
# SMALL UI FUNCTIONS
# ============================================================

def render_topbar():
    now = datetime.now()

    ui_html(
        f"""
        <div class="topbar">
            <div class="search-box">
                🔍 &nbsp; Discipline today, stronger tomorrow.
            </div>

            <div class="user-area">
                <div class="date-text">
                    {now.strftime("%a, %d %b %Y")}<br>
                    <b style="color:#e2e8f0;">AI TRAINING MODE</b>
                </div>

                <div class="notification">🔔</div>
                <div class="avatar">G</div>
            </div>
        </div>
        """
    )


def render_hero(label, title, highlighted, subtitle, pills=None):
    pills_html = ""

    if pills:
        for pill in pills:
            pills_html += f'<div class="feature-pill">{pill}</div>'

    ui_html(
        f"""
        <div class="hero">
            <div class="hero-label">{label}</div>

            <div class="hero-title">
                {title} <span>{highlighted}</span>
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

            {f'<div class="feature-pills">{pills_html}</div>' if pills else ''}
        </div>
        """
    )


def render_metric(icon, label, value, unit=""):
    ui_html(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">
                {value}
                <span class="metric-unit">{unit}</span>
            </div>
        </div>
        """
    )


def render_rep_panel(state):
    ui_html(
        f"""
        <div class="rep-panel">
            <div class="rep-label">CURRENT REPS</div>
            <div class="rep-number">{int(state["reps"]):02d}</div>
            <div class="rep-target">/ {int(st.session_state.target_reps)}</div>
        </div>
        """
    )


def render_score_panel(state):
    score = max(0, min(100, int(state["form_score"])))

    if score >= 85:
        status = "EXCELLENT"
    elif score >= 70:
        status = "GOOD"
    elif score > 0:
        status = "IMPROVE"
    else:
        status = "WAITING"

    ui_html(
        f"""
        <div class="score-panel">
            <div class="rep-label">FORM SCORE</div>
            <div class="score-number">{score}%</div>
            <div class="score-status">{status}</div>
        </div>
        """
    )


def render_coach(state):
    feedback = str(state["feedback"] or "Start your movement and I'll analyze your form.")
    feedback = html.escape(feedback)

    ui_html(
        f"""
        <div class="coach-card">
            <div class="coach-status">● AI LISTENING</div>

            <div class="coach-row">
                <div class="coach-avatar">🤖</div>

                <div>
                    <div class="card-title">AI COACH</div>
                    <div class="coach-caption">
                        REAL-TIME FORM INTELLIGENCE
                    </div>
                </div>
            </div>

            <div class="coach-text">
                “{feedback}”
            </div>
        </div>
        """
    )


def render_progress(state):
    reps = max(0, int(state["reps"]))
    target = max(1, int(st.session_state.target_reps))
    progress = min(100, int(reps / target * 100))

    dots = ""
    # Do not render hundreds of circles if target is accidentally large.
    display_target = min(target, 50)

    for i in range(1, display_target + 1):
        cls = "done" if i <= reps else "pending"
        dots += f'<span class="rep-dot {cls}">{i}</span>'

    ui_html(
        f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">WORKOUT PROGRESS</div>
                <div style="color:#94a3b8;font-size:9px;">
                    SET {int(state["set_number"])} OF {int(st.session_state.sets)}
                </div>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:8px;
            ">
                <span style="color:#94a3b8;font-size:9px;">
                    {reps} / {target} reps
                </span>

                <span style="
                    color:#c4b5fd;
                    font-size:9px;
                    font-weight:700;
                ">
                    {progress}%
                </span>
            </div>

            <div class="progress-track">
                <div class="progress-fill" style="width:{progress}%"></div>
            </div>

            <div class="rep-dots">
                {dots}
            </div>
        </div>
        """
    )


def render_tips():
    ui_html(
        """
        <div class="tip-card">
            <div class="card-title">💡 WORKOUT INTELLIGENCE</div>

            <div class="tip">✓ &nbsp; Keep your core engaged</div>
            <div class="tip">✓ &nbsp; Maintain proper posture</div>
            <div class="tip">✓ &nbsp; Control every movement</div>
            <div class="tip">✓ &nbsp; Use your full range of motion</div>
        </div>
        """
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    ui_html(
        """
        <div class="brand">
            <div class="brand-row">
                <div class="brand-icon">🏋️</div>

                <div>
                    <div class="brand-name">AI GYM</div>
                    <div class="brand-subtitle">INTELLIGENT FITNESS</div>
                </div>
            </div>
        </div>

        <div class="nav-title">NAVIGATION</div>
        """
    )

    pages = [
        ("🏠  Workout", "Workout"),
        ("📊  Dashboard", "Dashboard"),
        ("💪  Exercises", "Exercises"),
        ("🧠  AI Coach", "Coach"),
        ("🕘  History", "History"),
        ("⚙️  Settings", "Settings"),
    ]

    for label, page_name in pages:
        if st.button(label, use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

    ui_html(
        """
        <div class="sidebar-promo">
            <div class="sidebar-promo-title">
                Train Smarter<br>With AI
            </div>

            <div class="sidebar-promo-text">
                Real-time computer vision, intelligent
                form analysis and personalized coaching.
            </div>
        </div>

        <div class="system-status">
            <span class="status-dot"></span>
            AI Systems Ready
        </div>
        """
    )


# ============================================================
# TOP BAR
# ============================================================

render_topbar()


# ============================================================
# WORKOUT PAGE
# ============================================================

if st.session_state.page == "Workout":

    render_hero(
        "REAL-TIME COMPUTER VISION",
        "AI",
        "Workout Studio",
        "Your intelligent personal trainer that sees, understands and improves every movement.",
        [
            "🟢 Live Pose Detection",
            "⚡ AI Form Analysis",
            "💬 Real-time Feedback",
            "📈 Performance Tracking",
        ],
    )

    ui_html('<div class="section-title">LIVE TRAINING</div>')

    left, middle, right = st.columns(
        [1.65, 0.82, 0.90],
        gap="medium",
    )

    # --------------------------------------------------------
    # CAMERA
    # --------------------------------------------------------

    with left:

        ui_html(
            """
            <div class="card">
                <div class="card-header">
                    <div class="card-title">
                        🎥 &nbsp; LIVE AI CAMERA
                    </div>

                    <div class="live-badge">
                        <span class="live-dot"></span>
                        AI VISION ACTIVE
                    </div>
                </div>

                <div class="camera-shell">
            """
        )

        # IMPORTANT:
        # Do not put the WebRTC component inside an HTML <div>.
        # Streamlit components must stay as their own Streamlit element.
        webrtc_streamer(
            key="ai-gym-camera",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={
                "video": {
                    "width": {"ideal": 1280},
                    "height": {"ideal": 720},
                    "facingMode": "user",
                },
                "audio": False,
            },
            video_processor_factory=AIWorkoutProcessor,
            async_processing=True,
        )

        ui_html(
            """
                </div>

                <div class="camera-note">
                    Allow camera access in your browser. Keep your full body visible.
                </div>
            </div>
            """
        )

    # --------------------------------------------------------
    # LIVE METRICS
    # --------------------------------------------------------

    with middle:

        @st.fragment(run_every="700ms")
        def live_metrics():
            state = ai_state.snapshot()
            render_rep_panel(state)

            ui_html("<div style='height:10px'></div>")

            render_score_panel(state)

        live_metrics()

    # --------------------------------------------------------
    # WORKOUT CONTROL
    # --------------------------------------------------------

    with right:

        ui_html(
            """
            <div class="control-card">
                <div class="control-title">
                    <span class="control-title-icon">🏋️</span>
                    WORKOUT CONTROL
                </div>
            """
        )

        exercise_options = [
            "Bicep Curl",
            "Squat",
            "Push-up",
            "Shoulder Press",
            "Lateral Raise",
        ]

        current_exercise = st.session_state.exercise

        if current_exercise not in exercise_options:
            current_exercise = exercise_options[0]

        selected_exercise = st.selectbox(
            "Exercise",
            exercise_options,
            index=exercise_options.index(current_exercise),
        )

        st.session_state.exercise = selected_exercise

        st.session_state.sets = st.number_input(
            "Sets",
            min_value=1,
            max_value=20,
            value=int(st.session_state.sets),
            step=1,
        )

        st.session_state.target_reps = st.number_input(
            "Target Reps",
            min_value=1,
            max_value=100,
            value=int(st.session_state.target_reps),
            step=1,
        )

        st.session_state.weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=300.0,
            value=float(st.session_state.weight),
            step=0.5,
        )

        start_label = (
            "🔄  RESET WORKOUT"
            if st.session_state.workout_started
            else "🚀  START WORKOUT"
        )

        if st.button(
            start_label,
            type="primary",
            use_container_width=True,
        ):
            reset_ai()

            exercise_manager.set_exercise(
                st.session_state.exercise
            )

            st.session_state.workout_started = True
            st.session_state.start_time = time.time()

            ai_state.update(
                exercise=st.session_state.exercise,
                set_number=1,
                active=True,
                workout_enabled=True,
            )

            st.rerun()

        if st.button(
            "⏹️  STOP WORKOUT",
            use_container_width=True,
        ):
            st.session_state.workout_started = False
            ai_state.update(active=False, workout_enabled=False)
            st.rerun()

        ui_html("</div>")

    # --------------------------------------------------------
    # COACH + PROGRESS
    # --------------------------------------------------------

    coach_col, progress_col = st.columns(
        [1, 1],
        gap="medium",
    )

    with coach_col:

        @st.fragment(run_every="700ms")
        def live_coach():
            render_coach(ai_state.snapshot())

        live_coach()

    with progress_col:

        @st.fragment(run_every="700ms")
        def live_progress():
            render_progress(ai_state.snapshot())

        live_progress()

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    ui_html('<div class="section-title">PERFORMANCE</div>')

    @st.fragment(run_every="1s")
    def performance_metrics():

        state = ai_state.snapshot()

        if st.session_state.start_time:
            elapsed = max(
                0,
                int(time.time() - st.session_state.start_time),
            )
        else:
            elapsed = 0

        minutes = elapsed // 60
        seconds = elapsed % 60

        m1, m2, m3, m4 = st.columns(4, gap="medium")

        with m1:
            render_metric(
                "🔥",
                "CALORIES",
                f'{state["calories"]:.0f}',
                "kcal",
            )

        with m2:
            render_metric(
                "⏱️",
                "TIME ELAPSED",
                f"{minutes:02d}:{seconds:02d}",
            )

        with m3:
            render_metric(
                "🧠",
                "AI CONFIDENCE",
                f'{state["confidence"]}%',
            )

        with m4:
            score = int(state["form_score"])

            if score >= 85:
                quality = "Excellent"
            elif score >= 70:
                quality = "Good"
            else:
                quality = "Ready"

            render_metric(
                "📈",
                "MOVEMENT QUALITY",
                quality,
            )

    performance_metrics()

    # --------------------------------------------------------
    # INTELLIGENCE
    # --------------------------------------------------------

    tips_col, insight_col = st.columns(
        [1, 1],
        gap="medium",
    )

    with tips_col:
        render_tips()

    with insight_col:
        ui_html(
            """
            <div class="card">
                <div class="card-title">
                    📊 PERFORMANCE INSIGHT
                </div>

                <div style="
                    margin-top:15px;
                    color:#94a3b8;
                    font-size:11px;
                    line-height:1.75;
                ">
                    Your AI trainer continuously evaluates
                    movement quality, exercise recognition,
                    range of motion and consistency.
                </div>

                <div style="
                    margin-top:15px;
                    color:#a78bfa;
                    font-size:10px;
                    font-weight:700;
                ">
                    Small steps. Big changes. 🚀
                </div>
            </div>
            """
        )


# ============================================================
# DASHBOARD
# ============================================================

elif st.session_state.page == "Dashboard":

    render_hero(
        "PERFORMANCE CENTER",
        "Your",
        "Progress",
        "Track your training performance, consistency and AI form quality.",
    )

    ui_html('<div class="section-title">YOUR PERFORMANCE</div>')

    a, b, c, d = st.columns(4, gap="medium")

    with a:
        render_metric("🏋️", "WORKOUTS", "—")

    with b:
        render_metric("🔥", "TOTAL CALORIES", "—", "kcal")

    with c:
        render_metric("🔁", "TOTAL REPS", "—")

    with d:
        render_metric("🎯", "AVG FORM SCORE", "—", "%")

    ui_html('<div class="section-title">LIVE AI STATUS</div>')

    state = ai_state.snapshot()

    status = "ACTIVE" if state["active"] else "READY"
    exercise = html.escape(state["exercise"])
    feedback = html.escape(str(state["feedback"]))

    ui_html(
        f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">AI SESSION</div>
                <div class="live-badge">{status}</div>
            </div>

            <div style="color:#94a3b8;font-size:11px;line-height:1.8;">
                Exercise: <b style="color:white;">{exercise}</b><br>
                Reps: <b style="color:white;">{state["reps"]}</b><br>
                Form Score: <b style="color:#4ade80;">{state["form_score"]}%</b><br>
                Confidence: <b style="color:#38bdf8;">{state["confidence"]}%</b><br>
                Coach: <b style="color:#c4b5fd;">{feedback}</b>
            </div>
        </div>
        """
    )


# ============================================================
# EXERCISES
# ============================================================

elif st.session_state.page == "Exercises":

    render_hero(
        "AI EXERCISE LIBRARY",
        "Choose Your",
        "Movement",
        "Every exercise is analyzed using real-time computer vision.",
    )

    exercises = [
        ("💪", "Bicep Curl", "Arms", "Intermediate"),
        ("🦵", "Squat", "Legs", "Beginner"),
        ("🔥", "Push-up", "Chest / Arms", "Beginner"),
        ("🏋️", "Shoulder Press", "Shoulders", "Intermediate"),
        ("💥", "Lateral Raise", "Shoulders", "Intermediate"),
    ]

    for row in range(0, len(exercises), 3):

        cols = st.columns(3, gap="medium")

        for col, item in zip(cols, exercises[row:row + 3]):

            icon, name, muscle, difficulty = item

            try:
                info = exercise_manager.get_exercise_info(name)
            except Exception:
                info = None

            if isinstance(info, dict):
                muscles = info.get("muscles", muscle)
                category = info.get("category", "")
            else:
                muscles = muscle
                category = ""

            with col:
                ui_html(
                    f"""
                    <div class="card" style="margin-bottom:16px;">
                        <div style="font-size:35px;">{icon}</div>

                        <div style="
                            margin-top:14px;
                            font-size:18px;
                            font-weight:800;
                        ">
                            {name}
                        </div>

                        <div style="
                            margin-top:7px;
                            color:#64748b;
                            font-size:10px;
                        ">
                            {muscles}
                        </div>

                        <div style="
                            margin-top:13px;
                            color:#a78bfa;
                            font-size:9px;
                            font-weight:800;
                        ">
                            {difficulty.upper()}
                        </div>

                        <div style="
                            margin-top:7px;
                            color:#64748b;
                            font-size:9px;
                        ">
                            {category}
                        </div>
                    </div>
                    """
                )


# ============================================================
# AI COACH
# ============================================================

elif st.session_state.page == "Coach":

    render_hero(
        "ARTIFICIAL INTELLIGENCE",
        "Meet Your",
        "AI Coach",
        "Real-time movement intelligence designed to make every repetition better.",
    )

    @st.fragment(run_every="700ms")
    def coach_page():

        state = ai_state.snapshot()
        render_coach(state)

        st.write("")

        score = int(state["form_score"])
        confidence = int(state["confidence"])

        c1, c2 = st.columns(2)

        with c1:
            render_metric("🎯", "FORM QUALITY", f"{score}", "%")

        with c2:
            render_metric("🧠", "AI CONFIDENCE", f"{confidence}", "%")

    coach_page()


# ============================================================
# HISTORY
# ============================================================

elif st.session_state.page == "History":

    render_hero(
        "TRAINING HISTORY",
        "Your",
        "Journey",
        "Every workout is another step forward.",
    )

    ui_html(
        """
        <div class="card" style="margin-top:25px;">
            <div class="card-title">🕘 WORKOUT HISTORY</div>

            <div style="
                margin-top:14px;
                color:#94a3b8;
                font-size:11px;
                line-height:1.7;
            ">
                Workout history is connected to the project's
                SQLite database in the desktop/backend layer.
                For cloud deployment, persistent history should
                later be moved to a hosted database.
            </div>
        </div>
        """
    )


# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.page == "Settings":

    render_hero(
        "SYSTEM CONFIGURATION",
        "AI",
        "Settings",
        "Configure your intelligent training environment.",
    )

    ui_html('<div class="section-title">CAMERA & AI</div>')

    c1, c2 = st.columns(2, gap="medium")

    with c1:

        st.session_state.pose_enabled = st.checkbox(
            "Enable AI Pose Detection",
            value=st.session_state.pose_enabled,
        )

        st.session_state.form_enabled = st.checkbox(
            "Enable Real-time Form Analysis",
            value=st.session_state.form_enabled,
        )

        st.session_state.recognition_enabled = st.checkbox(
            "Enable AI Exercise Recognition",
            value=st.session_state.recognition_enabled,
        )

    with c2:

        st.session_state.voice_enabled = st.checkbox(
            "Enable Voice Coach",
            value=st.session_state.voice_enabled,
        )

        st.session_state.show_skeleton = st.checkbox(
            "Show Pose Skeleton",
            value=st.session_state.show_skeleton,
        )

        ai_state.update(
            show_skeleton=st.session_state.show_skeleton
        )

        st.session_state.show_confidence = st.checkbox(
            "Show AI Confidence",
            value=st.session_state.show_confidence,
        )

    ui_html(
        """
        <div class="card" style="margin-top:20px;">
            <div class="card-title">SYSTEM STATUS</div>

            <div style="
                margin-top:12px;
                color:#94a3b8;
                font-size:11px;
                line-height:1.8;
            ">
                🟢 MediaPipe Pose<br>
                🟢 Exercise Recognition<br>
                🟢 Form Analysis<br>
                🟢 WebRTC Camera<br>
                🟢 Streamlit Interface
            </div>
        </div>
        """
    )

    st.success("AI GYM is configured and ready.")


# ============================================================
# END
# ============================================================
