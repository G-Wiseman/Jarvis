from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import datetime
import os


def jarvis_make_image(message):
    im = Image.open('assets/jarvis_blank.gif')
    message = f"Jarvis, {message}"
    # A list of the frames to be outputted
    frames = []
    fontsize = 36
    fontOswald = ImageFont.truetype("./assets/fonts/Oswald/oswald.ttf", size=36)
    # Loop over each frame in the animated image
    for frame in ImageSequence.Iterator(im):
        d = ImageDraw.Draw(frame)
        while fontsize > 2:
            _, _, msg_w, msg_h = d.textbbox((0,0), message, font=fontOswald)
            if msg_w <= frame.width:
                break
            fontsize -= 1
            fontOswald = ImageFont.truetype("./assets/fonts/Oswald/oswald.ttf", size=fontsize)

        d.text((frame.width/2 - msg_w/2, 7 * frame.height/8 - msg_h/2), message, font=fontOswald, stroke_width=1)
        del d
        
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        
        # Then append the single frame image to a list of frames
        frames.append(frame)
    # Save the frames as a new image
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path_to = "./output/"
    filename = f"jarvis-{timestamp}.gif"
    frames[1].save(os.path.join(path_to, filename), save_all=True, append_images=frames[1:])
    return path_to, filename


if __name__ == "__main__":
    import sys
    jarvis_make_image(sys.argv[1])

