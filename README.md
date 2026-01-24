# Social Media Well-being Predictor 🧠

Hệ thống phân tích sức khỏe tinh thần dựa trên thói quen sử dụng mạng xã hội (Instagram) và các yếu tố lối sống, sử dụng **Machine Learning** để đưa ra đánh giá và khuyến nghị cá nhân hóa.

## ✨ Tính năng chính

- 🎯 **Dự đoán Happiness Score** (0-10) - Đánh giá mức độ hạnh phúc
- 📊 **Dự đoán Stress Score** (0-10) - Đánh giá mức độ căng thẳng  
- 👤 **Phân loại Persona** - Light User, Moderate User, Doom-Scroller
- 💡 **Khuyến nghị cá nhân hóa** - Gợi ý cải thiện dựa trên kết quả phân tích
- 🎨 **Giao diện đẹp** - Modern dark theme với responsive design

---

## 📋 Yêu cầu hệ thống

- **Python**: 3.8+ (khuyến nghị 3.11+)
- **pip**: Python package manager
- **Web browser**: Chrome, Firefox, Edge, Safari (phiên bản mới)
- **Optional**: Node.js 18+ và npm (cho frontend development)

---

## 🚀 Hướng dẫn cài đặt

### Bước 1: Cài đặt Backend

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 2: Chuẩn bị Models

Backend đã được nâng cấp lên scikit-learn 1.5.2 để tương thích với models được train trên Google Colab.

**Nếu vẫn gặp lỗi load models**, xem phần [Troubleshooting](#-troubleshooting) bên dưới.

---

## 🎮 Cách chạy ứng dụng

### Phương án 1: Sử dụng Mock API (Khuyến nghị cho demo)

Mock API sử dụng logic đơn giản thay vì ML models thật, phù hợp để test giao diện.

**Windows - Dùng file .bat:**
```bash
# Terminal 1: Chạy backend mock
start_backend_mock.bat

# Terminal 2: Mở frontend
# Click đúp vào frontend/index.html
```

**Chạy thủ công:**
```bash
# Terminal 1: Backend Mock
cd backend
python -m uvicorn app.main_mock:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (optional HTTP server)
cd frontend
python -m http.server 3000
# Sau đó mở: http://localhost:3000
```

### Phương án 2: Sử dụng ML Models thật

**Windows - Dùng file .bat:**
```bash
# Terminal 1: Chạy backend với models
start_backend.bat

# Terminal 2: Mở frontend
# Click đúp vào frontend/index.html
```

**Chạy thủ công:**
```bash
# Terminal 1: Backend Real
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
# Mở file frontend/index.html bằng browser hoặc:
cd frontend
python -m http.server 3000
```

### Truy cập ứng dụng

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: Mở file `frontend/index.html` hoặc http://localhost:3000

---

## 🎯 Cách sử dụng

1. **Mở frontend** trong browser
2. **Nhập thông tin** vào form (đã có giá trị mặc định sẵn)
3. **Tùy chỉnh** các giá trị theo nhu cầu hoặc giữ nguyên mặc định
4. **Click "Phân tích ngay"** để gửi request
5. **Xem kết quả**:
   - Chỉ số Hạnh phúc (0-10)
   - Chỉ số Căng thẳng (0-10)
   - Loại người dùng
   - Gợi ý cải thiện cá nhân hóa

---

## 📊 Cấu trúc dự án

```
Root/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI với ML models
│   │   ├── main_mock.py         # FastAPI với Mock API
│   │   ├── schemas.py           # Pydantic data models
│   │   ├── utils.py             # Utility functions
│   │   └── ml/
│   │       ├── __init__.py
│   │       ├── loader.py        # Model loader
│   │       └── predictor.py     # Prediction logic
│   ├── models/                   # ML models (joblib files)
│   │   ├── happiness_pipeline.joblib
│   │   ├── stress_pipeline.joblib
│   │   ├── persona_pipeline.joblib
│   │   ├── features.json
│   │   └── persona_labels.json
│   ├── requirements.txt          # Python dependencies
│   ├── test_models.py           # Model testing script
│   └── train_models.py          # Model training script
├── frontend/
│   ├── index.html               # Main HTML page
│   └── src/
│       ├── app.js              # JavaScript logic
│       └── styles.css          # CSS styling
├── Instagram.ipynb              # Jupyter notebook for training
├── instagram_users_lifestyle.csv # Dataset
├── start_backend.bat            # Windows: Run real backend
├── start_backend_mock.bat       # Windows: Run mock backend
├── start_frontend.bat           # Windows: Run frontend
└── README.md                    # This file
```

---

## 🔌 API Endpoints

### Health Check
```http
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Social Media Well-being Predictor API"
}
```

### Predict Well-being
```http
POST /predict
Content-Type: application/json
```

**Request Body** (28 features):
```json
{
  "age": 25,
  "gender": "Male",
  "country": "Vietnam",
  "urban_rural": "Urban",
  "income_level": "Medium",
  "employment_status": "Full-time",
  "education_level": "Bachelor",
  "relationship_status": "Single",
  "has_children": "No",
  "sleep_hours_per_night": 7,
  "exercise_hours_per_week": 3,
  "daily_steps_count": 5000,
  "diet_quality": "Average",
  "smoking": "No",
  "alcohol_frequency": "Rarely",
  "body_mass_index": 22.5,
  "weekly_work_hours": 40,
  "hobbies_count": 2,
  "social_events_per_month": 4,
  "daily_active_minutes_instagram": 60,
  "sessions_per_day": 5,
  "reels_watched_per_day": 10,
  "stories_viewed_per_day": 20,
  "time_on_feed_per_day": 30,
  "time_on_reels_per_day": 30,
  "likes_given_per_day": 15,
  "comments_written_per_day": 3,
  "notification_response_rate": 0.5
}
```

**Response:**
```json
{
  "happiness_score": 7.5,
  "stress_score": 4.2,
  "persona": "Light User",
  "recommendations": [
    "Điều chỉnh thời gian sử dụng Instagram",
    "Tăng cường hoạt động ngoài trời",
    "..."
  ]
}
```

### Get Features List
```http
GET /features
```

### Get Personas List
```http
GET /personas
```

---

## 📝 28 Features đầu vào

### 👤 Thông tin cá nhân (9 features)
| Feature | Mô tả | Giá trị |
|---------|-------|---------|
| `age` | Tuổi | 13-100 |
| `gender` | Giới tính | Male, Female, Other |
| `country` | Quốc gia | Text |
| `urban_rural` | Khu vực | Urban, Rural |
| `income_level` | Mức thu nhập | Low, Medium, High |
| `employment_status` | Tình trạng việc làm | Unemployed, Part-time, Full-time, Self-employed, Student, Retired |
| `education_level` | Trình độ học vấn | High School, Associate, Bachelor, Master, PhD |
| `relationship_status` | Tình trạng hôn nhân | Single, In a relationship, Married, Divorced, Widowed |
| `has_children` | Có con | Yes, No |

### 💪 Chỉ số sức khỏe (7 features)
| Feature | Mô tả | Giá trị |
|---------|-------|---------|
| `sleep_hours_per_night` | Giờ ngủ mỗi đêm | 0-24 |
| `exercise_hours_per_week` | Giờ tập thể dục mỗi tuần | ≥ 0 |
| `daily_steps_count` | Số bước mỗi ngày | ≥ 0 |
| `diet_quality` | Chất lượng chế độ ăn | Poor, Average, Good, Excellent |
| `smoking` | Hút thuốc | Yes, No |
| `alcohol_frequency` | Tần suất uống rượu | Never, Rarely, Occasionally, Frequently, Daily |
| `body_mass_index` | BMI | 10-60 |

### 💼 Công việc & Xã hội (3 features)
| Feature | Mô tả | Giá trị |
|---------|-------|---------|
| `weekly_work_hours` | Giờ làm việc mỗi tuần | ≥ 0 |
| `hobbies_count` | Số sở thích | ≥ 0 |
| `social_events_per_month` | Sự kiện xã hội mỗi tháng | ≥ 0 |

### 📱 Instagram Usage (9 features)
| Feature | Mô tả | Giá trị |
|---------|-------|---------|
| `daily_active_minutes_instagram` | Phút hoạt động mỗi ngày | ≥ 0 |
| `sessions_per_day` | Số phiên mỗi ngày | ≥ 0 |
| `reels_watched_per_day` | Reels xem mỗi ngày | ≥ 0 |
| `stories_viewed_per_day` | Stories xem mỗi ngày | ≥ 0 |
| `time_on_feed_per_day` | Thời gian xem feed (phút) | ≥ 0 |
| `time_on_reels_per_day` | Thời gian xem reels (phút) | ≥ 0 |
| `likes_given_per_day` | Likes cho mỗi ngày | ≥ 0 |
| `comments_written_per_day` | Comments viết mỗi ngày | ≥ 0 |
| `notification_response_rate` | Tỷ lệ phản hồi thông báo | 0-1 |

---

## 🛠️ Công nghệ sử dụng

### Backend
- **FastAPI** - Web framework hiện đại, hiệu suất cao
- **Scikit-learn 1.5.2** - Machine Learning models
- **Pydantic** - Data validation và serialization
- **Joblib** - Model persistence
- **Uvicorn** - ASGI server

### Frontend
- **HTML5/CSS3** - Giao diện hiện đại với dark theme
- **Vanilla JavaScript** - Logic và API calls
- **Google Fonts (Inter)** - Typography
- **Responsive Design** - Tương thích mọi thiết bị

### Machine Learning
- **RandomForestRegressor** - Happiness & Stress prediction
- **RandomForestClassifier** - Persona classification
- **Pipeline** - Data preprocessing và model chaining
- **StandardScaler** - Feature normalization

---

## 🧪 Test API với curl

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 25,
    "gender": "Male",
    "country": "Vietnam",
    "urban_rural": "Urban",
    "income_level": "Medium",
    "employment_status": "Full-time",
    "education_level": "Bachelor",
    "relationship_status": "Single",
    "has_children": "No",
    "sleep_hours_per_night": 7,
    "exercise_hours_per_week": 3,
    "daily_steps_count": 5000,
    "diet_quality": "Average",
    "smoking": "No",
    "alcohol_frequency": "Rarely",
    "body_mass_index": 22.5,
    "weekly_work_hours": 40,
    "hobbies_count": 2,
    "social_events_per_month": 4,
    "daily_active_minutes_instagram": 60,
    "sessions_per_day": 5,
    "reels_watched_per_day": 10,
    "stories_viewed_per_day": 20,
    "time_on_feed_per_day": 30,
    "time_on_reels_per_day": 30,
    "likes_given_per_day": 15,
    "comments_written_per_day": 3,
    "notification_response_rate": 0.5
  }'
```

---

## 🐛 Troubleshooting

### Backend không chạy được

**Vấn đề**: Backend không start hoặc báo lỗi import
```bash
# Kiểm tra Python version
python --version  # Phải >= 3.8

# Kiểm tra dependencies đã cài
pip list

# Cài lại dependencies
cd backend
pip install -r requirements.txt
```

### Lỗi load ML models (scikit-learn version mismatch)

**Vấn đề**: Models được train với sklearn version khác

**Giải pháp đã áp dụng**:
- Backend đã được nâng cấp lên **scikit-learn 1.5.2**
- Tương thích với models train trên Google Colab

**Nếu vẫn gặp lỗi**, dùng giải pháp dự phòng:

#### Giải pháp 1: Dùng Mock API
```bash
cd backend
python -m uvicorn app.main_mock:app --reload --host 0.0.0.0 --port 8000
```

Mock API sử dụng logic đơn giản để tính toán kết quả, không cần load models.

#### Giải pháp 2: Retrain models
```bash
# 1. Upload dataset lên Google Drive
# 2. Chạy notebook Instagram.ipynb trên Google Colab
# 3. Download các file .joblib về thư mục backend/models/
```

**Requirements để retrain**:
- Dataset: `instagram_users_lifestyle.csv`
- Notebook: `Instagram.ipynb`
- Google Colab (khuyến nghị) hoặc Jupyter local

### Frontend không kết nối Backend

**Vấn đề**: Frontend không gọi được API

**Kiểm tra**:
1. Backend đang chạy tại http://localhost:8000
2. Mở Console trong browser (F12) để xem lỗi
3. Kiểm tra file `frontend/src/app.js` - dòng `const API_BASE_URL`

**CORS Issues**:
- FastAPI đã enable CORS cho tất cả origins
- Kiểm tra `main.py` hoặc `main_mock.py` - phần `CORSMiddleware`

### Form validation errors

**Vấn đề**: Frontend báo lỗi khi submit form

**Kiểm tra**:
- Tất cả 28 fields đã được điền
- Giá trị nằm trong range hợp lệ (xem bảng features)
- Categorical values đúng format (Yes/No, Male/Female/Other, v.v.)

### Lỗi import modules

**Vấn đề**: `ModuleNotFoundError: No module named 'app'`

**Giải pháp**:
```bash
# Đảm bảo đang chạy từ đúng thư mục
cd backend

# Đảm bảo các file __init__.py đã được tạo
# backend/app/__init__.py
# backend/app/ml/__init__.py

# Chạy với python -m
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📚 Tài liệu tham khảo

- **FastAPI**: https://fastapi.tiangolo.com/
- **Scikit-learn**: https://scikit-learn.org/
- **Dataset**: `instagram_users_lifestyle.csv` (439MB, 10K+ users)
- **Training Notebook**: `Instagram.ipynb`

---

## 🚀 Next Steps

1. ✅ **Hiện tại**: Ứng dụng chạy được với Mock API và Real Models
2. 🔄 **Cải tiến**: 
   - Thêm lưu lịch sử phân tích
   - So sánh kết quả theo thời gian
   - Export PDF report
   - Data visualization charts (Chart.js)
3. 🎨 **Nâng cấp UI**:
   - User authentication
   - Dashboard với metrics
   - Mobile app version

---

## 📧 Liên hệ

**Đồ án môn Trí Tuệ Nhân Tạo - PTIT**  
Học viện Công nghệ Bưu chính Viễn thông

---

© 2026 Social Media Well-being Predictor | PTIT AI Project
