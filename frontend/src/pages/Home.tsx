import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  Box,
  Paper,
  Grid,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AssessmentIcon from '@mui/icons-material/Assessment';

const Home = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          AI-Powered Resume Analysis
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Upload your resume for automated analysis and bias detection
        </Typography>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 4,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              height: '100%',
            }}
          >
            <UploadFileIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" component="h2" gutterBottom>
              Upload Resume
            </Typography>
            <Typography color="text.secondary" paragraph>
              Upload your resume for automated analysis. Our AI will evaluate your
              qualifications and provide detailed feedback.
            </Typography>
            <Button
              variant="contained"
              size="large"
              startIcon={<UploadFileIcon />}
              onClick={() => navigate('/upload')}
              sx={{ mt: 2 }}
            >
              Upload Now
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper
            sx={{
              p: 4,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              height: '100%',
            }}
          >
            <AssessmentIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h5" component="h2" gutterBottom>
              View Analysis
            </Typography>
            <Typography color="text.secondary" paragraph>
              View detailed analysis of your resume, including bias detection and
              improvement suggestions.
            </Typography>
            <Button
              variant="contained"
              size="large"
              startIcon={<AssessmentIcon />}
              onClick={() => navigate('/analysis')}
              sx={{ mt: 2 }}
            >
              View Results
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home; 