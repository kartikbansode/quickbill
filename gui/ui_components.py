"""
QuickBill UI Components — Unified Design System
=================================================

Provides reusable button factories, confirmation dialogs, tooltips,
and design tokens for consistent styling across the entire application.

Usage:
    from gui.ui_components import (
        create_primary_button, create_success_button,
        create_danger_button, create_warning_button,
        create_secondary_button, set_button_state,
        show_confirmation, show_error, show_info, show_warning,
        show_choice, ToolTip,
        PRIMARY, SUCCESS, DANGER, WARNING, SECONDARY,
        FONT_BUTTON, FONT_LABEL, BG_CARD, TEXT_DARK, ...
    )
"""

import tkinter as tk


# ============================================================
# DESIGN TOKENS — Colors
# ============================================================

PRIMARY = "#2563eb"
PRIMARY_HOVER = "#1d4ed8"

SUCCESS = "#16a34a"
SUCCESS_HOVER = "#15803d"

DANGER = "#dc2626"
DANGER_HOVER = "#b91c1c"

WARNING = "#f59e0b"
WARNING_HOVER = "#d97706"

SECONDARY = "#64748b"
SECONDARY_HOVER = "#475569"

# Backgrounds
BG_MAIN = "#e9ecef"
BG_CARD = "#ffffff"
BG_HEADER = "#1d3557"
BG_STATUSBAR = "#1f2937"
BG_TOOLBAR = "#e5e7eb"
BG_DISABLED = "#94a3b8"

# Text
TEXT_DARK = "#1f2937"
TEXT_LIGHT = "#ffffff"
TEXT_MUTED = "#6b7280"
TEXT_DISABLED = "#9ca3af"

# Borders
BORDER_LIGHT = "#d1d5db"


# ============================================================
# DESIGN TOKENS — Fonts
# ============================================================

FONT_HEADING = ("Segoe UI", 18, "bold")
FONT_SUBHEADING = ("Segoe UI", 14, "bold")
FONT_SECTION = ("Segoe UI", 11, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_LABEL_BOLD = ("Segoe UI", 10, "bold")
FONT_BUTTON = ("Segoe UI", 9, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_INPUT = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 12)
FONT_TOTAL_LARGE = ("Segoe UI", 20, "bold")


# ============================================================
# BUTTON FACTORY
# ============================================================

def _create_button(parent, text, command, bg, hover_bg, fg=None,
                   width=14, height=2, font=None, state="normal", **kwargs):
    """Internal: create a styled button with hover effects."""
    if fg is None:
        fg = TEXT_LIGHT
    if font is None:
        font = FONT_BUTTON

    is_disabled = (state == "disabled")

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=BG_DISABLED if is_disabled else bg,
        fg=TEXT_DISABLED if is_disabled else fg,
        activebackground=hover_bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        width=width,
        height=height,
        font=font,
        cursor="" if is_disabled else "hand2",
        state=state,
        **kwargs,
    )

    # Store style metadata for state restoration
    btn._qb_style = {"bg": bg, "hover": hover_bg, "fg": fg}

    def _on_enter(e):
        if str(btn.cget("state")) != "disabled":
            btn.config(bg=hover_bg)

    def _on_leave(e):
        if str(btn.cget("state")) != "disabled":
            btn.config(bg=btn._qb_style["bg"])

    btn.bind("<Enter>", _on_enter)
    btn.bind("<Leave>", _on_leave)

    return btn


def create_primary_button(parent, text, command=None, **kwargs):
    """Blue button for important actions (Add, Save, Confirm, Search, View)."""
    return _create_button(parent, text, command, PRIMARY, PRIMARY_HOVER, **kwargs)


def create_success_button(parent, text, command=None, **kwargs):
    """Green button for positive/completion actions (Complete, Generate, Save)."""
    return _create_button(parent, text, command, SUCCESS, SUCCESS_HOVER, **kwargs)


def create_danger_button(parent, text, command=None, **kwargs):
    """Red button for destructive actions (Delete, Clear, Remove, Exit)."""
    return _create_button(parent, text, command, DANGER, DANGER_HOVER, **kwargs)


def create_warning_button(parent, text, command=None, **kwargs):
    """Amber button for risky/cautionary actions (Hold, Reset, Cancel Bill)."""
    return _create_button(parent, text, command, WARNING, WARNING_HOVER,
                          fg=TEXT_DARK, **kwargs)


def create_secondary_button(parent, text, command=None, **kwargs):
    """Gray button for neutral actions (Cancel, Back, Close, Refresh)."""
    return _create_button(parent, text, command, SECONDARY, SECONDARY_HOVER, **kwargs)


def set_button_state(btn, state):
    """Enable or disable a styled button with correct visual appearance."""
    style = getattr(btn, "_qb_style", None)
    if style is None:
        btn.config(state=state)
        return
    if state == "disabled":
        btn.config(state="disabled", bg=BG_DISABLED, fg=TEXT_DISABLED, cursor="")
    else:
        btn.config(state="normal", bg=style["bg"], fg=style["fg"], cursor="hand2")


# ============================================================
# CONFIRMATION DIALOG SYSTEM
# ============================================================

_DIALOG_STYLES = {
    "info":    {"color": PRIMARY, "icon": "\u2139"},
    "success": {"color": SUCCESS, "icon": "\u2713"},
    "warning": {"color": WARNING, "icon": "\u26A0"},
    "error":   {"color": DANGER,  "icon": "\u2715"},
    "confirm": {"color": PRIMARY, "icon": "?"},
    "danger":  {"color": DANGER,  "icon": "\u26A0"},
    "primary": {"color": PRIMARY, "icon": "\u2139"},
}


class _QuickBillDialog(tk.Toplevel):
    """QuickBill-styled modal dialog."""

    def __init__(self, parent, title, message, dialog_type="info",
                 buttons=None, detail=None):
        super().__init__(parent)
        self.result = None

        style = _DIALOG_STYLES.get(dialog_type, _DIALOG_STYLES["info"])
        accent = style["color"]
        icon_char = style["icon"]

        self.title(title)
        self.configure(bg=BG_CARD)
        self.resizable(False, False)
        self.overrideredirect(False)

        try:
            if parent.winfo_viewable():
                self.transient(parent)
        except tk.TclError:
            pass

        # --- Colored Header Bar ---
        header = tk.Frame(self, bg=accent, height=48)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"  {icon_char}   {title}",
            bg=accent,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        ).pack(side="left", fill="x", padx=8, expand=True)

        # --- Message Body ---
        body = tk.Frame(self, bg=BG_CARD)
        body.pack(fill="both", expand=True, padx=24, pady=(20, 16))

        tk.Label(
            body,
            text=message,
            bg=BG_CARD,
            fg=TEXT_DARK,
            font=FONT_LABEL,
            wraplength=360,
            justify="left",
            anchor="w",
        ).pack(fill="x", anchor="w")

        if detail:
            tk.Label(
                body,
                text=detail,
                bg=BG_CARD,
                fg=TEXT_MUTED,
                font=FONT_SMALL,
                wraplength=360,
                justify="left",
                anchor="w",
            ).pack(fill="x", anchor="w", pady=(8, 0))

        # --- Separator ---
        tk.Frame(self, bg=BORDER_LIGHT, height=1).pack(fill="x")

        # --- Button Row ---
        btn_frame = tk.Frame(self, bg=BG_CARD)
        btn_frame.pack(fill="x", padx=20, pady=14)

        _factory_map = {
            "primary": create_primary_button,
            "success": create_success_button,
            "danger": create_danger_button,
            "warning": create_warning_button,
            "secondary": create_secondary_button,
        }

        if buttons:
            for btn_text, btn_style, btn_value in reversed(buttons):
                factory = _factory_map.get(btn_style, create_secondary_button)
                b = factory(
                    btn_frame,
                    btn_text,
                    command=lambda v=btn_value: self._close(v),
                    width=14,
                    height=1,
                )
                b.pack(side="right", padx=(5, 0))

            # Enter confirms the last button (primary action)
            self.bind("<Return>", lambda e: self._close(buttons[-1][2]))

        # Escape always cancels
        self.bind("<Escape>", lambda e: self._close(None))
        self.protocol("WM_DELETE_WINDOW", lambda: self._close(None))

        # --- Center on parent ---
        self.update_idletasks()
        w = max(self.winfo_reqwidth(), 420)
        h = self.winfo_reqheight()
        self.geometry(f"{w}x{h}")
        self.update_idletasks()

        try:
            px = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
            py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        except tk.TclError:
            px, py = 200, 200
        self.geometry(f"+{max(0, px)}+{max(0, py)}")

        self.grab_set()
        self.focus_force()
        self.wait_window()

    def _close(self, value):
        self.result = value
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()


def show_confirmation(parent, title, message, confirm_text="Confirm",
                      cancel_text="Cancel", style="danger", detail=None):
    """Two-button confirmation dialog. Returns True if confirmed, else False."""
    buttons = [
        (cancel_text, "secondary", False),
        (confirm_text, style, True),
    ]
    dlg = _QuickBillDialog(parent, title, message, dialog_type=style,
                           buttons=buttons, detail=detail)
    return dlg.result is True


def show_warning(parent, title, message, detail=None):
    """Warning dialog with OK button."""
    buttons = [("OK", "warning", True)]
    _QuickBillDialog(parent, title, message, dialog_type="warning",
                     buttons=buttons, detail=detail)


def show_error(parent, title, message, detail=None):
    """Error dialog with OK button."""
    buttons = [("OK", "danger", True)]
    _QuickBillDialog(parent, title, message, dialog_type="error",
                     buttons=buttons, detail=detail)


def show_info(parent, title, message, detail=None):
    """Informational dialog with OK button."""
    buttons = [("OK", "primary", True)]
    _QuickBillDialog(parent, title, message, dialog_type="info",
                     buttons=buttons, detail=detail)


def show_choice(parent, title, message, choices, detail=None,
                dialog_type="warning"):
    """Multi-choice dialog.

    Args:
        choices: list of (text, style, return_value) tuples.
    Returns:
        The return_value of the chosen button, or None if cancelled.
    """
    dlg = _QuickBillDialog(parent, title, message, dialog_type=dialog_type,
                           buttons=choices, detail=detail)
    return dlg.result


# ============================================================
# TOOLTIP
# ============================================================

class ToolTip:
    """Lightweight hover tooltip for any widget."""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self._show, add="+")
        self.widget.bind("<Leave>", self._hide, add="+")

    def _show(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2 - 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 2

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)

        tk.Label(
            tw,
            text=self.text,
            bg="#1f2937",
            fg="#f9fafb",
            font=("Segoe UI", 8),
            padx=8,
            pady=3,
            relief="solid",
            bd=0,
        ).pack()

    def _hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

    def update_text(self, new_text):
        """Update tooltip text dynamically."""
        self.text = new_text
