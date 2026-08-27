# Hikvision Camera Checking Guide

Keywords: CCTV, Hikvision, SADP, entry camera, exit camera, weighbridge camera, front camera, top camera, camera configuration, weighbridge installation

## 1. Get Camera Details
- Collect 2 IP addresses and passwords from the client — one for the front camera and one for the top camera.

## 2. Check Camera Connection with SADP Tool
- Download and install the Hikvision SADP Tool.
- Open SADP Tool — it will display all Hikvision cameras connected to the network.
- ✅ If you can see the camera IP, the camera is connected properly.
- ⚠️ If no camera appears, ask the client or vendor to connect the camera to the network.

## 3. Verify Camera in Browser
- Open your web browser.
- Type the camera IP address in the address bar and press Enter.
- The Hikvision login page will appear.
- Username: `admin`
- Password: (given by client)
- If you can log in successfully, the camera is working correctly.

## 4. Configure Camera in Weighbridge Application
- Open the Weighbridge application and log in as Admin.
- Go to **App Settings → Camera tab**.
- Tick the checkboxes:
  - ✅ Enable Entry Camera
  - ✅ Enable Exit Camera
- Enter the following details:
  - Entry IP Address
  - Entry Password
  - Exit IP Address
  - Exit Password
  - Entry Channel No → usually 1
  - Exit Channel No → usually 1 (but may differ sometimes)
- Click **Save** after entering all details.

## 5. Restart and Verify
- Close the App Settings window.
- Restart the Weighbridge application.
- Click the Camera icon on the main screen.
- You should now see the live preview of both cameras.

## 6. Check Camera on Entry Screen
- Open the Entry screen.
- When you click **"Get Weight"**, you will see the front and top camera images captured automatically.

## Note
During installation, the camera image save path is set automatically. You do not need to change this path manually.
