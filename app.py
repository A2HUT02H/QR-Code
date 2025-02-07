from flask import Flask, render_template, request, send_file
import qrcode, random, base64
from datetime import datetime, timedelta
from io import BytesIO


secret_code = str(random.randint(1000,99999))
print(secret_code)
secret = open(r"templates\secret.txt","w")
secret.write(secret_code)
secret.flush()
secret.close()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        # Get form data
        
        room_no = request.form.get('roomNo')
        
        # Handle empty days and hours fields
        days = request.form.get('days', '0')  # Default to '0' if not provided
        hours = request.form.get('hours', '0')  # Default to '0' if not provided

        # Convert days and hours to integers (handle empty strings)
        try:
            days = int(days) if days else 0
        except ValueError:
            days = 0  # Fallback to 0 if conversion fails

        try:
            hours = int(hours) if hours else 0
        except ValueError:
            hours = 0  # Fallback to 0 if conversion fails

        # Calculate expiration time using both days and hours
        expiration_time = datetime.now() + timedelta(days=days, hours=hours)
        expiration_time_str = expiration_time.strftime("%d/%m/%Y %I:%M:%S %p")  # DD/MM/YYYY and 12-hour format

        # Generate QR code data
        qr_data = f"Room{room_no}|{expiration_time_str}"

        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=7, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill='blue', back_color='white')
        # img.save(f"QR saves/{room_no}_qr.png")
        # Save QR code to a BytesIO object
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)

        # Convert the image to base64 for embedding in HTML
        qr_code_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        # Return the QR code image and show the download button
        return render_template('index.html', qr_code=qr_code_base64, show_download=True)

    return render_template('index.html', qr_code=None, show_download=False)

@app.route('/download_qr')
def download_qr():
    # Get the QR code image from the request
    qr_code = request.args.get('qr_code')
    if qr_code:
        return send_file(
            BytesIO(base64.b64decode(qr_code)),
            mimetype='image/png',
            as_attachment=True,
            download_name='qr_code.png'
        )
    return "No QR code available."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)