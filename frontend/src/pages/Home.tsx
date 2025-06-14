import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AssessmentIcon from '@mui/icons-material/Assessment';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import SecurityIcon from '@mui/icons-material/Security';

const Home = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box sx={{ mb: 6, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          AI-Powered Resume Analysis
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Fair and unbiased resume screening with advanced AI technology
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Paper
            sx={{
              p: 4,
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <Typography variant="h5" gutterBottom>
              Upload Resume
            </Typography>
            <Typography paragraph>
              Upload a resume to analyze its content and detect potential biases in
              the screening process.
            </Typography>
            <Box sx={{ mt: 'auto' }}>
              <Button
                component={RouterLink}
                to="/upload"
                variant="contained"
                size="large"
                startIcon={<UploadFileIcon />}
                fullWidth
              >
                Upload Resume
              </Button>
            </Box>
          </Paper>
        </Box>

        <Box sx={{ flex: '1 1 300px', minWidth: 0 }}>
          <Paper
            sx={{
              p: 4,
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <Typography variant="h5" gutterBottom>
              View Analysis
            </Typography>
            <Typography paragraph>
              View detailed analysis results and bias detection metrics for all
              processed resumes.
            </Typography>
            <Box sx={{ mt: 'auto' }}>
              <Button
                component={RouterLink}
                to="/analysis"
                variant="outlined"
                size="large"
                startIcon={<AssessmentIcon />}
                fullWidth
              >
                View Analysis
              </Button>
            </Box>
          </Paper>
        </Box>
      </Box>

      <Box sx={{ mt: 6 }}>
        <Typography variant="h4" gutterBottom>
          Key Features
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
            <Paper sx={{ p: 3 }}>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Accurate Analysis"
                    secondary="Advanced NLP and machine learning for precise resume evaluation"
                  />
                </ListItem>
              </List>
            </Paper>
          </Box>
          <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
            <Paper sx={{ p: 3 }}>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <SecurityIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Bias Detection"
                    secondary="Comprehensive analysis of potential biases in the screening process"
                  />
                </ListItem>
              </List>
            </Paper>
          </Box>
          <Box sx={{ flex: '1 1 250px', minWidth: 0 }}>
            <Paper sx={{ p: 3 }}>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <AssessmentIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Detailed Metrics"
                    secondary="In-depth analysis of skills, experience, and demographic factors"
                  />
                </ListItem>
              </List>
            </Paper>
          </Box>
        </Box>
      </Box>
    </Container>
  );
};

export default Home; 