# Async Document Processing Workflow System

A full-stack asynchronous document processing system built with FastAPI (backend) and Next.js (frontend) that demonstrates modern web development practices.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
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

### Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✨ Features

- � **Document Upload** - Drag-and-drop interface
- ⚡ **Async Processing** - Background task simulation
- 📊 **Progress Tracking** - Real-time updates
- 🔍 **Search & Filter** - Advanced filtering
- 📤 **Export Functions** - JSON/CSV export
- 📱 **Responsive Design** - Mobile-friendly

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend     │◄──►│   Backend API   │◄──►│   Database      │
│  (Next.js)     │    │   (FastAPI)    │    │   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
predusk/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/v1/        # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   └── schemas/        # Data schemas
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── lib/           # API client
│   │   └── app/           # Pages
│   ├── package.json
│   └── Dockerfile
├── sample-documents/        # Test files
└── docker-compose.yml       # Container setup
```

## 🧪 Testing

Use sample documents in `sample-documents/`:
1. Upload a document
2. Monitor processing progress
3. Review extracted data
4. Export results

## � Documentation

See `SUBMISSION_INSTRUCTIONS.md` for detailed project documentation and assignment requirements.

---

**Built for academic submission demonstrating modern full-stack development practices.**

## 📊 Monitoring

### Health Checks
- Backend: `GET /health`
- Database: Connection status via API
- Redis: Connection status via API
- Celery: Worker status via CLI or API

### Logs

- Backend logs: Available via Docker logs or application logging
- Celery logs: Worker process logs
- Frontend logs: Browser console and server logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in environment variables
   - Verify database exists

2. **Redis Connection Error**
   - Ensure Redis is running
   - Check REDIS_URL in environment variables

3. **Celery Worker Not Processing**
   - Check if Celery worker is running
   - Verify broker connection
   - Check worker logs for errors

4. **WebSocket Connection Issues**
   - Ensure backend is accessible from frontend
   - Check firewall settings
   - Verify WebSocket endpoint is correct

5. **File Upload Issues**
   - Check upload directory permissions
   - Verify file size limits
   - Ensure sufficient disk space

### Getting Help

- Check the logs for detailed error messages
- Verify all services are running correctly
- Ensure environment variables are set correctly
- Check network connectivity between services

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced document parsing (PDF, DOCX, etc.)
- [ ] AI-powered content extraction
- [ ] Document versioning
- [ ] Batch processing capabilities
- [ ] Advanced filtering and search
- [ ] Email notifications
- [ ] Performance analytics and reporting
- [ ] Multi-language support
- [ ] Mobile application

## 📝 Notes

- AI tools were used during development for code generation and assistance
- The document processing logic is simulated for demonstration purposes
- In production, replace with actual parsing libraries and AI services
- Ensure proper security measures before deploying to production
- Regular updates and maintenance are recommended for production use
