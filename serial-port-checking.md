# Serial Port Checking – Easy Guide

Keywords: COM port, baud rate, HyperTerminal, Prolific USB driver, Serial-to-USB, weighbridge reading, ReverseApplicable, SubstringStart, SubstringRemoveLastChar, Read Line String

## 1. Open HyperTerminal
- Choose the correct COM port and baud rate.

## 2. If You Don't See Any Value
- ⚠️ Try changing the baud rate and check again.
- Make sure the cable is properly connected.
- If you're using a Serial-to-USB cable, install the **Prolific USB Driver**.

## 3. If You Get Values in HyperTerminal
- Note down the COM port name and baud rate.

## 4. Check the Reading
- Confirm that the value shown in HyperTerminal matches the vehicle weight shown on the weighbridge display.

## 5. Find the Separator
- When you get two weight readings, look for the special character (like a comma or space) between them and note it.

## 6. Set Up in Weighbridge Application
- Open the app and go to **App Settings**.
- Tick the checkbox near **Serial Port**.
- Set the COM port, baud rate, and **Read Line String** (the separator you found).
- Click **Save** — the app will restart automatically.

## 7. Check the Main Screen
- See if the weight value is showing correctly.

## 8. If the Weight Is Reversed
- ⚠️ Set `ReverseApplicable = 1`.

## 9. If Extra Numbers Appear at the Start
- Example: You see `1100` instead of `100`.
- ⚠️ Set `SubstringStart = 1` (this removes the first extra digit).

## 10. If Extra Numbers Appear at the End
- Example: You see `1001` instead of `100`.
- ⚠️ Set `SubstringRemoveLastChar = 1` (this removes the last extra digit).
