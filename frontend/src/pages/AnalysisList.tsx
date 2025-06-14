import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';

const API_URL = 'http://localhost:8000';

interface Analysis {
  filename: string;
  decision: string;
  confidence: number;
  analyzed_at: string;
}

const AnalysisList = () => {
  const navigate = useNavigate();
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        const response = await fetch(`${API_URL}/api/resumes`);
        if (!response.ok) {
          throw new Error('Failed to fetch analyses');
        }
        const data = await response.json();
        setAnalyses(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    };

    fetchAnalyses();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Resume Analysis Results
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Resume</TableCell>
              <TableCell>Decision</TableCell>
              <TableCell>Confidence</TableCell>
              <TableCell>Analyzed At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {analyses.map((analysis) => (
              <TableRow
                key={analysis.filename}
                hover
                onClick={() => navigate(`/analysis/${analysis.filename}`)}
                sx={{ cursor: 'pointer' }}
              >
                <TableCell>{analysis.filename}</TableCell>
                <TableCell>
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
                  />
                </TableCell>
                <TableCell>
                  {(analysis.confidence * 100).toFixed(1)}%
                </TableCell>
                <TableCell>{formatDate(analysis.analyzed_at)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default AnalysisList; 