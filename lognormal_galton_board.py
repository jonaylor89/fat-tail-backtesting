from manim import *
import random
import numpy as np

random.seed(2)

class LognormalGaltonBoard(Scene):
    def construct(self):
        # Constants
        ROWS = 12
        COLS = 12
        BALL_RADIUS = 0.06
        TOTAL_BALLS = 50
        
        # Lognormal specific constants
        BASE = 1.3  # The multiplicative factor
        # We want the board to be roughly centered.
        # The middle column corresponds to BASE^0 = 1.
        # We will shift everything by x_offset to center it on screen (x=0).
        # Let's say we want the geometric mean of the widest row to be at 0?
        # Or just map 1 to 0?
        # If we map 1 to 0, the board extends from BASE^(-6) to BASE^6.
        # 1.3^-6 ~= 0.2, 1.3^6 ~= 4.8.
        # Center is roughly (4.8 + 0.2)/2 = 2.5.
        # So we should shift by approx -2.5 if we want it visual center.
        # But wait, the "peak" of the lognormal distribution is at the mode.
        # For standard lognormal, mode is e^(mu - sigma^2).
        # Here we start at 1.
        # Let's just center the visual bounding box of the pegs.
        
        # Vertical spacing
        DY = 0.45 # Reduced from 0.5 to fit vertically
        START_Y = 3.2 # Shifted up slightly
        X_SCALE = 2.0 # Increased to widen, but not too much
        
        # Helper to get x position
        def get_x(row, col):
            # row 0: col 0. exponent 0.
            # row 1: col 0, 1. exponents -0.5, 0.5
            # row n: exponents from -n/2 to n/2
            exponent = col - row / 2
            val = BASE ** exponent
            # Scale it up a bit so it's not too cramped near 0?
            # Actually BASE determines the spread.
            # Let's multiply by a constant scale factor to make it visible?
            # If BASE is 1.3, values are 1, 1.3, 1.69...
            # If we just plot these x values, they are all positive.
            # We need to shift them left to center on screen.
            # Let's shift so that x=1 is at screen x=-2 (arbitrary) or just center the range.
            # Range at bottom: BASE^-6 to BASE^6.
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
        
        # Bin dividers
        # We need dividers between the possible final positions.
        # Final positions are effectively Row=ROWS (virtual).
        # There are ROWS+1 slots.
        # Dividers should be at the "half-integer" columns of the virtual row.
        # i.e. exponents -ROWS/2 - 0.5, ...
        
        for i in range(ROWS + 2):
            # Virtual column index i corresponds to exponents:
            # The balls land at indices 0 to ROWS.
            # These correspond to exponents: 0 - ROWS/2, 1 - ROWS/2, ...
            # The dividers should be between these.
            # So divider i is between landing spot i-1 and i?
            # Let's look at the exponents.
            # Landing spots exponents: e_0, e_1, ... e_ROWS
            # Divider i should be at (e_{i-1} + e_i) / 2 ?
            # Or rather, the geometric mean in value space -> arithmetic mean in exponent space.
            # Exponent for divider i: (i - 1 - ROWS/2) + 0.5 = i - ROWS/2 - 0.5
            
            exponent = i - ROWS / 2 - 0.5
            val = BASE ** exponent
            
            # Apply same transform as get_x
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
        # Connect the first and last divider bottom points
        # Actually just a line from min to max
        # Divider 0 and Divider ROWS+1
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
            # Start at top center (row 0, col 0)
            x = get_x(0, 0)
            return Circle(radius=BALL_RADIUS, color=BLUE, fill_opacity=1).move_to([x, START_Y + DY, 0])

        animations = []
        
        for _ in range(TOTAL_BALLS):
            ball = make_ball()
            balls.add(ball)
            
            # Calculate path
            # Track column index
            col_index = 0
            
            # Initial position
            current_row = -1 # Start above
            current_x = get_x(0, 0) # Approximation for start
            current_y = START_Y + DY
            
            path_points = [np.array([current_x, current_y, 0])]
            
            # Fall through pegs
            for row in range(ROWS):
                # Target row is 'row'
                # We are moving from row-1 to row
                # Actually the loop logic in previous code was:
                # current_y starts at top.
                # In loop, we move DOWN to the next row.
                
                # Logic:
                # At row `r`, ball is at `col`.
                # It chooses to go to `col` or `col+1` in row `r+1`.
                
                direction = random.choice([0, 1]) # 0 for left (same col index roughly?), 1 for right
                # Wait, in triangular grid:
                # (row, col) -> (row+1, col) [Left]
                # (row, col) -> (row+1, col+1) [Right]
                
                if direction == 1:
                    col_index += 1
                
                # Target position
                target_x = get_x(row, col_index)
                target_y = START_Y - row * DY
                
                path_points.append(np.array([target_x, target_y, 0]))

            # Fall into bin
            final_bin_index = col_index
            counts[final_bin_index] += 1
            
            # Calculate final stacked position
            # Stack height
            stack_height = counts[final_bin_index] * (BALL_RADIUS * 2)
            final_y = bin_y_bottom + BALL_RADIUS + stack_height - (BALL_RADIUS * 2)
            
            # X position is the landing spot (virtual row ROWS)
            # But wait, the bin is wide. We should center the ball in the bin?
            # Bin i is bounded by divider i and i+1.
            # Divider i exp: i - ROWS/2 - 0.5
            # Divider i+1 exp: i + 1 - ROWS/2 - 0.5
            # Center exp: i - ROWS/2
            # Which is exactly get_x(ROWS, i) if we extended get_x to row=ROWS.
            # So yes, the ball lands at get_x(ROWS, final_bin_index).
            
            # We need to define get_x for row=ROWS
            # get_x uses row to calculate exponent: col - row/2.
            # So yes, it works.
            
            final_x = get_x(ROWS, final_bin_index)
            
            path_points.append(np.array([final_x, final_y, 0]))
            
            path = VMobject()
            path.set_points_as_corners(path_points)
            
            anim = MoveAlongPath(ball, path, run_time=2.0, rate_func=linear)
            animations.append(anim)

        self.play(LaggedStart(*animations, lag_ratio=0.1, run_time=TOTAL_BALLS * 0.2 + 2))
        self.wait(2)
