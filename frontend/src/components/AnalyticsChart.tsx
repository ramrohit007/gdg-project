import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface ChartData {
  student_id: number
  student_name: string
  score: number
}

interface AnalyticsChartProps {
  data: ChartData[]
}

function AnalyticsChart({ data }: AnalyticsChartProps) {
  const chartData = data.map(item => ({
    name: item.student_name,
    score: item.score
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="name" 
          angle={-45}
          textAnchor="end"
          height={80}
          interval={0}
        />
        <YAxis 
          domain={[0, 100]}
          label={{ value: 'Score (%)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip 
          formatter={(value: number) => [`${value.toFixed(1)}%`, 'Score']}
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

