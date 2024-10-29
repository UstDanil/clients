from PIL import Image
import io


async def add_watermark_to_avatar(file, avatar_path):
    file_content = await file.read()
    with Image.open(io.BytesIO(file_content)) as base_image:
        watermark = Image.open("/application/static/watermark.jpg")
        position = (0, 0)
        base_image.paste(watermark, position)
        base_image = base_image.convert("RGB")
        base_image.save(avatar_path)
