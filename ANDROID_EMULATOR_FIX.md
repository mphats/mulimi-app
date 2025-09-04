# 🔧 IMMEDIATE FIX for Android Emulator Connectivity

## 🚨 Current Status
- ✅ Django server is running on `http://0.0.0.0:8000/`
- ✅ Server accessible locally at `http://127.0.0.1:8000/api/v1/health`
- ❌ Android emulator cannot connect to `http://10.0.2.2:8000`
- 🔥 **Issue**: Windows Firewall is blocking external connections to port 8000

## ⚡ IMMEDIATE SOLUTION (Choose Option 1 or 2)

### Option 1: Configure Windows Firewall (Recommended)

1. **Open Command Prompt as Administrator**:
   - Press `Win + X` → Click "Terminal (Admin)" or "Command Prompt (Admin)"
   - Click "Yes" when prompted

2. **Run firewall commands**:
   ```cmd
   netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow protocol=TCP localport=8000
   ```

3. **Verify the rule was added**:
   ```cmd
   netsh advfirewall firewall show rule name="Django Dev Server"
   ```

### Option 2: Temporarily Disable Windows Firewall (Quick Test)

1. **Open Windows Security**:
   - Press `Win + I` → Update & Security → Windows Security → Firewall & network protection

2. **Turn off firewall temporarily**:
   - Click on your active network (Private network or Public network)
   - Toggle "Microsoft Defender Firewall" to **Off**
   - ⚠️ **Remember to turn it back on after testing!**

## 🧪 TEST THE FIX

After applying either option:

1. **Keep Django server running**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Test from Flutter app**:
   - Your Flutter app should now connect successfully
   - Connection status should show green ✅
   - Login should work without timeout errors

3. **Verify in app logs**:
   ```
   I/flutter: DEBUG: Found working URL: http://10.0.2.2:8000/api/v1
   I/flutter: DEBUG: Switched to working URL: http://10.0.2.2:8000/api/v1
   ```

## 🔍 DIAGNOSTIC TOOLS

If issues persist, use these tools:

### 1. Test network connectivity:
```bash
python test_android_connectivity.py
```

### 2. Test specific endpoint:
```bash
curl http://127.0.0.1:8000/api/v1/health
```

### 3. Check firewall rules:
```cmd
netsh advfirewall firewall show rule name=all | findstr "Django"
```

## 🎯 Expected Results

After the fix:
- ✅ No more "Connection timeout" errors
- ✅ No more "Connection refused" errors  
- ✅ Flutter app shows green connection status
- ✅ Login works smoothly
- ✅ Debug screen shows successful health checks

## 🔧 Alternative Solutions (If above doesn't work)

### 1. Check for other security software:
- Disable any third-party antivirus temporarily
- Check if corporate firewall software is blocking

### 2. Use different port:
```bash
python manage.py runserver 0.0.0.0:8080
```
Then update Flutter app to use `:8080` instead of `:8000`

### 3. Check Android emulator network settings:
- Restart Android emulator
- Use "Cold Boot Now" in AVD Manager
- Check emulator's network connectivity

## 📋 Why This Happens

1. **Windows Firewall**: By default blocks external connections to development servers
2. **Android Emulator**: Uses special networking (`10.0.2.2`) to reach host machine
3. **Django Server**: Must bind to `0.0.0.0:8000` (not `127.0.0.1:8000`) for external access

## 🏁 Summary

The most likely fix is **configuring Windows Firewall** to allow connections to port 8000. Once done, your Flutter authentication should work perfectly!

**Priority**: Try Option 1 (firewall configuration) first, then Option 2 (temporary disable) for quick testing.