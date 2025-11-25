from manim import *
import random
import numpy as np

random.seed(1)

class ParetoGaltonBoard(Scene):
    def construct(self):
        # Constants
        ROWS = 12
        COLS = 12
        BALL_RADIUS = 0.06
        TOTAL_BALLS = 150
        
        # Pareto/Lognormal specific constants
        BASE = 1.3  # The multiplicative factor for spacing
        
        # Vertical spacing
        DY = 0.45
        START_Y = 3.2
        X_SCALE = 2.0 
        
        # Helper to get x position (Exponential spacing)
        def get_x(row, col):
            exponent = col - row / 2
            val = BASE ** exponent
            
            min_x = BASE ** (-ROWS/2)
            max_x = BASE ** (ROWS/2)
            mid_x = (min_x + max_x) / 2
            
            return (val - mid_x) * X_SCALE
            
        # Create Pegs
        pegs = VGroup()
        for row in range(ROWS):
            for col in range(row + 1):
                x = get_x(row, col)
                y = START_Y - row * DY
                peg = Dot(point=[x, y, 0], radius=0.05, color=WHITE)
                pegs.add(peg)
        
        self.add(pegs)

        # Create Bins
        bins = VGroup()
        bin_height = 1.5
        bin_y_top = START_Y - ROWS * DY + DY / 2
        bin_y_bottom = bin_y_top - bin_height
        
        for i in range(ROWS + 2):
            exponent = i - ROWS / 2 - 0.5
            val = BASE ** exponent
            
            min_x = BASE ** (-ROWS/2)
            max_x = BASE ** (ROWS/2)
            mid_x = (min_x + max_x) / 2
            x = (val - mid_x) * X_SCALE
            
            line = Line(
                start=[x, bin_y_top, 0], 
                end=[x, bin_y_bottom, 0], 
                color=GRAY, 
                stroke_width=2
            )
            bins.add(line)
            
        # Floor
        div_0_exp = 0 - ROWS/2 - 0.5
        div_last_exp = (ROWS + 1) - ROWS/2 - 0.5
        
        def transform_x(val):
             min_x = BASE ** (-ROWS/2)
             max_x = BASE ** (ROWS/2)
             mid_x = (min_x + max_x) / 2
             return (val - mid_x) * X_SCALE

        floor_start_x = transform_x(BASE ** div_0_exp)
        floor_end_x = transform_x(BASE ** div_last_exp)
        
        floor = Line(
            start=[floor_start_x, bin_y_bottom, 0],
            end=[floor_end_x, bin_y_bottom, 0],
            color=GRAY,
            stroke_width=2
        )
        bins.add(floor)
        self.add(bins)

        # Histogram counts
        counts = [0] * (ROWS + 1)
        
        # Balls Animation
        balls = VGroup()
        
        def make_ball():
            # Start at top center
            x = get_x(0, 0)
            return Circle(radius=BALL_RADIUS, color=RED, fill_opacity=1).move_to([x, START_Y + DY, 0])

        animations = []
        
        # Polya Urn Parameters for "Rich Get Richer"
        # P(right) = (k + alpha) / (n + alpha + beta)
        # We want a decaying distribution, so we need low probability of moving right initially.
        # But if you move right, it gets easier.
        ALPHA = 1.0
        BETA = 3.0
        
        for _ in range(TOTAL_BALLS):
            ball = make_ball()
            balls.add(ball)
            
            col_index = 0
            current_x = get_x(0, 0)
            current_y = START_Y + DY
            path_points = [np.array([current_x, current_y, 0])]
            
            # Fall through pegs
            for row in range(ROWS):
                # Polya Urn Probability
                # row is the number of steps taken so far (n)
                # col_index is the number of "rights" taken so far (k)
                
                # Formula: P(Right) = (col_index + ALPHA) / (row + ALPHA + BETA)
                prob_right = (col_index + ALPHA) / (row + ALPHA + BETA)
                
                if random.random() < prob_right:
                    direction = 1
                else:
                    direction = 0
                
                if direction == 1:
                    col_index += 1
                
                target_x = get_x(row, col_index)
                target_y = START_Y - row * DY
                path_points.append(np.array([target_x, target_y, 0]))

            # Fall into bin
            final_bin_index = col_index
            counts[final_bin_index] += 1
            
            stack_height = counts[final_bin_index] * (BALL_RADIUS * 2)
            final_y = bin_y_bottom + BALL_RADIUS + stack_height - (BALL_RADIUS * 2)
            final_x = get_x(ROWS, final_bin_index)
            
            path_points.append(np.array([final_x, final_y, 0]))
            
            path = VMobject()
            path.set_points_as_corners(path_points)
            
            anim = MoveAlongPath(ball, path, run_time=2.0, rate_func=linear)
            animations.append(anim)

        self.play(LaggedStart(*animations, lag_ratio=0.1, run_time=TOTAL_BALLS * 0.2 + 2))
        self.wait(2)
