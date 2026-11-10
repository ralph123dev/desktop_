import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import time
from threading import Thread

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name="dr3mjregj",
            api_key="697429124641716",
            api_secret="W0UJhD70RWfGmNYCCNqwXfWnGvY",
            secure=True
        )

    def upload_file(self, file_path, user_id, progress_callback=None):
        try:
            if os.path.getsize(file_path) > 600 * 1024 * 1024:  # 600MB
                raise ValueError("Le fichier est trop volumineux (max 600MB)")
            
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            # Simulation de lecture du fichier pour donner un feedback visuel
            if progress_callback:
                chunks = 20
                for i in range(chunks):
                    time.sleep(0.05) # Petit délai pour l'effet visuel
                    progress = (i + 1) / (chunks * 2) # On simule 50% pour la lecture
                    progress_callback(progress, file_name)
            
            # Upload réel
            response = cloudinary.uploader.upload(
                file_path,
                public_id=f"stark_log/{user_id}/{file_name}",
                resource_type="auto",
                use_filename=True
            )
            
            if progress_callback:
                progress_callback(1.0, file_name)  # 100%
                
            return response['secure_url']

        except Exception as e:
            print(f"Upload error: {str(e)}")
            raise

    def get_file_url(self, file_id, user_id):
        try:
            result = cloudinary.api.resource(f"stark_log/{user_id}/{file_id}")
            return result['secure_url']
        except:
            return None
