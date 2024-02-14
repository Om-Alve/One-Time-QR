import sqlite3
from flask import Flask, request, make_response
import qrcode
import io
import base64

app = Flask(__name__)

# Database connection (ensure the database file exists)
conn = sqlite3.connect("qrcodes.db")
cursor = conn.cursor()


@app.route("/generator", methods=["GET"])
def generate_qr_code():
    idx = generate_unique_id()

    # Create QR code image
    qr_img = qrcode.make("https://Ticketer.pythonanywhere.com/scan?id="+str(idx))

    # Create a response object with appropriate content type
    img_bytes = io.BytesIO()
    qr_img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Create response object with image as attachment
    response = make_response(img_bytes.read())
    response.headers.set('Content-Type', 'image/png')
    response.headers.set('Content-Disposition', 'attachment', filename=f'qr_code_{idx}.png')

    return response



# Function to generate unique identifier and save QR code
def generate_unique_id():
  conn = sqlite3.connect("qrcodes.db")
  cursor = conn.cursor()
  # Generate unique identifier
  cursor.execute("SELECT COUNT(*) FROM qrcodes")
  count = cursor.fetchone()[0]
  idx = count + 1
  print(idx)
  # Add the identifier and scanned status to the table
  cursor.execute("INSERT INTO qrcodes (qr_id, scanned) VALUES (?, ?)",
                 (str(idx), 0))
  conn.commit()

  return idx

@app.route("/scan", methods=["GET"])
def scan_qr_code():
    conn = sqlite3.connect("qrcodes.db")
    cursor = conn.cursor()
    idx = request.args.get("id")

    if idx:
        # Check if ID exists in the database
        cursor.execute("SELECT * FROM qrcodes WHERE qr_id = ?", (idx,))
        qr_code_data = cursor.fetchone()

        if qr_code_data:
            scanned = qr_code_data[1]  # Access "scanned" flag from the second column
            if scanned == 0:
                # Update scanned flag to True
                cursor.execute("UPDATE qrcodes SET scanned = 1 WHERE qr_id = ?", (idx,))
                conn.commit()
                response = "accepted"
            else:
                response = "This code has already been scanned"
        else:
            response = "invalid idx"
        return f"<h1 style='color: green' if response == 'accepted' else 'color: red'>{response.upper()}</h1>", 200
    else:
        return "<h1 style='color: red'>Missing ID parameter</h1>", 400

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False for production
