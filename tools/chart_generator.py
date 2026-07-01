"""
Generates chart PNG files for the weekly AI intelligence slide deck.
Brand colors: primary #1B3A6B, accent #4A9EDB, light #E8F4FD
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

PRIMARY = "#1B3A6B"
ACCENT = "#4A9EDB"
LIGHT = "#E8F4FD"
WHITE = "#FFFFFF"
GRAY = "#8B9BB4"


def _style():
    plt.rcParams.update(
        {
            "figure.facecolor": PRIMARY,
            "axes.facecolor": "#0F2347",
            "axes.edgecolor": ACCENT,
            "axes.labelcolor": WHITE,
            "xtick.color": GRAY,
            "ytick.color": WHITE,
            "text.color": WHITE,
            "grid.color": "#2A4A7A",
            "grid.linewidth": 0.5,
            "font.family": "DejaVu Sans",
            "font.size": 11,
        }
    )


def trending_topics_chart(themes: list[dict], output_path: str) -> str:
    """
    Horizontal bar chart of trending AI themes.
    themes: [{"name": str, "score": int, "video_count": int}, ...]
    """
    _style()
    themes_sorted = sorted(themes, key=lambda t: t["score"])
    names = [t["name"] for t in themes_sorted]
    scores = [t["score"] for t in themes_sorted]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(names, scores, color=ACCENT, height=0.6)

    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_width() + max(scores) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{score:,}",
            va="center",
            color=WHITE,
            fontsize=9,
        )

    ax.set_xlabel("Trend Score (video count × avg views)", color=GRAY, fontsize=9)
    ax.set_title("Trending AI Topics This Week", color=WHITE, fontsize=13, fontweight="bold", pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#2A4A7A")
    ax.set_xlim(0, max(scores) * 1.15)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=PRIMARY)
    plt.close()
    return output_path


def top_videos_chart(videos: list[dict], output_path: str) -> str:
    """
    Horizontal bar chart: top 10 videos by view count.
    videos: list of video dicts with title, views, channel
    """
    _style()
    top = videos[:10]
    labels = [v["title"][:45] + "…" if len(v["title"]) > 45 else v["title"] for v in reversed(top)]
    views = [v["views"] for v in reversed(top)]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [ACCENT if i % 2 == 0 else "#2E6DB4" for i in range(len(labels))]
    bars = ax.barh(labels, views, color=colors, height=0.65)

    def fmt(n):
        return f"{n/1e6:.1f}M" if n >= 1e6 else f"{n/1e3:.0f}K"

    for bar, v in zip(bars, views):
        ax.text(
            bar.get_width() + max(views) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            fmt(v),
            va="center",
            color=WHITE,
            fontsize=8.5,
        )

    ax.set_xlabel("Views", color=GRAY, fontsize=9)
    ax.set_title("Top 10 Videos This Week", color=WHITE, fontsize=13, fontweight="bold", pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#2A4A7A")
    ax.set_xlim(0, max(views) * 1.18)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=PRIMARY)
    plt.close()
    return output_path


def channel_subscribers_chart(channels: list[dict], output_path: str) -> str:
    """
    Bar chart of top channels by subscriber count.
    channels: [{"name": str, "subscribers": int}, ...]
    """
    _style()
    top = channels[:6]
    names = [c["name"] for c in top]
    subs = [c["subscribers"] for c in top]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(names))
    bars = ax.bar(x, subs, color=ACCENT, width=0.55)

    def fmt(n):
        return f"{n/1e6:.1f}M" if n >= 1e6 else f"{n/1e3:.0f}K"

    for bar, s in zip(bars, subs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(subs) * 0.015,
            fmt(s),
            ha="center",
            color=WHITE,
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Subscribers", color=GRAY, fontsize=9)
    ax.set_title("Top Channels in AI Space", color=WHITE, fontsize=13, fontweight="bold", pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(subs) * 1.18)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=PRIMARY)
    plt.close()
    return output_path


def engagement_scatter(videos: list[dict], output_path: str) -> str:
    """
    Scatter: views (x) vs. like rate (y). Size = comment count.
    Shows what's both popular AND resonating.
    """
    _style()
    top = [v for v in videos[:30] if v["views"] > 0 and v["likes"] > 0]
    if not top:
        return None

    views = [v["views"] for v in top]
    like_rate = [v["likes"] / v["views"] * 100 for v in top]
    comments = [max(v["comments"], 10) for v in top]
    sizes = [min(c / max(comments) * 300, 300) + 30 for c in comments]

    fig, ax = plt.subplots(figsize=(9, 5))
    sc = ax.scatter(views, like_rate, s=sizes, c=ACCENT, alpha=0.7, edgecolors=PRIMARY, linewidths=0.5)

    ax.set_xlabel("Total Views", color=GRAY, fontsize=9)
    ax.set_ylabel("Like Rate (%)", color=GRAY, fontsize=9)
    ax.set_title("Views vs. Engagement Rate", color=WHITE, fontsize=13, fontweight="bold", pad=12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(alpha=0.3)

    note = mpatches.Patch(color=ACCENT, label="Bubble size = comment count")
    ax.legend(handles=[note], loc="upper right", framealpha=0.3, labelcolor=WHITE, fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=PRIMARY)
    plt.close()
    return output_path
