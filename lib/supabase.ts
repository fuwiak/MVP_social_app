/**
 * Supabase Client Configuration
 * Handles database connections and authentication
 */

import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database Tables Types
export interface BusinessMetrics {
  id: string
  date: string
  revenue: number
  expenses: number
  profit: number
  roi: number
  created_at: string
}

export interface SocialMediaPost {
  id: string
  platform: 'facebook' | 'instagram' | 'twitter' | 'linkedin'
  content: string
  media_url?: string
  scheduled_time: string
  posted_time?: string
  status: 'draft' | 'scheduled' | 'posted' | 'failed'
  engagement: {
    likes: number
    shares: number
    comments: number
    reach: number
  }
  created_at: string
}

export interface AdCampaign {
  id: string
  name: string
  platform: string
  budget: number
  spent: number
  clicks: number
  impressions: number
  conversions: number
  ctr: number
  cpc: number
  roas: number
  status: 'active' | 'paused' | 'completed'
  created_at: string
}

export interface BrandAsset {
  id: string
  name: string
  type: 'logo' | 'image' | 'video' | 'document'
  url: string
  tags: string[]
  created_at: string
}

export interface CashFlow {
  id: string
  type: 'income' | 'expense'
  category: string
  amount: number
  description: string
  date: string
  created_at: string
}

export interface AIInsight {
  id: string
  type: 'strategy' | 'timing' | 'content' | 'competitor'
  title: string
  content: string
  confidence: number
  data_source: string
  created_at: string
}

// Database Service Functions
export class DatabaseService {
  // Business Metrics
  static async getBusinessMetrics(days: number = 30) {
    const { data, error } = await supabase
      .from('business_metrics')
      .select('*')
      .gte('date', new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString())
      .order('date', { ascending: false })
    
    if (error) throw error
    return data
  }

  static async addBusinessMetric(metric: Omit<BusinessMetrics, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('business_metrics')
      .insert(metric)
      .select()
    
    if (error) throw error
    return data[0]
  }

  // Social Media Posts
  static async getSocialMediaPosts(limit: number = 50) {
    const { data, error } = await supabase
      .from('social_media_posts')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit)
    
    if (error) throw error
    return data
  }

  static async scheduleSocialMediaPost(post: Omit<SocialMediaPost, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('social_media_posts')
      .insert(post)
      .select()
    
    if (error) throw error
    return data[0]
  }

  static async updatePostEngagement(postId: string, engagement: SocialMediaPost['engagement']) {
    const { data, error } = await supabase
      .from('social_media_posts')
      .update({ engagement })
      .eq('id', postId)
      .select()
    
    if (error) throw error
    return data[0]
  }

  // Ad Campaigns
  static async getAdCampaigns() {
    const { data, error } = await supabase
      .from('ad_campaigns')
      .select('*')
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  }

  static async updateAdCampaign(campaignId: string, updates: Partial<AdCampaign>) {
    const { data, error } = await supabase
      .from('ad_campaigns')
      .update(updates)
      .eq('id', campaignId)
      .select()
    
    if (error) throw error
    return data[0]
  }

  // Brand Assets
  static async getBrandAssets() {
    const { data, error } = await supabase
      .from('brand_assets')
      .select('*')
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  }

  static async addBrandAsset(asset: Omit<BrandAsset, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('brand_assets')
      .insert(asset)
      .select()
    
    if (error) throw error
    return data[0]
  }

  // Cash Flow
  static async getCashFlow(days: number = 30) {
    const { data, error } = await supabase
      .from('cash_flow')
      .select('*')
      .gte('date', new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString())
      .order('date', { ascending: false })
    
    if (error) throw error
    return data
  }

  static async addCashFlowEntry(entry: Omit<CashFlow, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('cash_flow')
      .insert(entry)
      .select()
    
    if (error) throw error
    return data[0]
  }

  // AI Insights
  static async getAIInsights(type?: AIInsight['type'], limit: number = 20) {
    let query = supabase
      .from('ai_insights')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(limit)
    
    if (type) {
      query = query.eq('type', type)
    }
    
    const { data, error } = await query
    
    if (error) throw error
    return data
  }

  static async saveAIInsight(insight: Omit<AIInsight, 'id' | 'created_at'>) {
    const { data, error } = await supabase
      .from('ai_insights')
      .insert(insight)
      .select()
    
    if (error) throw error
    return data[0]
  }
}



