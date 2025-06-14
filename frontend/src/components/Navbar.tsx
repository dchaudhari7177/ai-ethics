import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AssessmentIcon from '@mui/icons-material/Assessment';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
          }}
        >
          Resume Analysis
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            component={RouterLink}
            to="/upload"
            color="inherit"
            startIcon={<UploadFileIcon />}
          >
            Upload Resume
          </Button>
          <Button
            component={RouterLink}
            to="/analysis"
            color="inherit"
            startIcon={<AssessmentIcon />}
          >
            View Analysis
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 