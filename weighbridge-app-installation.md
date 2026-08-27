# Weighbridge App Installation Guide

Keywords: Quarry360, weighbridge software, WE45, install, setup, bin folder, database rename, global file path, SQLite DB connection

## 1. Download Required Files
- Download the latest Weighbridge Software and Quarry360 Weighbridge App.

## 2. Create Main Folder
- Create a folder named **Syvasoft** on your computer.
- Copy all downloaded files into this folder.
- Extract (unzip) the Quarry360WeighbridgeApp file inside the same folder.

## 3. Install Basic Requirements
- Install the following setup files in order:
  1. `01_SQLSysClrTypes.msi`
  2. `02_ReportViewer.msi`
- Install the fonts from the Fonts folder located inside the Weighbridge Software folder.

## 4. Copy the Bin Folder
- Extract the `bin` folder from the Weighbridge Software package.
- Copy the extracted `bin` folder into the Syvasoft folder.
- ⚠️ Make sure the copied folder is not inside another bin folder (e.g., avoid `bin\bin`).

## 5. Verify Folder Structure
After setup, your Syvasoft folder should contain the following:
Syvasoft
│
├── App
├── Data
├── Reports
├── bin
└── Weighbridge Software Folder

## 6. Rename the Database File
- Open the `Data` folder. You will find three database files:
  - `weighbridgedemo.db`
  - `vehiclelog.db`
  - `track.db`
- Rename `weighbridgedemo.db` to your project name.
  - Example: if your project name is Senthil Blue Metal, rename it to `senthilblumetal.db`.

## 7. Configure File Path
- Open the `App` folder and run `WE45.exe`.
- When prompted, enter the password to open the Settings window.
- At the top, find the **Global File Path** textbox.
  - Example: if your Syvasoft folder is in drive D, enter: `D:\Syvasoft\`
- Click **Change File Path**. This will automatically set the correct path for all files.

## 8. Update Database Connection
- In the same settings window, locate the **SQLite DB Connection** textbox.
- Update the database name from `weighbridgedemo.db` to your new project name.
  - Example: `D:\Syvasoft\Data\senthilblumetal.db`

## 9. Save and Restart
- Click **Save** and close the settings window.
- The app will automatically restart and display the login screen.
- You can now log in and start using the Weighbridge App.
