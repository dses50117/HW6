# 🌤️ Taiwan Weather App - Preloaded Database Version

> **⚡ Quick Deploy Version** - This branch includes a pre-populated database for instant deployment.

## 🔄 Version Comparison

| Feature | Main Branch | Preloaded Branch (This) |
|---------|-------------|------------------------|
| **Database** | Auto-fetch on first run | Pre-populated ✅ |
| **Deploy Time** | 5-10 minutes | < 1 minute ⚡ |
| **Data Freshness** | Always current | Static snapshot |
| **Use Case** | Production | Demo/Testing |

---

## 🚀 Quick Deploy to Streamlit Cloud

### Option A: Deploy This Branch (Fastest)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Create new app with:
   - **Repository**: `dses50117/HW6`
   - **Branch**: `preloaded-db` ⭐
   - **Main file**: `app.py`
3. Add secrets (Advanced Settings):
   ```toml
   [cwa]
   regional_api_key = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
   county_api_key = "CWA-67B3E062-3904-46EE-A0C9-C68C296349FD"
   ```
4. Deploy!

**Result**: App ready in < 1 minute with all 28 locations! 🎊

---

### Option B: Deploy Main Branch (Auto-fetch)

For always-fresh data, use the `main` branch instead.
- **Branch**: `main`
- **Note**: First deployment takes 5-10 minutes for data fetching

---

## 📊 Database Information

### Included Data
- **File**: `data.db` (SQLite)
- **Size**: ~100 KB
- **Records**: 118 weather entries
- **Locations**: 28 (6 regions + 22 counties)
- **Last Updated**: 2025-12-09

### Sample Data
```
北部地區: 16.0°C ~ 27.0°C, 晴時多雲
臺北市: 16.0°C ~ 25.0°C
新北市: 16.3°C ~ 19.7°C
... (25 more locations)
```

---

## 🔄 Updating the Database

To refresh the pre-populated database:

```bash
# 1. Switch to this branch
git checkout preloaded-db

# 2. Fetch latest weather data
python fetch_weather.py

# 3. Commit the updated database
git add data.db
git commit -m "Update weather database"
git push origin preloaded-db
```

Streamlit Cloud will auto-redeploy with fresh data!

---

## 📁 What's Different in This Branch?

1. **`.gitignore`**
   - ✅ Allows `data.db` tracking
   - ❌ (Main branch ignores all .db files)

2. **`data.db`**
   - ✅ Included in repository
   - ❌ (Main branch: auto-generated)

3. **Everything else**
   - ✅ Same as main branch
   - Same features, same UI, same functionality

---

## 💡 When to Use Which Branch?

### Use `preloaded-db` (This Branch) When:
- ✅ Quick demos or presentations
- ✅ Testing deployment process
- ✅ Avoiding API rate limits
- ✅ Offline development
- ✅ Consistent data for screenshots/docs

### Use `main` Branch When:
- ✅ Production deployment
- ✅ Need real-time data
- ✅ Long-term application
- ✅ Regular data updates important

---

## 🛠️ Technical Details

### Database Schema
```sql
CREATE TABLE weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    min_temp REAL,
    max_temp REAL,
    description TEXT,
    fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_type TEXT DEFAULT 'region'
);
```

### Auto-initialization Behavior
This branch **skips** auto-fetch because database already exists!

```python
# app.py checks database on startup
if database_exists and has_data:
    # ✅ Use existing data
    display_weather()
else:
    # ❌ Won't happen in preloaded branch
    auto_fetch()
```

---

## 📞 Support

- **Main Documentation**: See `README.md` for full project details
- **Repository**: [https://github.com/dses50117/HW6](https://github.com/dses50117/HW6)
- **Issues**: [GitHub Issues](https://github.com/dses50117/HW6/issues)

---

## 🎯 Quick Links

- 📘 [Full README](../README.md) - Complete CRISP-DM analysis
- 🚀 [Deployment Guide](../DEPLOYMENT.md) - Detailed deployment instructions
- 📊 [Main Branch](https://github.com/dses50117/HW6/tree/main) - Auto-fetch version

---

<div align="center">

**⚡ Preloaded Database Branch** | **Ready to Deploy in Seconds!**

[Deploy Now](https://share.streamlit.io) | [View Main Branch](https://github.com/dses50117/HW6)

</div>
