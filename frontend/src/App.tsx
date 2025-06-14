import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ResumeUpload from './pages/ResumeUpload';
import AnalysisList from './pages/AnalysisList';
import AnalysisDetail from './pages/AnalysisDetail';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<ResumeUpload />} />
          <Route path="/analysis" element={<AnalysisList />} />
          <Route path="/analysis/:filename" element={<AnalysisDetail />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
