from Frame import Frame
from exceptions import GridSizeMismatchError

from utils import animate_create_grid

class Animation:
    def __init__(self, width: int, height: int, scale: int):
        self.width = width
        self.height = height
        self.scale = scale

        self.num_frames = 0

        self.grid = animate_create_grid(width, height)

    def add_frame(self, frame: Frame):
        """ Adds a new frame to the animation. """

        if frame.width != self.width or frame.height != self.height:
            raise GridSizeMismatchError

        self.num_frames += 1

        for row in range(self.height):
            for col in range(self.width):
                # for each pixel, add its colour in this frame in the animation to the list
                # in the corresponding position in the grid
                # if the pixel was transparent, add None
                self.grid[row][col].append((None if frame.grid[row][col] is None else frame.grid[row][col].getAttribute('fill')))

    def add_frames(self, frames):
        """ Adds a list of frames. """

        for frame in frames:
            self.add_frame(frame)

    def _generate_svg_animation_for_pixel(self, row: int, col: int):
        """ Returns the 'animate' SVG tag(as a string) necessary to animate this pixel """

        # ? do we even need this if we check in the beginning of svg_for_pixel anyway
        if not self._does_pixel_need_animation(row, col):
            # the pixels retains its color during the animation
            return ''

        # TODO move these calculations into the function we will call for the
        # TODO whole object and take them in as parameters 
        frame_duration = 1.0 / self.num_frames
        key_times = []

        # every frame has two corresponding key times, one for when it comes into view
        # and one for when it goes out of view
        # the exit time of a frame is the same as the entry time of the next frame
        # this is to make transitions instant
        for i in range(self.num_frames):
            key_times.append(str(round(i * frame_duration, 2)))
            key_times.append(str(round((i+1) * frame_duration, 2)))

        color_values = []
        opacity_values = []

        # TODO use the last color if possible
        # assign values for each key time
        # the values for entry and exit key times for each frame are the same so that
        # the values persist over the frame
        for i in range(len(self.grid[row][col])):
            color = self.grid[row][col][i]
            if color is not None:
                color_values.append(color)
                color_values.append(color)
                opacity_values.append('1.0')
                opacity_values.append('1.0')
            else:
                color_values.append('white')
                color_values.append('white')
                opacity_values.append('0.0')
                opacity_values.append('0.0')

        key_times_str = '; '.join(key_times)
        color_values_str = '; '.join(color_values)
        opacity_values_str = '; '.join(opacity_values)

        # TODO assuming 100ms per frame. Add an option to change this
        animation_duration = f'{self.num_frames * 100}ms'

        return f'<animate attributeName="fill" dur="{animation_duration}" repeatCount="indefinite" begin="0s" keyTimes="{key_times_str}" values="{color_values_str}" /> \
            <animate attributeName="fill-opacity" dur="{animation_duration}" repeatCount="indefinite" begin="0s" keyTimes="{key_times_str}" values="{opacity_values_str}" />'

    def _generate_svg_for_pixel(self, row: int, col: int):
        """ Returns the complete SVG(including animations) markup for this pixel. """

        if not self._is_pixel_ever_filled(row, col):
            return ''
        if self.grid[row][col][0] is None:
            # if the pixel is transparent in the opening frame, start it out with white fill and 0 opacity
            return f'<rect x="{col* self.scale}" y="{row*self.scale}" width="{self.scale}" height="{self.scale}" fill="white" fill-opacity="0.0">{self._generate_svg_animation_for_pixel(row, col)}</rect>'
        else:
            return f'<rect x="{col* self.scale}" y="{row*self.scale}" width="{self.scale}" height="{self.scale}" fill="{self.grid[row][col][0]}" fill-opacity="1.0">{self._generate_svg_animation_for_pixel(row, col)}</rect>'

    def generate_svg(self):
        """ Returns the complete SVG markup for the animation. """

        pixels_svg_list = []
        for row in range(self.height):
            for col in range(self.width):
                pixels_svg_list.append(self._generate_svg_for_pixel(row, col))

        pixels_svg = '\n'.join(pixels_svg_list)

        return f'<svg version="1.1" width="{self.width * self.scale}" height="{self.height * self.scale}" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">{pixels_svg}</svg>'

    def _is_pixel_ever_filled(self, row: int, col: int):
        """ Returns true if the pixel at ([row], [col]) is ever non transparent. """

        for color in self.grid[row][col]:
            if color is not None:
                return True

        return False

    def _does_pixel_need_animation(self, row: int, col: int):
        """ Returns true if the pixel ever needs animation i.e. changes color or transparency. """

        color_each_frame = self.grid[row][col]

        if len(color_each_frame) == 1:
            #if there's only one frame then no animation is needed
            return False

        for i in range(1, len(color_each_frame)):
            if color_each_frame[i] != color_each_frame[i-1]:
                # color changes across frames
                return True

        return False
