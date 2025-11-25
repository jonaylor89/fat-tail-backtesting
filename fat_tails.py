import math

import numpy as np
from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    RED,
    RIGHT,
    UP,
    YELLOW,
    Axes,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Group,
    Line,
    Scene,
    Text,
    Transform,
    VGroup,
    VMobject,
    Write,
    rush_into,
)

# random seed for reproducibility
np.random.seed(42)


class FatTailsPresentation(Scene):
    def construct(self):
        # --- Part 1: The Gaussian Illusion ---

        # Title
        title = Text("The Illusion of Normality", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Axes for distribution
        axes = (
            Axes(
                x_range=[-4, 4, 1],
                y_range=[0, 0.5, 0.1],
                x_length=6,
                y_length=3,
                axis_config={"include_tip": False},
            )
            .to_edge(LEFT)
            .shift(DOWN * 0.5)
        )

        # axes_labels = axes.get_axis_labels(x_label="Return", y_label="Prob")
        x_label = Text("Return", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = Text("Prob", font_size=24).next_to(axes.y_axis, UP)
        axes_labels = VGroup(x_label, y_label)

        # Gaussian Curve
        gaussian = axes.plot(
            lambda x: (1 / (math.sqrt(2 * math.pi))) * math.exp(-0.5 * x**2), color=BLUE
        )
        gaussian_label = Text("Gaussian", color=BLUE, font_size=24).next_to(
            gaussian, UP
        )

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(gaussian), Write(gaussian_label))
        self.wait(1)

        # Simulating a Gaussian Price Path
        # 100 steps
        n_steps = 100
        gaussian_returns = np.random.normal(0.05, 0.5, n_steps)  # Slight drift up
        gaussian_prices = np.cumsum(gaussian_returns)

        # Axes for Price
        price_axes = (
            Axes(
                x_range=[0, n_steps, 20],
                y_range=[-5, 15, 5],
                x_length=6,
                y_length=3,
                axis_config={"include_tip": False},
            )
            .to_edge(RIGHT)
            .shift(DOWN * 0.5)
        )

        # price_labels = price_axes.get_axis_labels(x_label="Time", y_label="Price")
        p_x_label = Text("Time", font_size=24).next_to(price_axes.x_axis, RIGHT)
        p_y_label = Text("Price", font_size=24).next_to(price_axes.y_axis, UP)
        price_labels = VGroup(p_x_label, p_y_label)

        # Plotting the path
        # We create points for the path
        points = [price_axes.c2p(0, 0)]
        for i in range(1, n_steps):
            points.append(price_axes.c2p(i, gaussian_prices[i]))

        price_path = VMobject()
        price_path.set_points_as_corners(points)
        price_path.set_color(GREEN)

        self.play(Create(price_axes), Write(price_labels))
        self.play(Create(price_path, run_time=3))

        # Result text
        result_text = Text("Steady Growth", color=GREEN, font_size=36).next_to(
            price_axes, UP
        )
        self.play(Write(result_text))
        self.wait(2)

        # Clear Scene
        self.play(
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(gaussian),
            FadeOut(gaussian_label),
            FadeOut(price_axes),
            FadeOut(price_labels),
            FadeOut(price_path),
            FadeOut(result_text),
            FadeOut(title),
        )

        # --- Part 2: Fat Tails Reality ---

        title2 = Text("Reality: Fat Tails", font_size=48, color=RED)
        self.play(Write(title2))
        self.play(title2.animate.to_edge(UP))

        # Axes again (same setup)
        axes2 = (
            Axes(x_range=[-6, 6, 2], y_range=[0, 0.5, 0.1], x_length=6, y_length=3)
            .to_edge(LEFT)
            .shift(DOWN * 0.5)
        )

        # Gaussian (Ghost)
        gaussian_ghost = axes2.plot(
            lambda x: (1 / (math.sqrt(2 * math.pi))) * math.exp(-0.5 * x**2),
            color=BLUE,
            fill_opacity=0,
        )

        # Fat Tail (Cauchy/Student-t proxy)
        # Using Cauchy for dramatic effect: 1 / (pi * (1 + x^2))
        fat_tail = axes2.plot(
            lambda x: 1 / (math.pi * (1 + (x / 0.5) ** 2)) * 0.5, color=RED
        )
        fat_tail_label = Text("Fat Tailed", color=RED, font_size=24).next_to(
            fat_tail, UP
        )

        self.play(Create(axes2))
        self.play(Create(gaussian_ghost))
        self.play(Transform(gaussian_ghost, fat_tail), Write(fat_tail_label))
        self.wait(1)

        # Simulating Fat Tail Price Path
        # Mixture of Gaussian + occasional large shocks
        fat_returns = np.random.normal(0.05, 0.5, n_steps)
        # Add shocks
        shock_indices = np.random.choice(n_steps, 5, replace=False)
        fat_returns[shock_indices] -= np.random.uniform(3, 6, 5)  # Massive drops

        fat_prices = np.cumsum(fat_returns)

        # Axes for Price
        price_axes2 = (
            Axes(
                x_range=[0, n_steps, 20], y_range=[-20, 10, 10], x_length=6, y_length=3
            )
            .to_edge(RIGHT)
            .shift(DOWN * 0.5)
        )

        points2 = [price_axes2.c2p(0, 0)]
        for i in range(1, n_steps):
            points2.append(price_axes2.c2p(i, fat_prices[i]))

        price_path2 = VMobject()
        price_path2.set_points_as_corners(points2)
        price_path2.set_color(RED)

        self.play(Create(price_axes2))
        self.play(Create(price_path2, run_time=3))

        crash_text = Text("CRASH", color=RED, font_size=36).next_to(price_axes2, DOWN)
        self.play(Write(crash_text))
        self.wait(2)

        self.play(
            FadeOut(axes2),
            FadeOut(gaussian_ghost),
            FadeOut(fat_tail),
            FadeOut(fat_tail_label),
            FadeOut(price_axes2),
            FadeOut(price_path2),
            FadeOut(crash_text),
            FadeOut(title2),
        )

        # --- Part 3: Convex vs Concave ---

        title3 = Text("Payoff Profiles", font_size=48)
        self.play(Write(title3))
        self.play(title3.animate.to_edge(UP))

        # Axes
        payoff_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 4, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.5)

        # labels = payoff_axes.get_axis_labels(x_label="Market Move", y_label="Profit/Loss")
        pay_x_label = Text("Market Move", font_size=24).next_to(
            payoff_axes.x_axis, RIGHT
        )
        pay_y_label = Text("Profit/Loss", font_size=24).next_to(payoff_axes.y_axis, UP)
        labels = VGroup(pay_x_label, pay_y_label)

        # Concave Curve (Selling Volatility)
        # e.g. y = 1 - e^(-x) is bounded? Let's use -x^2 shifted or something simpler to visualize
        # The blog uses: Concave = 1 - exp(-4x) (for x>0?), Convex = exp(4x) - 1
        # Let's stick to the visual concept:
        # Concave: Small gains usually, huge loss on big moves.
        # Convex: Small losses usually, huge gain on big moves.

        # Let's use simple exponentials for visual clarity over the range [-2, 2]
        # Convex: y = x^2 (if long straddle) or e^x
        # Let's use the blog's idea roughly.

        convex_curve = payoff_axes.plot(
            lambda x: 0.5 * (math.exp(x) - 1), x_range=[-2, 2.5], color=GREEN
        )
        convex_label = Text("Convex (Antifragile)", color=GREEN, font_size=24).next_to(
            convex_curve, UP
        )

        concave_curve = payoff_axes.plot(
            lambda x: 0.5 * (1 - math.exp(x)), x_range=[-2, 2.5], color=RED
        )
        concave_label = Text("Concave (Fragile)", color=RED, font_size=24).next_to(
            concave_curve, DOWN
        )

        self.play(Create(payoff_axes), Write(labels))
        self.play(Create(convex_curve), Write(convex_label))
        self.play(Create(concave_curve), Write(concave_label))

        # Animate a "Black Swan" event
        # A dot moves far to the right (large market move)

        dot_convex = Dot(color=GREEN).move_to(payoff_axes.c2p(0, 0))
        dot_concave = Dot(color=RED).move_to(payoff_axes.c2p(0, 0))

        self.play(FadeIn(dot_convex), FadeIn(dot_concave))

        # Move normal
        self.play(
            dot_convex.animate.move_to(payoff_axes.c2p(0.5, 0.5 * (math.exp(0.5) - 1))),
            dot_concave.animate.move_to(
                payoff_axes.c2p(0.5, 0.5 * (1 - math.exp(0.5)))
            ),
            run_time=1,
        )
        self.wait(0.5)

        # Move Extreme
        self.play(
            dot_convex.animate.move_to(payoff_axes.c2p(2.2, 0.5 * (math.exp(2.2) - 1))),
            dot_concave.animate.move_to(
                payoff_axes.c2p(2.2, 0.5 * (1 - math.exp(2.2)))
            ),
            run_time=1.5,
            rate_func=rush_into,
        )

        # Highlight the difference
        line_diff = Line(
            dot_convex.get_center(), dot_concave.get_center(), color=YELLOW
        )
        self.play(Create(line_diff))
        self.wait(2)

        self.play(
            FadeOut(
                Group(
                    payoff_axes,
                    labels,
                    convex_curve,
                    convex_label,
                    concave_curve,
                    concave_label,
                    dot_convex,
                    dot_concave,
                    line_diff,
                    title3,
                )
            )
        )

        final_text = Text("Backtest for Convexity.", font_size=36)
        self.play(Write(final_text))
        self.wait(3)
