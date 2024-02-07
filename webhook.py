from flask import Flask, request, abort
import hmac
import hashlib
import subprocess

app = Flask(__name__)

# Replace SECRET_TOKEN и SECRET_KEY on real data
SECRET_TOKEN = '12345678'
SECRET_KEY = 'test'

@app.route('/webhook/iface/iface_set', methods=['POST'])
def webhook_handler():
    # Check token
    token = request.headers.get('Authorization')
    if token != SECRET_TOKEN:
        abort(401, 'Unauthorized')

    # Check X-Hook-Signature
    signature = request.headers.get('X-Hook-Signature')
    expected_signature = hmac.new(SECRET_KEY.encode('utf-8'), request.data, hashlib.sha512).hexdigest()
    if signature != expected_signature:
        abort(401, 'Unauthorized')

    # Get need value from JSON data
    data = request.get_json()
    state_if = data.get("data", {}).get("enabled")
    name_if = data.get("data", {}).get("display")
    device_name = data.get("data", {}).get('device', {}).get('name')
    mode_value = data.get("data", {}).get('mode', {}).get('value')
    untagged_vlan_vid = data.get("data", {}).get('untagged_vlan', {}).get('vid')

    # Write variables to a file
    with open('variables.txt', 'w') as file:
        file.write(f"data: {data}\n\n\n")
        file.write(f"State: {state_if}\n")
        file.write(f"Name: {name_if}\n")
        file.write(f"Device: {device_name}\n")
        file.write(f"Mode: {mode_value}\n")
        file.write(f"Untagged VLAN ID: {untagged_vlan_vid}\n")

    # Exec script iface_set.py with getting variables
    subprocess.run(['python', 'iface_set.py', f"--state_if={state_if}", f"--name_if={name_if}", f"--device_name={device_name}", f"--mode_value={mode_value}", f"--untagged_vlan_vid={untagged_vlan_vid}"])

    return 'Webhook received successfully!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
