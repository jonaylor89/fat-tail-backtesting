from manim import *
import random
import numpy as np

# Set seed for reproducibility across the whole scene
random.seed(42)

class CombinedGaltonScene(Scene):
    def construct(self):
        # Title
        title = Text("The Galton Board", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # --- Part 1: Normal Distribution ---
        self.show_phase_title("Part 1: The Order of Chaos\n(Normal Distribution)")
        
        # Create Normal Board
        self.pegs, self.bins, self.floor = self.create_normal_board_objects()
        self.play(Create(self.pegs), Create(self.bins), Create(self.floor))
        
        # Run Normal Balls
        self.run_balls(distribution="normal")
        
        # Clear balls only
        self.play(FadeOut(self.balls), FadeOut(self.histogram_bars))
        
        # --- Part 2: Lognormal Distribution ---
        self.show_phase_title("Part 2: The Multiplicative World\n(Lognormal Distribution)")
        
        # Create Lognormal Board Objects (Target)
        target_pegs, target_bins, target_floor = self.create_lognormal_board_objects()
        
        # Interpolate Board
        self.play(
            Transform(self.pegs, target_pegs),
            Transform(self.bins, target_bins),
            Transform(self.floor, target_floor),
            run_time=2
        )
        self.wait(0.5)
        
        # Run Lognormal Balls
        self.run_balls(distribution="lognormal")
        
        # Clear balls
        self.play(FadeOut(self.balls), FadeOut(self.histogram_bars))
        
        # --- Part 3: Pareto Distribution ---
        self.show_phase_title("Part 3: The Rich Get Richer\n(Pareto Distribution)")
        
        # Create Pareto Board Objects (Target)
        # Same geometry as Lognormal, but pegs change appearance
        pareto_pegs, _, _ = self.create_pareto_board_objects()
        
        # Transform Pegs to show bias
        self.play(Transform(self.pegs, pareto_pegs), run_time=2)
        self.wait(0.5)
        
        # Run Pareto Balls
        self.run_balls(distribution="pareto")
        
        self.wait(2)

    def show_phase_title(self, text):
        phase_title = Text(text, font_size=36).to_edge(UP)
        if hasattr(self, 'current_title'):
            self.play(FadeOut(self.current_title), FadeIn(phase_title))
        else:
            self.play(FadeOut(self.mobjects[0]), FadeIn(phase_title))
        
        self.current_title = phase_title
        self.wait(2)

    def create_normal_board_objects(self):
        GRID_SIZE = 0.35
        ROWS = 12
        START_Y = 3.0
        
        pegs = VGroup()
        for row in range(ROWS):
            for col in range(row + 1):
                x = (col - row / 2) * GRID_SIZE
                y = START_Y - row * GRID_SIZE
                peg = Dot(point=[x, y, 0], radius=0.05, color=WHITE)
                pegs.add(peg)
        
        bins = VGroup()
        bin_height = 1.5
        bin_y_top = START_Y - ROWS * GRID_SIZE + GRID_SIZE / 2
        bin_y_bottom = bin_y_top - bin_height
        
        for i in range(ROWS + 2):
            x = (i - (ROWS + 1) / 2) * GRID_SIZE
            line = Line(start=[x, bin_y_top, 0], end=[x, bin_y_bottom, 0], color=GRAY, stroke_width=2)
            bins.add(line)
            
        floor_width = (ROWS + 1) * GRID_SIZE
        floor = Line(start=[-floor_width/2, bin_y_bottom, 0], end=[floor_width/2, bin_y_bottom, 0], color=GRAY, stroke_width=2)
        
        return pegs, bins, floor

    def create_lognormal_board_objects(self):
        ROWS = 12
        BASE = 1.3
        DY = 0.45
        START_Y = 3.2
        X_SCALE = 2.0
        
        def get_x(row, col):
            exponent = col - row / 2
            val = BASE ** exponent
            min_x = BASE ** (-ROWS/2)
            max_x = BASE ** (ROWS/2)
            mid_x = (min_x + max_x) / 2
            return (val - mid_x) * X_SCALE

        pegs = VGroup()
        for row in range(ROWS):
            for col in range(row + 1):
                x = get_x(row, col)
                y = START_Y - row * DY
                peg = Dot(point=[x, y, 0], radius=0.05, color=WHITE)
                pegs.add(peg)
        
        bins = VGroup()
        bin_y_top = START_Y - ROWS * DY + DY / 2
        bin_y_bottom = bin_y_top - 1.5
        
        for i in range(ROWS + 2):
            exponent = i - ROWS / 2 - 0.5
            val = BASE ** exponent
            min_x = BASE ** (-ROWS/2)
            max_x = BASE ** (ROWS/2)
            mid_x = (min_x + max_x) / 2
            x = (val - mid_x) * X_SCALE
            bins.add(Line(start=[x, bin_y_top, 0], end=[x, bin_y_bottom, 0], color=GRAY, stroke_width=2))
            
        div_0_exp = 0 - ROWS/2 - 0.5
        div_last_exp = (ROWS + 1) - ROWS/2 - 0.5
        def transform_x(val):
             min_x = BASE ** (-ROWS/2)
             max_x = BASE ** (ROWS/2)
             mid_x = (min_x + max_x) / 2
             return (val - mid_x) * X_SCALE
        floor = Line(start=[transform_x(BASE**div_0_exp), bin_y_bottom, 0], end=[transform_x(BASE**div_last_exp), bin_y_bottom, 0], color=GRAY, stroke_width=2)
        
        return pegs, bins, floor

    def create_pareto_board_objects(self):
        # Same geometry as Lognormal
        ROWS = 12
        BASE = 1.3
        DY = 0.45
        START_Y = 3.2
        X_SCALE = 2.0
        
        ALPHA = 1.0
        BETA = 3.0
        
        def get_x(row, col):
            exponent = col - row / 2
            val = BASE ** exponent
            min_x = BASE ** (-ROWS/2)
            max_x = BASE ** (ROWS/2)
            mid_x = (min_x + max_x) / 2
            return (val - mid_x) * X_SCALE

        pegs = VGroup()
        for row in range(ROWS):
            for col in range(row + 1):
                x = get_x(row, col)
                y = START_Y - row * DY
                
                # Calculate Probability of Right Turn
                # P(Right) = (k + alpha) / (n + alpha + beta)
                # k = col (number of right turns so far)
                # n = row (number of steps so far)
                prob_right = (col + ALPHA) / (row + ALPHA + BETA)
                
                # Visuals based on probability
                # 0.5 -> Neutral (White, Upright)
                # > 0.5 -> Right Bias (Red, Tilted Right)
                # < 0.5 -> Left Bias (Blue, Tilted Left)
                
                # Color interpolation
                color = interpolate_color(BLUE, RED, prob_right)
                
                # Rotation
                # 0.5 -> 0 degrees
                # 1.0 -> -45 degrees (-PI/4)
                # 0.0 -> +45 degrees (+PI/4)
                angle = (0.5 - prob_right) * PI / 2 # 90 degrees range
                
                # Shape: Triangle
                peg = Triangle(fill_opacity=1, color=color).scale(0.08).move_to([x, y, 0])
                peg.rotate(angle)
                
                pegs.add(peg)
        
        # Bins and floor are same as lognormal, re-create or reuse
        # We only need pegs for transform really, but for completeness:
        bins = VGroup() # Placeholder if needed, but we won't transform bins
        floor = VGroup()
        
        return pegs, bins, floor

    def run_balls(self, distribution):
        ROWS = 12
        BALL_RADIUS = 0.06
        TOTAL_BALLS = 100
        
        # Determine constants based on current board state (approximated from pegs)
        # Actually we need the logic constants.
        # Normal:
        NORM_GRID_SIZE = 0.35
        NORM_START_Y = 3.0
        
        # Lognormal/Pareto:
        LOG_BASE = 1.3
        LOG_DY = 0.45
        LOG_START_Y = 3.2
        LOG_X_SCALE = 2.0
        
        def get_log_x(row, col):
            exponent = col - row / 2
            val = LOG_BASE ** exponent
            min_x = LOG_BASE ** (-ROWS/2)
            max_x = LOG_BASE ** (ROWS/2)
            mid_x = (min_x + max_x) / 2
            return (val - mid_x) * LOG_X_SCALE

        counts = [0] * (ROWS + 1)
        self.balls = VGroup()
        self.histogram_bars = VGroup() # To track stacked balls if we wanted to fade them, but balls VGroup has them all
        
        animations = []
        
        # Color based on distribution
        color = BLUE if distribution == "normal" else (GREEN if distribution == "lognormal" else RED)
        
        for _ in range(TOTAL_BALLS):
            # Start position
            if distribution == "normal":
                start_pos = [0, NORM_START_Y + NORM_GRID_SIZE, 0]
            else:
                start_pos = [get_log_x(0,0), LOG_START_Y + LOG_DY, 0]
                
            ball = Circle(radius=BALL_RADIUS, color=color, fill_opacity=1).move_to(start_pos)
            self.balls.add(ball)
            
            path_points = [np.array(start_pos)]
            col_index = 0
            
            # Simulation
            if distribution == "normal":
                current_x = 0
                current_y = NORM_START_Y + NORM_GRID_SIZE
                for row in range(ROWS):
                    current_y -= NORM_GRID_SIZE
                    direction = random.choice([-1, 1])
                    current_x += direction * NORM_GRID_SIZE / 2
                    if direction == 1: col_index += 1
                    path_points.append(np.array([current_x, current_y, 0]))
                
                # Bin bottom
                bin_y_bottom = NORM_START_Y - ROWS * NORM_GRID_SIZE + NORM_GRID_SIZE / 2 - 1.5
                final_x = current_x # Normal board balls fall straight down roughly
                
            else:
                # Lognormal / Pareto
                current_x = get_log_x(0,0)
                current_y = LOG_START_Y + LOG_DY
                
                for row in range(ROWS):
                    if distribution == "lognormal":
                        direction = random.choice([0, 1])
                    else: # Pareto
                        ALPHA = 1.0
                        BETA = 3.0
                        prob_right = (col_index + ALPHA) / (row + ALPHA + BETA)
                        direction = 1 if random.random() < prob_right else 0
                        
                    if direction == 1: col_index += 1
                    target_x = get_log_x(row, col_index)
                    target_y = LOG_START_Y - row * LOG_DY
                    path_points.append(np.array([target_x, target_y, 0]))
                
                bin_y_bottom = LOG_START_Y - ROWS * LOG_DY + LOG_DY / 2 - 1.5
                final_x = get_log_x(ROWS, col_index)

            final_bin_index = col_index
            counts[final_bin_index] += 1
            stack_height = counts[final_bin_index] * (BALL_RADIUS * 2)
            final_y = bin_y_bottom + BALL_RADIUS + stack_height - (BALL_RADIUS * 2)
            
            path_points.append(np.array([final_x, final_y, 0]))
            
            path = VMobject()
            path.set_points_as_corners(path_points)
            animations.append(MoveAlongPath(ball, path, run_time=1.5, rate_func=linear))
            
        self.play(LaggedStart(*animations, lag_ratio=0.05, run_time=TOTAL_BALLS * 0.1 + 2))
        self.wait(1)
