/**
 * API Client for FastAPI Backend
 * Handles all communication between Next.js frontend and FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class APIClient {
  private baseURL: string
  
  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    }

    const config: RequestInit = {
      headers: { ...defaultHeaders, ...options.headers },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed: ${config.method || 'GET'} ${endpoint}`, error)
      throw error
    }
  }

  // Dashboard API
  async getDashboardMetrics(days: number = 30) {
    return this.request(`/api/dashboard/metrics?days=${days}`)
  }

  async getAIInsights() {
    return this.request('/api/dashboard/insights')
  }

  async getSystemStatus() {
    return this.request('/api/dashboard/system-status')
  }

  async refreshInsights() {
    return this.request('/api/dashboard/refresh-insights', { method: 'POST' })
  }

  async getRecentActivity(limit: number = 20) {
    return this.request(`/api/dashboard/recent-activity?limit=${limit}`)
  }

  // Social Media API
  async getSocialMediaPosts(filters: {
    platform?: string
    status?: string
    limit?: number
  } = {}) {
    const params = new URLSearchParams()
    if (filters.platform) params.append('platform', filters.platform)
    if (filters.status) params.append('status', filters.status)
    if (filters.limit) params.append('limit', filters.limit.toString())
    
    return this.request(`/api/social-media/posts?${params}`)
  }

  async createSocialMediaPost(post: {
    platform: string
    content: string
    media_url?: string
    scheduled_time: string
    hashtags?: string[]
  }) {
    return this.request('/api/social-media/posts', {
      method: 'POST',
      body: JSON.stringify(post)
    })
  }

  async generateAIContent(request: {
    prompt: string
    platform: string
    tone?: string
    include_hashtags?: boolean
  }) {
    return this.request('/api/social-media/generate-content', {
      method: 'POST',
      body: JSON.stringify(request)
    })
  }

  async getOptimalPostingTimes(platform: string) {
    return this.request(`/api/social-media/optimal-times/${platform}`)
  }

  async updatePostEngagement(postId: string, engagement: {
    likes: number
    comments: number
    shares: number
    reach: number
  }) {
    return this.request(`/api/social-media/posts/${postId}/engagement`, {
      method: 'PUT',
      body: JSON.stringify(engagement)
    })
  }

  async getEngagementAnalytics(days: number = 30) {
    return this.request(`/api/social-media/analytics/engagement?days=${days}`)
  }

  async getContentSuggestions(platform: string, industry: string = 'technology', tone: string = 'professional') {
    return this.request(`/api/social-media/content-suggestions?platform=${platform}&industry=${industry}&tone=${tone}`)
  }

  // AI Services API
  async generateBusinessStrategy(data: {
    business_data: any
    market_data: any
  }) {
    return this.request('/api/ai/generate-strategy', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async analyzeCompetitors(data: {
    competitor_data: any[]
    own_business_data: any
  }) {
    return this.request('/api/ai/analyze-competitors', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async forecastROI(data: {
    historical_data: any[]
    planned_investments: any[]
    market_conditions: any
  }) {
    return this.request('/api/ai/forecast-roi', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async getInsightsByType(type: string, limit: number = 10) {
    return this.request(`/api/ai/insights/${type}?limit=${limit}`)
  }

  // Analytics API
  async getRevenueAnalytics(days: number = 30) {
    return this.request(`/api/analytics/revenue?days=${days}`)
  }

  async getSocialPerformance(days: number = 30) {
    return this.request(`/api/analytics/social-performance?days=${days}`)
  }

  async getAdPerformance() {
    return this.request('/api/analytics/ad-performance')
  }

  async getROIAnalysis(days: number = 30) {
    return this.request(`/api/analytics/roi-analysis?days=${days}`)
  }

  async getDashboardSummary() {
    return this.request('/api/analytics/dashboard-summary')
  }

  // Automation API
  async getAutomationRules() {
    return this.request('/api/automation/rules')
  }

  async createAutomationRule(rule: {
    name: string
    description: string
    trigger_type: string
    actions: any[]
    conditions?: any
    schedule?: string
    enabled?: boolean
  }) {
    return this.request('/api/automation/rules', {
      method: 'POST',
      body: JSON.stringify(rule)
    })
  }

  async getN8NWorkflows() {
    return this.request('/api/automation/workflows/n8n')
  }

  async triggerAutomationRule(ruleId: string) {
    return this.request(`/api/automation/trigger/${ruleId}`, { method: 'POST' })
  }

  async getExecutionHistory(limit: number = 50) {
    return this.request(`/api/automation/execution-history?limit=${limit}`)
  }

  async getAutomationMetrics() {
    return this.request('/api/automation/metrics')
  }

  // Brand Assets API
  async getBrandAssets(filters: {
    asset_type?: string
    tags?: string
    limit?: number
  } = {}) {
    const params = new URLSearchParams()
    if (filters.asset_type) params.append('asset_type', filters.asset_type)
    if (filters.tags) params.append('tags', filters.tags)
    if (filters.limit) params.append('limit', filters.limit.toString())
    
    return this.request(`/api/brand-assets/assets?${params}`)
  }

  async createBrandAsset(asset: {
    name: string
    type: string
    url: string
    tags: string[]
    description?: string
  }) {
    return this.request('/api/brand-assets/assets', {
      method: 'POST',
      body: JSON.stringify(asset)
    })
  }

  async uploadBrandAsset(formData: FormData) {
    return this.request('/api/brand-assets/assets/upload', {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set Content-Type for FormData
    })
  }

  async getBrandAsset(assetId: string) {
    return this.request(`/api/brand-assets/assets/${assetId}`)
  }

  async getAssetCollections() {
    return this.request('/api/brand-assets/collections')
  }

  async getUsageAnalytics(days: number = 30) {
    return this.request(`/api/brand-assets/usage-analytics?days=${days}`)
  }

  // Cash Flow API
  async getCashFlowEntries(filters: {
    days?: number
    transaction_type?: string
    category?: string
    limit?: number
  } = {}) {
    const params = new URLSearchParams()
    if (filters.days) params.append('days', filters.days.toString())
    if (filters.transaction_type) params.append('transaction_type', filters.transaction_type)
    if (filters.category) params.append('category', filters.category)
    if (filters.limit) params.append('limit', filters.limit.toString())
    
    return this.request(`/api/cash-flow/entries?${params}`)
  }

  async createCashFlowEntry(entry: {
    type: 'income' | 'expense'
    category: string
    amount: number
    description: string
    date: string
    tags?: string[]
  }) {
    return this.request('/api/cash-flow/entries', {
      method: 'POST',
      body: JSON.stringify(entry)
    })
  }

  async getCashFlowSummary(days: number = 30) {
    return this.request(`/api/cash-flow/summary?days=${days}`)
  }

  async getCashFlowCategories() {
    return this.request('/api/cash-flow/categories')
  }

  async getCashFlowForecast(months: number = 6) {
    return this.request(`/api/cash-flow/forecast?months=${months}`)
  }

  async getBudgetAnalysis(days: number = 30) {
    return this.request(`/api/cash-flow/budget-analysis?days=${days}`)
  }

  // Ad Campaigns API
  async getAdCampaigns(filters: {
    platform?: string
    status?: string
    limit?: number
  } = {}) {
    const params = new URLSearchParams()
    if (filters.platform) params.append('platform', filters.platform)
    if (filters.status) params.append('status', filters.status)
    if (filters.limit) params.append('limit', filters.limit.toString())
    
    return this.request(`/api/ad-campaigns/campaigns?${params}`)
  }

  async createAdCampaign(campaign: {
    name: string
    platform: string
    budget: number
    target_audience: string
    campaign_type: string
    start_date: string
    end_date?: string
  }) {
    return this.request('/api/ad-campaigns/campaigns', {
      method: 'POST',
      body: JSON.stringify(campaign)
    })
  }

  async getCampaignDetails(campaignId: string) {
    return this.request(`/api/ad-campaigns/campaigns/${campaignId}`)
  }

  async updateCampaign(campaignId: string, updates: {
    budget?: number
    status?: string
    target_audience?: string
  }) {
    return this.request(`/api/ad-campaigns/campaigns/${campaignId}`, {
      method: 'PUT',
      body: JSON.stringify(updates)
    })
  }

  async optimizeCampaign(campaignId: string) {
    return this.request(`/api/ad-campaigns/campaigns/${campaignId}/optimize`, { method: 'POST' })
  }

  async getPerformanceAnalytics(days: number = 30) {
    return this.request(`/api/ad-campaigns/performance-analytics?days=${days}`)
  }

  async generateAdCreative(data: {
    product_description: string
    target_audience: string
    platform: string
    campaign_objective?: string
  }) {
    const params = new URLSearchParams()
    params.append('product_description', data.product_description)
    params.append('target_audience', data.target_audience)
    params.append('platform', data.platform)
    if (data.campaign_objective) params.append('campaign_objective', data.campaign_objective)
    
    return this.request(`/api/ad-campaigns/generate-ad-creative?${params}`, { method: 'POST' })
  }

  async getBudgetRecommendations(data: {
    campaign_objective?: string
    target_audience_size?: number
    competition_level?: string
  } = {}) {
    const params = new URLSearchParams()
    if (data.campaign_objective) params.append('campaign_objective', data.campaign_objective)
    if (data.target_audience_size) params.append('target_audience_size', data.target_audience_size.toString())
    if (data.competition_level) params.append('competition_level', data.competition_level)
    
    return this.request(`/api/ad-campaigns/budget-recommendations?${params}`)
  }

  // Health Check
  async healthCheck() {
    return this.request('/health')
  }
}

// Export singleton instance
export const apiClient = new APIClient()

// Export individual API methods for convenience
export const {
  getDashboardMetrics,
  getAIInsights,
  getSystemStatus,
  refreshInsights,
  getRecentActivity,
  getSocialMediaPosts,
  createSocialMediaPost,
  generateAIContent,
  getOptimalPostingTimes,
  updatePostEngagement,
  getEngagementAnalytics,
  getContentSuggestions,
  generateBusinessStrategy,
  analyzeCompetitors,
  forecastROI,
  getInsightsByType,
  getRevenueAnalytics,
  getSocialPerformance,
  getAdPerformance,
  getROIAnalysis,
  getDashboardSummary,
  getAutomationRules,
  createAutomationRule,
  getN8NWorkflows,
  triggerAutomationRule,
  getExecutionHistory,
  getAutomationMetrics,
  getBrandAssets,
  createBrandAsset,
  uploadBrandAsset,
  getBrandAsset,
  getAssetCollections,
  getUsageAnalytics,
  getCashFlowEntries,
  createCashFlowEntry,
  getCashFlowSummary,
  getCashFlowCategories,
  getCashFlowForecast,
  getBudgetAnalysis,
  getAdCampaigns,
  createAdCampaign,
  getCampaignDetails,
  updateCampaign,
  optimizeCampaign,
  getPerformanceAnalytics,
  generateAdCreative,
  getBudgetRecommendations,
  healthCheck
} = apiClient

