import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Alert, Chip } from '@mui/material';
import SignLanguageRoundedIcon from '@mui/icons-material/SignLanguageRounded';
import AutoAwesomeRoundedIcon from '@mui/icons-material/AutoAwesomeRounded';

function Login() {
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState('');

  const handleLogin = () => {
    if (email === 'guru@bisindo.com' && password === 'admin123') {
      localStorage.setItem('token', 'dummy_token');
      window.location.href = '/dashboard';
    } else {
      setError('Email atau password salah');
    }
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Box
        sx={{
          flex: 1,
          display: { xs: 'none', md: 'flex' },
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'flex-start',
          bgcolor: 'background.paper',
          borderRight: '1px solid',
          borderColor: 'divider',
          p: 8,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Box sx={{
          position: 'absolute', top: -80, right: -80, width: 280, height: 280,
          borderRadius: '50%', bgcolor: 'rgba(56,189,248,0.08)', filter: 'blur(10px)',
        }} />

        <Chip
          icon={<AutoAwesomeRoundedIcon sx={{ fontSize: 15 }} />}
          label="Didukung AI Engine"
          size="small"
          sx={{ bgcolor: 'rgba(56,189,248,0.12)', color: 'primary.main', mb: 4 }}
        />

        <Box
          sx={{
            width: 64, height: 64, borderRadius: '16px', mb: 3,
            background: 'linear-gradient(135deg, #38BDF8, #0EA5E9)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
        >
          <SignLanguageRoundedIcon sx={{ fontSize: 34, color: '#0A1220' }} />
        </Box>

        <Typography variant="h4" mb={1.5}>
          BicaraUntukku
        </Typography>
        <Typography variant="body1" color="text.secondary" maxWidth={380} sx={{ lineHeight: 1.7 }}>
          Menerjemahkan bahasa isyarat BISINDO menjadi teks dan suara, untuk komunikasi yang lebih setara bagi teman tuli dan tunawicara.
        </Typography>

        <Box sx={{ display: 'flex', gap: 3, mt: 6 }}>
          <Box>
            <Typography variant="h6" color="primary.main">32</Typography>
            <Typography variant="caption" color="text.secondary">Kosakata BISINDO</Typography>
          </Box>
          <Box>
            <Typography variant="h6" color="primary.main">MediaPipe</Typography>
            <Typography variant="caption" color="text.secondary">+ LSTM Model</Typography>
          </Box>
        </Box>
      </Box>

      <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', p: 3 }}>
        <Box sx={{ width: '100%', maxWidth: 360 }}>
          <Typography variant="overline" color="primary.main">Selamat datang</Typography>
          <Typography variant="h5" mb={0.5}>
            Masuk ke dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={3.5}>
            Khusus untuk guru dan pendamping SLB
          </Typography>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          <TextField
            fullWidth label="Email" type="email"
            value={email} onChange={e => setEmail(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            fullWidth label="Password" type="password"
            value={password} onChange={e => setPassword(e.target.value)}
            sx={{ mb: 3 }}
          />
          <Button
            fullWidth variant="contained" size="large"
            onClick={handleLogin} sx={{ py: 1.3 }}
          >
            Masuk
          </Button>

          <Typography variant="caption" color="text.secondary" display="block" textAlign="center" mt={2.5}>
            Demo: guru@bisindo.com / admin123
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}

export default Login;