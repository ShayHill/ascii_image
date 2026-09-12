# ascii_image

Create an ascii-art approximation of an image.

- create an 8d vector for each ascii printable character in a given font (by rasterizing each character into a 2x4 grid)
- resize the input image such that each "pixel" will be 2x4
- use the maximum color channel (not the grayscale, because we're painting the ascii characters with color)
- create an 8d vector for each 2x4 region of the input image
- use nearest-neighbor interpolation to select a character for each 2x4 region
- resize the input image such that each 2x4 region is now one pixel (thus one color)
- color the output ascii image using those colors

- output to svg
- output to terminal
