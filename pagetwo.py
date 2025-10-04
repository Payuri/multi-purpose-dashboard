import base64
from io import BytesIO
from dash import Dash, dcc, html, Input, Output, State, callback, callback_context
from dash.dcc import Download
from PIL import Image, ImageEnhance

# project uses pillow and base64 (weird)
# pillow image to base64
def pil_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()
# data:image string is a way to not have to use a image link. image=the base64 conversion buffered=bytesio. base64conversion.save(bytesio, format=png)
# image.save wrote raw png data to bytesio, buffered.getvalue returns all bytes as raw png data. 
# .decode makes the bytes into a python string because you can't use only bytes, it needs to be a python string
layout = html.Div([
    dcc.Store(id='image-store'), # dcc.store stores data in memory, it remembers what edits have been done and how many times
# buttons and visuals
    dcc.Upload(
        id='upload-img',
        children=html.Div([
            'Drag and Drop or ',
            html.A("Select Files")
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Br(),
    html.Button("Rotate 90°", id="rotate-btn"),
    html.Button("Increase Brightness", id="brightness-btn"),
    html.Button("Decrease Brightness", id="brightness-down-btn"),
    html.Button("Increase Sharpness", id="sharpness-btn"),
    html.Button("Decrease Sharpness", id="sharpness-down-btn"),
    html.Br(),
    html.Img(id="editable-img", style={'maxWidth': '500px'}),
    html.Br(),
    html.Button("Download Edited Image", id="download-btn"),
    dcc.Download(id="download-image")
])
# first callback
@callback(
    Output("editable-img", "src"),
    Output("image-store", "data"),
    Input("upload-img", "contents"),
    Input("rotate-btn", "n_clicks"),
    Input("brightness-btn", "n_clicks"),
    Input("brightness-down-btn", "n_clicks"),
    Input("sharpness-btn", "n_clicks"),
    Input("sharpness-down-btn", "n_clicks"),
    State("image-store", "data"), # state doesn't trigger updates
    prevent_initial_call=True
)
# without this line there's no way to know what thing causes the callback aka everything explodes
def edit_image(uploaded_contents, rotate_clicks, bright_up, bright_down, sharp_up, sharp_down, stored_data):
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    # ctx is callback context, ctx.triggered=callback context triggered=keep track of what triggers. 
    # 0 is the counter prop_id finds the exact name. split splits the data after a "." last part is a safeguard.

    # new upload
    if stored_data is None and uploaded_contents is not None:
        return uploaded_contents, {
            'original': uploaded_contents,
            'rotate': 0,
            'brightness': 0,
            'sharpness': 0
        }
# stored data is edits made + original image as data, 
# so stored data=none means no edits done and uploaded contents not none means a new image was uploaded, 
# so it resets everything to 0 just incase
    if stored_data is None:
        return None, None # safeguard if something triggered but there was no data, just stops it

    # restores counters so it doesn't break
    rotate_count = stored_data.get('rotate', 0)
    brightness_count = stored_data.get('brightness', 0)
    sharpness_count = stored_data.get('sharpness', 0)

    # updates all counters
    if button_id == "rotate-btn":
        rotate_count += 1
    elif button_id == "brightness-btn":
        brightness_count += 1
    elif button_id == "brightness-down-btn":
        brightness_count -= 1
    elif button_id == "sharpness-btn":
        sharpness_count += 1
    elif button_id == "sharpness-down-btn":
        sharpness_count -= 1

    # original by default
    img_b64 = stored_data['original'] # stored data is the data from dcc.store, original is the base64 string for the image
    img = Image.open(BytesIO(base64.b64decode(img_b64.split(',')[1]))) # base64.b64encode makes it into actual image data
    # bytesio makes a file-like object from its memory which pillow can read and display as an image
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB") # if image isn't an rgb image, it makes it into a rgb image, 
        # and image.open opens that file-like data


    # transforms always new
    img = img.rotate(-90 * rotate_count, expand=True)
    img = ImageEnhance.Brightness(img).enhance(1 + 0.2 * brightness_count)
    img = ImageEnhance.Sharpness(img).enhance(1 + 0.2 * sharpness_count)

    new_b64 = pil_to_base64(img)

    return new_b64, {
        'original': stored_data['original'],
        'rotate': rotate_count,
        'brightness': brightness_count,
        'sharpness': sharpness_count
    }
# second callback for downloads so they're not mixed in 1
@callback(
    Output("download-image", "data"),
    Input("download-btn", "n_clicks"),
    State("editable-img", "src"),
    prevent_initial_call=True
)
# download function
def download_image(n_clicks, current_src): # when clicks download, n_clicks is there to make sure to know when it's pressed
    # current_src is the current image displayed on screen
    if not current_src:
        return None
    content_string = current_src.split(',')[1]
    return dcc.send_bytes(base64.b64decode(content_string), filename="edited_image.png")
# current_src looks like this: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..., split chooses the 2nd part which is base64 data
# base64.b64decode(content_string) converts to image bytes so you can download the file as a png
# dcc.send_bytes generates a downloadable image through dash, filename is the name of the file