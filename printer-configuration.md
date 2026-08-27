# Printer Configuration Steps

Keywords: printer setup, print test page, PrinterConfig table, A4, 80mm, DotMatrix, DirectPrint, PDFPrint, FirstTrip, SecondTrip, weighbridge printer

## 1. Check Printer Availability
- Press the Windows key, type "Printer" or open **Settings → Devices → Printers & scanners**.
- Verify that your printer is listed there.

## 2. Test the Printer
- Click the printer and select **"Print Test Page"**.
- ✅ If the test print is successful, the printer is working fine.
- ⚠️ If not, check for connectivity or driver issues.

## 3. Configure Printer in Weighbridge App
- Open the Weighbridge app and log in.
- On the main screen, click **App Settings** and select **Printer**.
- For each report, set `Active = Y`.

## 4. Set Printer Name
- **In older apps:** open the SQLite database, find the `PrinterConfig` table, and copy the printer name from Windows printer settings.
- **In newer apps:** you can update all printer names at once by selecting printers for A4, 80mm, and DotMatrix and clicking **Update**.

## 5. Report Default Settings
- If report wants to print by default in the first trip: `FirstTrip = Y` and `IsFirstDefault = Y`
- If report wants to print by default in the second trip: `SecondTrip = Y` and `IsSecondDefault = Y`

## 6. Direct Print
- Always set `DirectPrint = Y`.

## 7. WhereClause Column
- Used to filter and show which records should appear in the print menu.

## 8. WeighmentEntryType Column
- Used to filter reports by entry type in the print menu.

## 9. PDF Print Option
- Set `PDFPrint = Y` if you want to preview the report.
- Set `PDFPrint = N` to print directly to the printer.
