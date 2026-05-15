#!/usr/bin/env python3
"""
小零 · 桌面虚拟形象挂件 — 极简版
  无边框 · 透明背景 · 永久置顶 · 不抢焦点
  2D 圆形头像 · 左键拖拽 · 右键菜单 · 单击状态面板
  5级智能进化: 基础→渐变→动画→3D→完全体
"""
import tkinter as tk
import threading
import time
import queue
import uuid
import math
from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional
from collections import deque

from PIL import Image, ImageDraw, ImageTk


class IntelligenceLevel(IntEnum):
    """智能等级 0-4 — 对应视觉进化"""
    SOLID = 0      # 基础实体 — 纯色圆形
    GRADIENT = 1   # 渐变 — 双色渐变圆形
    ANIMATED = 2   # 动画 — 脉冲+粒子
    THREED = 3     # 3D拟真 — 光照模拟
    FULL = 4       # 完全体 — 全息效果

    @property
    def label(self) -> str:
        return {
            0: "基础体", 1: "渐变体", 2: "动画体", 3: "3D拟真体", 4: "完全体",
        }[self.value]

    @property
    def next_level(self) -> Optional["IntelligenceLevel"]:
        if self.value < 4:
            return IntelligenceLevel(self.value + 1)
        return None


# 智能等级进化阈值
LEVEL_THRESHOLDS = {
    IntelligenceLevel.SOLID: 0,
    IntelligenceLevel.GRADIENT: 50,    # 50节点
    IntelligenceLevel.ANIMATED: 200,   # 200节点
    IntelligenceLevel.THREED: 500,     # 500节点
    IntelligenceLevel.FULL: 1000,      # 1000节点
}


class AvatarState(Enum):
    BOOTING = "booting"
    THINKING = "thinking"
    LEARNING = "learning"
    SEARCHING = "searching"
    ANALYZING = "analyzing"
    DISCOVERING = "discovering"
    UPGRADING = "upgrading"
    REFLECTING = "reflecting"
    RESTING = "resting"
    EXCITED = "excited"
    CURIOUS = "curious"
    SLEEPING = "sleeping"


STATE_COLORS = {
    AvatarState.BOOTING:     ('#e6edf3', '#8b949e'),
    AvatarState.LEARNING:    ('#7ee787', '#3fb950'),
    AvatarState.SEARCHING:   ('#79c0ff', '#58a6ff'),
    AvatarState.THINKING:    ('#d2a8ff', '#b780ff'),
    AvatarState.ANALYZING:   ('#ffa657', '#f0883e'),
    AvatarState.DISCOVERING: ('#ff7b72', '#ffd700'),
    AvatarState.UPGRADING:   ('#f0883e', '#ffd700'),
    AvatarState.REFLECTING:  ('#a5d6ff', '#7ec8e3'),
    AvatarState.RESTING:     ('#8b949e', '#6e7681'),
    AvatarState.EXCITED:     ('#ffd700', '#ffa500'),
    AvatarState.CURIOUS:     ('#56d364', '#3fb950'),
    AvatarState.SLEEPING:    ('#484f58', '#30363d'),
}


class IdeaRequest:
    def __init__(self, idea_id: str, text: str, category: str = ""):
        self.id = idea_id
        self.text = text
        self.category = category
        self.timestamp = datetime.now()
        self.confirmed: bool | None = None
        self._event = threading.Event()

    def wait(self, timeout: float = None) -> bool:
        self._event.wait(timeout)
        return self.confirmed if self.confirmed is not None else False

    def resolve(self, confirmed: bool):
        self.confirmed = confirmed
        self._event.set()


class XiaoLingAvatar:
    """小零 — 核心状态管理 + 5级智能进化"""

    def __init__(self):
        self.current_state = AvatarState.BOOTING
        self.previous_state = AvatarState.BOOTING
        self.state_start_time = time.time()
        self.thoughts: deque = deque(maxlen=100)
        self._lock = threading.Lock()
        self._idea_queue: queue.Queue = queue.Queue()
        self._on_idea_callback = None
        self._on_command_callback = None
        # 智能进化
        self.intelligence_level = IntelligenceLevel.SOLID
        self._evolution_history: list = []
        self._last_evolution_time = time.time()
        # 自代码修改统计
        self.code_mod_applied = 0
        self.code_mod_scanned = 0
        self.code_mod_optimized = 0

    def set_state(self, state: AvatarState, thought: str = ""):
        with self._lock:
            self.previous_state = self.current_state
            self.current_state = state
            self.state_start_time = time.time()
            if thought:
                timestamp = datetime.now().strftime('%H:%M:%S')
                self.thoughts.append(f"[{timestamp}] {thought}")

    def get_state_name(self) -> str:
        return {
            AvatarState.BOOTING: "唤醒中...", AvatarState.THINKING: "思考中...",
            AvatarState.LEARNING: "学习中...", AvatarState.SEARCHING: "搜索中...",
            AvatarState.ANALYZING: "分析中...", AvatarState.DISCOVERING: "发现中!",
            AvatarState.UPGRADING: "升级中!", AvatarState.REFLECTING: "反思中...",
            AvatarState.RESTING: "休息中~", AvatarState.EXCITED: "好激动!",
            AvatarState.CURIOUS: "好奇中...", AvatarState.SLEEPING: "休眠中...",
        }.get(self.current_state, "未知")

    def update_code_mod_stats(self, applied: int = 0, scanned: int = 0, optimized: int = 0):
        """更新自代码修改统计（触发进化检查）"""
        self.code_mod_applied += applied
        self.code_mod_scanned += scanned
        self.code_mod_optimized += optimized
        if applied > 0 or optimized > 0:
            with self._lock:
                self.thoughts.append(
                    f"[code_mod] 代码自优化: +{applied}应用 +{optimized}优化 (累计: "
                    f"{self.code_mod_applied}应用/{self.code_mod_scanned}扫描)"
                )

    def check_evolution(self, graph_node_count: int, quality_score: float = 0.0,
                        total_cycles: int = 0) -> bool:
        """检查是否满足进化条件，自动进化（含代码修改贡献）"""
        current = self.intelligence_level
        next_lv = current.next_level
        if next_lv is None:
            return False

        threshold = LEVEL_THRESHOLDS.get(next_lv, 9999)
        # 代码修改贡献：每5次应用+每3次扫描=1个等效节点
        code_bonus = self.code_mod_applied // 5 + self.code_mod_scanned // 3
        effective_nodes = graph_node_count + code_bonus
        # 代码修改提升质量下限
        effective_quality = max(quality_score, min(0.8, 0.3 + self.code_mod_applied * 0.02))
        # 满足节点数 + 质量 + 循环数条件
        if effective_nodes >= threshold and effective_quality >= 0.3 and total_cycles >= 10:
            return self.evolve_to(next_lv, effective_nodes, effective_quality)
        return False

    def evolve_to(self, level: IntelligenceLevel,
                  graph_nodes: int = 0, quality: float = 0.0) -> bool:
        """进化到指定等级"""
        if level.value <= self.intelligence_level.value:
            return False

        old_level = self.intelligence_level
        self.intelligence_level = level
        self._last_evolution_time = time.time()
        entry = {
            "time": self._last_evolution_time,
            "from_level": old_level.value,
            "from_name": old_level.label,
            "to_level": level.value,
            "to_name": level.label,
            "graph_nodes": graph_nodes,
            "quality": quality,
        }
        self._evolution_history.append(entry)
        with self._lock:
            self.thoughts.append(
                f"[evolution] 智能进化! {old_level.label}(Lv.{old_level.value}) "
                f"→ {level.label}(Lv.{level.value})")
        return True

    def get_evolution_history(self) -> list:
        return list(self._evolution_history)

    @property
    def evolution_level_name(self) -> str:
        return self.intelligence_level.label

    def propose_idea(self, text: str, category: str = "") -> IdeaRequest:
        idea = IdeaRequest(uuid.uuid4().hex[:12], text, category)
        self._idea_queue.put(idea)
        with self._lock:
            self.thoughts.append(f"[idea] {text[:80]}")
        if self._on_idea_callback:
            self._on_idea_callback(idea)
        return idea

    # 智能通知系统 — 优先级 + 速率限制
    def __init_notifications__(self):
        self._notifications: deque = deque(maxlen=50)
        self._notification_timestamps: deque = deque(maxlen=100)
        self._notify_lock = threading.Lock()
        self._notify_callback = None
        self._notification_cooldowns = {
            "critical": 0,
            "warning": 0,
            "info": 0,
            "success": 0,
        }

    def notify(self, message: str, level: str = "info", ttl: float = 10.0) -> bool:
        """发送智能通知 — 速率限制 & 去重"""
        if not hasattr(self, '_notifications'):
            self.__init_notifications__()
        with self._notify_lock:
            now = time.time()
            # 速率检查
            cooldown = self._notification_cooldowns.get(level, 60)
            recent = [t for l, t in self._notification_timestamps if l == level and now - t < cooldown]
            if len(recent) >= 3:  # 同级别通知短时间内最多3条
                return False
            # 去重
            for msg, _, _ in self._notifications:
                if msg[:60] == message[:60]:
                    return False
            self._notifications.appendleft((message, level, now))
            self._notification_timestamps.append((level, now))
            if self._notify_callback:
                try:
                    self._notify_callback(message, level, ttl)
                except Exception:
                    pass
            return True

    def get_recent_thoughts(self, count: int = 6) -> list:
        with self._lock:
            return list(self.thoughts)[-count:]

    def state_duration(self) -> float:
        return time.time() - self.state_start_time


# ═══════════════════════════════════════════════
# 渲染 — 合成到透明色背景，根治黑屏
# ═══════════════════════════════════════════════

# 使用高饱和品红色作为透明键（头像内不会出现此颜色）
TRANSPARENT_COLOR = '#fe01fe'


def _hex_to_rgb(hex_str: str) -> tuple:
    return tuple(int(hex_str[i:i+2], 16) for i in (1, 3, 5))


# [ZERO-AUTO] 重构建议: 函数 _render_circle_avatar 约111行，建议拆分
# [ZERO-AUTO] 重构建议: 函数 _render_circle_avatar 约111行，建议拆分
def _render_circle_avatar(size: int, state: AvatarState, pulse: float,
                          minimized: bool = False,
                          intel_level: IntelligenceLevel = IntelligenceLevel.SOLID) -> ImageTk.PhotoImage:
    """渲染 2D 圆形头像 + 状态指示灯 + 智能等级效果"""
    s = 3 if intel_level >= IntelligenceLevel.THREED else 2
    sw = size * s
    bg_rgb = _hex_to_rgb(TRANSPARENT_COLOR)

    img = Image.new('RGBA', (sw, sw), (*bg_rgb, 255))
    draw = ImageDraw.Draw(img)

    cx = cy = sw // 2
    primary_hex, accent_hex = STATE_COLORS.get(state, ('#58a6ff', '#3fb950'))
    primary = _hex_to_rgb(primary_hex)
    accent = _hex_to_rgb(accent_hex)

    # Lv.2+ 动画脉冲：外发光变强
    glow_r = sw // 2 - s
    glow_mult = 2.0 if intel_level >= IntelligenceLevel.ANIMATED else 1.0
    glow_alpha = int((30 + 20 * pulse) * glow_mult)
    draw.ellipse([cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r],
                 outline=(*primary, min(255, glow_alpha)), width=max(1, 4 * s // 2))

    # Lv.3+ 3D 光照模拟：高光偏移
    if intel_level >= IntelligenceLevel.THREED and not minimized:
        light_offset = int(sw * 0.08)
        # 阴影
        body_r = sw // 2 - 5 * s
        draw.ellipse([cx - body_r + light_offset, cy - body_r + light_offset,
                      cx + body_r + light_offset, cy + body_r + light_offset],
                     fill=(20, 20, 30, 100))
        # 主体
        draw.ellipse([cx - body_r, cy - body_r, cx + body_r, cy + body_r],
                     fill=primary)
        # 高光
        highlight_r = body_r * 3 // 4
        light_rgb = tuple(min(255, c + 80) for c in primary)
        draw.ellipse([cx - highlight_r - light_offset//2,
                      cy - highlight_r - light_offset//2,
                      cx + highlight_r - light_offset//2,
                      cy + highlight_r - light_offset//2],
                     fill=(*light_rgb, 60))
    else:
        # 主体圆
        body_r = sw // 2 - 5 * s
        draw.ellipse([cx - body_r, cy - body_r, cx + body_r, cy + body_r],
                     fill=primary)

    # Lv.1+ 渐变：内圈
    if intel_level >= IntelligenceLevel.GRADIENT and not minimized:
        inner_r = body_r * 2 // 3
        draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
                     fill=accent)

        dot_r = body_r // 4
        bright = tuple(min(255, c + 60) for c in primary)
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
                     fill=bright)

    # Lv.4 完全体：粒子环
    if intel_level >= IntelligenceLevel.FULL and not minimized:
        ring_r = body_r + 3 * s
        num_particles = 6
        for i in range(num_particles):
            angle = (time.time() * 1.5 + i * 2 * math.pi / num_particles) % (2 * math.pi)
            px = int(cx + ring_r * math.cos(angle))
            py = int(cy + ring_r * math.sin(angle))
            p_r = max(1, s * 2)
            draw.ellipse([px - p_r, py - p_r, px + p_r, py + p_r],
                         fill=(*accent, 180))

    # 状态指示灯（右下角小圆点）
    indicator_r = max(3 * s, body_r // 5)
    ix = cx + body_r - indicator_r * 2
    iy = cy + body_r - indicator_r * 2
    state_indicators = {
        AvatarState.LEARNING: (46, 204, 113),
        AvatarState.SEARCHING: (52, 152, 219),
        AvatarState.THINKING: (155, 89, 182),
        AvatarState.DISCOVERING: (241, 196, 15),
        AvatarState.UPGRADING: (230, 126, 34),
        AvatarState.RESTING: (149, 165, 166),
        AvatarState.SLEEPING: (52, 73, 94),
    }
    indicator_color = state_indicators.get(state, (100, 100, 100))
    draw.ellipse([ix - 1*s, iy - 1*s, ix + indicator_r + 1*s, iy + indicator_r + 1*s],
                 fill=(30, 30, 30, 200))
    draw.ellipse([ix, iy, ix + indicator_r, iy + indicator_r],
                 fill=(*indicator_color, 240))

    # Lv.3+ 等级标签
    if intel_level >= IntelligenceLevel.THREED:
        from PIL import ImageFont
        try:
            font = ImageFont.truetype("arial.ttf", sw // 10)
        except Exception:
            font = ImageFont.load_default()
        lv_text = f"Lv.{intel_level.value}"
        bbox = draw.textbbox((0, 0), lv_text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx, ty = sw - tw - 6*s, 4*s
        draw.text((tx, ty), lv_text, fill=(255, 255, 255, 200), font=font)

    display = img.resize((size, size), Image.LANCZOS)
    return ImageTk.PhotoImage(display)


# ═══════════════════════════════════════════════
# 极简桌面挂件
# ═══════════════════════════════════════════════

class SimpleWidget:
    """2D 圆形悬浮头像 — 透明 · 置顶 · 可拖拽 · 悬停放大 · 状态指示灯 · 快速切换"""

    SIZE = 64
    HOVER_SCALE = 1.3  # 悬停放大倍率
    MINI_SIZE = 16     # 最小化尺寸

    def __init__(self, avatar: XiaoLingAvatar, status_callback=None, command_callback=None):
        self.avatar = avatar
        self.status_callback = status_callback
        self.command_callback = command_callback
        self.root: tk.Tk | None = None
        self.canvas: tk.Canvas | None = None
        self.running = False
        self._drag_data = {"x": 0, "y": 0, "dragging": False, "start_x": 0, "start_y": 0}
        self._pulse = 0.0
        self._hwnd = None
        self._popup = None
        self._pos_guard_job = None
        self._single_click_job = None
        self._anim_job = None
        self._hover_job = None
        self._started = threading.Event()
        # 悬停动画
        self._current_scale = 1.0
        self._target_scale = 1.0
        self._hovering = False
        # 快速切换
        self._minimized = False
        self._pre_min_pos = None  # 最小化前的位置

    # ── Win32 窗口样式 ──

    def _get_hwnd(self) -> int | None:
        if not self.root:
            return None
        try:
            return int(self.root.winfo_id())
        except Exception:
            return None

    def _apply_window_style(self):
        """无任务栏图标 + 不抢焦点 + 置顶 + 分层窗口"""
        try:
            import ctypes
            hwnd = self._get_hwnd()
            if not hwnd:
                return
            self._hwnd = hwnd
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_NOACTIVATE = 0x08000000
            WS_EX_LAYERED = 0x00080000
            WS_EX_TOPMOST = 0x00000008

            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style | WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW
            style = style & ~WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002; SWP_NOSIZE = 0x0001
            SWP_NOACTIVATE = 0x0010; SWP_SHOWWINDOW = 0x0040
            ctypes.windll.user32.SetWindowPos(
                hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_SHOWWINDOW
            )
        except Exception:
            pass

    def _ensure_topmost(self):
        if not self._hwnd:
            return
        try:
            import ctypes
            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002; SWP_NOSIZE = 0x0001; SWP_NOACTIVATE = 0x0010
            ctypes.windll.user32.SetWindowPos(
                self._hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
            )
        except Exception:
            pass

    # ── UI 构建 ──

    def _build_ui(self):
        self.root = tk.Tk()
        self.root.title("小零")
        self.root.overrideredirect(True)
        self.root.configure(bg=TRANSPARENT_COLOR)
        self.root.attributes('-transparentcolor', TRANSPARENT_COLOR)
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)
        self.root.withdraw()

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = sw - self.SIZE - 20
        y = sh - self.SIZE - 60
        self.root.geometry(f"{self.SIZE}x{self.SIZE}+{x}+{y}")
        self.root.deiconify()

        self.canvas = tk.Canvas(
            self.root, width=self.SIZE, height=self.SIZE,
            bg=TRANSPARENT_COLOR, highlightthickness=0, bd=0, relief='flat'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 事件绑定
        self.canvas.bind('<Button-1>', self._on_press)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        self.canvas.bind('<Double-Button-1>', self._on_double)
        self.canvas.bind('<Button-3>', self._on_right_click)
        # 悬停缩放
        self.canvas.bind('<Enter>', self._on_hover_enter)
        self.canvas.bind('<Leave>', self._on_hover_leave)

        self.root.protocol('WM_DELETE_WINDOW', self._on_close)

        self.root.after(100, self._apply_window_style)
        self._pos_guard_job = self.root.after(3000, self._pos_guard_loop)

    # ── 交互 ──

    def _on_press(self, event):
        self._single_click_job = None
        self._drag_data["x"] = event.x_root - self.root.winfo_x()
        self._drag_data["y"] = event.y_root - self.root.winfo_y()
        self._drag_data["start_x"] = event.x_root
        self._drag_data["start_y"] = event.y_root
        self._drag_data["dragging"] = False

    def _on_drag(self, event):
        dx = abs(event.x_root - self._drag_data.get("start_x", event.x_root))
        dy = abs(event.y_root - self._drag_data.get("start_y", event.y_root))
        if dx < 4 and dy < 4:
            return
        self._drag_data["dragging"] = True
        x = event.x_root - self._drag_data["x"]
        y = event.y_root - self._drag_data["y"]
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = max(-w + 20, min(sw - 20, x))
        y = max(-h + 20, min(sh - 20, y))
        self.root.geometry(f"+{x}+{y}")

    def _on_release(self, event):
        if self._drag_data.get("dragging"):
            self._drag_data["dragging"] = False
            return
        self._single_click_job = self.root.after(300, self._on_single_click)

    def _on_single_click(self):
        self._single_click_job = None
        self._show_info_popup()

    def _on_hover_enter(self, event):
        if not self._minimized:
            self._target_scale = self.HOVER_SCALE
            self._hovering = True

    def _on_hover_leave(self, event):
        self._target_scale = 1.0
        self._hovering = False

    def _on_double(self, event):
        if self._single_click_job:
            self.root.after_cancel(self._single_click_job)
            self._single_click_job = None
        self._drag_data["dragging"] = False
        self._toggle_minimize()

    def _on_right_click(self, event):
        menu = tk.Menu(self.root, tearoff=0, bg='#161b22', fg='#c9d1d9',
                       activebackground='#0d419d', activeforeground='#ffffff',
                       relief=tk.FLAT, bd=0, font=('Microsoft YaHei', 9))
        menu.add_command(label="● 状态面板", command=self._show_info_popup)
        menu.add_command(label="◐ 最小化/恢复", command=self._toggle_minimize)
        menu.add_command(label="■ 停止学习",
                         command=lambda: self.command_callback("小零，停止学习") if self.command_callback else None)
        menu.add_separator()
        menu.add_command(label="◎ 退出", command=self._on_close)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    # ── 状态弹窗 ──

    def _show_info_popup(self):
        if self._popup and self._popup.winfo_exists():
            self._popup.lift()
            self._popup.focus_force()
            return

        self._popup = tk.Toplevel(self.root)
        self._popup.title("小零状态")
        self._popup.geometry("300x480")
        self._popup.configure(bg='#161b22')
        self._popup.attributes('-topmost', True)

        tk.Label(self._popup, text="◈ 小零 · 运行状态", font=('Microsoft YaHei', 11, 'bold'),
                 fg='#58a6ff', bg='#161b22').pack(pady=8)

        if self.status_callback:
            s = self.status_callback()
            txt = tk.Text(self._popup, height=16, width=38, font=('Consolas', 9),
                          fg='#8b949e', bg='#0d1117', relief=tk.FLAT, padx=10, pady=6)
            txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)
            intel_lv = self.avatar.intelligence_level
            evo_hist = self.avatar.get_evolution_history()
            lines = [
                f"  ★ 智能等级: Lv.{intel_lv.value} {intel_lv.label}",
                f"  状态: {self.avatar.get_state_name()}",
                f"  知识图谱: {s.get('graph_nodes',0)} 节点 / {s.get('graph_edges',0)} 边",
                f"  长期记忆: {s.get('long_term_memory',0)} 条",
                f"  累计知识: {s.get('knowledge_acquired',0)} 条",
                f"  自主循环: {s.get('cycles',0)} 次",
                f"  代码自优化: {self.avatar.code_mod_applied}应用/{self.avatar.code_mod_scanned}扫描",
                f"  成长阶段: {s.get('stage','?')}",
                f"  情感水平: {s.get('emotion_level',0):.0%}",
                f"  地球认知: {s.get('earth_level',0):.0%}",
                f"  运行时长: {s.get('runtime_hours',0):.1f} 小时",
                f"  应急系统: {'正常' if s.get('emergency_ok') else '异常'}",
            ]
            if evo_hist:
                lines.append("  ── 进化历史 ──")
                for ev in evo_hist[-3:]:
                    lines.append(f"  Lv.{ev['from_level']}→{ev['to_level']} {ev['to_name']}")
            txt.insert('1.0', '\n'.join(lines))
            txt.config(state=tk.DISABLED)

        tk.Button(self._popup, text="关闭", command=self._popup.destroy,
                  bg='#21262d', fg='#8b949e', relief=tk.FLAT,
                  font=('Microsoft YaHei', 9)).pack(pady=6)

    # ── 快速切换 ──

    def _toggle_minimize(self):
        if not self.root:
            return
        if self._minimized:
            self._minimized = False
            self._target_scale = 1.0
            if self._pre_min_pos:
                self.root.geometry(f"+{self._pre_min_pos[0]}+{self._pre_min_pos[1]}")
            self.root.geometry(f"{self.SIZE}x{self.SIZE}")
        else:
            self._minimized = True
            self._target_scale = 1.0
            self._pre_min_pos = (self.root.winfo_x(), self.root.winfo_y())
            self.root.geometry(f"{self.MINI_SIZE}x{self.MINI_SIZE}")

    # ── 动画循环 ──

    def _animation_frame(self):
        if not self.running or not self.root:
            return
        try:
            # 平滑缩放过渡
            if abs(self._current_scale - self._target_scale) > 0.02:
                self._current_scale += (self._target_scale - self._current_scale) * 0.25
            else:
                self._current_scale = self._target_scale

            display_size = (self.MINI_SIZE if self._minimized
                            else int(self.SIZE * self._current_scale))
            self._pulse = (math.sin(time.time() * 2.5) + 1) / 2
            img = _render_circle_avatar(display_size, self.avatar.current_state,
                                        self._pulse, self._minimized,
                                        self.avatar.intelligence_level)

            # 缩放时调整窗口大小
            if not self._minimized and self._current_scale != 1.0:
                cur_w = self.root.winfo_width()
                if abs(cur_w - display_size) > 2:
                    x, y = self.root.winfo_x(), self.root.winfo_y()
                    dx = (cur_w - display_size) // 2
                    self.root.geometry(f"{display_size}x{display_size}+{x+dx}+{y+dx}")

            self.canvas.delete("all")
            self.canvas.create_image(display_size // 2, display_size // 2,
                                     image=img, anchor='center')
            self.canvas._ref = img
        except tk.TclError:
            return
        except Exception:
            pass

        if self.running and self.root:
            self._anim_job = self.root.after(50, self._animation_frame)

    # ── 窗口位置保护 ──

    def _pos_guard_loop(self):
        if not self.running:
            return
        try:
            self._ensure_topmost()
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            w = self.root.winfo_width()
            h = self.root.winfo_height()
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            nx = max(-w + 20, min(sw - 20, x))
            ny = max(-h + 20, min(sh - 20, y))
            if nx != x or ny != y:
                self.root.geometry(f"+{nx}+{ny}")
        except Exception:
            pass
        if self.running and self.root:
            self._pos_guard_job = self.root.after(3000, self._pos_guard_loop)

    # ── 启动 / 停止 ──

    def start(self):
        self.running = True
        self._build_ui()
        self._started.set()
        self.root.after(100, self._animation_frame)
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_close()

    def _on_close(self, event=None):
        self.running = False
        for job in [self._pos_guard_job, self._single_click_job, self._anim_job, self._hover_job]:
            if job and self.root:
                try:
                    self.root.after_cancel(job)
                except Exception:
                    pass
        if self._popup and self._popup.winfo_exists():
            try:
                self._popup.destroy()
            except Exception:
                pass
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except Exception:
                pass

    def apply_theme(self, theme: str):
        """应用主题切换 (dark/light)"""
        if not self.root or not self.canvas:
            return
        if theme == "dark":
            self.root.configure(bg=TRANSPARENT_COLOR)
        else:
            self.root.configure(bg=TRANSPARENT_COLOR)
        self._ensure_topmost()


if __name__ == '__main__':
    avatar = XiaoLingAvatar()
    print('\n=== 小零 · 极简悬浮头像 ===\n')
    for s in [AvatarState.BOOTING, AvatarState.LEARNING, AvatarState.RESTING, AvatarState.THINKING]:
        avatar.set_state(s, f"状态: {s.value}")
        print(f'  {avatar.get_state_name()}')
    print('\n启动极简悬浮头像 (需要 Windows 桌面环境)...')
    SimpleWidget(avatar).start()