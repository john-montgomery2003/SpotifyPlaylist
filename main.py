from dotenv import load_dotenv
load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO


scope = "ugc-image-upload playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
barcodeFont = ImageFont.truetype("LibreBarcode128Text-Regular.ttf", 500)
bottomFont = ImageFont.truetype("Viga-Regular.ttf", 200)


with open('loadfile.json', 'r') as f:
    x = json.loads(f.read())

for item in x["playlists"]:
    im = Image.open(item['image'])
    width, height = im.size  # Get dimensions
    sq = min(width, height)
    left = (width - height) / 2
    top = (height - height) / 2
    right = (width + height) / 2
    bottom = (height + height) / 2

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    im.thumbnail((3000,3000), Image.ANTIALIAS)

    draw = ImageDraw.Draw(im)
    draw.rectangle((0,300,2500, 880), fill='#606060')
    newx = 2500 - barcodeFont.getsize(item["barcode_text"])[0]
    draw.text((newx, 330), item["barcode_text"], fill='#FFF', font=barcodeFont)
    newx = (3000-bottomFont.getsize(item["bottom_text"])[0])/2
    draw.text((newx, 2750), item["bottom_text"], fill='#FFF', font=bottomFont)

    im.thumbnail((1000, 1000), Image.ANTIALIAS)

    buffered = BytesIO()
    im.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    id = item["playlist_url"].split('/')[-1].split('?')[0]
    sp.playlist_upload_cover_image(id, img_str)
