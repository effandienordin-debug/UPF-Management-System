import qrcode
import os
from uuid import UUID

def generate_visitor_qr(visitor_id: UUID, pass_code: str) -> str:
    """Generates a QR code for a visitor and returns the file path."""
    qr_data = f"UPF-PASS:{visitor_id}:{pass_code}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Ensure directory exists
    static_dir = os.path.join(os.getcwd(), "static", "qr_codes")
    os.makedirs(static_dir, exist_ok=True)
    
    file_path = os.path.join(static_dir, f"{visitor_id}.png")
    img.save(file_path)
    
    return file_path
