'use client'

import { useState, useEffect } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  DollarSign, 
  Target, 
  Zap,
  Calendar,
  Brain,
  Settings,
  Bell,
  RefreshCw
} from 'lucide-react'

// Mock data - In real app, this would come from Supabase
const mockBusinessMetrics = {
  revenue: 45420,
  profit: 12340,
  roi: 2.8,
  growth: 15.5
}

const mockSocialMediaStats = {
  totalPosts: 45,
  engagement: 8.5,
  reach: 25400,
  newFollowers: 320
}

const mockAdPerformance = {
  activeCampaigns: 8,
  totalSpend: 5420,
  conversions: 156,
  ctr: 3.2
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(true)
  const [currentTime, setCurrentTime] = useState(new Date())

  // Simulate loading and real-time updates
  useEffect(() => {
    const timer = setTimeout(() => setIsLoading(false), 1500)
    const clockTimer = setInterval(() => setCurrentTime(new Date()), 1000)
    
    return () => {
      clearTimeout(timer)
      clearInterval(clockTimer)
    }
  }, [])

  const StatCard = ({ 
    title, 
    value, 
    change, 
    icon: Icon, 
    color = 'blue',
    isLoading = false 
  }: {
    title: string
    value: string | number
    change: string
    icon: any
    color?: string
    isLoading?: boolean
  }) => (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          {isLoading ? (
            <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
          ) : (
            <p className="text-2xl font-bold text-gray-900">{value}</p>
          )}
          <p className={`text-sm ${change.startsWith('+') ? 'text-green-600' : 'text-red-600'} flex items-center gap-1`}>
            <TrendingUp className="w-4 h-4" />
            {change}
          </p>
        </div>
        <div className={`p-3 rounded-full bg-${color}-100`}>
          <Icon className={`w-6 h-6 text-${color}-600`} />
        </div>
      </div>
    </div>
  )

  const QuickAction = ({ 
    title, 
    description, 
    icon: Icon, 
    onClick,
    color = 'blue' 
  }: {
    title: string
    description: string
    icon: any
    onClick: () => void
    color?: string
  }) => (
    <button
      onClick={onClick}
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 text-left hover:shadow-md transition-shadow group"
    >
      <div className="flex items-start gap-4">
        <div className={`p-3 rounded-full bg-${color}-100 group-hover:bg-${color}-200 transition-colors`}>
          <Icon className={`w-6 h-6 text-${color}-600`} />
        </div>
        <div>
          <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
      </div>
    </button>
  )

  const AIInsightCard = ({ 
    title, 
    content, 
    confidence 
  }: { 
    title: string
    content: string
    confidence: number 
  }) => (
    <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 border border-purple-200">
      <div className="flex items-center gap-2 mb-3">
        <Brain className="w-5 h-5 text-purple-600" />
        <h3 className="font-semibold text-gray-900">{title}</h3>
        <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
          {confidence}% confidence
        </span>
      </div>
      <p className="text-sm text-gray-700">{content}</p>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">AI Business System</h1>
                <p className="text-xs text-gray-500">Intelligent Business Management</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-600">
                {currentTime.toLocaleTimeString()}
              </div>
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Bell className="w-5 h-5" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome to Your AI-Powered Business Dashboard
          </h2>
          <p className="text-gray-600">
            Real-time insights, automated workflows, and intelligent recommendations to grow your business.
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Revenue"
            value={`$${mockBusinessMetrics.revenue.toLocaleString()}`}
            change="+15.5%"
            icon={DollarSign}
            color="green"
            isLoading={isLoading}
          />
          <StatCard
            title="ROI"
            value={`${mockBusinessMetrics.roi}x`}
            change="+8.2%"
            icon={TrendingUp}
            color="blue"
            isLoading={isLoading}
          />
          <StatCard
            title="Social Reach"
            value={mockSocialMediaStats.reach.toLocaleString()}
            change="+12.3%"
            icon={Users}
            color="purple"
            isLoading={isLoading}
          />
          <StatCard
            title="Active Campaigns"
            value={mockAdPerformance.activeCampaigns}
            change="+3 new"
            icon={Target}
            color="orange"
            isLoading={isLoading}
          />
        </div>

        {/* AI Insights */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-900 flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-600" />
              AI Insights
            </h3>
            <button className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1">
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AIInsightCard
              title="Optimal Posting Time"
              content="Based on audience analysis, posting at 10:30 AM on weekdays shows 23% higher engagement."
              confidence={89}
            />
            <AIInsightCard
              title="Revenue Opportunity"
              content="Increasing ad spend on Facebook by 15% could generate an additional $2,300 in revenue this month."
              confidence={76}
            />
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <QuickAction
              title="Schedule Social Post"
              description="Create and schedule posts across all platforms"
              icon={Calendar}
              onClick={() => alert('Social Media Manager - Coming up next!')}
              color="blue"
            />
            <QuickAction
              title="Generate Ad Campaign"
              description="AI-powered ad creation and optimization"
              icon={Target}
              onClick={() => alert('Ad Generator - Coming up next!')}
              color="green"
            />
            <QuickAction
              title="Analyze Competitors"
              description="Get insights on competitor strategies"
              icon={BarChart3}
              onClick={() => alert('Competitor Analysis - Coming up next!')}
              color="purple"
            />
          </div>
        </div>

        {/* System Status */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">AI Services: Online</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Database: Connected</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span className="text-sm text-gray-600">N8N Automation: Syncing</span>
            </div>
          </div>
        </div>

        {/* Development Note */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">🚀 Development Progress</h3>
          <p className="text-blue-800 mb-4">
            This is the main dashboard of your AI Business System. The foundation is complete with:
          </p>
          <ul className="list-disc list-inside text-blue-700 space-y-1 mb-4">
            <li>✅ Next.js 14 + TypeScript + Tailwind CSS</li>
            <li>✅ Supabase integration ready</li>
            <li>✅ OpenAI services configured</li>
            <li>✅ Real-time dashboard with mock data</li>
            <li>🔄 Social Media Manager (next)</li>
            <li>⏳ Ad Generator & Analytics</li>
            <li>⏳ N8N Automation workflows</li>
          </ul>
          <p className="text-sm text-blue-600">
            Next: I&apos;ll build the Social Media Manager with real posting capabilities!
          </p>
        </div>
      </main>
    </div>
  )
}
