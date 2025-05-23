import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

interface RougeResult {
  Query: string;
  Generated: string;
  'ROUGE-1 F1': number;
  'ROUGE-1 Precision': number;
  'ROUGE-1 Recall': number;
  'ROUGE-L F1': number;
  'ROUGE-L Precision': number;
  'ROUGE-L Recall': number;
}

const RougeResults: React.FC = () => {
  const [results, setResults] = useState<RougeResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/rouge-results');
      setResults(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch ROUGE results');
      console.error('Error fetching ROUGE results:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 2 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        ROUGE Test Results
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Query</TableCell>
              <TableCell>Generated Answer</TableCell>
              <TableCell align="right">ROUGE-1 F1</TableCell>
              <TableCell align="right">ROUGE-1 Precision</TableCell>
              <TableCell align="right">ROUGE-1 Recall</TableCell>
              <TableCell align="right">ROUGE-L F1</TableCell>
              <TableCell align="right">ROUGE-L Precision</TableCell>
              <TableCell align="right">ROUGE-L Recall</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {results.map((result, index) => (
              <TableRow key={index}>
                <TableCell>{result.Query}</TableCell>
                <TableCell>{result.Generated}</TableCell>
                <TableCell align="right">{result['ROUGE-1 F1'].toFixed(4)}</TableCell>
                <TableCell align="right">{result['ROUGE-1 Precision'].toFixed(4)}</TableCell>
                <TableCell align="right">{result['ROUGE-1 Recall'].toFixed(4)}</TableCell>
                <TableCell align="right">{result['ROUGE-L F1'].toFixed(4)}</TableCell>
                <TableCell align="right">{result['ROUGE-L Precision'].toFixed(4)}</TableCell>
                <TableCell align="right">{result['ROUGE-L Recall'].toFixed(4)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default RougeResults; 