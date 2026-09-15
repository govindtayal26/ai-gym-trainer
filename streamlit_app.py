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

from coaching.coach import AICoach
from coaching.voice_coach import VoiceCoach


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
# HTML
# ============================================================

def ui_html(content: str):
    st.html(content)


# ============================================================
# PREMIUM CSS
# ============================================================

ui_html(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

:root {
    --bg: #05070d;
    --panel: #0b1120;
    --panel2: #10182a;
    --border: rgba(148,163,184,.12);
    --purple: #8b5cf6;
    --blue: #38bdf8;
    --cyan: #22d3ee;
    --green: #22c55e;
    --green2: #4ade80;
    --red: #fb7185;
    --white: #f8fafc;
    --muted: #94a3b8;
    --muted2: #64748b;
}

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(124,58,237,.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 8%,
            rgba(14,165,233,.12),
            transparent 26%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(168,85,247,.08),
            transparent 35%
        ),
        var(--bg);

    color: var(--white);
}

.block-container {
    max-width: 1750px;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(8,11,20,.99),
            rgba(4,6,12,.99)
        );

    border-right:
        1px solid rgba(139,92,246,.18);
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

    background:
        linear-gradient(
            135deg,
            rgba(139,92,246,.30),
            rgba(56,189,248,.18)
        );

    border:
        1px solid rgba(139,92,246,.42);

    box-shadow:
        0 0 28px rgba(139,92,246,.20);
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
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
    color: var(--muted2);
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
}

div.stButton > button:hover {
    border-color: rgba(139,92,246,.48);
    color: white;
    background: rgba(139,92,246,.09);
}

.stButton button[kind="primary"] {
    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #2563eb
        );

    border:
        1px solid rgba(167,139,250,.50);

    color: white;

    box-shadow:
        0 10px 30px rgba(124,58,237,.25);
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    overflow: hidden;

    padding: 29px;
    border-radius: 25px;

    background:
        radial-gradient(
            circle at 82% 0%,
            rgba(37,99,235,.21),
            transparent 34%
        ),
        radial-gradient(
            circle at 18% 100%,
            rgba(139,92,246,.17),
            transparent 36%
        ),
        linear-gradient(
            135deg,
            rgba(9,16,31,.97),
            rgba(7,10,20,.95)
        );

    border:
        1px solid rgba(56,189,248,.16);

    box-shadow:
        0 20px 70px rgba(0,0,0,.25);
}

.hero-label {
    color: #a78bfa;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero-title {
    margin-top: 7px;
    font-size: 40px;
    line-height: 1.08;
    font-weight: 800;
}

.hero-title span {
    background:
        linear-gradient(
            90deg,
            #a78bfa,
            #38bdf8
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 9px;
    color: var(--muted);
    font-size: 13px;
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

/* ============================================================
   CARDS
   ============================================================ */

.card,
.control-card,
.coach-card,
.rep-panel,
.score-panel,
.metric-card {
    border-radius: 20px;
}

.card {
    padding: 19px;

    background:
        linear-gradient(
            145deg,
            rgba(17,24,39,.84),
            rgba(8,12,23,.82)
        );

    border:
        1px solid rgba(148,163,184,.10);

    box-shadow:
        0 15px 50px rgba(0,0,0,.20);
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}

.card-title {
    font-size: 12px;
    font-weight: 800;
}

.section-title {
    margin: 25px 0 11px;

    color: #cbd5e1;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

/* ============================================================
   CAMERA
   ============================================================ */

.camera-shell {
    padding: 5px;
    border-radius: 21px;

    background:
        linear-gradient(
            135deg,
            rgba(34,211,238,.42),
            rgba(139,92,246,.38),
            rgba(34,197,94,.18)
        );

    box-shadow:
        0 0 60px rgba(56,189,248,.07);
}

.camera-note {
    margin-top: 8px;
    color: var(--muted2);
    font-size: 9px;
    text-align: center;
}

/* ============================================================
   METRICS
   ============================================================ */

.rep-panel {
    min-height: 174px;
    padding: 18px;
    text-align: center;

    background:
        linear-gradient(
            145deg,
            rgba(12,18,34,.94),
            rgba(7,10,18,.92)
        );

    border:
        1px solid rgba(139,92,246,.16);
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

    background:
        linear-gradient(
            135deg,
            white,
            #a78bfa
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.rep-target {
    margin-top: 5px;
    color: var(--muted2);
    font-size: 10px;
}

.score-panel {
    min-height: 174px;
    padding: 18px;
    text-align: center;

    background:
        linear-gradient(
            145deg,
            rgba(8,25,26,.94),
            rgba(7,12,20,.92)
        );

    border:
        1px solid rgba(34,197,94,.15);
}

.score-number {
    margin-top: 24px;
    color: var(--green2);
    font-size: 41px;
    line-height: 1;
    font-weight: 800;
}

.score-status {
    margin-top: 10px;
    color: var(--green2);
    font-size: 9px;
    font-weight: 800;
}

/* ============================================================
   METRIC CARD
   ============================================================ */

.metric-card {
    min-height: 132px;
    padding: 19px;

    background:
        linear-gradient(
            145deg,
            rgba(13,20,37,.90),
            rgba(7,10,18,.90)
        );

    border:
        1px solid rgba(148,163,184,.10);
}

.metric-icon {
    font-size: 21px;
}

.metric-label {
    margin-top: 12px;
    color: var(--muted2);
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
    color: var(--muted2);
    font-size: 10px;
}

/* ============================================================
   CONTROL
   ============================================================ */

.control-card {
    padding: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(13,21,38,.96),
            rgba(7,10,18,.94)
        );

    border:
        1px solid rgba(56,189,248,.14);
}

.control-title {
    margin-bottom: 16px;
    font-size: 12px;
    font-weight: 800;
}

/* ============================================================
   COACH
   ============================================================ */

.coach-card {
    min-height: 155px;
    padding: 20px;

    background:
        radial-gradient(
            circle at 0% 100%,
            rgba(139,92,246,.17),
            transparent 36%
        ),
        linear-gradient(
            145deg,
            rgba(23,18,50,.94),
            rgba(8,11,22,.94)
        );

    border:
        1px solid rgba(139,92,246,.24);
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

    background:
        linear-gradient(
            135deg,
            rgba(139,92,246,.38),
            rgba(37,99,235,.25)
        );

    font-size: 22px;
}

.coach-caption {
    margin-top: 3px;
    color: var(--muted2);
    font-size: 9px;
}

.coach-text {
    margin-top: 13px;
    color: #e2e8f0;
    font-size: 12px;
    line-height: 1.65;
}

/* ============================================================
   PROGRESS
   ============================================================ */

.progress-track {
    height: 8px;
    overflow: hidden;
    border-radius: 999px;
    background: rgba(30,41,59,.80);
}

.progress-fill {
    height: 100%;
    border-radius: inherit;

    background:
        linear-gradient(
            90deg,
            #8b5cf6,
            #38bdf8
        );
}

.rep-dots {
    margin-top: 13px;
    text-align: center;
}

.rep-dot {
    display: inline-flex;

    width: 24px;
    height: 24px;

    margin: 3px;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    font-size: 8px;
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

</style>
"""
)


# ============================================================
# DEFAULT SESSION STATE
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
# SHARED AI STATE
# ============================================================

@dataclass
class AIState:

    lock: threading.Lock = field(
        default_factory=threading.Lock
    )

    exercise: str = "Unknown"

    reps: int = 0

    stage: str = "up"

    form_score: int = 0

    feedback: str = (
        "Position yourself in front of the camera."
    )

    confidence: int = 0

    set_number: int = 1

    calories: float = 0.0

    active: bool = False

    workout_enabled: bool = False

    last_rep_time: float = 0.0

    total_reps: int = 0

    last_feedback: str = ""

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
                "total_reps": self.total_reps,
                "last_feedback": self.last_feedback,
            }


@st.cache_resource
def get_ai_state():

    return AIState()


ai_state = get_ai_state()


# ============================================================
# AI SYSTEMS
# ============================================================

@st.cache_resource
def get_ai_systems():

    detector = ExerciseDetector()

    stabilizer = ExerciseStabilizer()

    exercise_manager = ExerciseManager()

    coach = AICoach()

    voice = VoiceCoach()

    return (
        detector,
        stabilizer,
        exercise_manager,
        coach,
        voice,
    )


(
    detector,
    stabilizer,
    exercise_manager,
    coach,
    voice_coach,
) = get_ai_systems()


# ============================================================
# RESET AI
# ============================================================

def reset_ai():

    detector.current_exercise = "Unknown"

    stabilizer.reset()

    exercise_manager.reset()

    coach.reset()

    ai_state.update(
        exercise="Unknown",
        reps=0,
        stage="up",
        form_score=0,
        feedback=(
            "Position yourself in front of the camera."
        ),
        confidence=0,
        set_number=1,
        calories=0.0,
        total_reps=0,
        last_feedback="",
        active=False,
        workout_enabled=False,
    )


# ============================================================
# MEDIAPIPE PROCESSOR
# ============================================================

class AIWorkoutProcessor(VideoProcessorBase):

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.mp_drawing = (
            mp.solutions.drawing_utils
        )

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.current_exercise = "Unknown"

        self.previous_reps = 0

        self.last_spoken_feedback = ""

        self.last_feedback_time = 0.0

        self.previous_calories = 0.0

    # --------------------------------------------------------
    # DRAW TEXT
    # --------------------------------------------------------

    def draw_text(
        self,
        image,
        text,
        position,
        scale=0.6,
        color=(235,245,255),
        thickness=2,
    ):

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

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    def draw_hud(self, image, state):

        h, w = image.shape[:2]

        # --------------------------------------------
        # AI STATUS
        # --------------------------------------------

        cv2.rectangle(
            image,
            (18, 18),
            (300, 70),
            (8, 15, 28),
            -1,
        )

        cv2.circle(
            image,
            (40, 44),
            7,
            (40,220,120),
            -1,
        )

        self.draw_text(
            image,
            "AI VISION ACTIVE",
            (58, 51),
            0.60,
            (220,240,255),
            2,
        )

        # --------------------------------------------
        # RIGHT HUD
        # --------------------------------------------

        hud_x = max(20, w - 360)

        cv2.rectangle(
            image,
            (hud_x, 18),
            (w - 18, 175),
            (8,15,28),
            -1,
        )

        self.draw_text(
            image,
            "EXERCISE",
            (hud_x + 18, 45),
            0.43,
            (150,170,190),
            1,
        )

        exercise = state["exercise"]

        if exercise == "Unknown":

            exercise = self.current_exercise

        self.draw_text(
            image,
            exercise,
            (hud_x + 18, 80),
            0.70,
            (255,255,255),
            2,
        )

        self.draw_text(
            image,
            f"CONFIDENCE  {state['confidence']}%",
            (hud_x + 18, 112),
            0.42,
            (80,220,255),
            1,
        )

        self.draw_text(
            image,
            f"REPS  {state['reps']}",
            (hud_x + 18, 140),
            0.44,
            (130,240,160),
            1,
        )

        self.draw_text(
            image,
            f"FORM  {state['form_score']}%",
            (hud_x + 150, 140),
            0.44,
            (180,140,255),
            1,
        )

        self.draw_text(
            image,
            f"SET  {state['set_number']}",
            (hud_x + 18, 165),
            0.40,
            (180,190,205),
            1,
        )

    # --------------------------------------------------------
    # VOICE
    # --------------------------------------------------------

    def speak_feedback(self, message):

        if not st.session_state.voice_enabled:
            return

        message = str(message).strip()

        if not message:
            return

        now = time.time()

        # Do not repeat the same sentence continuously.
        if message == self.last_spoken_feedback:

            if now - self.last_feedback_time < 4:
                return

        self.last_spoken_feedback = message

        self.last_feedback_time = now

        voice_coach.speak_feedback(message)

    # --------------------------------------------------------
    # PROCESS FRAME
    # --------------------------------------------------------

    def recv(self, frame):

        # ====================================================
        # WEBRTC → OPENCV
        # ====================================================

        image = frame.to_ndarray(
            format="bgr24"
        )

        image = cv2.flip(
            image,
            1
        )

        # ====================================================
        # START/STOP GATE
        # ====================================================

        state = ai_state.snapshot()

        if not state["workout_enabled"]:

            self.draw_text(
                image,
                "PRESS START TO BEGIN",
                (35, 90),
                0.75,
                (80,220,255),
                2,
            )

            return frame.from_ndarray(
                image,
                format="bgr24",
            )

        # ====================================================
        # MEDIAPIPE
        # ====================================================

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        results = self.pose.process(
            rgb
        )

        # ====================================================
        # NO PERSON
        # ====================================================

        if not results.pose_landmarks:

            ai_state.update(
                active=False,
                confidence=0,
                feedback=(
                    "Move into the camera frame."
                ),
            )

            self.draw_text(
                image,
                "NO PERSON DETECTED",
                (35, 90),
                0.75,
                (80,190,255),
                2,
            )

            return frame.from_ndarray(
                image,
                format="bgr24",
            )

        # ====================================================
        # LANDMARKS
        # ====================================================

        landmarks = (
            results.pose_landmarks.landmark
        )

        # ====================================================
        # SKELETON
        # ====================================================

        if st.session_state.show_skeleton:

            self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(
                    color=(80,210,255),
                    thickness=2,
                    circle_radius=3,
                ),
                self.mp_drawing.DrawingSpec(
                    color=(160,80,255),
                    thickness=2,
                    circle_radius=2,
                ),
            )

        # ====================================================
        # EXERCISE RECOGNITION
        # ====================================================

        if st.session_state.recognition_enabled:

            detected = detector.detect(
                landmarks
            )

            stable = stabilizer.update(
                detected
            )

        else:

            stable = (
                st.session_state.exercise
            )

        # ====================================================
        # UNKNOWN
        # ====================================================

        if stable == "Unknown":

            # Never destroy the previously recognized
            # exercise because of one bad frame.

            ai_state.update(
                active=True,
                confidence=0,
            )

            self.draw_hud(
                image,
                ai_state.snapshot(),
            )

            return frame.from_ndarray(
                image,
                format="bgr24",
            )

        # ====================================================
        # EXERCISE CHANGE
        # ====================================================

        if stable != self.current_exercise:

            self.current_exercise = stable

            exercise_manager.set_exercise(
                stable
            )

            self.previous_reps = 0

            coach.reset()

            self.last_spoken_feedback = ""

        # ====================================================
        # EXERCISE UPDATE
        # ====================================================

        result = exercise_manager.update(
            landmarks
        )

        reps = int(
            result.get(
                "reps",
                0,
            )
        )

        stage = result.get(
            "stage",
            "up",
        )

        form_score = int(
            result.get(
                "form_score",
                0,
            )
        )

        exercise_feedback = result.get(
            "feedback",
            "Keep moving.",
        )

        # ====================================================
        # CONFIDENCE
        # ====================================================

        if st.session_state.recognition_enabled:

            scores = detector.get_scores(
                landmarks
            )

            confidence = int(
                scores.get(
                    stable,
                    0,
                )
            )

        else:

            confidence = 100

        # ====================================================
        # AI COACH
        # ====================================================

        if st.session_state.form_enabled:

            coach_result = coach.update(
                {
                    "exercise": stable,
                    "reps": reps,
                    "stage": stage,
                    "form_score": form_score,
                    "feedback": exercise_feedback,
                }
            )

            if isinstance(
                coach_result,
                dict,
            ):

                coaching_feedback = (
                    coach_result.get(
                        "feedback",
                        exercise_feedback,
                    )
                )

            else:

                coaching_feedback = (
                    str(coach_result)
                    if coach_result
                    else exercise_feedback
                )

        else:

            coaching_feedback = (
                exercise_feedback
            )

        # ====================================================
        # REP DETECTION
        # ====================================================

        rep_changed = (
            reps > self.previous_reps
        )

        now = time.time()

        if rep_changed:

            voice_coach.speak_rep(
                reps,
                coaching_feedback,
            )

            ai_state.update(
                last_rep_time=now
            )

        self.previous_reps = reps

        # ====================================================
        # CALORIES
        # ====================================================

        # Simple live estimate.
        # Workout backend can later replace this
        # with MET-based calculation.

        calories = (
            reps * 0.35
        )

        # ====================================================
        # SHARED STATE
        # ====================================================

        ai_state.update(

            exercise=stable,

            reps=reps,

            stage=stage,

            form_score=form_score,

            feedback=coaching_feedback,

            confidence=confidence,

            calories=calories,

            total_reps=reps,

            active=True,

            last_feedback=coaching_feedback,
        )

        # ====================================================
        # GENERAL VOICE FEEDBACK
        # ====================================================

        if (
            not rep_changed
            and coaching_feedback
            and form_score > 0
        ):

            self.speak_feedback(
                coaching_feedback
            )

        # ====================================================
        # HUD
        # ====================================================

        self.draw_hud(
            image,
            ai_state.snapshot(),
        )

        # ====================================================
        # RETURN FRAME
        # ====================================================

        return frame.from_ndarray(
            image,
            format="bgr24",
        )


# ============================================================
# RTC
# ============================================================

RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302"
                ]
            }
        ]
    }
)


# ============================================================
# UI HELPERS
# ============================================================

def render_topbar():

    now = datetime.now()

    ui_html(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:18px;
        ">

            <div style="
                padding:12px 17px;
                border-radius:14px;
                background:rgba(10,17,31,.80);
                border:1px solid rgba(56,189,248,.16);
                color:#64748b;
                font-size:12px;
            ">
                🔍 &nbsp;
                Discipline today, stronger tomorrow.
            </div>

            <div style="
                color:#94a3b8;
                font-size:10px;
                text-align:right;
            ">
                {now.strftime("%a, %d %b %Y")}<br>
                <b style="color:#e2e8f0;">
                    AI TRAINING MODE
                </b>
            </div>

        </div>
        """
    )


def render_hero(
    label,
    title,
    highlighted,
    subtitle,
    pills=None,
):

    pills_html = ""

    if pills:

        for pill in pills:

            pills_html += (
                f"""
                <div class="feature-pill">
                    {pill}
                </div>
                """
            )

    ui_html(
        f"""
        <div class="hero">

            <div class="hero-label">
                {label}
            </div>

            <div class="hero-title">
                {title}
                <span>{highlighted}</span>
            </div>

            <div class="hero-subtitle">
                {subtitle}
            </div>

            {
                f'<div class="feature-pills">'
                f'{pills_html}'
                f'</div>'
                if pills
                else ''
            }

        </div>
        """
    )


def render_metric(
    icon,
    label,
    value,
    unit="",
):

    ui_html(
        f"""
        <div class="metric-card">

            <div class="metric-icon">
                {icon}
            </div>

            <div class="metric-label">
                {label}
            </div>

            <div class="metric-value">
                {value}
                <span class="metric-unit">
                    {unit}
                </span>
            </div>

        </div>
        """
    )


def render_rep_panel(state):

    target = int(
        st.session_state.target_reps
    )

    ui_html(
        f"""
        <div class="rep-panel">

            <div class="rep-label">
                CURRENT REPS
            </div>

            <div class="rep-number">
                {int(state["reps"]):02d}
            </div>

            <div class="rep-target">
                / {target}
            </div>

        </div>
        """
    )


def render_score_panel(state):

    score = max(
        0,
        min(
            100,
            int(state["form_score"])
        )
    )

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

            <div class="rep-label">
                FORM SCORE
            </div>

            <div class="score-number">
                {score}%
            </div>

            <div class="score-status">
                {status}
            </div>

        </div>
        """
    )


def render_coach(state):

    feedback = html.escape(
        str(
            state["feedback"]
            or
            "Start your movement and I'll analyze your form."
        )
    )

    ui_html(
        f"""
        <div class="coach-card">

            <div class="coach-row">

                <div class="coach-avatar">
                    🤖
                </div>

                <div>

                    <div class="card-title">
                        AI COACH
                    </div>

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

    reps = max(
        0,
        int(state["reps"])
    )

    target = max(
        1,
        int(st.session_state.target_reps)
    )

    progress = min(
        100,
        int(
            reps / target * 100
        )
    )

    dots = ""

    display_target = min(
        target,
        50
    )

    for i in range(
        1,
        display_target + 1
    ):

        cls = (
            "done"
            if i <= reps
            else "pending"
        )

        dots += (
            f"""
            <span class="rep-dot {cls}">
                {i}
            </span>
            """
        )

    ui_html(
        f"""
        <div class="card">

            <div class="card-header">

                <div class="card-title">
                    WORKOUT PROGRESS
                </div>

                <div style="
                    color:#94a3b8;
                    font-size:9px;
                ">
                    SET {state["set_number"]}
                    OF {st.session_state.sets}
                </div>

            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:8px;
            ">

                <span style="
                    color:#94a3b8;
                    font-size:9px;
                ">
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

                <div
                    class="progress-fill"
                    style="width:{progress}%"
                ></div>

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
        <div class="card">

            <div class="card-title">
                💡 WORKOUT INTELLIGENCE
            </div>

            <div style="
                margin-top:12px;
                color:#cbd5e1;
                font-size:10px;
                line-height:2;
            ">

                ✓ &nbsp; Keep your core engaged<br>

                ✓ &nbsp; Maintain proper posture<br>

                ✓ &nbsp; Control every movement<br>

                ✓ &nbsp; Use your full range of motion

            </div>

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

                <div class="brand-icon">
                    🏋️
                </div>

                <div>

                    <div class="brand-name">
                        AI GYM
                    </div>

                    <div class="brand-subtitle">
                        INTELLIGENT FITNESS
                    </div>

                </div>

            </div>

        </div>

        <div class="nav-title">
            NAVIGATION
        </div>
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

        if st.button(
            label,
            use_container_width=True,
        ):

            st.session_state.page = page_name

            st.rerun()

    ui_html(
        """
        <div style="
            margin-top:25px;
            padding:19px;
            border-radius:20px;
            background:
                linear-gradient(
                    145deg,
                    rgba(21,17,46,.96),
                    rgba(8,11,22,.96)
                );
            border:1px solid rgba(139,92,246,.27);
        ">

            <div style="
                font-size:17px;
                font-weight:800;
            ">
                Train Smarter
            </div>

            <div style="
                color:#94a3b8;
                font-size:11px;
                line-height:1.65;
                margin-top:8px;
            ">
                Real-time computer vision,
                intelligent form analysis
                and personalized coaching.
            </div>

        </div>

        <div style="
            margin:20px 5px 0;
            color:#94a3b8;
            font-size:11px;
        ">
            🟢 AI Systems Ready
        </div>
        """
    )


# ============================================================
# TOP BAR
# ============================================================

render_topbar()


# ============================================================
# WORKOUT
# ============================================================

if st.session_state.page == "Workout":

    render_hero(
        "REAL-TIME COMPUTER VISION",
        "AI",
        "Workout Studio",
        (
            "Your intelligent personal trainer that sees, "
            "understands and improves every movement."
        ),
        [
            "🟢 Live Pose Detection",
            "⚡ AI Form Analysis",
            "💬 AI Coaching",
            "🎯 Exercise Recognition",
        ],
    )

    ui_html(
        '<div class="section-title">'
        'LIVE TRAINING'
        '</div>'
    )

    left, middle, right = st.columns(
        [1.65, 0.82, 0.90],
        gap="medium",
    )

    # ========================================================
    # CAMERA
    # ========================================================

    with left:

        ui_html(
            """
            <div class="card">

                <div class="card-header">

                    <div class="card-title">
                        🎥 LIVE AI CAMERA
                    </div>

                    <div style="
                        padding:6px 10px;
                        border-radius:999px;
                        background:rgba(34,197,94,.08);
                        color:#4ade80;
                        font-size:9px;
                        font-weight:800;
                    ">
                        ● LIVE
                    </div>

                </div>

                <div class="camera-shell">
            """
        )

        # ====================================================
        # IMPORTANT:
        # ALWAYS keep WebRTC mounted.
        # Do not conditionally create it based on
        # workout_started.
        # ====================================================

        webrtc_streamer(
            key="ai-gym-camera",

            mode=WebRtcMode.SENDRECV,

            rtc_configuration=RTC_CONFIGURATION,

            media_stream_constraints={
                "video": {
                    "width": {
                        "ideal": 1280
                    },
                    "height": {
                        "ideal": 720
                    },
                    "facingMode": "user",
                },
                "audio": False,
            },

            video_processor_factory=(
                AIWorkoutProcessor
            ),

            async_processing=True,
        )

        ui_html(
            """
                </div>

                <div class="camera-note">
                    Allow camera access.
                    Keep your full body visible.
                </div>

            </div>
            """
        )

    # ========================================================
    # LIVE METRICS
    # ========================================================

    with middle:

        @st.fragment(run_every="700ms")
        def live_metrics():

            state = ai_state.snapshot()

            render_rep_panel(state)

            ui_html(
                "<div style='height:10px'></div>"
            )

            render_score_panel(state)

        live_metrics()

    # ========================================================
    # CONTROLS
    # ========================================================

    with right:

        ui_html(
            """
            <div class="control-card">

                <div class="control-title">
                    🏋️ WORKOUT CONTROL
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

        current = (
            st.session_state.exercise
        )

        if current not in exercise_options:

            current = exercise_options[0]

        selected = st.selectbox(
            "Exercise",
            exercise_options,
            index=exercise_options.index(
                current
            ),
        )

        st.session_state.exercise = selected

        st.session_state.sets = (
            st.number_input(
                "Sets",
                min_value=1,
                max_value=20,
                value=int(
                    st.session_state.sets
                ),
            )
        )

        st.session_state.target_reps = (
            st.number_input(
                "Target Reps",
                min_value=1,
                max_value=100,
                value=int(
                    st.session_state.target_reps
                ),
            )
        )

        st.session_state.weight = (
            st.number_input(
                "Weight (kg)",
                min_value=0.0,
                max_value=300.0,
                value=float(
                    st.session_state.weight
                ),
                step=0.5,
            )
        )

        # ====================================================
        # START / RESET
        # ====================================================

        if st.session_state.workout_started:

            start_label = (
                "🔄 RESET WORKOUT"
            )

        else:

            start_label = (
                "🚀 START WORKOUT"
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

            st.session_state.start_time = (
                time.time()
            )

            ai_state.update(
                exercise=(
                    st.session_state.exercise
                ),
                set_number=1,
                active=True,
                workout_enabled=True,
            )

            # DO NOT call st.rerun().
            # The button already causes the rerun.

        # ====================================================
        # STOP
        # ====================================================

        if st.button(
            "⏹️ STOP WORKOUT",
            use_container_width=True,
        ):

            st.session_state.workout_started = False

            ai_state.update(
                active=False,
                workout_enabled=False,
            )

        ui_html(
            """
            </div>
            """
        )

    # ========================================================
    # COACH + PROGRESS
    # ========================================================

    coach_col, progress_col = st.columns(
        [1, 1],
        gap="medium",
    )

    with coach_col:

        @st.fragment(run_every="700ms")
        def live_coach():

            render_coach(
                ai_state.snapshot()
            )

        live_coach()

    with progress_col:

        @st.fragment(run_every="700ms")
        def live_progress():

            render_progress(
                ai_state.snapshot()
            )

        live_progress()

    # ========================================================
    # PERFORMANCE
    # ========================================================

    ui_html(
        '<div class="section-title">'
        'PERFORMANCE'
        '</div>'
    )

    @st.fragment(run_every="1s")
    def performance():

        state = ai_state.snapshot()

        if st.session_state.start_time:

            elapsed = max(
                0,
                int(
                    time.time()
                    -
                    st.session_state.start_time
                ),
            )

        else:

            elapsed = 0

        minutes = elapsed // 60

        seconds = elapsed % 60

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            render_metric(
                "🔥",
                "CALORIES",
                f'{state["calories"]:.0f}',
                "kcal",
            )

        with c2:

            render_metric(
                "⏱️",
                "TIME",
                f"{minutes:02d}:{seconds:02d}",
            )

        with c3:

            render_metric(
                "🧠",
                "AI CONFIDENCE",
                f'{state["confidence"]}%',
            )

        with c4:

            score = int(
                state["form_score"]
            )

            if score >= 85:

                quality = "Excellent"

            elif score >= 70:

                quality = "Good"

            elif score > 0:

                quality = "Improve"

            else:

                quality = "Ready"

            render_metric(
                "📈",
                "FORM QUALITY",
                quality,
            )

    performance()

    # ========================================================
    # TIPS
    # ========================================================

    tips, insight = st.columns(2)

    with tips:

        render_tips()

    with insight:

        ui_html(
            """
            <div class="card">

                <div class="card-title">
                    📊 AI PERFORMANCE INSIGHT
                </div>

                <div style="
                    margin-top:15px;
                    color:#94a3b8;
                    font-size:11px;
                    line-height:1.75;
                ">

                    AI continuously evaluates:

                    <br><br>

                    • Exercise recognition<br>
                    • Movement quality<br>
                    • Range of motion<br>
                    • Repetition count<br>
                    • Form score<br>
                    • Coaching feedback

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
        "Track your training performance and AI form quality.",
    )

    state = ai_state.snapshot()

    a, b, c, d = st.columns(4)

    with a:

        render_metric(
            "🏋️",
            "CURRENT EXERCISE",
            state["exercise"],
        )

    with b:

        render_metric(
            "🔁",
            "TOTAL REPS",
            state["total_reps"],
        )

    with c:

        render_metric(
            "🎯",
            "FORM SCORE",
            state["form_score"],
            "%",
        )

    with d:

        render_metric(
            "🧠",
            "CONFIDENCE",
            state["confidence"],
            "%",
        )

    ui_html(
        '<div class="section-title">'
        'AI SESSION'
        '</div>'
    )

    render_coach(state)


# ============================================================
# EXERCISES
# ============================================================

elif st.session_state.page == "Exercises":

    render_hero(
        "AI EXERCISE LIBRARY",
        "Choose Your",
        "Movement",
        "Exercises supported by real-time computer vision.",
    )

    exercises = [
        (
            "💪",
            "Bicep Curl",
            "Arms",
            "Intermediate",
        ),
        (
            "🦵",
            "Squat",
            "Legs",
            "Beginner",
        ),
        (
            "🔥",
            "Push-up",
            "Chest / Arms",
            "Beginner",
        ),
        (
            "🏋️",
            "Shoulder Press",
            "Shoulders",
            "Intermediate",
        ),
        (
            "💥",
            "Lateral Raise",
            "Shoulders",
            "Intermediate",
        ),
    ]

    for row in range(
        0,
        len(exercises),
        3,
    ):

        cols = st.columns(3)

        for col, item in zip(
            cols,
            exercises[row:row + 3],
        ):

            icon, name, muscle, difficulty = item

            with col:

                ui_html(
                    f"""
                    <div class="card"
                         style="margin-bottom:16px;">

                        <div style="
                            font-size:35px;
                        ">
                            {icon}
                        </div>

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
                            {muscle}
                        </div>

                        <div style="
                            margin-top:13px;
                            color:#a78bfa;
                            font-size:9px;
                            font-weight:800;
                        ">
                            {difficulty.upper()}
                        </div>

                    </div>
                    """
                )


# ============================================================
# AI COACH PAGE
# ============================================================

elif st.session_state.page == "Coach":

    render_hero(
        "ARTIFICIAL INTELLIGENCE",
        "Meet Your",
        "AI Coach",
        "Real-time movement intelligence for better repetitions.",
    )

    @st.fragment(run_every="700ms")
    def coach_dashboard():

        state = ai_state.snapshot()

        render_coach(state)

        st.write("")

        c1, c2, c3 = st.columns(3)

        with c1:

            render_metric(
                "🎯",
                "FORM",
                state["form_score"],
                "%",
            )

        with c2:

            render_metric(
                "🧠",
                "CONFIDENCE",
                state["confidence"],
                "%",
            )

        with c3:

            render_metric(
                "🔁",
                "REPS",
                state["reps"],
            )

    coach_dashboard()


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
        <div class="card">

            <div class="card-title">
                🕘 WORKOUT HISTORY
            </div>

            <div style="
                margin-top:14px;
                color:#94a3b8;
                font-size:11px;
                line-height:1.7;
            ">

                Workout history will be connected
                to the SQLite / hosted database layer
                in the next integration stage.

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

    ui_html(
        '<div class="section-title">'
        'CAMERA & AI'
        '</div>'
    )

    c1, c2 = st.columns(2)

    with c1:

        st.session_state.pose_enabled = (
            st.checkbox(
                "Enable AI Pose Detection",
                value=(
                    st.session_state.pose_enabled
                ),
            )
        )

        st.session_state.form_enabled = (
            st.checkbox(
                "Enable Real-time Form Analysis",
                value=(
                    st.session_state.form_enabled
                ),
            )
        )

        st.session_state.recognition_enabled = (
            st.checkbox(
                "Enable AI Exercise Recognition",
                value=(
                    st.session_state.recognition_enabled
                ),
            )
        )

    with c2:

        st.session_state.voice_enabled = (
            st.checkbox(
                "Enable Voice Coach",
                value=(
                    st.session_state.voice_enabled
                ),
            )
        )

        st.session_state.show_skeleton = (
            st.checkbox(
                "Show Pose Skeleton",
                value=(
                    st.session_state.show_skeleton
                ),
            )
        )

        st.session_state.show_confidence = (
            st.checkbox(
                "Show AI Confidence",
                value=(
                    st.session_state.show_confidence
                ),
            )
        )

        ai_state.update(
            show_skeleton=(
                st.session_state.show_skeleton
            )
        )

    st.success(
        "AI GYM is configured and ready."
    )