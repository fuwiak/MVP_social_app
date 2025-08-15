'use client'

import { useState, useEffect } from 'react'
import { 
  Calendar,
  Clock,
  Send,
  Image,
  Hash,
  BarChart3,
  Users,
  Heart,
  MessageCircle,
  Share,
  TrendingUp,
  Plus,
  Settings,
  Zap,
  Brain,
  RefreshCw,
  CheckCircle,
  XCircle,
  Clock3
} from 'lucide-react'

// Mock data for social media posts
const mockPosts = [
  {
    id: '1',
    platform: 'instagram',
    content: 'Just launched our new AI-powered business analytics dashboard! 🚀 Helping entrepreneurs make smarter decisions with real-time insights.',
    media_url: '/api/placeholder/400/400',
    scheduled_time: '2024-01-15T10:30:00Z',
    status: 'posted',
    engagement: { likes: 245, comments: 32, shares: 18, reach: 3420 },
    created_at: '2024-01-15T08:00:00Z'
  },
  {
    id: '2',
    platform: 'linkedin',
    content: 'The future of business intelligence is here. Our AI system analyzes market trends and provides actionable insights in real-time.',
    scheduled_time: '2024-01-15T14:00:00Z',
    status: 'scheduled',
    engagement: { likes: 0, comments: 0, shares: 0, reach: 0 },
    created_at: '2024-01-15T09:30:00Z'
  },
  {
    id: '3',
    platform: 'twitter',
    content: 'Small businesses using AI see 40% better ROI on average. Ready to join them? 📈 #AI #BusinessGrowth #SmartBusiness',
    scheduled_time: '2024-01-15T16:30:00Z',
    status: 'draft',
    engagement: { likes: 0, comments: 0, shares: 0, reach: 0 },
    created_at: '2024-01-15T10:00:00Z'
  }
]

const platformConfig = {
  instagram: { 
    name: 'Instagram', 
    color: 'pink', 
    bgColor: 'bg-pink-500',
    maxChars: 2200,
    bestTimes: ['10:00', '14:00', '19:00']
  },
  linkedin: { 
    name: 'LinkedIn', 
    color: 'blue', 
    bgColor: 'bg-blue-600',
    maxChars: 1300,
    bestTimes: ['08:00', '12:00', '17:00']
  },
  twitter: { 
    name: 'Twitter', 
    color: 'sky', 
    bgColor: 'bg-sky-500',
    maxChars: 280,
    bestTimes: ['09:00', '13:00', '18:00']
  },
  facebook: { 
    name: 'Facebook', 
    color: 'blue', 
    bgColor: 'bg-blue-500',
    maxChars: 2000,
    bestTimes: ['10:00', '15:00', '20:00']
  }
}

export default function SocialMediaManager() {
  const [posts, setPosts] = useState(mockPosts)
  const [activeTab, setActiveTab] = useState('overview')
  const [selectedPlatform, setSelectedPlatform] = useState<string[]>(['instagram'])
  const [newPostContent, setNewPostContent] = useState('')
  const [scheduledTime, setScheduledTime] = useState('')
  const [isGeneratingAI, setIsGeneratingAI] = useState(false)
  const [showNewPostModal, setShowNewPostModal] = useState(false)

  // Calculate engagement stats
  const engagementStats = posts.reduce((acc, post) => {
    if (post.status === 'posted') {
      acc.totalLikes += post.engagement.likes
      acc.totalComments += post.engagement.comments
      acc.totalShares += post.engagement.shares
      acc.totalReach += post.engagement.reach
      acc.postsCount += 1
    }
    return acc
  }, { totalLikes: 0, totalComments: 0, totalShares: 0, totalReach: 0, postsCount: 0 })

  const avgEngagement = engagementStats.postsCount > 0 
    ? ((engagementStats.totalLikes + engagementStats.totalComments + engagementStats.totalShares) / engagementStats.postsCount).toFixed(1)
    : 0

  // AI Content Generation
  const generateAIContent = async (prompt: string) => {
    setIsGeneratingAI(true)
    
    // Simulate AI content generation
    setTimeout(() => {
      const aiSuggestions = [
        "Transform your business with AI-powered insights! 🤖 Our latest analytics dashboard helps you make data-driven decisions faster than ever. #BusinessIntelligence #AI",
        "Ready to 10x your business growth? 📈 Discover how successful entrepreneurs are using AI to automate workflows and boost ROI. #Entrepreneurship #Automation",
        "The secret to staying ahead of competition? Real-time business analytics powered by artificial intelligence. Join the revolution! 🚀 #Innovation #SmartBusiness"
      ]
      
      const randomSuggestion = aiSuggestions[Math.floor(Math.random() * aiSuggestions.length)]
      setNewPostContent(randomSuggestion)
      setIsGeneratingAI(false)
    }, 2000)
  }

  const PostCard = ({ post }: { post: typeof mockPosts[0] }) => {
    const platform = platformConfig[post.platform as keyof typeof platformConfig]
    const statusColors = {
      posted: 'bg-green-100 text-green-800',
      scheduled: 'bg-blue-100 text-blue-800',
      draft: 'bg-gray-100 text-gray-800',
      failed: 'bg-red-100 text-red-800'
    }

    const StatusIcon = {
      posted: CheckCircle,
      scheduled: Clock3,
      draft: Clock,
      failed: XCircle
    }

    const IconComponent = StatusIcon[post.status as keyof typeof StatusIcon]

    return (
      <div className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${platform.bgColor}`}></div>
            <span className="font-medium text-gray-900">{platform.name}</span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[post.status]} flex items-center gap-1`}>
              <IconComponent className="w-3 h-3" />
              {post.status}
            </span>
          </div>
          <div className="text-xs text-gray-500">
            {new Date(post.scheduled_time).toLocaleString()}
          </div>
        </div>
        
        <p className="text-gray-700 mb-4 line-clamp-3">{post.content}</p>
        
        {post.status === 'posted' && (
          <div className="grid grid-cols-4 gap-4 pt-4 border-t border-gray-100">
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 text-red-500 mb-1">
                <Heart className="w-4 h-4" />
                <span className="text-sm font-semibold">{post.engagement.likes}</span>
              </div>
              <div className="text-xs text-gray-500">Likes</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 text-blue-500 mb-1">
                <MessageCircle className="w-4 h-4" />
                <span className="text-sm font-semibold">{post.engagement.comments}</span>
              </div>
              <div className="text-xs text-gray-500">Comments</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 text-green-500 mb-1">
                <Share className="w-4 h-4" />
                <span className="text-sm font-semibold">{post.engagement.shares}</span>
              </div>
              <div className="text-xs text-gray-500">Shares</div>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 text-purple-500 mb-1">
                <Users className="w-4 h-4" />
                <span className="text-sm font-semibold">{post.engagement.reach}</span>
              </div>
              <div className="text-xs text-gray-500">Reach</div>
            </div>
          </div>
        )}
      </div>
    )
  }

  const NewPostModal = () => {
    if (!showNewPostModal) return null

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-6 w-full max-w-2xl mx-4">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-gray-900">Create New Post</h3>
            <button 
              onClick={() => setShowNewPostModal(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <XCircle className="w-6 h-6" />
            </button>
          </div>

          {/* Platform Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">Select Platforms</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.entries(platformConfig).map(([key, platform]) => (
                <label key={key} className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedPlatform.includes(key)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedPlatform([...selectedPlatform, key])
                      } else {
                        setSelectedPlatform(selectedPlatform.filter(p => p !== key))
                      }
                    }}
                    className="rounded border-gray-300"
                  />
                  <div className={`w-3 h-3 rounded-full ${platform.bgColor}`}></div>
                  <span className="text-sm">{platform.name}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Content Input */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium text-gray-700">Content</label>
              <button
                onClick={() => generateAIContent('Generate engaging social media post')}
                disabled={isGeneratingAI}
                className="flex items-center gap-2 text-sm text-purple-600 hover:text-purple-700 disabled:opacity-50"
              >
                <Brain className="w-4 h-4" />
                {isGeneratingAI ? 'Generating...' : 'AI Generate'}
              </button>
            </div>
            <textarea
              value={newPostContent}
              onChange={(e) => setNewPostContent(e.target.value)}
              placeholder="What's happening in your business today?"
              className="w-full h-32 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <div className="flex justify-between items-center mt-2">
              <div className="text-sm text-gray-500">
                {selectedPlatform.length > 0 && (
                  <span>
                    Max: {Math.min(...selectedPlatform.map(p => platformConfig[p as keyof typeof platformConfig].maxChars))} characters
                  </span>
                )}
              </div>
              <div className="text-sm text-gray-500">
                {newPostContent.length} characters
              </div>
            </div>
          </div>

          {/* Scheduling */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Schedule Time</label>
            <input
              type="datetime-local"
              value={scheduledTime}
              onChange={(e) => setScheduledTime(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            {selectedPlatform.length > 0 && (
              <div className="mt-2 text-sm text-blue-600">
                💡 Best times for {platformConfig[selectedPlatform[0] as keyof typeof platformConfig].name}: {
                  platformConfig[selectedPlatform[0] as keyof typeof platformConfig].bestTimes.join(', ')
                }
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3">
            <button
              onClick={() => setShowNewPostModal(false)}
              className="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button className="btn-secondary">
              Save as Draft
            </button>
            <button className="btn-primary">
              Schedule Post
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg">
                <Users className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Social Media Manager</h1>
                <p className="text-xs text-gray-500">AI-Powered Content & Automation</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowNewPostModal(true)}
                className="btn-primary flex items-center gap-2"
              >
                <Plus className="w-4 h-4" />
                New Post
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: BarChart3 },
              { id: 'posts', name: 'Posts', icon: Calendar },
              { id: 'analytics', name: 'Analytics', icon: TrendingUp },
              { id: 'automation', name: 'Automation', icon: Zap }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="dashboard-stat">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Reach</p>
                    <p className="text-2xl font-bold text-gray-900">{engagementStats.totalReach.toLocaleString()}</p>
                    <p className="text-sm text-green-600 flex items-center gap-1">
                      <TrendingUp className="w-4 h-4" />
                      +12.5%
                    </p>
                  </div>
                  <div className="p-3 rounded-full bg-blue-100">
                    <Users className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </div>

              <div className="dashboard-stat">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Avg. Engagement</p>
                    <p className="text-2xl font-bold text-gray-900">{avgEngagement}</p>
                    <p className="text-sm text-green-600 flex items-center gap-1">
                      <TrendingUp className="w-4 h-4" />
                      +8.3%
                    </p>
                  </div>
                  <div className="p-3 rounded-full bg-green-100">
                    <Heart className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </div>

              <div className="dashboard-stat">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Posts</p>
                    <p className="text-2xl font-bold text-gray-900">{posts.length}</p>
                    <p className="text-sm text-blue-600 flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      This month
                    </p>
                  </div>
                  <div className="p-3 rounded-full bg-purple-100">
                    <Send className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </div>

              <div className="dashboard-stat">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">AI Suggestions</p>
                    <p className="text-2xl font-bold text-gray-900">24</p>
                    <p className="text-sm text-purple-600 flex items-center gap-1">
                      <Brain className="w-4 h-4" />
                      Active
                    </p>
                  </div>
                  <div className="p-3 rounded-full bg-orange-100">
                    <Zap className="w-6 h-6 text-orange-600" />
                  </div>
                </div>
              </div>
            </div>

            {/* AI Insights */}
            <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 border border-purple-200">
              <div className="flex items-center gap-2 mb-4">
                <Brain className="w-5 h-5 text-purple-600" />
                <h3 className="font-semibold text-gray-900">AI Social Media Insights</h3>
                <button className="ml-auto text-sm text-purple-600 hover:text-purple-700 flex items-center gap-1">
                  <RefreshCw className="w-4 h-4" />
                  Refresh
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">Optimal Posting Schedule</h4>
                  <p className="text-sm text-gray-600 mb-2">Based on your audience activity:</p>
                  <ul className="text-sm space-y-1">
                    <li>📸 Instagram: 10:30 AM, 2:00 PM</li>
                    <li>💼 LinkedIn: 8:00 AM, 12:00 PM</li>
                    <li>🐦 Twitter: 9:00 AM, 1:00 PM, 6:00 PM</li>
                  </ul>
                </div>
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">Content Recommendations</h4>
                  <p className="text-sm text-gray-600 mb-2">Trending topics for your audience:</p>
                  <div className="flex flex-wrap gap-2">
                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">#AIBusiness</span>
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">#Productivity</span>
                    <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">#Automation</span>
                    <span className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full">#Innovation</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'posts' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">All Posts</h2>
              <div className="flex items-center gap-4">
                <select className="input-field w-auto">
                  <option>All Platforms</option>
                  <option>Instagram</option>
                  <option>LinkedIn</option>
                  <option>Twitter</option>
                  <option>Facebook</option>
                </select>
                <select className="input-field w-auto">
                  <option>All Status</option>
                  <option>Posted</option>
                  <option>Scheduled</option>
                  <option>Draft</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {posts.map((post) => (
                <PostCard key={post.id} post={post} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Social Media Analytics</h2>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold mb-4">Engagement Over Time</h3>
              <div className="h-64 flex items-center justify-center text-gray-500">
                📊 Analytics charts will be implemented with Recharts
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold mb-4">Top Performing Posts</h3>
                <div className="space-y-3">
                  {posts.filter(p => p.status === 'posted').map((post) => (
                    <div key={post.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <div className="flex-1">
                        <p className="text-sm text-gray-900 line-clamp-1">{post.content}</p>
                        <p className="text-xs text-gray-500">{platformConfig[post.platform as keyof typeof platformConfig].name}</p>
                      </div>
                      <div className="text-sm font-semibold text-green-600">
                        {post.engagement.likes + post.engagement.comments + post.engagement.shares} engagements
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold mb-4">Platform Performance</h3>
                <div className="space-y-4">
                  {Object.entries(platformConfig).map(([key, platform]) => (
                    <div key={key} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${platform.bgColor}`}></div>
                        <span className="text-sm font-medium">{platform.name}</span>
                      </div>
                      <div className="text-sm text-gray-600">
                        {Math.floor(Math.random() * 100)}% engagement rate
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'automation' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Automation Rules</h2>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Active Automations</h3>
                <button className="btn-primary">
                  Add New Rule
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium">Auto-post daily tips</h4>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm text-green-600">Active</span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">Posts AI-generated business tips to LinkedIn every weekday at 9:00 AM</p>
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span>🕘 Daily at 9:00 AM</span>
                    <span>📱 LinkedIn</span>
                    <span>🤖 AI Content</span>
                  </div>
                </div>

                <div className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium">Engagement response</h4>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm text-green-600">Active</span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">Automatically likes and responds to comments on Instagram posts</p>
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span>⚡ Real-time</span>
                    <span>📸 Instagram</span>
                    <span>💬 Auto-respond</span>
                  </div>
                </div>

                <div className="border border-gray-200 rounded-lg p-4 opacity-60">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium">Cross-platform sharing</h4>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                      <span className="text-sm text-gray-500">Paused</span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">Automatically shares Instagram posts to Facebook and Twitter</p>
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <span>🔄 On publish</span>
                    <span>📱 Multi-platform</span>
                    <span>📋 Auto-share</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* New Post Modal */}
      <NewPostModal />
    </div>
  )
}



