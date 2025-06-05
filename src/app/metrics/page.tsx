'use client';

import { useQuery } from '@tanstack/react-query';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

export default function MetricsPage() {
  const { data: trends } = useQuery({
    queryKey: ['metrics-trends'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/api/v1/metrics/trends');
      if (!res.ok) throw new Error('Failed to fetch metrics trends');
      return res.json();
    },
  });

  const { data: protectedAttributes } = useQuery({
    queryKey: ['protected-attributes'],
    queryFn: async () => {
      const res = await fetch(
        'http://localhost:8000/api/v1/metrics/protected-attributes'
      );
      if (!res.ok) throw new Error('Failed to fetch protected attributes');
      return res.json();
    },
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Fairness Metrics</h1>
        <p className="mt-2 text-gray-600">
          Detailed analysis of bias and fairness in recruitment decisions
        </p>
      </div>

      {/* Metrics Overview */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-sm font-medium text-gray-500">Demographic Parity</h3>
          <div className="mt-2">
            <div className="flex items-baseline">
              <p className="text-3xl font-semibold text-gray-900">
                {trends?.[trends.length - 1]?.metrics.demographic_parity.toFixed(2)}
              </p>
              <p
                className={`ml-2 text-sm ${
                  (trends?.[trends.length - 1]?.metrics.demographic_parity ?? 0) >
                  0.8
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {(trends?.[trends.length - 1]?.metrics.demographic_parity ?? 0) >
                0.8
                  ? 'Good'
                  : 'Needs Improvement'}
              </p>
            </div>
            <p className="mt-1 text-xs text-gray-500">
              Measures if protected groups have equal probability of positive
              outcome
            </p>
          </div>
        </div>

        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-sm font-medium text-gray-500">Equal Opportunity</h3>
          <div className="mt-2">
            <div className="flex items-baseline">
              <p className="text-3xl font-semibold text-gray-900">
                {trends?.[trends.length - 1]?.metrics.equal_opportunity.toFixed(2)}
              </p>
              <p
                className={`ml-2 text-sm ${
                  (trends?.[trends.length - 1]?.metrics.equal_opportunity ?? 0) >
                  0.8
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {(trends?.[trends.length - 1]?.metrics.equal_opportunity ?? 0) >
                0.8
                  ? 'Good'
                  : 'Needs Improvement'}
              </p>
            </div>
            <p className="mt-1 text-xs text-gray-500">
              Measures equal true positive rates across protected groups
            </p>
          </div>
        </div>

        <div className="rounded-lg bg-white p-6 shadow">
          <h3 className="text-sm font-medium text-gray-500">Disparate Impact</h3>
          <div className="mt-2">
            <div className="flex items-baseline">
              <p className="text-3xl font-semibold text-gray-900">
                {trends?.[trends.length - 1]?.metrics.disparate_impact.toFixed(2)}
              </p>
              <p
                className={`ml-2 text-sm ${
                  Math.abs(
                    (trends?.[trends.length - 1]?.metrics.disparate_impact ?? 1) -
                      1
                  ) < 0.2
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}
              >
                {Math.abs(
                  (trends?.[trends.length - 1]?.metrics.disparate_impact ?? 1) - 1
                ) < 0.2
                  ? 'Good'
                  : 'Needs Improvement'}
              </p>
            </div>
            <p className="mt-1 text-xs text-gray-500">
              Ratio of positive outcomes between protected and unprotected groups
            </p>
          </div>
        </div>
      </div>

      {/* Trends Chart */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h2 className="text-lg font-medium text-gray-900">Metrics Trends</h2>
        <div className="mt-6 h-96">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
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
              <Legend />
              <Line
                type="monotone"
                dataKey="metrics.demographic_parity"
                name="Demographic Parity"
                stroke="#4F46E5"
                activeDot={{ r: 8 }}
              />
              <Line
                type="monotone"
                dataKey="metrics.equal_opportunity"
                name="Equal Opportunity"
                stroke="#10B981"
                activeDot={{ r: 8 }}
              />
              <Line
                type="monotone"
                dataKey="metrics.disparate_impact"
                name="Disparate Impact"
                stroke="#F59E0B"
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Protected Attributes Analysis */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h2 className="text-lg font-medium text-gray-900">
          Protected Attributes Analysis
        </h2>
        <div className="mt-6">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {protectedAttributes &&
              Object.entries(protectedAttributes).map(([attr, metrics]: [string, any]) => (
                <div
                  key={attr}
                  className="rounded-lg border border-gray-200 p-4"
                >
                  <h3 className="text-sm font-medium text-gray-900">
                    {attr.charAt(0).toUpperCase() + attr.slice(1)}
                  </h3>
                  <dl className="mt-4 grid grid-cols-2 gap-4">
                    <div>
                      <dt className="text-xs text-gray-500">Total Samples</dt>
                      <dd className="text-sm font-medium text-gray-900">
                        {metrics.total}
                      </dd>
                    </div>
                    <div>
                      <dt className="text-xs text-gray-500">
                        Avg. Demographic Parity
                      </dt>
                      <dd className="text-sm font-medium text-gray-900">
                        {metrics.avg_demographic_parity.toFixed(2)}
                      </dd>
                    </div>
                    <div>
                      <dt className="text-xs text-gray-500">
                        Avg. Equal Opportunity
                      </dt>
                      <dd className="text-sm font-medium text-gray-900">
                        {metrics.avg_equal_opportunity.toFixed(2)}
                      </dd>
                    </div>
                    <div>
                      <dt className="text-xs text-gray-500">
                        Avg. Disparate Impact
                      </dt>
                      <dd className="text-sm font-medium text-gray-900">
                        {metrics.avg_disparate_impact.toFixed(2)}
                      </dd>
                    </div>
                  </dl>
                </div>
              ))}
          </div>
        </div>
      </div>

      {/* Mitigation Recommendations */}
      <div className="rounded-lg bg-white p-6 shadow">
        <h2 className="text-lg font-medium text-gray-900">
          Mitigation Recommendations
        </h2>
        <div className="mt-6 space-y-4">
          {trends?.[trends.length - 1]?.metrics.demographic_parity < 0.8 && (
            <div className="rounded-lg bg-yellow-50 p-4">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-yellow-800">
                    Low Demographic Parity
                  </h3>
                  <div className="mt-2 text-sm text-yellow-700">
                    <p>Recommended actions:</p>
                    <ul className="mt-2 list-disc space-y-1 pl-5">
                      <li>Review feature selection for potential bias</li>
                      <li>Apply pre-processing techniques to balance dataset</li>
                      <li>Consider using a fairness-aware model</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {Math.abs(
            (trends?.[trends.length - 1]?.metrics.disparate_impact ?? 1) - 1
          ) > 0.2 && (
            <div className="rounded-lg bg-yellow-50 p-4">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-yellow-800">
                    High Disparate Impact
                  </h3>
                  <div className="mt-2 text-sm text-yellow-700">
                    <p>Recommended actions:</p>
                    <ul className="mt-2 list-disc space-y-1 pl-5">
                      <li>Analyze decision thresholds</li>
                      <li>Apply post-processing techniques</li>
                      <li>Review and update training data</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 