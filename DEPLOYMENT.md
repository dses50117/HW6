# Streamlit Cloud 部署指南

## ✅ GitHub 已就緒！

代碼已成功推送到：**https://github.com/dses50117/HW6.git**

---

## 🚀 在 Streamlit Cloud 部署步驟

### 1. 訪問 Streamlit Cloud
前往：**https://share.streamlit.io/**

### 2. 登錄
使用您的 GitHub 帳戶登錄

### 3. 創建新應用
點擊 **"New app"** 按鈕

### 4. 配置應用

填寫以下資訊：

- **Repository**: `dses50117/HW6`
- **Branch**: `main`
- **Main file path**: `app.py`

### 5. 設置 Secrets (重要！)

點擊 **"Advanced settings"** → **"Secrets"**

複製以下內容並貼上：

```toml
[cwa]
regional_api_key = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
county_api_key = "CWA-67B3E062-3904-46EE-A0C9-C68C296349FD"
```

### 6. 部署
點擊 **"Deploy!"** 按鈕

---

## ⚠️ 注意事項

### 資料庫初始化
第一次運行時，應用程式會顯示錯誤，因為沒有 `data.db` 文件。

**解決方案：**

有兩個選擇：

#### 選項 A：手動運行 fetch_weather.py（推薦）
1. 部署後，使用 Streamlit Cloud 的終端機功能
2. 運行: `python fetch_weather.py`
3. 重新啟動應用程式

#### 選項 B：修改 app.py 自動初始化
在 `app.py` 的 `main()` 函數開頭添加：

```python
# Auto-fetch data if database is empty
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM weather WHERE fetch_time > datetime('now', '-1 day')")
count = cursor.fetchone()[0]
conn.close()

if count == 0:
    import subprocess
    subprocess.run(['python', 'fetch_weather.py'])
```

### API 限制
- CWA API 有請求頻率限制
- 建議每小時自動更新一次資料
- 可使用 Streamlit Cloud 的計時功能

---

## 📱 訪問您的應用

部署完成後，您會獲得一個 URL，格式如下：

```
https://your-app-name.streamlit.app
```

---

## 🔄 更新應用

當您修改代碼後：

```bash
git add .
git commit -m "Update message"
git push origin main
```

Streamlit Cloud 會自動重新部署！

---

## ✅ 功能檢查清單

部署後請驗證：

- [ ] 應用程式可正常訪問
- [ ] 28 個地點都有資料
- [ ] 地圖正確顯示標記
- [ ] 資料篩選功能正常
- [ ] 圖表顯示正確
- [ ] Excel/JSON 匯出功能正常

---

## 🐛 常見問題

### 問題：應用顯示 "No weather data available"
**解決**：執行 `python fetch_weather.py` 來初始化資料庫

### 問題：地圖不顯示
**解決**：檢查 `streamlit-folium` 是否在 `requirements.txt` 中

### 問題：API 錯誤
**解決**：確認 Secrets 中的 API keys 正確設置

---

## 📞 支援

如有問題，請檢查：
- Streamlit Cloud 日誌
- GitHub repository issues
- CWA API 狀態

**祝部署成功！** 🎉
