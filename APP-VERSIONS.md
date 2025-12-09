# 🌤️ Taiwan Weather App - 雙版本說明

本專案提供**兩個 Streamlit 應用程式**，適用於不同場景：

---

## 📱 版本 A: app.py（雲端即時版本）

### 🎯 特點
- ✅ **自動抓取**: 首次啟動自動從 CWA API 獲取資料
- ✅ **即時資料**: 總是顯示最新天氣資訊  
- ✅ **適合生產**: 長期運行的線上服務
- ⏳ **首次較慢**: 初始化需要 5-10 分鐘（僅首次）

### 🚀 啟動方式
```bash
streamlit run app.py
```

### 🌐 Streamlit Cloud 部署
```
Repository: dses50117/HW6
Branch: main
Main file: app.py
```

### 📝 說明
- 適合部署到 Streamlit Cloud 作為公開服務
- 自動偵測資料庫，無資料時自動抓取
- 需要網路連線訪問 CWA API

---

## 📊 版本 B: new-app.py（本地資料庫版本）

### 🎯 特點  
- ✅ **使用本地 DB**: 讀取預先準備的 data.db
- ✅ **快速啟動**: < 5 秒即可使用
- ✅ **離線可用**: 不需要網路連線
- ✅ **適合展示**: 穩定的資料快照，適合 demo

### 🚀 啟動方式

**步驟 1**: 準備資料庫（如果還沒有）
```bash
python fetch_weather.py
```

**步驟 2**: 啟動應用
```bash
streamlit run new-app.py
```

### 🌐 Streamlit Cloud 部署
```
Repository: dses50117/HW6
Branch: preloaded-db
Main file: new-app.py
```

### 📝 說明
- 需要先執行 fetch_weather.py 建立 data.db
- 適合本地展示、測試、教學
- 資料為靜態快照，需手動更新

---

## 📊 版本比較表

| 特性 | app.py (雲端版) | new-app.py (本地版) |
|------|----------------|---------------------|
| **啟動時間** | ⏳ 5-10 分鐘 (首次) | ⚡ < 5 秒 |
| **資料新鮮度** | 🔄 即時 | 📸 快照 |
| **網路需求** | ✅ 必須 | ❌ 不需要 |
| **自動抓取** | ✅ 是 | ❌ 否 |
| **適用場景** | 🌐 線上服務 | 📺 本地展示 |
| **資料庫** | ⚙️ 自動生成 | 📁 預先準備 |
| **Streamlit Cloud** | ✅ 自動初始化 | ✅ 需上傳 DB |

---

## 🔄 使用情境

### 使用 app.py 當：
- ✅ 部署到 Streamlit Cloud 供他人訪問
- ✅ 需要即時、最新的天氣資料
- ✅ 應用程式會長期運行
- ✅ 有穩定的網路連線

### 使用 new-app.py 當：
- ✅ 快速 demo 給他人看
- ✅ 離線環境展示
- ✅ 不需要最新資料（例如教學用途）
- ✅ 想要更快的啟動速度
- ✅ 測試功能和 UI

---

## 💾 資料庫準備

### 建立新資料庫
```bash
python fetch_weather.py
```
這會創建 `data.db` 並抓取 28 個地點的資料

### 更新現有資料庫
```bash
# 直接執行會新增資料（保留歷史）
python fetch_weather.py

# 或者刪除舊資料庫後重新建立
rm data.db
python fetch_weather.py
```

---

## 🚀 同時運行兩個版本

可以在不同端口運行兩個版本：

```bash
# Terminal 1: 雲端版
streamlit run app.py

# Terminal 2: 本地版
streamlit run new-app.py --server.port 8502
```

訪問：
- 雲端版: http://localhost:8501
- 本地版: http://localhost:8502

---

## 📁 主要差異

### app.py
```python
# 自動檢測並初始化資料庫
if database_not_exist or empty:
    from fetch_weather import main as fetch_main
    fetch_main()  # 自動抓取
    st.rerun()    # 重新載入
```

### new-app.py  
```python
# 只檢測，不自動抓取
if database_not_exist or empty:
    st.error("Please run: python fetch_weather.py")
    st.stop()  # 停止執行
```

---

## 🎯 推薦使用方式

### 開發與測試階段
1. 使用 `new-app.py` 本地快速測試
2. 定期執行 `fetch_weather.py` 更新資料

### 正式部署階段
1. 將 `app.py` 部署到 Streamlit Cloud
2. 設定好 API keys
3. 讓它自動處理資料抓取

### 展示與教學
1. 預先準備 `data.db`
2. 使用 `new-app.py` 快速展示
3. 無需等待資料抓取

---

## 📞 支援

完整文件請參考：
- [README.md](README.md) - CRISP-DM 完整分析
- [DEPLOYMENT.md](DEPLOYMENT.md) - 部署指南

---

<div align="center">

**選擇適合您的版本開始使用！** 🚀

`app.py` 適合雲端 | `new-app.py` 適合本地

</div>
