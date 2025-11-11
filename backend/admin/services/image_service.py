import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from backend.models import db
from backend.models.content import ImageAsset

class ImageService:
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ImageService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_image(file, alt_text=None):
        if not file or not ImageService.allowed_file(file.filename):
            raise ValueError('Invalid file type')
        
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        
        filepath = os.path.join(ImageService.UPLOAD_FOLDER, unique_filename)
        os.makedirs(ImageService.UPLOAD_FOLDER, exist_ok=True)
        
        img = Image.open(file)
        
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(filepath, optimize=True, quality=85)
        
        width, height = img.size
        file_size = os.path.getsize(filepath)
        
        image_asset = ImageAsset(
            file_name=unique_filename,
            original_name=original_filename,
            alt_text=alt_text or '',
            width=width,
            height=height,
            mime_type=f'image/{extension}',
            file_size=file_size
        )
        
        db.session.add(image_asset)
        db.session.commit()
        
        return image_asset
    
    @staticmethod
    def crop_image(image_id, x, y, width, height):
        image_asset = ImageAsset.query.get(image_id)
        if not image_asset:
            raise ValueError('Image not found')
        
        filepath = os.path.join(ImageService.UPLOAD_FOLDER, image_asset.file_name)
        if not os.path.exists(filepath):
            raise ValueError('Image file not found')
        
        img = Image.open(filepath)
        
        cropped = img.crop((x, y, x + width, y + height))
        
        cropped.save(filepath, optimize=True, quality=85)
        
        image_asset.width = width
        image_asset.height = height
        image_asset.file_size = os.path.getsize(filepath)
        
        db.session.commit()
        
        return image_asset
    
    @staticmethod
    def get_all_images():
        return ImageAsset.query.order_by(ImageAsset.uploaded_at.desc()).all()
    
    @staticmethod
    def get_image(image_id):
        return ImageAsset.query.get(image_id)
    
    @staticmethod
    def delete_image(image_id):
        image_asset = ImageAsset.query.get(image_id)
        if not image_asset:
            return False
        
        filepath = os.path.join(ImageService.UPLOAD_FOLDER, image_asset.file_name)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        db.session.delete(image_asset)
        db.session.commit()
        
        return True

image_service = ImageService()
