# 🚀 Getting Started - AI Business System

Quick start guide to get your AI Business System running in minutes!

## 📋 **Prerequisites**

### **Option A: Docker (Recommended)**
- Docker Desktop installed
- Docker Compose installed
- Git

### **Option B: Manual Setup**
- Node.js 18+ with pnpm
- Python 3.9+
- Git

### **Required API Keys**
- Supabase account (free tier available)
- OpenAI API key (for AI features)
- Social media API keys (optional)

---

## 🐳 **Quick Start with Docker**

### **1. Clone and Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-business-system

# Quick setup command
make quick-start
```

### **2. Configure Environment**
```bash
# Edit the created .env file
nano .env

# Required variables (minimum):
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
```

### **3. Start the System**
```bash
# Start backend in Docker
make dev

# In another terminal, start frontend for development
pnpm install
pnpm dev
```

### **4. Access the Application**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📖 **API Documentation**: http://localhost:8000/docs

---

## 🛠️ **Manual Setup (No Docker)**

### **1. Setup Backend**
```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Setup environment
cp env.example .env
# Edit .env with your API keys

# Start FastAPI server
python start.py
```

### **2. Setup Frontend**
```bash
# In new terminal, go to project root
cd ..

# Install Node.js dependencies
pnpm install

# Create frontend environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
echo "NEXT_PUBLIC_SUPABASE_URL=your_supabase_url" >> .env.local
echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key" >> .env.local

# Start Next.js development server
pnpm dev
```

---

## 🔑 **API Keys Setup**

### **1. Supabase Setup**
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings → API
4. Copy URL and anon key
5. Copy service role key (for backend)

### **2. OpenAI Setup**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create API key
3. Add billing method (required for API usage)

### **3. Social Media APIs (Optional)**
- **Facebook/Instagram**: Meta for Developers
- **Twitter**: Twitter Developer Portal
- **LinkedIn**: LinkedIn Developer Network

---

## 🧪 **Testing the Setup**

### **1. Health Check**
```bash
# Check backend health
curl http://localhost:8000/health

# Or use make command with Docker
make health
```

### **2. Frontend Check**
- Visit http://localhost:3000
- You should see the AI Business Dashboard
- Check that widgets load with mock data

### **3. API Testing**
```bash
# Test API endpoints
curl http://localhost:8000/api/dashboard/metrics
curl http://localhost:8000/api/social-media/posts
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Kill processes on ports 3000 or 8000
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:8000 | xargs kill -9
```

#### **Docker Build Fails**
```bash
# Clean Docker cache
make clean
docker system prune -a

# Rebuild from scratch
make build
```

#### **API Keys Not Working**
1. Check .env file format (no spaces around =)
2. Restart services after changing environment
3. Verify API keys in provider dashboards

#### **Database Connection Issues**
1. Check Supabase project is active
2. Verify URL and keys are correct
3. Check Supabase dashboard for connection info

### **Docker Specific Issues**

#### **Permission Denied**
```bash
# On Linux/Mac, add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

#### **Container Won't Start**
```bash
# Check logs
make logs

# Check specific service
docker-compose logs backend
docker-compose logs frontend
```

---

## 📊 **Development Workflow**

### **Daily Development**
```bash
# Start development environment
make dev

# In another terminal
pnpm dev

# Make changes to code
# Changes automatically reload
```

### **Testing Changes**
```bash
# View logs
make logs

# Check status
make status

# Restart if needed
make restart
```

### **Database Updates**
```bash
# Reset development database (if using local DB)
make db-reset

# Or update Supabase schema manually
```

---

## 🌟 **Next Steps**

### **1. Explore the Dashboard**
- Check out the main dashboard
- Navigate to Social Media Manager
- Explore analytics sections

### **2. Configure AI Features**
- Test content generation
- Try strategy insights
- Experiment with automation rules

### **3. Setup Social Media Integration**
- Add social media API keys
- Test posting functionality
- Configure automation workflows

### **4. Customize Your Setup**
- Modify dashboard widgets
- Add your brand assets
- Configure cash flow categories

---

## 🆘 **Need Help?**

### **Documentation**
- 📖 Main README.md
- 🔧 API Documentation: http://localhost:8000/docs
- 📊 Architecture overview in README

### **Logs and Debugging**
```bash
# View all logs
make logs

# Backend logs only
make logs-backend

# Check container status
make status
```

### **Make Commands Reference**
```bash
# See all available commands
make help

# Key commands:
make dev          # Development environment
make up           # Production environment
make down         # Stop all services
make clean        # Clean up resources
make health       # Health check
```

---

**🎉 Congratulations! Your AI Business System is now running!**

Visit http://localhost:3000 to start managing your business with AI-powered insights and automation.

---

*For detailed documentation, see the main README.md file.*


