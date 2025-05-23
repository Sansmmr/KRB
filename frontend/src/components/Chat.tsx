import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Paper, Typography, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { QueryResponse } from '../types';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const Chat: React.FC = () => {
    const [query, setQuery] = useState('');
    const [history, setHistory] = useState<QueryResponse[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/history');
            console.log('History response:', response.data);
            setHistory(response.data);
        } catch (error) {
            console.error('Error fetching history:', error);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        try {
            console.log('Sending query:', query);
            const response = await axios.post('http://localhost:8000/api/query', { text: query });
            console.log('Query response:', response.data);
            
            const newResponse: QueryResponse = {
                query: query,
                answer: response.data.answer,
                timestamp: new Date().toISOString()
            };
            
            setHistory(prev => [...prev, newResponse]);
            setQuery('');
        } catch (error) {
            console.error('Error sending query:', error);
            if (axios.isAxiosError(error)) {
                console.error('Response data:', error.response?.data);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
                {history.map((item, index) => (
                    <Box key={index} sx={{ mb: 2 }}>
                        <Paper sx={{ p: 2, bgcolor: '#f5f5f5' }}>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Question:
                            </Typography>
                            <Typography variant="body1" sx={{ mb: 1 }}>
                                {item.query}
                            </Typography>
                            <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                Answer:
                            </Typography>
                            <Box sx={{ 
                                '& h1': { fontSize: '2em', mb: 1 },
                                '& h2': { fontSize: '1.5em', mb: 1 },
                                '& h3': { fontSize: '1.17em', mb: 1 },
                                '& ul, & ol': { pl: 2 },
                                '& li': { mb: 0.5 },
                                '& p': { mb: 1 },
                                '& strong': { fontWeight: 'bold' },
                                '& em': { fontStyle: 'italic' }
                            }}>
                                <ReactMarkdown>
                                    {item.answer}
                                </ReactMarkdown>
                            </Box>
                            {item.timestamp && (
                                <Typography variant="caption" sx={{ display: 'block', mt: 1, color: 'text.secondary' }}>
                                    {new Date(item.timestamp).toLocaleString()}
                                </Typography>
                            )}
                        </Paper>
                    </Box>
                ))}
            </Box>
            <Box sx={{ p: 2, bgcolor: 'background.paper' }}>
                <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px' }}>
                    <TextField
                        fullWidth
                        variant="outlined"
                        placeholder="Ask a question..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        disabled={loading}
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        disabled={loading}
                        endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                    >
                        Send
                    </Button>
                </form>
            </Box>
        </Box>
    );
};

export default Chat; 