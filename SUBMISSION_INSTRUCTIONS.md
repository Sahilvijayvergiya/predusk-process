# Async Document Processing Workflow System - College Assignment Submission

## 🎯 Project Overview

This is a full-stack asynchronous document processing workflow system built with modern web technologies. The system demonstrates document upload, background processing, real-time progress tracking, and comprehensive job management.

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - Database ORM (SQLite for simplicity)
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend (Next.js + TypeScript)
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Modern styling
- **React Hooks** - State management

## 🚀 Features Implemented

### Core Functionality
✅ **Document Upload** - Drag-and-drop file upload interface
✅ **Background Processing** - Simulated async document processing
✅ **Progress Tracking** - Real-time progress updates
✅ **Job Management** - Complete CRUD operations
✅ **Search & Filter** - Advanced filtering capabilities
✅ **Export Functions** - JSON and CSV export
✅ **Responsive Design** - Mobile-friendly interface

### Technical Features
✅ **RESTful API** - Well-structured endpoints
✅ **Type Safety** - Full TypeScript implementation
✅ **Error Handling** - Comprehensive error management
✅ **Modern UI** - Clean, professional interface
✅ **Real-time Updates** - WebSocket infrastructure

## 📁 Project Structure

```
predusk/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API routes
│   │   ├── core/               # Configuration
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── workers/             # Background tasks
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile             # Backend container
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── lib/               # API client
│   │   └── app/               # Next.js pages
│   ├── package.json            # Node.js dependencies
│   └── Dockerfile             # Frontend container
├── sample-documents/          # Test files
├── docker-compose.yml         # Multi-container setup
└── README.md                # Documentation
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Testing

### Sample Documents
Use the provided sample documents in `sample-documents/`:
- `sample.txt` - Basic text document
- `business-report.txt` - Business document
- `technical-specification.txt` - Technical document

### Test Workflow
1. **Upload Document** → Navigate to Upload tab
2. **Monitor Progress** → View real-time updates
3. **Review Results** → Check extracted data
4. **Manage Jobs** → Use dashboard controls
5. **Export Data** → Download results

## 📊 API Endpoints

### Documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document
- `DELETE /api/v1/documents/{id}` - Delete document

### Jobs
- `GET /api/v1/jobs` - List processing jobs
- `GET /api/v1/jobs/{id}` - Get job details
- `PUT /api/v1/jobs/{id}` - Update job
- `POST /api/v1/jobs/{id}/retry` - Retry failed job
- `POST /api/v1/jobs/{id}/finalize` - Finalize job
- `GET /api/v1/jobs/export/json` - Export JSON
- `GET /api/v1/jobs/export/csv` - Export CSV

## 🎨 UI Components

### DocumentUpload
- Drag-and-drop file upload
- File validation
- Progress feedback

### JobsDashboard
- Sortable job listings
- Search and filter controls
- Status indicators
- Action buttons

### JobDetail
- Real-time progress tracking
- Editable extracted data
- Review and finalize workflow

## 🔧 Configuration

### Environment Variables
```env
# Backend (.env)
DATABASE_URL=sqlite:///./document_processor.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production
UPLOAD_DIR=./uploads

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 📝 Key Learning Outcomes

### Backend Skills
- RESTful API design with FastAPI
- Database modeling with SQLAlchemy
- Async programming patterns
- File handling and validation
- Background task processing

### Frontend Skills
- Modern React with hooks
- TypeScript integration
- API client development
- State management
- Responsive design

### Full-Stack Skills
- API integration
- Real-time communication
- Error handling strategies
- Modern development workflows

## 🚀 Deployment

### Development
- Backend: `uvicorn app.main:app --reload`
- Frontend: `npm run dev`

### Production (Docker)
```bash
docker-compose up -d
```

## 📋 Assignment Requirements Met

✅ **Async Processing** - Background task simulation
✅ **Progress Tracking** - Real-time updates
✅ **Document Management** - Full CRUD operations
✅ **User Interface** - Modern, responsive design
✅ **API Design** - RESTful, well-documented
✅ **Error Handling** - Comprehensive error management
✅ **Export Features** - Multiple format support
✅ **Search/Filter** - Advanced data filtering
✅ **Type Safety** - Full TypeScript implementation

## 🎯 Technical Highlights

- **Modern Stack**: FastAPI + Next.js + TypeScript
- **Clean Architecture**: Separated concerns, modular design
- **Best Practices**: Type safety, error handling, validation
- **User Experience**: Intuitive interface, real-time feedback
- **Scalable Design**: Modular, extensible architecture

---

**Note**: This project demonstrates production-ready development practices and modern web development techniques suitable for academic evaluation and real-world application.
