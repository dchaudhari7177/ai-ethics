import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import AssessmentIcon from '@mui/icons-material/Assessment';

const API_URL = 'http://localhost:8000';

interface AnalysisResult {
  filename: string;
  decision: string;
  confidence: number;
  features: {
    skills: string[];
    experience: number;
    entities: Record<string, string>;
  };
  bias_metrics: {
    overall: {
      total_candidates: number;
      shortlisted: number;
      rejection_rate: number;
    };
    demographics: {
      gender?: {
        value: string;
        shortlisted: number;
        total: number;
        shortlist_rate: number;
      };
      age?: {
        value: number;
        group: string;
      };
    };
    fairness: {
      demographic_parity?: number;
      equal_opportunity?: number;
    };
  };
  analyzed_at: string;
}

const AnalysisDetail = () => {
  const { filename } = useParams<{ filename: string }>();
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await fetch(`${API_URL}/api/analysis/${filename}`);
        if (!response.ok) {
          throw new Error('Failed to fetch analysis');
        }
        const data = await response.json();
        setAnalysis(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [filename]);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error || !analysis) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error || 'Analysis not found'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Resume Analysis
          </Typography>
          <Typography color="text.secondary">
            Analyzed on {new Date(analysis.analyzed_at).toLocaleString()}
          </Typography>
        </Box>

        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Decision
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Chip
                  icon={
                    analysis.decision === 'shortlist' ? (
                      <CheckCircleIcon />
                    ) : (
                      <CancelIcon />
                    )
                  }
                  label={analysis.decision}
                  color={analysis.decision === 'shortlist' ? 'success' : 'error'}
                  size="large"
                />
                <Typography>
                  Confidence: {(analysis.confidence * 100).toFixed(1)}%
                </Typography>
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Skills
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {analysis.features.skills.map((skill) => (
                  <Chip key={skill} label={skill} />
                ))}
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Experience
              </Typography>
              <Typography>
                Years of Experience: {analysis.features.experience}
              </Typography>
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Bias Analysis
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" gutterBottom>
                    Overall Statistics
                  </Typography>
                  <Typography>
                    Total Candidates: {analysis.bias_metrics.overall.total_candidates}
                  </Typography>
                  <Typography>
                    Shortlisted: {analysis.bias_metrics.overall.shortlisted}
                  </Typography>
                  <Typography>
                    Rejection Rate: {(analysis.bias_metrics.overall.rejection_rate * 100).toFixed(1)}%
                  </Typography>
                </Grid>

                {analysis.bias_metrics.demographics.gender && (
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle1" gutterBottom>
                      Gender Statistics
                    </Typography>
                    <Typography>
                      Gender: {analysis.bias_metrics.demographics.gender.value}
                    </Typography>
                    <Typography>
                      Shortlist Rate: {(analysis.bias_metrics.demographics.gender.shortlist_rate * 100).toFixed(1)}%
                    </Typography>
                  </Grid>
                )}

                {analysis.bias_metrics.demographics.age && (
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle1" gutterBottom>
                      Age Statistics
                    </Typography>
                    <Typography>
                      Age: {analysis.bias_metrics.demographics.age.value}
                    </Typography>
                    <Typography>
                      Age Group: {analysis.bias_metrics.demographics.age.group}
                    </Typography>
                  </Grid>
                )}

                {analysis.bias_metrics.fairness && (
                  <Grid item xs={12}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="subtitle1" gutterBottom>
                      Fairness Metrics
                    </Typography>
                    {analysis.bias_metrics.fairness.demographic_parity && (
                      <Typography>
                        Demographic Parity: {(analysis.bias_metrics.fairness.demographic_parity * 100).toFixed(1)}%
                      </Typography>
                    )}
                    {analysis.bias_metrics.fairness.equal_opportunity && (
                      <Typography>
                        Equal Opportunity: {(analysis.bias_metrics.fairness.equal_opportunity * 100).toFixed(1)}%
                      </Typography>
                    )}
                  </Grid>
                )}
              </Grid>
            </Paper>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AnalysisDetail; 