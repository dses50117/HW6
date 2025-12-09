# 🌐 Streamlit Cloud 部署指南 - 雙版本說明

## 📦 兩個版本可供選擇

本專案提供**兩個 Git 分支**，適用於不同的部署場景：

---

## ⚡ 版本 A: 預載資料庫版本（推薦用於展示）

### 🎯 分支: `preloaded-db`

**特點**：
- ✅ **超快部署**: < 1 分鐘即可使用
- ✅ **包含完整資料**: 28 個地點天氣資料已預載
- ✅ **無需等待**: 不需要等待 API 抓取
- ✅ **適合展示**: 穩定的資料快照

**部署步驟**：
1. 前往 [share.streamlit.io](https://share.streamlit.io)
2. 登入 GitHub 帳號
3. 點擊 **"New app"**
4. 設定：
   ```
   Repository: dses50117/HW6
   Branch: preloaded-db  ⭐
   Main file path: app.py
   ```
5. **Advanced settings** → **Secrets**：
   ```toml
   [cwa]
   regional_api_key = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
   county_api_key = "CWA-67B3E062-3904-46EE-A0C9-C68C296349FD"
   ```
6. 點擊 **"Deploy!"**
7. ⏰ 等待 < 1 分鐘

**🎊 完成！應用程式立即可用！**

---

## 🔄 版本 B: 自動抓取版本（推薦用於生產）

### 🎯 分支: `main`

**特點**：
- ✅ **總是最新**: 每次啟動自動抓取最新天氣資料
- ✅ **即時資料**: 直接從 CWA API 獲取
- ✅ **適合生產**: 長期運行的應用程式
- ⏳ **首次較慢**: 初始化需要 5-10 分鐘

**部署步驟**：
1. 前往 [share.streamlit.io](https://share.streamlit.io)
2. 登入 GitHub 帳號
3. 點擊 **"New app"**
4. 設定：
   ```
   Repository: dses50117/HW6
   Branch: main  ⭐
   Main file path: app.py
   ```
5. **Advanced settings** → **Secrets**：
   ```toml
   [cwa]
   regional_api_key = "CWA-1FFDDAEC-161F-46A3-BE71-93C32C52829F"
   county_api_key = "CWA-67B3E062-3904-46EE-A0C9-C68C296349FD"
   ```
6. 點擊 **"Deploy!"**
7. ⏰ 等待 5-10 分鐘（首次初始化）

**首次會顯示**：
```
⚠️ First time setup detected. Initializing database...
🔄 Fetching weather data from CWA API for all 28 locations...
```

**🎊 初始化完成後自動刷新！**

---

## 📊 版本比較

| 項目 | 預載版本 (preloaded-db) | 自動抓取版本 (main) |
|------|------------------------|---------------------|
| **部署時間** | ⚡ < 1 分鐘 | ⏳ 5-10 分鐘 |
| **資料新鮮度** | 📸 資料快照 | 🔄 即時更新 |
| **API 調用** | ❌ 不需要 | ✅ 自動執行 |
| **適用場景** | 📺 展示、測試 | 🚀 生產環境 |
| **穩定性** | ✅ 高（靜態資料） | ✅ 高（有錯誤處理） |
| **資料庫** | ✅ 已包含 | ⚙️ 自動生成 |

---

## 🤔 如何選擇？

### 選擇預載版本 (preloaded-db) 如果：
- ✅ 需要**快速展示**給他人看
- ✅ 正在**測試**部署流程
- ✅ 不需要**即時**資料
- ✅ 想要**避免** API 調用延遲
- ✅ 需要**一致的**資料（例如文檔截圖）

### 選擇自動抓取版本 (main) 如果：
- ✅ 這是**生產環境**應用
- ✅ 需要**最新**天氣資料
- ✅ 計劃**長期運行**
- ✅ 可以接受**首次啟動**較慢
- ✅ 資料**即時性**很重要

---

## 🔧 技術細節

### 預載版本的資料
```
檔案: data.db
大小: ~100 KB
記錄數: 118 筆
地點數: 28 (6 區域 + 22 縣市)
更新時間: 2025-12-09
```

### 自動抓取版本的流程
```python
1. Streamlit Cloud 啟動應用
2. app.py 檢查資料庫
3. 發現資料庫為空
4. 自動調用 fetch_weather.main()
5. 從 CWA API 抓取 28 個地點資料
6. 儲存到資料庫
7. 自動刷新頁面
8. 完成！
```

---

## 🔄 更新預載資料庫

如果您使用預載版本，想要更新資料：

```bash
# 1. 切換到預載分支
git checkout preloaded-db

# 2. 抓取最新資料
python fetch_weather.py

# 3. 提交更新
git add data.db
git commit -m "Update weather database - $(date +%Y-%m-%d)"
git push origin preloaded-db
```

Streamlit Cloud 會自動重新部署！

---

## 📱 同時部署兩個版本

您可以在 Streamlit Cloud 上**同時部署**兩個版本：

1. **應用 1**: `preloaded-db` 分支
   - URL: `https://hw6-preloaded.streamlit.app`
   - 用途: 快速展示

2. **應用 2**: `main` 分支
   - URL: `https://hw6-live.streamlit.app`
   - 用途: 即時資料

兩個應用**完全獨立**，互不影響！

---

## 🆘 故障排除

### 預載版本問題

**Q: 資料太舊了怎麼辦？**
A: 按照上面的「更新預載資料庫」步驟更新

**Q: 可以在本地更新嗎？**
A: 可以！執行 `python fetch_weather.py` 後提交

### 自動抓取版本問題

**Q: 超過 10 分鐘還在載入？**
A: 請檢查 Streamlit Cloud 日誌，可能是 API 問題

**Q: 顯示 API 錯誤？**
A: 檢查 Secrets 中的 API keys 是否正確

**Q: 想要更快的部署？**
A: 改用 `preloaded-db` 分支

---

## 📞 支援

- **問題回報**: [GitHub Issues](https://github.com/dses50117/HW6/issues)
- **完整文檔**: [README.md](README.md)
- **部署指南**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

<div align="center">

**選擇適合您的版本，開始部署！** 🚀

[預載版本部署](https://share.streamlit.io) | [自動抓取版本部署](https://share.streamlit.io)

</div>
