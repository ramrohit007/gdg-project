import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface TopicAverage {
  topic_id: number
  topic_name: string
  average_score: number
}

interface AnalyticsChartProps {
  data: TopicAverage[]
}

function AnalyticsChart({ data }: AnalyticsChartProps) {
  const chartData = data.map(item => ({
    name: item.topic_name,
    score: item.average_score
  }))

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="name" 
          angle={-45}
          textAnchor="end"
          height={100}
          interval={0}
          label={{ value: 'Topics', position: 'insideBottom', offset: -5 }}
        />
        <YAxis 
          domain={[0, 100]}
          label={{ value: 'Average Score (%)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip 
          formatter={(value: number) => [`${value.toFixed(2)}%`, 'Average Score']}
        />
        <Bar 
          dataKey="score" 
          fill="#667eea"
          radius={[8, 8, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  )
}

export default AnalyticsChart

