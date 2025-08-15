# 🚀 AI-Powered Business System

[![CI/CD Pipeline](https://github.com/fuwiak/MVP_social_app/actions/workflows/ci.yml/badge.svg)](https://github.com/fuwiak/MVP_social_app/actions/workflows/ci.yml)
[![Code Quality](https://github.com/fuwiak/MVP_social_app/actions/workflows/quality.yml/badge.svg)](https://github.com/fuwiak/MVP_social_app/actions/workflows/quality.yml)
[![Docker Build](https://github.com/fuwiak/MVP_social_app/actions/workflows/docker-build.yml/badge.svg)](https://github.com/fuwiak/MVP_social_app/actions/workflows/docker-build.yml)

Complete AI-driven business management system with automation, analytics, and intelligent insights.

## 🏗️ **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Frontend                         │
│                   (Port: 3000)                             │
│  ┌─────────────────┬─────────────────┬─────────────────┐   │
│  │   Dashboard     │  Social Media   │   Analytics     │   │
│  │   Management    │   Manager       │   & Reports     │   │
│  └─────────────────┴─────────────────┴─────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST API
┌─────────────────────────▼───────────────────────────────────┐
│                   FastAPI Backend                          │
│                   (Port: 8000)                             │
│  ┌─────────────────┬─────────────────┬─────────────────┐   │
│  │   AI Services   │   Automation    │   Data Layer    │   │
│  │   (OpenAI)      │   (N8N)         │   (Supabase)    │   │
│  └─────────────────┴─────────────────┴─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 **Features Implemented**

### ✅ **Core Foundation**
- Next.js 14 + TypeScript + Tailwind CSS
- FastAPI backend with Python
- Supabase database integration
- OpenAI AI services
- Complete API documentation

### ✅ **AI Business Dashboard**
- Real-time business metrics
- AI-generated insights
- System health monitoring
- Activity tracking
- Interactive widgets

### ✅ **Social Media Manager**
- Multi-platform posting (Instagram, LinkedIn, Twitter, Facebook)
- AI content generation
- Optimal timing analysis
- Engagement tracking
- Content scheduling
- Performance analytics

### ✅ **Analytics & Reporting**
- Revenue analytics
- Social media performance
- Ad campaign tracking
- ROI analysis
- Dashboard summaries

### ✅ **Automation System**
- N8N workflow integration
- Rule-based automation
- Execution monitoring
- Performance metrics
- Background task processing

### ✅ **Brand Assets Manager**
- Digital asset storage
- File upload system
- Asset categorization
- Usage analytics
- Collections management

### ✅ **Cash Flow Tracking**
- Income/expense tracking
- Category management
- Budget analysis
- Cash flow forecasting
- Financial insights

### ✅ **Ad Campaign Management**
- Campaign creation & management
- Performance tracking
- AI-powered optimization
- Creative generation
- Budget recommendations

## 🛠️ **Tech Stack**

### **Frontend**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Icon library
- **Recharts** - Data visualization
- **React Hot Toast** - Notifications

### **Backend**
- **FastAPI** - Modern Python web framework
- **Python 3.9+** - Programming language
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python-dotenv** - Environment management

### **Database & Storage**
- **Supabase** - PostgreSQL database
- **File storage** - Asset management
- **Real-time subscriptions** - Live updates

### **AI & Integrations**
- **OpenAI GPT-4** - Content generation & insights
- **N8N** - Workflow automation
- **Social Media APIs** - Platform integrations
- **Analytics APIs** - Performance tracking

## 🚀 **Quick Start**

### **Prerequisites**
- Docker & Docker Compose (recommended)
- OR Node.js 18+ with pnpm + Python 3.9+ (manual setup)
- Supabase account
- OpenAI API key

## 🐳 **Docker Setup (Recommended)**

### **Option 1: Super Quick Start**
```bash
# Clone and setup everything at once
git clone <your-repo>
cd ai-business-system

# One command setup
make quick-start

# Edit .env file with your API keys
nano .env

# Start frontend separately (for hot reload)
pnpm install && pnpm dev
# Frontend: http://localhost:3000
# Backend: http://localhost:8000 (already running in Docker)
```

### **Option 2: Step by Step Docker**
```bash
# 1. Setup environment
cp env.docker.example .env
# Edit .env with your API keys

# 2. Build and start services
make build
make up

# 3. Start frontend development server
pnpm install
pnpm dev

# Available at:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### **Option 3: Full Production Docker**
```bash
# Start everything including frontend in Docker
make build
make up

# With N8N automation
make up-automation

# Available at:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# N8N: http://localhost:5678 (admin/admin123)
```

### **Docker Management Commands**
```bash
# Show all available commands
make help

# Common commands
make dev          # Development backend only
make up           # Production environment
make down         # Stop all services
make logs         # Show logs
make status       # Show container status
make clean        # Clean up resources
make health       # Health check
```

## 🛠️ **Manual Setup (Without Docker)**

### **1. Setup Frontend**
```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev
# Frontend available at: http://localhost:3000
```

### **2. Setup Backend**
```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp env.example .env
# Edit .env with your API keys

# Start FastAPI server
python start.py
# Backend available at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

### **3. Environment Variables**

**For Docker (.env in root):**
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
OPENAI_API_KEY=your_openai_api_key
# ... other API keys (see env.docker.example)
```

**For manual setup:**
- Frontend (.env.local): NEXT_PUBLIC_* variables
- Backend (.env): All backend variables

## 📊 **Database Schema**

The system uses the following main tables in Supabase:

```sql
-- Business Metrics
CREATE TABLE business_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  date DATE NOT NULL,
  revenue DECIMAL(10,2),
  expenses DECIMAL(10,2),
  profit DECIMAL(10,2),
  roi DECIMAL(5,2),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Social Media Posts
CREATE TABLE social_media_posts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  platform VARCHAR(50) NOT NULL,
  content TEXT NOT NULL,
  media_url TEXT,
  scheduled_time TIMESTAMP,
  posted_time TIMESTAMP,
  status VARCHAR(20) DEFAULT 'draft',
  engagement JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Ad Campaigns
CREATE TABLE ad_campaigns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  platform VARCHAR(50) NOT NULL,
  budget DECIMAL(10,2),
  spent DECIMAL(10,2) DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  impressions INTEGER DEFAULT 0,
  conversions INTEGER DEFAULT 0,
  ctr DECIMAL(5,2) DEFAULT 0,
  cpc DECIMAL(5,2) DEFAULT 0,
  roas DECIMAL(5,2) DEFAULT 0,
  status VARCHAR(20) DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Cash Flow
CREATE TABLE cash_flow (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  type VARCHAR(20) NOT NULL, -- 'income' or 'expense'
  category VARCHAR(100) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  description TEXT,
  date DATE NOT NULL,
  tags JSONB DEFAULT '[]',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Brand Assets
CREATE TABLE brand_assets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,
  url TEXT NOT NULL,
  tags JSONB DEFAULT '[]',
  created_at TIMESTAMP DEFAULT NOW()
);

-- AI Insights
CREATE TABLE ai_insights (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255),
  content TEXT,
  confidence DECIMAL(3,2),
  data_source VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 🔌 **API Endpoints**

### **Dashboard**
- `GET /api/dashboard/metrics` - Business metrics
- `GET /api/dashboard/insights` - AI insights
- `GET /api/dashboard/system-status` - System health
- `POST /api/dashboard/refresh-insights` - Refresh AI insights

### **Social Media**
- `GET /api/social-media/posts` - Get posts
- `POST /api/social-media/posts` - Create post
- `POST /api/social-media/generate-content` - AI content generation
- `GET /api/social-media/optimal-times/{platform}` - Optimal posting times
- `GET /api/social-media/analytics/engagement` - Engagement analytics

### **AI Services**
- `POST /api/ai/generate-strategy` - Business strategy
- `POST /api/ai/analyze-competitors` - Competitor analysis
- `POST /api/ai/forecast-roi` - ROI forecasting
- `GET /api/ai/insights/{type}` - Get insights by type

### **Analytics**
- `GET /api/analytics/revenue` - Revenue analytics
- `GET /api/analytics/social-performance` - Social performance
- `GET /api/analytics/ad-performance` - Ad performance
- `GET /api/analytics/roi-analysis` - ROI analysis

### **Automation**
- `GET /api/automation/rules` - Automation rules
- `POST /api/automation/rules` - Create rule
- `GET /api/automation/workflows/n8n` - N8N workflows
- `POST /api/automation/trigger/{rule_id}` - Trigger rule

### **Brand Assets**
- `GET /api/brand-assets/assets` - Get assets
- `POST /api/brand-assets/assets` - Create asset
- `POST /api/brand-assets/assets/upload` - Upload file
- `GET /api/brand-assets/collections` - Asset collections

### **Cash Flow**
- `GET /api/cash-flow/entries` - Cash flow entries
- `POST /api/cash-flow/entries` - Create entry
- `GET /api/cash-flow/summary` - Financial summary
- `GET /api/cash-flow/forecast` - Cash flow forecast

### **Ad Campaigns**
- `GET /api/ad-campaigns/campaigns` - Get campaigns
- `POST /api/ad-campaigns/campaigns` - Create campaign
- `GET /api/ad-campaigns/campaigns/{id}` - Campaign details
- `POST /api/ad-campaigns/campaigns/{id}/optimize` - AI optimization

## 🤖 **AI Features**

### **Content Generation**
- Social media posts with platform optimization
- Ad copy and creative suggestions
- Business strategy recommendations
- Competitive analysis insights

### **Predictive Analytics**
- ROI forecasting
- Cash flow predictions
- Performance optimization
- Market trend analysis

### **Automation Intelligence**
- Optimal posting time detection
- Audience behavior analysis
- Budget optimization recommendations
- Performance anomaly detection

## 🔧 **Development**

### **Project Structure**
```
ai-business-system/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Dashboard
│   ├── social-media/      # Social media manager
│   ├── globals.css        # Global styles
│   └── layout.tsx         # Root layout
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── core/          # Core modules
│   │   ├── routers/       # API routes
│   │   └── services/      # Business logic
│   ├── main.py           # FastAPI app
│   └── requirements.txt   # Python dependencies
├── lib/                   # Shared utilities
│   ├── api.ts            # API client
│   └── supabase.ts       # Database client
├── components/            # React components (future)
└── README.md             # This file
```

### **Code Style**
- TypeScript for type safety
- ESLint + Prettier for formatting
- Pydantic for API validation
- Comprehensive error handling
- Detailed API documentation

### **Testing** (Future Implementation)
- Jest for frontend testing
- Pytest for backend testing
- Integration test suite
- API endpoint testing

## 🚀 **Deployment**

### **🐳 Docker Deployment (Recommended)**

#### **Production with Docker Compose**
```bash
# 1. Clone repository on server
git clone <your-repo>
cd ai-business-system

# 2. Setup production environment
cp env.docker.example .env
# Edit .env with production API keys

# 3. Deploy with Docker Compose
docker-compose up -d --build

# 4. Monitor logs
docker-compose logs -f
```

#### **Individual Service Deployment**
```bash
# Backend only
docker build -t ai-business-backend ./backend
docker run -d -p 8000:8000 --env-file .env ai-business-backend

# Frontend only  
docker build -t ai-business-frontend .
docker run -d -p 3000:3000 ai-business-frontend
```

### **☁️ Cloud Deployment**

#### **Frontend (Vercel)**
```bash
# Deploy to Vercel
vercel --prod

# Environment variables in Vercel:
# NEXT_PUBLIC_API_URL=https://your-api-domain.com
# NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
# NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

#### **Backend (Railway/Render/DigitalOcean)**
```bash
# Railway deployment
railway login
railway init
railway add
railway deploy

# Or Docker Hub + any cloud provider
docker build -t yourusername/ai-business-backend ./backend
docker push yourusername/ai-business-backend
```

#### **Full Stack (DigitalOcean App Platform)**
```yaml
# .do/app.yaml
name: ai-business-system
services:
- name: backend
  source_dir: /backend
  github:
    repo: your-username/ai-business-system
    branch: main
  run_command: uvicorn main:app --host 0.0.0.0 --port 8080
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  
- name: frontend
  source_dir: /
  github:
    repo: your-username/ai-business-system
    branch: main
  build_command: pnpm install && pnpm build
  run_command: pnpm start
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
```

### **🔧 Production Checklist**
- [ ] All API keys configured
- [ ] Database URLs updated
- [ ] CORS origins set correctly
- [ ] Security keys rotated
- [ ] SSL certificates installed
- [ ] Monitoring setup
- [ ] Backup strategy implemented
- [ ] Health checks configured

## 📈 **Future Enhancements**

### **Phase 1 Additions**
- [ ] Email marketing automation
- [ ] Customer CRM integration
- [ ] Advanced reporting dashboard
- [ ] Mobile app (React Native)

### **Phase 2 Features**
- [ ] AI chatbot for customer support
- [ ] Predictive sales analytics
- [ ] Advanced competitor monitoring
- [ ] Integration marketplace

### **Phase 3 Scaling**
- [ ] Multi-tenant architecture
- [ ] White-label solutions
- [ ] Enterprise features
- [ ] Advanced AI models

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- 📖 **Documentation**: Check `/docs` for detailed guides
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💬 **Discussions**: Join our community discussions
- 📧 **Contact**: Email for enterprise support

---

**Built with ❤️ using Next.js, FastAPI, and AI**