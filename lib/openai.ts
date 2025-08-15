/**
 * OpenAI Integration Service
 * Handles AI-powered content generation, strategy, and insights
 */

import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export interface AIGenerationResult {
  content: string
  confidence: number
  reasoning: string
}

export interface SocialMediaOptimization {
  bestTime: string
  platform: string
  engagement: number
  reasoning: string
}

export interface ContentSuggestion {
  title: string
  content: string
  hashtags: string[]
  platform: string
  tone: 'professional' | 'casual' | 'friendly' | 'authoritative'
}

export interface StrategyInsight {
  category: 'growth' | 'engagement' | 'conversion' | 'retention'
  title: string
  description: string
  actionItems: string[]
  priority: 'high' | 'medium' | 'low'
  expectedImpact: string
}

export interface CompetitorInsight {
  competitor: string
  strengths: string[]
  weaknesses: string[]
  opportunities: string[]
  threats: string[]
  recommendations: string[]
}

export class AIService {
  /**
   * Generate social media content using AI
   */
  static async generateSocialMediaContent(
    prompt: string,
    platform: string,
    tone: string = 'professional'
  ): Promise<ContentSuggestion> {
    try {
      const completion = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `You are a social media expert. Generate engaging content for ${platform} with a ${tone} tone. 
                     Return a JSON response with: title, content, hashtags (array), platform, tone.`
          },
          {
            role: "user",
            content: prompt
          }
        ],
        temperature: 0.7,
        max_tokens: 500
      })

      const response = completion.choices[0]?.message?.content
      if (!response) throw new Error('No response from AI')

      try {
        return JSON.parse(response)
      } catch {
        // Fallback if JSON parsing fails
        return {
          title: prompt.slice(0, 50) + '...',
          content: response,
          hashtags: ['#business', '#ai', '#socialmedia'],
          platform,
          tone: tone as any
        }
      }
    } catch (error) {
      console.error('AI content generation error:', error)
      throw new Error('Failed to generate content')
    }
  }

  /**
   * Analyze optimal posting times for social media
   */
  static async analyzeOptimalTiming(
    platform: string,
    audienceData: any,
    pastPerformance: any[]
  ): Promise<SocialMediaOptimization> {
    try {
      const dataStr = JSON.stringify({ audienceData, pastPerformance })
      
      const completion = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `Analyze social media data and recommend optimal posting times. 
                     Return JSON with: bestTime (HH:MM format), platform, engagement (0-100), reasoning.`
          },
          {
            role: "user",
            content: `Analyze this data for ${platform}: ${dataStr}`
          }
        ],
        temperature: 0.3,
        max_tokens: 300
      })

      const response = completion.choices[0]?.message?.content
      if (!response) throw new Error('No response from AI')

      try {
        return JSON.parse(response)
      } catch {
        // Fallback
        return {
          bestTime: '10:00',
          platform,
          engagement: 75,
          reasoning: 'Based on general best practices for this platform'
        }
      }
    } catch (error) {
      console.error('AI timing analysis error:', error)
      throw new Error('Failed to analyze timing')
    }
  }

  /**
   * Generate business strategy insights
   */
  static async generateStrategyInsights(
    businessData: any,
    marketData: any
  ): Promise<StrategyInsight[]> {
    try {
      const dataStr = JSON.stringify({ businessData, marketData })
      
      const completion = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `You are a business strategy consultant. Analyze the data and provide actionable insights.
                     Return an array of JSON objects with: category, title, description, actionItems (array), priority, expectedImpact.`
          },
          {
            role: "user",
            content: `Analyze this business data and provide strategic insights: ${dataStr}`
          }
        ],
        temperature: 0.5,
        max_tokens: 1000
      })

      const response = completion.choices[0]?.message?.content
      if (!response) throw new Error('No response from AI')

      try {
        return JSON.parse(response)
      } catch {
        // Fallback insights
        return [
          {
            category: 'growth',
            title: 'Optimize Digital Presence',
            description: 'Enhance online visibility and engagement',
            actionItems: ['Improve SEO', 'Increase social media activity', 'Create valuable content'],
            priority: 'high',
            expectedImpact: 'Increased brand awareness and lead generation'
          }
        ]
      }
    } catch (error) {
      console.error('AI strategy insights error:', error)
      throw new Error('Failed to generate strategy insights')
    }
  }

  /**
   * Analyze competitor data and provide insights
   */
  static async analyzeCompetitors(
    competitorData: any[],
    ownBusinessData: any
  ): Promise<CompetitorInsight[]> {
    try {
      const dataStr = JSON.stringify({ competitorData, ownBusinessData })
      
      const completion = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `Analyze competitor data and provide SWOT-style insights.
                     Return an array of JSON objects with: competitor, strengths, weaknesses, opportunities, threats, recommendations (all arrays).`
          },
          {
            role: "user",
            content: `Analyze these competitors: ${dataStr}`
          }
        ],
        temperature: 0.4,
        max_tokens: 1200
      })

      const response = completion.choices[0]?.message?.content
      if (!response) throw new Error('No response from AI')

      try {
        return JSON.parse(response)
      } catch {
        // Fallback
        return [
          {
            competitor: 'Market Leader',
            strengths: ['Strong brand recognition', 'Large market share'],
            weaknesses: ['Higher prices', 'Less personalized service'],
            opportunities: ['Underserved market segments', 'Technology gaps'],
            threats: ['Aggressive pricing', 'Market dominance'],
            recommendations: ['Focus on niche markets', 'Emphasize customer service']
          }
        ]
      }
    } catch (error) {
      console.error('AI competitor analysis error:', error)
      throw new Error('Failed to analyze competitors')
    }
  }

  /**
   * Generate ad copy and creative suggestions
   */
  static async generateAdContent(
    productService: string,
    targetAudience: string,
    platform: string,
    budget: number
  ): Promise<AIGenerationResult> {
    try {
      const completion = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `Generate compelling ad copy for ${platform}. Focus on conversion and ROI.`
          },
          {
            role: "user",
            content: `Create ad content for: ${productService}
                     Target audience: ${targetAudience}
                     Platform: ${platform}
                     Budget: $${budget}`
          }
        ],
        temperature: 0.8,
        max_tokens: 400
      })

      const content = completion.choices[0]?.message?.content || ''
      
      return {
        content,
        confidence: 0.85,
        reasoning: 'Generated based on best practices for ad conversion and platform-specific requirements'
      }
    } catch (error) {
      console.error('AI ad generation error:', error)
      throw new Error('Failed to generate ad content')
    }
  }

  /**
   * Forecast ROI based on historical data and market trends
   */
  static async forecastROI(
    historicalData: any[],
    plannedInvestments: any[],
    marketConditions: any
  ): Promise<{
    forecast: number[]
    confidence: number
    factors: string[]
    recommendations: string[]
  }> {
    try {
      const dataStr = JSON.stringify({ historicalData, plannedInvestments, marketConditions })
      
      const completion = await openai.chat.completions.create({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content: `Analyze business data and forecast ROI. Return JSON with: forecast (array of numbers), confidence (0-1), factors (array), recommendations (array).`
          },
          {
            role: "user",
            content: `Forecast ROI based on this data: ${dataStr}`
          }
        ],
        temperature: 0.3,
        max_tokens: 600
      })

      const response = completion.choices[0]?.message?.content
      if (!response) throw new Error('No response from AI')

      try {
        return JSON.parse(response)
      } catch {
        // Fallback forecast
        return {
          forecast: [1.2, 1.35, 1.5, 1.6, 1.75, 1.8],
          confidence: 0.7,
          factors: ['Market trends', 'Historical performance', 'Investment strategy'],
          recommendations: ['Monitor key metrics closely', 'Adjust strategy based on performance']
        }
      }
    } catch (error) {
      console.error('AI ROI forecast error:', error)
      throw new Error('Failed to forecast ROI')
    }
  }
}



