import React, { useState } from 'react';
import { Container, AppBar, Toolbar, Typography, CssBaseline, ThemeProvider, createTheme, Tabs, Tab, Box } from '@mui/material';
import Chat from './components/Chat';
import RougeResults from './components/RougeResults';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              RAG Chat Assistant
            </Typography>
            <Tabs value={tabValue} onChange={handleTabChange} textColor="inherit" indicatorColor="secondary">
              <Tab label="Chat" />
              <Tab label="ROUGE Results" />
            </Tabs>
          </Toolbar>
        </AppBar>
        <Container maxWidth="lg" style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', padding: '24px' }}>
          <div style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', height: 'calc(100vh - 128px)' }}>
            <TabPanel value={tabValue} index={0}>
              <Chat />
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              <RougeResults />
            </TabPanel>
          </div>
        </Container>
      </div>
    </ThemeProvider>
  );
}

export default App;
