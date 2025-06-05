'use client';

import { useQuery } from '@tanstack/react-query';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

export default function Dashboard() {
  const { data: summary } = useQuery({
    queryKey: ['metrics-summary'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/v1/metrics/summary');
      if (!res.ok) throw new Error('Failed to fetch metrics summary');
      return res.json();
    },
  });

  const { data: trends } = useQuery({
    queryKey: ['metrics-trends'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/v1/metrics/trends');
      if (!res.ok) throw new Error('Failed to fetch metrics trends');
      return res.json();
    },
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Monitor bias metrics and recruitment analytics
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-sm font-medium text-gray-500">Total Resumes</h3>
          <p className="mt-2 text-3xl font-semibold text-gray-900">
            {summary?.total_resumes ?? 0}
          </p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-sm font-medium text-gray-500">Shortlist Rate</h3>
          <p className="mt-2 text-3xl font-semibold text-gray-900">
            {((summary?.shortlist_rate ?? 0) * 100).toFixed(1)}%
          </p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-sm font-medium text-gray-500">
            Avg. Demographic Parity
          </h3>
          <p className="mt-2 text-3xl font-semibold text-gray-900">
            {(summary?.average_metrics?.demographic_parity ?? 0).toFixed(2)}
          </p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-sm font-medium text-gray-500">
            Avg. Equal Opportunity
          </h3>
          <p className="mt-2 text-3xl font-semibold text-gray-900">
            {(summary?.average_metrics?.equal_opportunity ?? 0).toFixed(2)}
          </p>
        </div>
      </div>

      {/* Trends Chart */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h2 className="text-lg font-medium text-gray-900">Fairness Metrics Trends</h2>
        <div className="mt-6 h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={trends}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Bar
                dataKey="metrics.demographic_parity"
                name="Demographic Parity"
                fill="#4F46E5"
              />
              <Bar
                dataKey="metrics.equal_opportunity"
                name="Equal Opportunity"
                fill="#10B981"
              />
              <Bar
                dataKey="metrics.disparate_impact"
                name="Disparate Impact"
                fill="#F59E0B"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h2 className="text-lg font-medium text-gray-900">Recent Activity</h2>
        <div className="mt-6">
          <div className="flow-root">
            <ul role="list" className="-mb-8">
              {[1, 2, 3].map((item, itemIdx) => (
                <li key={item}>
                  <div className="relative pb-8">
                    {itemIdx !== 2 ? (
                      <span
                        className="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200"
                        aria-hidden="true"
                      />
                    ) : null}
                    <div className="relative flex space-x-3">
                      <div>
                        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500">
                          <span className="text-sm font-medium text-white">
                            {item}
                          </span>
                        </span>
                      </div>
                      <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                        <div>
                          <p className="text-sm text-gray-500">
                            Resume analyzed with confidence score{' '}
                            <span className="font-medium text-gray-900">85%</span>
                          </p>
                        </div>
                        <div className="whitespace-nowrap text-right text-sm text-gray-500">
                          <time dateTime="2024-03-16">1h ago</time>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
