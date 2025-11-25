from manim import *
import random
import numpy as np

random.seed(42)

class GaltonBoard(Scene):
    def construct(self):
        # Constants
        GRID_SIZE = 0.35  # Reduced from 0.5 to fit
        ROWS = 12
        COLS = 12
        BALL_RADIUS = 0.06 # Reduced radius
        TOTAL_BALLS = 50 # Increased balls slightly since they are smaller
        ANIMATION_SPEED = 0.5

        # Calculate board dimensions
        board_width = COLS * GRID_SIZE
        board_height = ROWS * GRID_SIZE
        
        # Offset to center the board
        # Manim frame height is 8 (-4 to 4)
        # Total height approx: ROWS * GRID_SIZE + bin_height
        # 12 * 0.35 = 4.2
        # Bin height = 1.5
        # Total = 5.7. Fits easily.
        start_y = 3.0
        
        # Create Pegs
        pegs = VGroup()
        for row in range(ROWS):
            for col in range(row + 1):
                # Triangular arrangement
                x = (col - row / 2) * GRID_SIZE
                y = start_y - row * GRID_SIZE
                peg = Dot(point=[x, y, 0], radius=0.05, color=WHITE)
                pegs.add(peg)
        
        self.add(pegs)

        # Create Bins
        bins = VGroup()
        bin_height = 1.5
        bin_y_top = start_y - ROWS * GRID_SIZE + GRID_SIZE / 2
        bin_y_bottom = bin_y_top - bin_height
        
        # Bin dividers
        for i in range(ROWS + 2):
            x = (i - (ROWS + 1) / 2) * GRID_SIZE
            line = Line(
                start=[x, bin_y_top, 0], 
                end=[x, bin_y_bottom, 0], 
                color=GRAY, 
                stroke_width=2
            )
            bins.add(line)
            
        # Floor
        floor_width = (ROWS + 1) * GRID_SIZE
        floor = Line(
            start=[-floor_width/2, bin_y_bottom, 0],
            end=[floor_width/2, bin_y_bottom, 0],
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
            return Circle(radius=BALL_RADIUS, color=BLUE, fill_opacity=1).move_to([0, start_y + GRID_SIZE, 0])

        animations = []
        
        for _ in range(TOTAL_BALLS):
            ball = make_ball()
            balls.add(ball)
            
            # Calculate path
            current_x = 0
            current_y = start_y + GRID_SIZE
            path_points = [np.array([current_x, current_y, 0])]
            
            # Fall through pegs
            col_index = 0
            for row in range(ROWS):
                # Fall down to next row
                current_y -= GRID_SIZE
                
                # Randomly go left or right
                direction = random.choice([-1, 1]) # -1 left, 1 right
                # Actually in triangular grid, it's more like:
                # current x is shifted by +/- GRID_SIZE / 2
                
                current_x += direction * GRID_SIZE / 2
                
                if direction == 1:
                    col_index += 1
                
                path_points.append(np.array([current_x, current_y, 0]))

            # Fall into bin
            final_bin_index = col_index
            counts[final_bin_index] += 1
            
            # Calculate final stacked position
            # Stack height depends on how many balls are in that bin
            stack_height = counts[final_bin_index] * (BALL_RADIUS * 2)
            final_y = bin_y_bottom + BALL_RADIUS + stack_height - (BALL_RADIUS * 2)
            
            path_points.append(np.array([current_x, final_y, 0]))
            
            # Create animation for this ball
            # We can use a succession of movements or a path
            # Using TracedPath or just animating the move
            
            # To make them fall sequentially but overlapping, we can use lag_ratio in a LaggedStart
            # But here we want to construct the full animation sequence
            
            # Let's define a custom animation for the ball following the path
            
            # Simplified: Just move to final point? No, need the bounce.
            # We can create a path object
            path = VMobject()
            path.set_points_as_corners(path_points)
            
            # Animate move along path
            # run_time needs to be fast
            anim = MoveAlongPath(ball, path, run_time=2.0, rate_func=linear)
            animations.append(anim)

        # Play animations
        # Grouping them to play with lag
        self.play(LaggedStart(*animations, lag_ratio=0.1, run_time=TOTAL_BALLS * 0.2 + 2))
        
        self.wait(2)
